import sys
import cv2
import os
import numpy as np
import imghdr

def imread_for_2byte(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None

def imwrite_for_2byte(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False        

def twitch_resize_func(input_file_path, resize_list=[112, 56, 28],aa_enable=True,):

    # ファイルが存在するか確認
    if os.path.exists(input_file_path):
        None
    else:
        raise ValueError('Error. this file is not exist!')

    if os.path.isdir(input_file_path):
        raise ValueError('Error. this file is directory!')

    # ファイルが画像ファイルかどうかの確認
    if (imghdr.what(input_file_path) is None):
        raise ValueError('Error. this file is not image!')
    
    # imread で画像を読み込み
    img = imread_for_2byte(f"{input_file_path}", cv2.IMREAD_UNCHANGED)
    # ファイルパスからファイル名を抜き出します
    input_file_name = os.path.splitext(os.path.basename(input_file_path))[0]
    input_file_dir = os.path.dirname(input_file_path)
    # 112x112, 56x56, 28x28 の画像に resize して、保存する
    for size in resize_list:
        # リサイズの数値計算
        resize_pixel = int(size)

        # アウトプットの名前作成
        output_file_name=f"{input_file_dir}/{input_file_name}_{resize_pixel}.png"

        # resize 関数でリサイズ
        # 画像にブラーをかける
        if aa_enable :
            blursize=int(size/2)
            img = cv2.blur(img, (blursize,blursize))
        dest = cv2.resize(img, dsize=(resize_pixel, resize_pixel), interpolation=cv2.INTER_LANCZOS4 )

        # 保存
        imwrite_for_2byte(output_file_name, dest)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("need filepath")
        exit (1)

    input_file_path=sys.argv[1]
    twitch_resize_func(input_file_path)