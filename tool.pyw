from gui import App
from tkinter import BOTH, filedialog
from tkinter.ttk import Notebook, Frame
import windnd
from utility import merge_pdf_by_path, split_pdf_by_path, encrypt_pdf_by_path, decrypt_pdf_by_path, watermark_pdf_by_path, get_current_time_string, get_filename


app =  App({'title':'pdf工具箱2.1(李小龙@安联检测)','size':(375,292),'loc':(500,300)})

root = app.instance

note=Notebook(root) 
note.pack(fill=BOTH,expand=True)

fr1=Frame(root,relief='ridge', borderwidth=1) 
fr2=Frame(root,relief='ridge', borderwidth=1) 
fr3=Frame(root,relief='ridge', borderwidth=1) 
fr4=Frame(root,relief='ridge', borderwidth=1) 

note.add(fr1,text='合并')
note.add(fr2,text='分割')
note.add(fr3,text='加/解密')
note.add(fr4,text='水印')


merge_dst_var = app.string_var(f'合并导出{get_current_time_string()}.pdf')
split_dst_var = app.string_var(f'分割导出{get_current_time_string()}.pdf')
split_src_var = app.string_var(f'')
split_page_start_var = app.string_var(f'1')
split_page_end_var = app.string_var(f'1')
crypt_dst_var = app.string_var(f'加解密导出{get_current_time_string()}.pdf')
crypt_src_var = app.string_var(f'')
crypt_pwd_var = app.string_var(f'')
watermark_dst_var = app.string_var(f'水印导出{get_current_time_string()}.pdf')
watermark_src_var = app.string_var('')
watermark_wmk_var = app.string_var('')


menu = None
file_paths = [
]

label = app.label(fr1, '导出文件')
label.pack()
label.place(x=1,y=5)

ipt = app.input(fr1, merge_dst_var, width=27)
ipt.pack()
ipt.place(x=55,y=5)

label = app.label(fr2, '导出文件')
label.pack()
label.place(x=1,y=5)

ipt = app.input(fr2, split_dst_var, width=43)
ipt.pack()
ipt.place(x=55,y=5)

label = app.label(fr2, '输入文件')
label.pack()
label.place(x=1,y=35)

ipt = app.input(fr2, split_src_var, width=34, state="disabled")
ipt.pack()
ipt.place(x=55,y=35)

label = app.label(fr2, '开始页')
label.pack()
label.place(x=1,y=65)

ipt = app.input(fr2, split_page_start_var, width=3)
ipt.pack()
ipt.place(x=55,y=65)

label = app.label(fr2, '结束页')
label.pack()
label.place(x=85,y=65)

ipt = app.input(fr2, split_page_end_var, width=3)
ipt.pack()
ipt.place(x=131,y=65)

label = app.label(fr3, '导出文件')
label.pack()
label.place(x=1,y=5)

ipt = app.input(fr3, crypt_dst_var, width=43)
ipt.pack()
ipt.place(x=55,y=5)

label = app.label(fr3, '输入文件')
label.pack()
label.place(x=1,y=35)

ipt = app.input(fr3, crypt_src_var, width=34, state="disabled")
ipt.pack()
ipt.place(x=55,y=35)

label = app.label(fr3, '密码')
label.pack()
label.place(x=1,y=65)

ipt = app.input(fr3, crypt_pwd_var, width=30)
ipt.pack()
ipt.place(x=55,y=65)

label = app.label(fr4, '导出文件')
label.pack()
label.place(x=1,y=5)

ipt = app.input(fr4, watermark_dst_var, width=43)
ipt.pack()
ipt.place(x=55,y=5)

label = app.label(fr4, '输入文件')
label.pack()
label.place(x=1,y=35)

ipt = app.input(fr4, watermark_src_var, width=34, state="disabled")
ipt.pack()
ipt.place(x=55,y=35)

label = app.label(fr4, '水印文件')
label.pack()
label.place(x=1,y=65)

ipt = app.input(fr4, watermark_wmk_var, width=34, state="disabled")
ipt.pack()
ipt.place(x=55,y=65)



def render_filelist():
    global menu
    global file_paths
    menu = app.menu(fr1, [get_filename(file_path) for file_path in file_paths], width=51, height=10)
    menu.pack()
    menu.place(x=3,y=30)


def select_files():
    global file_paths
    selected_files = filedialog.askopenfilenames()
    file_paths = [*file_paths, *selected_files]
    render_filelist()
    

