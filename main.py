from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox

import twitch_resize

def open_file_clicked():
    info_text.set('Open Fileを押して、ファイルを選択し、Resize ボタンでリサイズされます')
    file = filedialog.askopenfile()
    if file:
        filepath.set(file.name)
        # contents = file.read()
        print(file.name)
        file.close()

def resize_clicked(resize_list=[112, 56, 28], aa_enable=True, keep_aspect=False):
    """
    リサイズボタンを押したときの挙動
    デフォルト 112x112, 56x56, 28x28 で出力する
    72x72 とかも対応出来るようにする
    """
    info_text.set("変換中")
    resize_filepath = filepath.get()
    if not resize_filepath:
        messagebox.showerror("Error", "ファイルパスが設定されていません。")
        info_text.set("ファイルパスが設定されていません。")
    else:
        try:
            twitch_resize.twitch_resize_func(resize_filepath, resize_list, aa_enable, keep_aspect=keep_aspect)
        except ValueError as e:
            messagebox.showerror("Error", "ファイルが画像でない可能性があります。")
            info_text.set("ファイルが画像でない可能性があります。")
            return -1
        info_text.set("リサイズが完了しました。")
        # messagebox.showinfo("info", "リサイズが完了しました。")

def help_cliked():
    info_text.set('Open Fileを押して、ファイルを選択し、Resize ボタンでリサイズされます')
    messagebox.showinfo("Resize Help", f"Open Fileを押して、ファイルを選択し、Resize ボタンでリサイズされます。\nリサイズされたファイルは元ファイルと同じ場所に作成されます。\n Resize ボタンで 112x112, 56x56, 28x28\tResize_72 ボタンで 72x72, 36x36, 18x18 が生成されます。\n画像のぼやけが気になる場合は、No_AA を使ってください。\nアニメーションGifは強制的にアンチエイリアスが無効になります（透過処理の問題）")

