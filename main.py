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

def resize_clicked(resize_list=[112, 56, 28], aa_enable=True):
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
            twitch_resize.twitch_resize_func(resize_filepath, resize_list, aa_enable)
        except ValueError as e:
            messagebox.showerror("Error", "ファイルが画像でない可能性があります。")
            info_text.set("ファイルが画像でない可能性があります。")
            return -1
        info_text.set("リサイズが完了しました。")
        # messagebox.showinfo("info", "リサイズが完了しました。")

def help_cliked():
    info_text.set('Open Fileを押して、ファイルを選択し、Resize ボタンでリサイズされます')
    messagebox.showinfo("Resize Help", f"Open Fileを押して、ファイルを選択し、Resize ボタンでリサイズされます。\nリサイズされたファイルは元ファイルと同じ場所に作成されます。\n Resize ボタンで 112x112, 56x56, 28x28\tResize_72 ボタンで 72x72, 36x36, 18x18 が生成されます。\n画像のぼやけが気になる場合は、No_AA を使ってください。")

if __name__ == "__main__":
    root = Tk()
    root.title('Twitch icon resizer')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.geometry("600x200")

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

    # Buttons Frame
    buttons_frame = ttk.Frame(root, padding=10)
    buttons_frame.columnconfigure(0, weight=3)
    buttons_frame.columnconfigure(1, weight=1)
    buttons_frame.rowconfigure(0, weight=1)
    buttons_frame.rowconfigure(1, weight=1)
    buttons_frame.grid(sticky=(N, W, S, E))

    # Resize Button frame
    resize_button_frame = ttk.Frame(buttons_frame, padding=10)
    resize_button_frame.columnconfigure(0, weight=1)
    resize_button_frame.columnconfigure(1, weight=1)
    resize_button_frame.rowconfigure(0, weight=1)
    resize_button_frame.rowconfigure(1, weight=1)
    resize_button_frame.grid(row=0, column=0, sticky=(N, W, S, E))

    # Resize Button
    resize_112_button = ttk.Button(
        resize_button_frame, text='Resize', width=20,
        command=resize_clicked)
    resize_112_button.grid(row=0, column=0, )
    resize_112_label  = ttk.Label(resize_button_frame, text='112x112, 56x56, 28x28')
    resize_112_label.grid(row=1, column=0,)

    resize_72_button = ttk.Button(
        resize_button_frame, text='Resize_72', width=20,
        command=lambda: resize_clicked(resize_list=[72, 36, 18]))
    resize_72_button.grid(row=0, column=1, )
    resize_72_label  = ttk.Label(resize_button_frame, text='72x72, 36x36, 18x18')
    resize_72_label.grid(row=1, column=1,)

    # No AA Resize Button frame
    resize_button_no_aa_frame = ttk.Frame(buttons_frame, padding=10)
    resize_button_no_aa_frame.columnconfigure(0, weight=1)
    resize_button_no_aa_frame.columnconfigure(1, weight=1)
    resize_button_no_aa_frame.rowconfigure(0, weight=1)
    resize_button_no_aa_frame.rowconfigure(1, weight=1)
    resize_button_no_aa_frame.grid(row=1, column=0, sticky=(N, W, S, E))

    # No AA Resize Button
    resize_112_no_aa_button = ttk.Button(
        resize_button_no_aa_frame, text='No_AA_Resize', width=20,
        command=lambda: resize_clicked(aa_enable=False))
    resize_112_no_aa_button.grid(row=0, column=0,)
    resize_112_no_aa_label  = ttk.Label(resize_button_no_aa_frame, text='No anti-aliasing 112x112, 56x56, 28x28')
    resize_112_no_aa_label.grid(row=1, column=0,)

    resize_72_no_aa_button = ttk.Button(
        resize_button_no_aa_frame, text='No_AA_Resize_72', width=20,
        command=lambda: resize_clicked(resize_list=[72, 36, 18],aa_enable=False))
    resize_72_no_aa_button.grid(row=0, column=1,)
    resize_72_no_aa_label  = ttk.Label(resize_button_no_aa_frame, text='No anti-aliasing 72x72, 36x36, 18x18')
    resize_72_no_aa_label.grid(row=1, column=1,)

    # help Button
    help_button = ttk.Button(
        buttons_frame, text='Help', width=10,
        command=help_cliked)
    help_button.grid(row=0, column=1, rowspan=2, sticky=(E))


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
    sep.pack(fill="both")
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