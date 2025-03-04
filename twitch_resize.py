import os
from PIL import Image

def twitch_resize_func(input_file_path, resize_list=[112, 56, 28], aa_enable=True, keep_aspect=False):
    """
    画像リサイズ関数
    Args:
        input_file_path (str): 入力ファイルのパス
        resize_list (list): リサイズする大きさのリスト
        aa_enable (bool): アンチエイリアスを有効にするかどうか
        keep_aspect (bool): アスペクト比を維持するかどうか
    Returns:
        bool: 処理が成功したかどうか
    """
    resizer = ImageResizer(input_file_path, resize_list, aa_enable, keep_aspect)
    return resizer.process()

class ImageResizer:
    SUPPORTED_FORMATS = {'PNG', 'JPEG', 'GIF', 'BMP', 'WEBP'}

    def __init__(self, input_file_path, resize_list=[112, 56, 28], aa_enable=True, keep_aspect=False):
        self.input_file_path = input_file_path
        self.resize_list = resize_list
        self.aa_enable = aa_enable
        self.keep_aspect = keep_aspect
        self.validate_input()

    def validate_input(self):
        """入力ファイルの検証"""
        if not os.path.exists(self.input_file_path):
            raise ValueError('Error: このファイルは存在しません!')
        if os.path.isdir(self.input_file_path):
            raise ValueError('Error: このパスはディレクトリです!')
        
        try:
            with Image.open(self.input_file_path) as img:
                format = img.format
                if format not in self.SUPPORTED_FORMATS:
                    raise ValueError(f'Error: この画像形式 ({format}) はサポートされていません!\n'
                                  f'サポートされている形式: {", ".join(self.SUPPORTED_FORMATS)}')
        except Exception as e:
            raise ValueError(f'Error: ファイルを画像として開けません: {str(e)}')

    def get_output_path(self, size, frame_number=None):
        """出力ファイルパスの生成"""
        input_file_name = os.path.splitext(os.path.basename(self.input_file_path))[0]
        input_file_dir = os.path.dirname(self.input_file_path)
        
        # 元の入力がGIFの場合は出力もGIFに
        with Image.open(self.input_file_path) as img:
            output_ext = '.gif' if img.format == 'GIF' else '.png'
        
        if frame_number is not None:
            return f"{input_file_dir}/{input_file_name}_{size}_frame{frame_number}{output_ext}"
        return f"{input_file_dir}/{input_file_name}_{size}{output_ext}"

    def resize_frame(self, img, size):
        """単一フレームのリサイズ処理"""
        resize_width = size
        resize_height = size

        if self.keep_aspect:
            width, height = img.size
            resize_height = round(height * (size / width))

        resampling = Image.Resampling.LANCZOS if self.aa_enable else Image.Resampling.NEAREST
        return img.resize((resize_width, resize_height), resampling)

    def resize_static_image(self):
        """静止画のリサイズ処理"""
        with Image.open(self.input_file_path) as img:
            for size in self.resize_list:
                resized = self.resize_frame(img, size)
                output_path = self.get_output_path(size)
                resized.save(output_path, optimize=True)

    def resize_animated_gif(self):
        self.aa_enable = False
        """アニメーションGIFのリサイズ処理"""
        with Image.open(self.input_file_path) as img:
            # アニメーションGIFでない場合は通常の処理を行う
            if not getattr(img, "is_animated", False):
                self.resize_static_image()
                return

            # 元画像の基本情報を取得
            base_info = img.info.copy()

            for size in self.resize_list:
                frames = []
                frame_settings = []
                
                # 全フレームを処理し、各フレームの設定を保持
                for frame in range(img.n_frames):
                    img.seek(frame)
                    
                    # 現在のフレームの情報を保存
                    current_frame_info = {
                        'palette': img.getpalette(),
                        'duration': img.info.get('duration', 100),
                        'disposal': img.disposal_method if hasattr(img, 'disposal_method') else 2,
                        'transparency': img.info.get('transparency', 255)
                    }
                    
                    # 現在のフレームをコピーしてリサイズ
                    frame_copy = img.copy()
                    new_frame = self.resize_frame(frame_copy, size)

                    # RGBAの場合の処理
                    if new_frame.mode == 'RGBA':
                        # ピクセルデータを取得し、アルファ値0のピクセルを(0,0,0,0)に統一
                        data = new_frame.getdata()
                        unified_data = [(0,0,0,0) if a == 0 else (r,g,b,a) for r,g,b,a in data]
                        new_frame.putdata(unified_data)
                        # アルファチャネルを保存（パレット変換前に取得）
                        alpha = new_frame.split()[3]
                        # RGBとアルファを分離してパレット変換
                        rgb_image = Image.new('RGB', new_frame.size, (0, 0, 0))
                        rgb_image.paste(new_frame.convert('RGB'), (0, 0))
                        new_frame = rgb_image.convert('P', palette=Image.Palette.ADAPTIVE, colors=255)
                        
                        # 保存したアルファ情報を使用して透過ピクセルを設定
                        mask = alpha.point(lambda x: 255 if x < 128 else 0)
                        new_frame.paste(255, mask)
                        new_frame.info['transparency'] = 255
                        
                    # 各フレームに透過設定を適用
                    if current_frame_info['transparency'] is not None:
                        new_frame.info['transparency'] = current_frame_info['transparency']
                    frames.append(new_frame)
                    frame_settings.append(current_frame_info)

                # アニメーションGIFとして保存
                output_path = self.get_output_path(size)
                
                # 基本の保存設定
                save_kwargs = {
                    'format': 'GIF',
                    'save_all': True,
                    'append_images': frames[1:],
                    'optimize': False,
                    'loop': base_info.get('loop', 0),
                    'duration': [info['duration'] for info in frame_settings],
                    'disposal': [info['disposal'] for info in frame_settings],
                }
                
                # GIFとして保存
                frames[0].save(output_path, **save_kwargs)

    def process(self):
        """画像処理のメイン関数"""
        try:
            # 入力がGIFの場合はアニメーション処理を行う
            with Image.open(self.input_file_path) as img:
                if img.format == 'GIF' and getattr(img, "is_animated", False):
                    self.resize_animated_gif()
                else:
                    self.resize_static_image()
            return True
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        print("ファイルパスが必要です")
        sys.exit(1)

    try:
        result = twitch_resize_func(sys.argv[1])
        if result:
            print("処理が完了しました")
        else:
            print("処理中にエラーが発生しました")
    except ValueError as e:
        print(e)
        sys.exit(1)