if __name__ == "__main__":
    root = Tk()
    root.title('Twitch image resizer')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.geometry("650x320")

    file_path_frame = ttk.Frame(root, padding=[10,0,10,0])
    file_path_frame.columnconfigure(0, weight=1)
    file_path_frame.columnconfigure(1, weight=5)
    file_path_frame.rowconfigure(0, weight=1)
    file_path_frame.grid(sticky=(N, W, S, E))

    # Open File Button
    b1 = ttk.Button(
        file_path_frame, text='Open File', width=15,
        command=open_file_clicked)
    b1.grid(row=0, column=0, sticky=(W))

    # File Entry 
    filepath = StringVar()
    filepath_entry = ttk.Entry(
        file_path_frame,
        textvariable=filepath)
    filepath_entry.grid(row=0, column=1, sticky=(W, E))

    # style
    style = ttk.Style()
    style.configure('GreenBack.TFrame', background="green")
    style.configure('BlueBack.TFrame', background="blue")
    style.configure('RedBack.TFrame', background="red")

    style = ttk.Style()
    style.configure("BW.TLabel", foreground="white", background="black")

    # Buttons Frame
    buttons_frame = ttk.Frame(root, padding=10,)
    buttons_frame.columnconfigure(0, weight=2)
    buttons_frame.columnconfigure(1, weight=2)
    buttons_frame.columnconfigure(2, weight=2)
    buttons_frame.columnconfigure(3, weight=1)
    buttons_frame.grid(sticky=(N, W, S, E))

    # Resize frame For 112x112
    resize_112_frame = ttk.Frame(buttons_frame, padding=10,)
    resize_112_frame.rowconfigure(0, weight=1)
    resize_112_frame.rowconfigure(1, weight=1)
    resize_112_frame.rowconfigure(2, weight=1)
    resize_112_frame.rowconfigure(3, weight=1)
    resize_112_frame.rowconfigure(4, weight=1)
    resize_112_frame.grid(row=0, column=0)

    # Resize frame For 112x112 description
    button_112_description = ttk.Label(resize_112_frame, text='エモート/チャネポ向け\n112x112, 56x56, 28x28')
    button_112_description.grid(row=0, column=0,)

    # Resize Button
    resize_112_button = ttk.Button(
        resize_112_frame, text='Resize', width=20,
        command=resize_clicked)
    resize_112_button.grid(row=1, column=0, )
    resize_112_label  = ttk.Label(resize_112_frame, text='')
    resize_112_label.grid(row=2, column=0,)

    # No AA Resize Button
    resize_112_no_aa_button = ttk.Button(
        resize_112_frame, text='No_AA_Resize', width=20,
        command=lambda: resize_clicked(aa_enable=False))
    resize_112_no_aa_button.grid(row=3, column=0,)
    resize_112_no_aa_label  = ttk.Label(resize_112_frame, text='No anti-aliasing')
    resize_112_no_aa_label.grid(row=4, column=0,)

    # Resize frame For 72x72
    resize_72_frame = ttk.Frame(buttons_frame, padding=10)
    resize_72_frame.rowconfigure(0, weight=1)
    resize_72_frame.rowconfigure(1, weight=1)
    resize_72_frame.rowconfigure(2, weight=1)
    resize_72_frame.rowconfigure(3, weight=1)
    resize_72_frame.grid(row=0, column=1)

    # Resize frame For 72x72 description
    button_72_description = ttk.Label(resize_72_frame, text='バッジ向け\n72x72, 36x36, 18x18')
    button_72_description.grid(row=0, column=0,)

    resize_72_button = ttk.Button(
        resize_72_frame, text='Resize_72', width=20,
        command=lambda: resize_clicked(resize_list=[72, 36, 18]))
    resize_72_button.grid(row=1, column=0, )
    resize_72_label  = ttk.Label(resize_72_frame, text='')
    resize_72_label.grid(row=2, column=0,)

    resize_72_no_aa_button = ttk.Button(
        resize_72_frame, text='No_AA_Resize_72', width=20,
        command=lambda: resize_clicked(resize_list=[72, 36, 18],aa_enable=False))
    resize_72_no_aa_button.grid(row=3, column=0,)
    resize_72_no_aa_label  = ttk.Label(resize_72_frame, text='No anti-aliasing')
    resize_72_no_aa_label.grid(row=4, column=0,)

    # Resize frame For 320
    resize_320_frame = ttk.Frame(buttons_frame, padding=10,)
    resize_320_frame.rowconfigure(0, weight=1)
    resize_320_frame.rowconfigure(1, weight=1)
    resize_320_frame.rowconfigure(2, weight=1)
    resize_320_frame.rowconfigure(3, weight=1)
    resize_320_frame.grid(row=0, column=2,)

    # Resize frame For 320 description
    button_320_description = ttk.Label(resize_320_frame,text='バナー向け\n320')
    button_320_description.grid(row=0, column=0,)

    resize_320_button = ttk.Button(
        resize_320_frame, text='Resize_320', width=20,
        command=lambda: resize_clicked(resize_list=[320], keep_aspect=True))
    resize_320_button.grid(row=1, column=0, )
    resize_320_label  = ttk.Label(resize_320_frame, text='')
    resize_320_label.grid(row=2, column=0,)

    resize_320_no_aa_button = ttk.Button(
        resize_320_frame, text='No_AA_Resize_320', width=20,
        command=lambda: resize_clicked(resize_list=[320],aa_enable=False, keep_aspect=True))
    resize_320_no_aa_button.grid(row=3, column=0,)
    resize_320_no_aa_label  = ttk.Label(resize_320_frame, text='No anti-aliasing')
    resize_320_no_aa_label.grid(row=4, column=0,)

    # help Button
    help_button = ttk.Button(
        buttons_frame, text='Help', width=10,
        command=help_cliked)
    help_button.grid(row=0, column=3, rowspan=2, sticky=(E))

    # free size frame
    free_size_resize_frame = ttk.Frame(root, padding=10)
    free_size_resize_frame.columnconfigure(0, weight=1)  # Description
    free_size_resize_frame.columnconfigure(1, weight=1)  # Input fields
    free_size_resize_frame.columnconfigure(2, weight=1)  # Buttons
    free_size_resize_frame.grid(sticky=(N, W, S, E))

    # Left: Description Label
    free_size_description = ttk.Label(
        free_size_resize_frame,
        text='カスタムサイズ\n現在は幅のみ指定可能\n(正方形として出力)'
    )
    free_size_description.grid(row=0, column=0, padx=5)

    # Middle: Input Fields Frame
    input_frame = ttk.Frame(free_size_resize_frame)
    input_frame.grid(row=0, column=1, padx=5)

    # Width Input and Checkbox
    width_label = ttk.Label(input_frame, text='幅:')
    width_label.grid(row=0, column=0, sticky=E)
    width_var = StringVar()
    width_entry = ttk.Entry(
        input_frame,
        textvariable=width_var,
        width=10
    )
    width_entry.grid(row=0, column=1, sticky=W, padx=(5, 0))

    # Size limit override checkbox
    override_size_limit = BooleanVar()
    override_checkbox = ttk.Checkbutton(
        input_frame,
        text='制限解除',
        variable=override_size_limit
    )
    override_checkbox.grid(row=0, column=2, padx=(5, 0), sticky=W)

    # Additional note for size limit
    size_limit_note = ttk.Label(
        input_frame,
        text='※デフォルトは最大4096ピクセルまで',
        font=('', 8)
    )
    size_limit_note.grid(row=1, column=0, columnspan=3, sticky=W, pady=(2, 0))

    # Height Input (disabled)
    height_label = ttk.Label(input_frame, text='高さ:')
    height_label.grid(row=2, column=0, sticky=E)
    height_var = StringVar()
    height_entry = ttk.Entry(
        input_frame,
        textvariable=height_var,
        width=10,
        state='disabled'
    )
    height_entry.grid(row=2, column=1, sticky=W, padx=(5, 0))

    # Additional note for height
    note_label = ttk.Label(
        input_frame,
        text='※高さ指定は今後対応予定',
        font=('', 8)
    )
    note_label.grid(row=3, column=0, columnspan=3, sticky=W, pady=(2, 0))

    # Right: Buttons Frame
    button_frame = ttk.Frame(free_size_resize_frame)
    button_frame.grid(row=0, column=2, padx=5)

    def free_size_resize(aa_enable=True):
        try:
            width = int(width_var.get())
            if width <= 0:
                raise ValueError("サイズは正の整数を入力してください")
            
            # サイズ制限チェック
            if not override_size_limit.get() and width > 4096:
                messagebox.showerror(
                    "Error", 
                    "4096ピクセルを超えるサイズを指定する場合は、制限解除のチェックボックスをオンにしてください"
                )
                info_text.set("サイズが制限を超えています")
                return

            resize_clicked(resize_list=[width], aa_enable=aa_enable, keep_aspect=True)
        except ValueError as e:
            messagebox.showerror("Error", "正しいサイズを入力してください")
            info_text.set("正しいサイズを入力してください")

    free_size_button = ttk.Button(
        button_frame,
        text='リサイズ',
        width=20,
        command=lambda: free_size_resize(aa_enable=True)
    )
    free_size_button.grid(row=0, column=0, pady=(0, 5))

    free_size_no_aa_button = ttk.Button(
        button_frame,
        text='No_AA_リサイズ',
        width=20,
        command=lambda: free_size_resize(aa_enable=False)
    )
    free_size_no_aa_button.grid(row=1, column=0)

    # info frame
    info_frame = ttk.Frame(root, padding=[10,0,10,0])
    info_frame.grid()
    info_frame.columnconfigure(0, weight=1)
    info_frame.columnconfigure(1, weight=7)
    info_frame.grid(sticky=(N, W, S, E))

###--------------------------------------###



###--------------------------------------###

    # 分割線
    sep = ttk.Separator(info_frame)
    # sep.pack(fill="both")
    sep.grid(row=0, column=0, columnspan = 2,  sticky=(E,W))

    # 表示領域
    info_label = ttk.Label(
        info_frame,
        text='INFO',
    )
    info_label.grid(row=1, column=0)
    info_text = StringVar()
    info_text.set('Open Fileを押して、ファイルを選択し、Resize ボタンでリサイズされます')
    info_text_label = ttk.Label(
        info_frame,
        textvariable=info_text
    )
    info_text_label.grid(row=1, column=1)
    
    root.mainloop()