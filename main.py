from tkinter import *
from tkinter import filedialog, messagebox
import cv2
import time
from functools import partial
from PIL import Image
import PIL.ImageTk
from tkinter.font import BOLD
import my_module

listItem = [
    "Cân bằng histogram",
    "Tách ngưỡng",
    "Lấy âm bản",
    "Biến đổi Logarith",
    "Tăng tương phản",
    "Lọc trung bình",
    "Lọc trung vị",
    "Lọc Gaussian",
    "Lọc sắc nét",
    "Lấy ảnh gradient",
    "Nhận diện biên",
    "Lọc thông thấp",
    "Lọc thông cao",
    "Lọc Bilateral",
    "Lọc NonLocalMeans"
]
listFunc = [
    my_module.can_bang_histogram,
    my_module.tach_nguong,
    my_module.am_ban,
    my_module.logarith,
    my_module.tang_tuong_phan,
    my_module.loc_trung_binh,
    my_module.loc_trung_vi,
    my_module.loc_gauss,
    my_module.loc_sac_net,
    my_module.gradient,
    my_module.nhan_dien_bien,
    my_module.thong_thap_LPF,
    my_module.thong_cao_HPF,
    my_module.bilateral,
    my_module.nonLocalMeans ]

def process(current):
    #global: biến toàn cục
    global cv_final
    global original_height,original_width

    #nhận diện nút đc ấn
    for i in range(15):
        # btn đc ấn (raised)
        btn[i].configure(relief=RAISED)
    #nút đó có hiệu ứng đóng vào bên trong (sunken)
    btn[current].configure(relief=SUNKEN)

    start_time = time.time()
    end_time = time.time()
    cv_final = listFunc[current](cv_img)[0]
    
    print('Thời gian thực hiện phép %s là %f ms' %
          (listItem[current], (end_time-start_time)*1000))

    temp_image = cv_final# Copy ảnh kết quả


    if original_width > original_height:
        ratio = original_width / original_height
        preview_image = cv2.resize(temp_image, (int(320), int(320 / ratio)))

    elif original_width <= original_height:
        ratio = original_height / original_width
        preview_image = cv2.resize(temp_image, (int(320 / ratio), int(320)))

    #đổi định dạng ảnh từ BGR->RGB
    pil_preview = cv2.cvtColor(preview_image, cv2.COLOR_BGR2RGB)
    
    new = PIL.ImageTk.PhotoImage(Image.fromarray(pil_preview))
    imgR.configure(image=new)
    imgR.image = new


#cập nhật giao diện ng dùng khi hình ảnh thay đổi
def update_UI(old, new):
    imgL.configure(image=old)#cập nhật
    imgR.configure(image=new)

    imgL.image = old#gán
    imgR.image = new

    labelL.pack()#hiển thị nhãn lên giao diện
    imgL.pack()
    btn_open.pack(pady=5)# 1 ~ dọc = 5 pixel.

    labelR.pack()
    imgR.pack()
    btn_save.pack(pady=5)
    
    #kích thước của các btn
    for i in range(15):
        btn[i] = Button(footer, text=listItem[i],
                        relief=RAISED, command=partial(process, i), width=15, height=1, padx=5, pady=5)
        
        btn[i].grid(row=int(i / 5), column=i % 5)#1 hàng có 5 btn


def select_img():
    global cv_img, ratio
    global original_height, original_width

    path = filedialog.askopenfilename()

    try:
        cv_img = cv2.imread(path)
        h,w,_ = cv_img.shape
        original_height = h
        original_width = w

        if w>h :
            ratio = w / h 
            cv_preview = cv2.resize(cv_img, (int(320), int(320 / ratio)))
        elif w<=h :
            ratio = h / w
            cv_preview = cv2.resize(cv_img, (int(320 / ratio),int(320)))
        pil_img = cv2.cvtColor(cv_preview, cv2.COLOR_BGR2RGB)

        old = PIL.ImageTk.PhotoImage(Image.fromarray(pil_img))
        new = PIL.ImageTk.PhotoImage(Image.fromarray(pil_img))

        b.destroy()
        update_UI(old, new)
    except:
        if(path != ''):
            messagebox.showerror("ERROR", "Vui lòng chọn đúng định dạng ảnh!")


def save_img():
    path = filedialog.asksaveasfilename(initialdir="/", title="Select file", filetypes=(
        ('JPEG', ('*.jpg', '*.jpeg', '*.jpe')), ('PNG', '*.png'), ('BMP', ('*.bmp', '*.jdib')), ('GIF', '*.gif')))
    
    filetypes = (
            ('JPEG', ('.jpg', '.jpeg', '.jpe')),
            ('PNG', '.png'),
            ('BMP', ('.bmp', '.jdib')),
            ('GIF', '.gif')
        )
    file_type_index = None
    for index, (type_name, type_ext) in enumerate(filetypes):
        if path.endswith(type_ext):
            file_type_index = index
            break

    if file_type_index is None:
        file_type_index = 0

    file_type_exts = filetypes[file_type_index][1]

    ext_match = False
    for ext in file_type_exts:
        if path.endswith(ext):
            ext_match = True
            break

    if not ext_match:
        path += file_type_exts[0]

    cv2.imwrite(path, cv_final)


win = Tk()#tạo 1 form
win.resizable(width=False,height=False)
win.title("Xử lý ảnh")

header = Frame()#1 khung giao diện mới = header
content = Label(
    header, text="CHƯƠNG TRÌNH THỰC HIỆN CÁC PHÉP XỬ LÝ ẢNH", font=("Arial", 20))
content.pack()# nhãn content đc gói trong header
header.pack(side=TOP)# đặt ở TOP của khung 

body = Frame()#1 khung giao diện mới = body

bodyL = LabelFrame(body)#con của body
labelL = Label(bodyL, text="Ảnh ban đầu", font=(10))
imgL = Label(bodyL)
btn_open = Button(bodyL, text="Chọn ảnh khác", command=select_img)
bodyL.pack(side=LEFT)# nhãn bodyL đc đặt ở LEFT của khung

bodyR = LabelFrame(body)#con của body
labelR = Label(bodyR, text="Ảnh sau khi xử lý", font=("Segoe UI",10))
imgR = Label(bodyR)
btn_save = Button(bodyR, text="Lưu kết quả", command=save_img)
bodyR.pack(side=RIGHT)# nhãn bodyR đc đặt ở RIGHT của khung


body.pack(side=TOP, pady=10)

footer = Frame()
btn = [0] * 15 #gồm 15 phần tử
footer.pack(side=BOTTOM)#đặt footer ở dưới 

#tạo 1 nút bấm mới
b = Button(text="Chọn file ảnh", command=select_img)
b.pack(ipadx=10, ipady=10, pady=10)
cv_final = ''
cv_img = ''
original_w = 0
original_h = 0
ratio = 0

if __name__ == "__main__":
    mainloop()


#C:/Users/HP/AppData/Local/Microsoft/WindowsApps/python3.12.exe "d:/xử lí ảnh/NguyenThiLinhNhi_94318-DeTai1/xu_ly_anh/code/main.py"
#C:/Users/HP/AppData/Local/Microsoft/WindowsApps/python3.12.exe -m pip install --upgrade --force-reinstall Pillow
#pip install Pillow