from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import ImageTk, Image
import os
import wave
import numpy as np
import io

class Hide:
    art = '''
Data hiding
In Audio
    '''
    art2 = ''''''
    output_audio_size = 0

    def main(self, root):
        root.title('AudioSteganography')
        root.geometry('600x700')
        root.resizable(width=True, height=True)
        f = Frame(root)

        title = Label(f, text='Secure file Sharing using \nAudio Steganography')
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
        l1 = Label(f2, text='Select the Audio file in which \nyou want to hide image')
        l1.config(font=('Helvetica', 18), fg='darkblue')
        l1.grid()

        bws_button = Button(f2, text='Select Audio', padx=15, pady=10, command=lambda: self.frame2_encode(f2))
        bws_button.config(font=('Helvetica', 16, 'bold'), bg='lightgreen', fg='black')
        bws_button.grid(pady=20)
        back_button = Button(f2, text='Cancel', padx=15, pady=10, command=lambda: self.home(f2))
        back_button.config(font=('Helvetica', 16, 'bold'), bg='lightcoral', fg='black')
        back_button.grid(pady=15)
        f2.grid()

    def frame2_encode(self, f2):
        ep = Frame(root)
        audio_file = filedialog.askopenfilename(filetypes=[('WAV', '*.wav'), ('All Files', '*.*')])
        if not audio_file:
            messagebox.showerror("Error", "You have selected nothing!")
            self.home(ep)
            return
        
        try:
            # Get audio info
            with wave.open(audio_file, 'rb') as audio:
                params = audio.getparams()
                self.o_audio_frames = audio.getnframes()
                self.o_audio_channels = params.nchannels
                self.o_audio_samplewidth = params.sampwidth
                self.o_audio_framerate = params.framerate
                self.output_audio_size = os.stat(audio_file).st_size
            
            # Now ask for image to hide
            image_file = filedialog.askopenfilename(filetypes=[('png', '*.png'), ('jpeg', '*.jpeg'), ('jpg', '*.jpg'), ('All Files', '*.*')])
            if not image_file:
                messagebox.showerror("Error", "No image selected!")
                self.home(ep)
                return
            
            # Display the image to be hidden
            myimg = Image.open(image_file)
            myimage = myimg.resize((300, 200))
            img = ImageTk.PhotoImage(myimage)
            
            l3 = Label(ep, text='Image to be hidden:')
            l3.config(font=('Helvetica', 18, 'bold'), fg='darkblue')
            l3.grid(pady=10)
            
            panel = Label(ep, image=img)
            panel.image = img
            panel.grid()
            
            encode_button = Button(ep, text='Cancel', padx=15, pady=10, command=lambda: self.home(ep))
            encode_button.config(font=('Helvetica', 14, 'bold'), bg='lightcoral', fg='black')
            encode_button.grid(pady=10)
            
            back_button = Button(ep, text='Encode', padx=15, pady=10, 
                               command=lambda: [self.encode_audio_image(audio_file, image_file), self.home(ep)])
            back_button.config(font=('Helvetica', 14, 'bold'), bg='lightgreen', fg='black')
            back_button.grid(pady=15)
            
            ep.grid(row=1)
            f2.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process files: {str(e)}")
            self.home(ep)

    def frame1_decode(self, f):
        f.destroy()
        d_f2 = Frame(root)
        label_art = Label(d_f2, text='DECODE')
        label_art.config(font=('Helvetica', 50, 'bold'), fg='green')
        label_art.grid(row=1, pady=50)
        l1 = Label(d_f2, text='Select Audio With Hidden Image: ')
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
        audio_file = filedialog.askopenfilename(filetypes=[('WAV', '*.wav'), ('All Files', '*.*')])
        if not audio_file:
            messagebox.showerror("Error", "Nothing Selected")
            self.home(d_f3)
            return
        
        try:
            # Decode the image from audio
            hidden_image = self.decode_audio_image(audio_file)
            
            if hidden_image is None:
                messagebox.showerror("Error", "No hidden image found or decoding failed")
                self.home(d_f3)
                return
            
            # Display the decoded image
            myimage = hidden_image.resize((300, 200))
            img = ImageTk.PhotoImage(myimage)
            
            l4 = Label(d_f3, text="Hidden Image: ")
            l4.config(font=('Helvetica', 18, 'bold'), fg='darkblue')
            l4.grid(pady=10)
            
            panel = Label(d_f3, image=img)
            panel.image = img
            panel.grid()
            
            # Save button
            save_button = Button(d_f3, text='Save Image', padx=15, pady=10, 
                               command=lambda: self.save_image(hidden_image))
            save_button.config(font=('Helvetica', 14, 'bold'), bg='lightgreen', fg='black')
            save_button.grid(pady=15)
            
            back_button = Button(d_f3, text='Cancel', padx=15, pady=10, command=lambda: self.home(d_f3))
            back_button.config(font=('Helvetica', 14, 'bold'), bg='lightcoral', fg='black')
            back_button.grid(pady=10)
            
            d_f3.grid(row=1)
            d_f2.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Decoding failed: {str(e)}")
            self.home(d_f3)

    def save_image(self, image):
        save_path = filedialog.asksaveasfilename(filetypes=[('PNG', '*.png')], defaultextension=".png")
        if save_path:
            try:
                image.save(save_path)
                messagebox.showinfo("Success", f"Image successfully saved as {save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")

    def encode_audio_image(self, audio_path, image_path):
        try:
            # Read the image data
            with open(image_path, 'rb') as img_file:
                image_data = img_file.read()
            
            # Convert image data to binary string
            binary_data = ''.join([format(byte, '08b') for byte in image_data])
            
            # Add header to mark the start and end of image data
            header = 'IMGSTART' + str(len(binary_data)) + 'IMGEND'
            header_binary = ''.join([format(ord(char), '08b') for char in header])
            full_data = header_binary + binary_data
            
            # Read the audio file
            with wave.open(audio_path, 'rb') as audio:
                params = audio.getparams()
                frames = audio.readframes(audio.getnframes())
                audio_array = np.frombuffer(frames, dtype=np.int16)
            
            # Check if audio is large enough
            if len(full_data) > len(audio_array):
                messagebox.showerror("Error", "Audio file is too small to hide this image")
                return False
            
            # Make a copy of the array to avoid modifying the original
            audio_array_copy = audio_array.copy()
            
            # Encode the data in LSB of audio samples
            for i in range(len(full_data)):
                bit = int(full_data[i])
                audio_array_copy[i] = (audio_array_copy[i] & ~1) | bit
            
            # Save the new audio file
            temp = os.path.splitext(os.path.basename(audio_path))[0]
            save_path = filedialog.asksaveasfilename(
                initialfile=temp + "_encoded",
                filetypes=[('WAV', '*.wav')],
                defaultextension=".wav"
            )
            
            if save_path:
                with wave.open(save_path, 'wb') as output:
                    output.setparams(params)
                    output.writeframes(audio_array_copy.tobytes())
                
                self.d_audio_size = os.stat(save_path).st_size
                messagebox.showinfo("Success", f"Encoding Successful\nFile is saved as {save_path}")
                return True
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Encoding failed: {str(e)}")
            return False

    def decode_audio_image(self, audio_path):
        try:
            
            with wave.open(audio_path, 'rb') as audio:
                frames = audio.readframes(audio.getnframes())
                audio_array = np.frombuffer(frames, dtype=np.int16)
            
            
            binary_data = ''.join([str(sample & 1) for sample in audio_array])
            
            
            header_marker = ''.join([format(ord(char), '08b') for char in 'IMGSTART'])
            header_start = binary_data.find(header_marker)
            if header_start == -1:
                return None
            
            
            end_marker = ''.join([format(ord(char), '08b') for char in 'IMGEND'])
            length_start = header_start + len(header_marker)
            length_end = binary_data.find(end_marker, length_start)
            if length_end == -1:
                return None
            
            
            length_str = binary_data[length_start:length_end]
            try:
                
                length = int(''.join([chr(int(length_str[i:i+8], 2)) for i in range(0, len(length_str), 8)]))
            except:
                return None
            
            
            data_start = length_end + len(end_marker)
            data_end = data_start + length
            if data_end > len(binary_data):
                return None
            
            image_binary = binary_data[data_start:data_end]
            
            
            image_bytes = bytearray()
            for i in range(0, len(image_binary), 8):
                byte = image_binary[i:i+8]
                if len(byte) < 8:  
                    byte = byte.ljust(8, '0')
                image_bytes.append(int(byte, 2))
            
            
            try:
                image = Image.open(io.BytesIO(image_bytes))
                return image
            except Exception as e:
                print(f"Image creation error: {str(e)}")
                return None
        except Exception as e:
            print(f"Decoding error: {str(e)}")
            return None

    def info(self):
        try:
            info_str = (
                'original audio:-\n'
                f'size of original audio: {self.output_audio_size / 1000000:.2f}mb\n'
                f'frames: {self.o_audio_frames}\n'
                f'channels: {self.o_audio_channels}\n'
                f'sample width: {self.o_audio_samplewidth}\n'
                f'frame rate: {self.o_audio_framerate}\n\n'
                'encoded audio:- \n'
                f'size of encoded audio: {self.d_audio_size / 1000000:.2f}mb'
            )
            messagebox.showinfo('Info', info_str)
        except Exception as e:
            messagebox.showinfo('Info', f'Unable to get the information: {e}')


root = Tk()
o = Hide()
o.main(root)
root.mainloop()
