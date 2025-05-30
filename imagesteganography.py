from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import ImageTk, Image
from io import BytesIO
import os

class Hide:
    art = '''
Data hiding
In Image
    '''
    art2 = ''''''
    output_image_size = 0

    def main(self, root):
        root.title('ImageSteganography')
        root.geometry('600x700')
        root.resizable(width=True, height=True)
        f = Frame(root)

        title = Label(f, text='Secure file Sharing using \nImage Steganography')
        title.config(font=('Helvetica', 30, 'bold'), fg='blue')
        title.grid(pady=20)

        b_encode = Button(f, text='Encode', padx=20, pady=10, command=lambda: self.frame1_encode(f))
        b_encode.config(font=('Helvetica', 16, 'bold'), bg='lightgreen', fg='black')
        b_encode.grid(pady=15)
        b_decode = Button(f, text='Decode', padx=20, pady=10, command=lambda: self.frame1_decode(f))
        b_decode.config(font=('Helvetica', 16, 'bold'), bg='lightblue', fg='black')
        b_decode.grid(pady=15)

        ascii_art = Label(f, text=self.art)
        ascii_art.config(font=('Courier', 40, 'bold'), fg='purple')

        ascii_art2 = Label(f, text=self.art2)
        ascii_art2.config(font=('Courier', 14, 'bold'), fg='darkred')

        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

        f.grid()
        title.grid(row=1)
        b_encode.grid(row=2)
        b_decode.grid(row=3)
        ascii_art.grid(row=4, pady=20)
        ascii_art2.grid(row=5, pady=10)

    def home(self, frame):
        frame.destroy()
        self.main(root)

    def frame1_encode(self, f):
        f.destroy()
        f2 = Frame(root)
        label_art = Label(f2, text='ENCODE')
        label_art.config(font=('Helvetica', 50, 'bold'), fg='green')
        label_art.grid(row=1, pady=50)
        l1 = Label(f2, text='Select the Image in which \nyou want to hide text')
        l1.config(font=('Helvetica', 18), fg='darkblue')
        l1.grid()

        bws_button = Button(f2, text='Select', padx=15, pady=10, command=lambda: self.frame2_encode(f2))
        bws_button.config(font=('Helvetica', 16, 'bold'), bg='lightgreen', fg='black')
        bws_button.grid(pady=20)
        back_button = Button(f2, text='Cancel', padx=15, pady=10, command=lambda: self.home(f2))
        back_button.config(font=('Helvetica', 16, 'bold'), bg='lightcoral', fg='black')
        back_button.grid(pady=15)
        f2.grid()

    def frame2_encode(self, f2):
        ep = Frame(root)
        myfile = filedialog.askopenfilename(filetypes=[('png', '*.png'), ('jpeg', '*.jpeg'), ('jpg', '*.jpg'),('All Files', '*.*')])
        if not myfile:
            messagebox.showerror("Error", "You have selected nothing!")
        else:
            myimg = Image.open(myfile)
            myimage = myimg.resize((300, 200))
            img = ImageTk.PhotoImage(myimage)
            l3 = Label(ep, text='Selected Image')
            l3.config(font=('Helvetica', 18, 'bold'), fg='darkblue')
            l3.grid(pady=10)
            panel = Label(ep, image=img)
            panel.image = img
            self.output_image_size = os.stat(myfile).st_size
            self.o_image_w, self.o_image_h = myimg.size
            panel.grid()
            l2 = Label(ep, text='Enter the message')
            l2.config(font=('Helvetica', 18, 'bold'), fg='darkblue')
            l2.grid(pady=15)
            text_area = Text(ep, width=50, height=10, font=('Helvetica', 12))
            text_area.grid()
            encode_button = Button(ep, text='Cancel', padx=15, pady=10, command=lambda: self.home(ep))
            encode_button.config(font=('Helvetica', 14, 'bold'), bg='lightcoral', fg='black')
            encode_button.grid(pady=10)
            back_button = Button(ep, text='Encode', padx=15, pady=10, command=lambda: [self.enc_fun(text_area, myimg), self.home(ep)])
            back_button.config(font=('Helvetica', 14, 'bold'), bg='lightgreen', fg='black')
            back_button.grid(pady=15)
            ep.grid(row=1)
            f2.destroy()

    def frame1_decode(self, f):
        f.destroy()
        d_f2 = Frame(root)
        label_art = Label(d_f2, text='DECODE')
        label_art.config(font=('Helvetica', 50, 'bold'), fg='green')
        label_art.grid(row=1, pady=50)
        l1 = Label(d_f2, text='Select Image With Hidden Text: ')
        l1.config(font=('Helvetica', 18, 'bold'), fg='darkblue')
        l1.grid()

        bws_button = Button(d_f2, text='Select', padx=15, pady=10, command=lambda: self.frame2_decode(d_f2))
        bws_button.config(font=('Helvetica', 16, 'bold'), bg='lightblue', fg='black')
        bws_button.grid(pady=20)
        back_button = Button(d_f2, text='Cancel', padx=15, pady=10, command=lambda: self.home(d_f2))
        back_button.config(font=('Helvetica', 16, 'bold'), bg='lightcoral', fg='black')
        back_button.grid(pady=15)
        d_f2.grid()

    def frame2_decode(self, d_f2):
        d_f3 = Frame(root)
        myfile = filedialog.askopenfilename(filetypes=[('png', '*.png'), ('jpeg', '*.jpeg'), ('jpg', '*.jpg'), ('All Files', '*.*')])
        if not myfile:
            messagebox.showerror("Error", "Nothing Selected")
        else:
            myimg = Image.open(myfile, 'r')
            myimage = myimg.resize((300, 200))
            img = ImageTk.PhotoImage(myimage)
            l4 = Label(d_f3, text="Selected Image: ")
            l4.config(font=('Helvetica', 18, 'bold'), fg='darkblue')
            l4.grid(pady=10)
            panel = Label(d_f3, image=img)
            panel.image = img
            panel.grid()
            hidden_data = self.decode(myimg)
            l2 = Label(d_f3, text='Hidden data is: ')
            l2.config(font=('Helvetica', 18, 'bold'), fg='darkblue')
            l2.grid(pady=10)
            text_area = Text(d_f3, width=50, height=10, font=('Helvetica', 12))
            text_area.insert(INSERT, hidden_data)
            text_area.grid()
            back_button = Button(d_f3, text='Cancel', padx=15, pady=10, command=lambda: self.home(d_f3))
            back_button.config(font=('Helvetica', 14, 'bold'), bg='lightcoral', fg='black')
            back_button.grid(pady=15)
            show_info = Button(d_f3, text='More Info', padx=15, pady=10, command=self.info)
            show_info.config(font=('Helvetica', 14, 'bold'), bg='lightblue', fg='black')
            show_info.grid(pady=10)
            d_f3.grid(row=1)
            d_f2.destroy()

    def decode(self, image):
        data = ''
        imgdata = iter(image.getdata())

        while True:
            pixels = [value for value in imgdata.__next__()[:3] +
                      imgdata.__next__()[:3] +
                      imgdata.__next__()[:3]]
            binstr = ''
            for i in pixels[:8]:
                if i % 2 == 0:
                    binstr += '0'
                else:
                    binstr += '1'

            data += chr(int(binstr, 2))
            if pixels[-1] % 2 != 0:
                return data

    def info(self):
        try:
            info_str = (
                'original image:-\n'
                f'size of original image: {self.output_image_size / 1000000:.2f}mb\n'
                f'width: {self.o_image_w}\n'
                f'height: {self.o_image_h}\n\n'
                'decoded image:- \n'
                f'size of decoded image: {self.d_image_size / 1000000:.2f}mb\n'
                f'width: {self.d_image_w}\n'
                f'height: {self.d_image_h}'
            )
            messagebox.showinfo('Info', info_str)
        except Exception as e:
            messagebox.showinfo('Info', f'Unable to get the information: {e}')

    def genData(self, data):
        newd = []

        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd

    def modPix(self, pix, data):
        datalist = self.genData(data)
        lendata = len(datalist)
        imdata = iter(pix)
        for i in range(lendata):
            pix = [value for value in imdata.__next__()[:3] +
                   imdata.__next__()[:3] +
                   imdata.__next__()[:3]]
            for j in range(0, 8):
                if (datalist[i][j] == '0') and (pix[j] % 2 != 0):
                    pix[j] -= 1
                elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                    pix[j] -= 1
            if i == lendata - 1:
                if pix[-1] % 2 == 0:
                    pix[-1] -= 1
            else:
                if pix[-1] % 2 != 0:
                    pix[-1] -= 1
            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

    def encode_enc(self, newimg, data):
        w = newimg.size[0]
        (x, y) = (0, 0)

        for pixel in self.modPix(newimg.getdata(), data):
            newimg.putpixel((x, y), pixel)
            if x == w - 1:
                x = 0
                y += 1
            else:
                x += 1

    def enc_fun(self, text_area, myimg):
        data = text_area.get("1.0", "end-1c")
        if len(data) == 0:
            messagebox.showinfo("Alert", "Kindly enter text in TextBox")
        else:
            newimg = myimg.copy()
            self.encode_enc(newimg, data)
            temp = os.path.splitext(os.path.basename(myimg.filename))[0]
            save_path = filedialog.asksaveasfilename (initialfile=temp, filetypes=[('png', '*.png')], defaultextension=".png")
            newimg.save(save_path)
            self.d_image_size = os.stat(save_path).st_size
            self.d_image_w, self.d_image_h = newimg.size
            messagebox.showinfo("Success", f"Encoding Successful\nFile is saved as {save_path}")


root = Tk()

o = Hide()
o.main(root)

root.mainloop()