def dragged_files(files):
    global file_paths
    file_paths = [*file_paths, *[file.decode('gbk') for file in files]]
    render_filelist()


def delete_file():
    global menu
    global file_paths
    value = menu.curselection()
    index = value[0] if value else 0
    del file_paths[index]
    render_filelist()


def merge_files():
    global file_paths
    global merge_dst_var
    filename = merge_dst_var.get()
    print(filename)
    try:
        merge_pdf_by_path(file_paths, filename)
    except Exception as e:
        app.alert('提示', f'合并导出失败：{e}')
        return 
    app.alert('提示', '合并导出成功')


def split_file():
    global split_src_var
    global split_dst_var
    global split_page_start_var
    global split_page_end_var
    src_path = split_src_var.get()
    dst_path = split_dst_var.get()
    page_start = int(split_page_start_var.get())
    page_end = int(split_page_end_var.get())
    try:
        split_pdf_by_path(src_path, dst_path, page_start, page_end)
    except Exception as e:
        app.alert('提示', f'分割导出失败：{e}')
        return 
    app.alert('提示', '分割导出成功')


def encrypt_file():
    global crypt_src_var
    global crypt_dst_var
    global crypt_pwd_var
    src_path = crypt_src_var.get()
    dst_path = crypt_dst_var.get()
    password = crypt_pwd_var.get()
    try:
        encrypt_pdf_by_path(src_path, dst_path, password)
    except Exception as e:
        app.alert('提示', f'加密导出失败：{e}')
        return 
    app.alert('提示', '加密导出成功')


def decrypt_file():
    global crypt_src_var
    global crypt_dst_var
    global crypt_pwd_var
    src_path = crypt_src_var.get()
    dst_path = crypt_dst_var.get()
    password = crypt_pwd_var.get()
    try:
        decrypt_pdf_by_path(src_path, dst_path, password)
    except Exception as e:
        app.alert('提示', f'解密导出失败：{e}')
        return 
    app.alert('提示', '解密导出成功')


def watermark_file():
    global watermark_src_var
    global watermark_dst_var
    global watermark_wmk_var
    src_path = watermark_src_var.get()
    dst_path = watermark_dst_var.get()
    wmk_path = watermark_wmk_var.get()
    try:
        watermark_pdf_by_path(src_path, dst_path, wmk_path)
    except Exception as e:
        app.alert('提示', f'水印导出失败：{e}')
        return 
    app.alert('提示', '水印导出成功')


def select_split_src_file():
    global split_src_var
    selected_file = filedialog.askopenfilename()
    split_src_var.set(selected_file)


def select_crypt_src_file():
    global crypt_src_var
    selected_file = filedialog.askopenfilename()
    crypt_src_var.set(selected_file)


def select_watermark_src_file():
    global watermark_src_var
    selected_file = filedialog.askopenfilename()
    watermark_src_var.set(selected_file)


def select_watermark_wmk_file():
    global watermark_wmk_var
    selected_file = filedialog.askopenfilename()
    watermark_wmk_var.set(selected_file)


btn = app.button(fr1, '添加', select_files, width=7)
btn.pack()
btn.place(x=250,y=2)


btn = app.button(fr1, '删除', delete_file, width=7)
btn.pack()
btn.place(x=304,y=2)


btn = app.button(fr1, '合并', merge_files , width=13)
btn.pack()
btn.place(x=130,y=220)


btn = app.button(fr2, '浏览', select_split_src_file, width=7)
btn.pack()
btn.place(x=300,y=32)


btn = app.button(fr2, '分割', split_file , width=13)
btn.pack()
btn.place(x=130,y=220)

btn = app.button(fr3, '浏览', select_crypt_src_file, width=7)
btn.pack()
btn.place(x=300,y=32)

btn = app.button(fr3, '加密', encrypt_file , width=7)
btn.pack()
btn.place(x=120,y=220)

btn = app.button(fr3, '解密', decrypt_file , width=7)
btn.pack()
btn.place(x=180,y=220)

btn = app.button(fr4, '浏览', select_watermark_src_file, width=7)
btn.pack()
btn.place(x=300,y=32)

btn = app.button(fr4, '浏览', select_watermark_wmk_file, width=7)
btn.pack()
btn.place(x=300,y=62)

btn = app.button(fr4, '添加水印', watermark_file , width=13)
btn.pack()
btn.place(x=130,y=220)

render_filelist()
windnd.hook_dropfiles(root, func=dragged_files)
app.run()