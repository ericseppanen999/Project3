## CMPT 365 Project 3 Question 2 ## 

# dialogs from project 2, scrap other dropdowns

# constructor

# initialize

# huffman, lossless helper functions
# similar to project 2 implementation

import tkinter as tk
from tkinter import filedialog, Menu
import numpy as np
from PIL import Image
import random
from PQ import MinHeap, Node

class BMPViewer(tk.Tk):
    # BMP viewer initializer
    def __init__(self):
        tk.Tk.__init__(self)
        print("intializing")

        # set window title and size
        self.title("CMPT 365 - Project 2, Photo Editing")
        self.geometry("1200x500")

        # create frame
        self.frame = tk.Frame(self)
        self.frame.pack()

        # canvas for original image
        self.canvas=tk.Canvas(self.frame,width=100,height=100,bg="white")
        self.canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        
        # variable to store selected core operation
        self.selected_option=tk.StringVar()
        self.selected_option.set(None)
        self.selected_option.trace_add("write",self.handle_selection)

        # variable to store file path
        self.filepath=tk.StringVar()
        self.filepath.set(None)

        self.create_menus()



    def create_menus(self):
        print("* C * creating menus")

        # create main menu
        main_menu =Menu(self)
        self.config(menu=main_menu)

        # create core operations dropdown menu    
        core_dropdown_menu=Menu(main_menu,tearoff=False)
        core_options=["open file","exit"]
        for option in core_options:
            # add radio buttons for each core operation
            core_dropdown_menu.add_radiobutton(label=option,variable=self.selected_option,value=option)
        main_menu.add_cascade(label="Core Operations",menu=core_dropdown_menu)


    def open_file_dialog(self):
        print("* O_F * opening file dialog")

        # open file dialog to select BMP file
        file_path=filedialog.askopenfilename(
            filetypes=[("BMP files","*.bmp")],title="Select a BMP file"
        )

        # if file path is not empty, set the file path variable and print the original image
        if file_path:
            self.filepath.set(file_path)
            self.check_header(file_path,None)


    def handle_selection(self,*args):
        print("* H_S * handling selection")

        # get selected core operation
        core_option=self.selected_option.get()

        # if core operation is exit, quit the application
        if core_option=="exit":
            self.quit()
            return
        
        # if core operation is open file, open file dialog
        if core_option=="open file":
            self.open_file_dialog()
            return
        
        # get file path
        file_path=self.filepath.get()

        # if file path is empty or doesnt exist for some reason, print error message
        if not file_path or file_path=="None":
            print("error in handle selection,no file selected")
            return


    # HELPER FUNCTIONS #
    
    """
    start=np.array([[0,2],[3,1]])
    for i in range(3):
        start=create_bayer_matrix(2,start)
    """


    def scaler(self,g,lower_bound,upper_bound):
        # helper function to scale a value between a lower and upper bound
        return max(lower_bound,min(upper_bound,g))



    def int_from_bytes(self,byte_sequence):
        # convert byte sequence to int
        # assumes byte order is little endian
        if not isinstance(byte_sequence,(bytes, bytearray)):
            raise ValueError("invalid byte_sequence")
        byte_iter=reversed(byte_sequence)
        res=0
        for byte in byte_iter:
            res=res*256+byte
        return res



    def normalize(self,value,value_min,value_max):
        # normalize range
        if value_max>value_min:
            new_value=int((value-value_min)/(value_max-value_min)*255)
        else:
            new_value=value
        new_value=max(0,min(255,new_value))
        return new_value



    # CORE OPERATIONS # 


    def clear(self):
        self.canvas.delete("all")
        self.operation_canvas.delete("all")

    # FLOW CONTROL #
    # i.e. a hub for all operations



    def flow_control(self,pixels,w,h,operation_flag=None):
        # hub for all operations
        # this is not great code

        print("* F_C * flow control")
        # basically, for each flag, we print the operation pixels.
        self.print_bmp(w,h,pixels)
        


    # BMP PARSING #


    def unpack_header(self,header):
        print("* U_H * unpacking header")
        # helper function to unpack header
        w=self.int_from_bytes(header[4:8])
        h=self.int_from_bytes(header[8:12])
        bpp=self.int_from_bytes(header[14:16])
        compression= self.int_from_bytes(header[16:20])

        return w,h,bpp,compression        



    def check_header(self,filepath,operation_flag=None):
        print("* C_H * checking header")
        print("operation flag: ",operation_flag)
        # parse header
        with open(filepath,"rb") as file:
            if file is None:
                raise ValueError("no file?")

            header = file.read(14)
            if header is None:
                raise ValueError("invalid header")

            if header[:2]!=b"BM":
                raise ValueError("incorrect file format")

            pixel_start = self.int_from_bytes(header[10:14])
            dib_header = file.read(40)

            if dib_header is None:
                raise ValueError("no dib header or invalid")
            
            w,h,bpp,compression= self.unpack_header(dib_header)

            if h>576 or w>704:
                raise ValueError("image too big")

            if compression!=0:
                raise ValueError("compressed image")

            if bpp!=24:
                raise ValueError("image must be 24 bit")

            file.seek(pixel_start)
            pixels = []
            row_padding = (4-(w*3)%4)%4

            for y in range(h):
                row = []
                for x in range(w):
                    b=file.read(1)[0]
                    g=file.read(1)[0]
                    r=file.read(1)[0]
                    row.append((r,g,b))

                pixels.append(row)
                file.read(row_padding)
    
        pixels.reverse() # images were upside down for some reason

        self.flow_control(pixels,w,h,operation_flag)
        self.huffman_compression(pixels,w,h)

    def count_frequencies(self,pixels):
        frequencies={}
        for row in pixels:
            for pixel in row:
                if pixel in frequencies:
                    frequencies[pixel]+=1
                else:
                    frequencies[pixel]=1
        return frequencies
    
    # BMP DISPLAY #

    def build_huffman_tree(self,frequencies):
        heap=MinHeap()
        for pixel,frequency in frequencies.items():
            heap.insert(Node(pixel,frequency))
        while len(heap.heap)>1:
            l=heap.extract_min()
            r=heap.extract_min()
            merged=Node(None,l.frequency+r.frequency)
            merged.left=l
            merged.right=r
            heap.insert(merged)
        return heap.extract_min()
    
    def build_huffman_codes(self,root,curr="",codes={}):
        if root is None:
            return
        if root.pixel is not None:
            codes[root.pixel]=curr
            return
        self.build_huffman_codes(root.left,curr+"0",codes)
        self.build_huffman_codes(root.right,curr+"1",codes)
        return codes

    def encode_pixels(self, pixels, codes):
        encoded_data = ""
        for row in pixels:
            for pixel in row:
                encoded_data += codes[pixel]
        return encoded_data

    def huffman_compression(self,pixels,w,h):
        print("* H_C * huffman compression")
        if pixels is None:
            raise ValueError("no pixels")
        frequencies=self.count_frequencies(pixels)
        huffman_tree=self.build_huffman_tree(frequencies)
        huffman_codes=self.build_huffman_codes(huffman_tree)
        encoded_pixels=self.encode_pixels(pixels,huffman_codes)
        print(w*h*24)
        print(len(encoded_pixels))
        print("compression ratio: ",(w*h*24)/len(encoded_pixels))

    def A_pixel(self,pixels,x,y):
        if x>0:
            return pixels[y][x-1]
        else:
            return 0

    def B_pixel(self,pixels,x,y):
        if y>0:
            return pixels[y-1][x]
        else:
            return 0
    
    def C_pixel(self,pixels,x,y):
        if x>0 and y>0:
            return pixels[y-1][x-1]
        else:
            return 0
    
    def predictors(self,A,B,C):
        return {"P1":A,"P2":B,"P3":C,"P4":A+B-C,"P5":A+(B-C)//2,"P6":B+(A-C)//2,"P7":(A+B)//2}
    
    def min_predictor(self,predictors):
        min_predictor=None
        min_error=float("inf")
        for key,value in predictors.items():
            error=abs(value)
            if error<min_error:
                min_error=error
                min_predictor=key
        return min_predictor,predictors[min_predictor]
    
    def compute_residuals(self,pixels,w,h):
        residuals=[]
        predictor_log=[]
        for x in range(w):
            row_res=[]
            row_pred=[]
            for y in range(h):
                A=self.A_pixel(pixels,x,y)
                B=self.B_pixel(pixels,x,y)
                C=self.C_pixel(pixels,x,y)
                predictors=self.predictors(A,B,C)
                min_pred,value=self.min_predictor(predictors)
                row_res.append(pixels[y][x]-value)
                


    def print_bmp(self,w,h,pixels):
        # printing the original image

        print("* P_B * printing bmp")

        # reinitialize canvas
        self.canvas.config(width=w,height=h)
        self.canvas.delete("all")

        # using tkinter photo image because is faster than drawing rectangles
        photo = tk.PhotoImage(width=w,height=h)
        
        for x in range(w):
            for y in range(h):
                rgb_instance=pixels[y][x]
                color="#%02x%02x%02x"%rgb_instance
                photo.put(color,(x,y)) # plot each pixel

        self.canvas.create_image(0,0,image=photo,anchor=tk.NW)
        self.canvas.image=photo

if __name__=="__main__":
    app=BMPViewer()
    app.mainloop()
