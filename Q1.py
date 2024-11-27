from math import sqrt, cos
import random
import tkinter as tk
from tkinter import messagebox
pi = 3.141592653589793
## CMPT 365 Project 3 Question 1 ## 

# constructor

# initialize

# take user input, N = x, create dialog box for inputting a NxN matrix (2 <= N <= 8)
# validate input as ints, or generate random matrix between 0,255
class question1(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Question 1")
        self.geometry("500x500")
        self.size=tk.IntVar()
        self.size.set(2)
        self.matrix=None
        self.create_menus()
        self.generate_button=tk.Button(self,text="Input Matrix",command=self.open_matrix_input)
        self.generate_button.pack(pady=20)

    def create_menus(self):
        main_menu = tk.Menu(self)
        self.config(menu=main_menu)
        size_menu=tk.Menu(main_menu,tearoff=False)
        sizes=range(2,9)
        for size in sizes:
            size_menu.add_radiobutton(label=str(size),variable=self.size,value=size)
        main_menu.add_cascade(label="Size",menu=size_menu)

    def open_matrix_input(self):
        size = self.size.get()
        self.input_window = tk.Toplevel(self)
        self.input_window.title(f"Input {size}x{size} Matrix")
        self.input_window.geometry("600x600")
        self.entries = []
        for i in range(size):
            row_entries = []
            for j in range(size):
                entry = tk.Entry(self.input_window, width=5)
                entry.grid(row=i, column=j, padx=5, pady=5)
                row_entries.append(entry)
            self.entries.append(row_entries)

        random_button = tk.Button(self.input_window, text="Generate Random Matrix", command=self.generate_random_matrix)
        random_button.grid(row=size + 1, column=0, columnspan=size, pady=10)

        save_button = tk.Button(self.input_window, text="Save Matrix", command=self.save_and_apply_transformations)
        save_button.grid(row=size + 2, column=0, columnspan=size, pady=10)

    def generate_random_matrix(self):
        size = self.size.get()
        for i in range(size):
            for j in range(size):
                random_value = random.randint(0, 255)
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, str(random_value))

    def save_and_apply_transformations(self):
        size = self.size.get()
        matrix = []
        try:
            for i in range(size):
                row = []
                for j in range(size):
                    value = int(self.entries[i][j].get())  # Validate as integer
                    row.append(value)
                matrix.append(row)
            self.matrix = matrix
            transformed_one = self.one(matrix)
            transformed_two = self.two(matrix)
            are_equivalent = self.equivalent(transformed_one, transformed_two)
            self.display_matrix(transformed_one,False,are_equivalent,title="Row, then col", row_offset=size+20)
            self.display_matrix(transformed_two,True,are_equivalent,title="Col, then row", row_offset=size+32)


        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers in all fields.")

    def display_matrix(self, matrix,flag,are_equivalent,title, row_offset):
        tk.Label(self.input_window, text=title, font=("Arial", 12, "bold")).grid(row=row_offset, column=0, columnspan=len(matrix), pady=5)
        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                tk.Label(self.input_window, text=str(value), width=5, borderwidth=1, relief="solid").grid(row=row_offset + 1 + i, column=j, padx=2, pady=2)
        if flag and are_equivalent:
            tk.Label(self.input_window,text="Equivalent",font=("Arial",12,"bold")).grid(row=row_offset+1+len(matrix),column=0)
        elif flag and not are_equivalent:
            tk.Label(self.input_window,text="Not Equivalent",font=("Arial",12,"bold")).grid(row=row_offset+1+len(matrix),column=0)

    """
    def generate_random_matrix(self,N):
        res=[[0 for _ in range(N)] for _ in range(N)]
        for i in range(N):
            for j in range(N):
                res[i][j]=random.randint(0,255)
        return res
    """


    def pow(self,x,n):
        p=1
        for i in range(n):
            p=p*x
        return p
    
    def abs(self,x):
        if (x<0):
            return -x
        return x

    def factorial(self,x):
        if (x==0):
            return 1
        return x*self.factorial(x-1)

    def cosine(self,x):
        # flag = even (true)
        limit = 0.00000001
        term=1
        cos_value=term
        i=2
        sign=-1
        while self.abs(term)>limit:
            term=(self.pow(x,i))/(self.factorial(i))
            cos_value+=sign*term
            sign*=-1
            i+=2
        return cos_value

    # helper math functions

    # probably matrix operations
    
    # (1) rows then columns
    # i,j=0,...,N-1.
    # c_{i,j} = a*cos((2j+1)*i*pi)
    # if i == 0 : a = sqrt(1/n)
    # if i > 0 : a = sqrt(2/n)
    # construct T
    # c[i][j] = a*cos(sqrt(1/N)*cos(((2j+1)*i*pi)/2N)

    def dot_product(self,A,B):
        N=len(A[0])
        res=[[0 for _ in range(N)] for _ in range(N)]
        for i in range(N):
            for j in range(N):
                for k in range(N):
                    res[i][j]+=A[i][k]*B[k][j]
        return res

    def construct_transform_matrix(self,M):
        N = len(M[0])
        T = []
        for i in range(N):
            T.append([None for _ in range(N)])
        for i in range(N):
            for j in range(N):
                if (i==0):
                    a=1/sqrt(N)
                else:
                    a=sqrt(2/N)
                T[i][j]=a*self.cosine(((2*j+1)*i*pi)/(2*N))
        return T

    def transpose(self,M):
        N=len(M[0])
        transposed=[[0 for _ in range(N)] for _ in range(N)]
        for i in range(N):
            for j in range(N):
                transposed[j][i]=M[i][j]
        return transposed

    def equivalent(self,A,B):
        N=len(A[0])
        # assumption, sizes are the same and square
        for i in range(N):
            for j in range(N):
                if A[i][j]!=B[i][j]:
                    return False
        return True

    def convert_to_int(self,A):
        N=len(A[0])
        for i in range(N):
            for j in range(N):
                A[i][j]=int(A[i][j])
        return A
    def one(self,M):
        # row then column
        T=self.construct_transform_matrix(M)
        Y=self.dot_product(T,M)
        T=self.transpose(T)
        Y=self.dot_product(Y,T)
        Y=self.convert_to_int(Y)
        return Y

    def two(self,M):
        # column then row
        T=self.construct_transform_matrix(M)
        Y=self.dot_product(M,self.transpose(T))
        Y=self.dot_product(T,Y)
        Y=self.convert_to_int(Y)
        return Y
        
    # (2) columns then rows
            
    # output on the canvas
    # output difference, which is bigger, or equivalency

    def print_matrix(self,matrix):
        for row in matrix:
            print(" ".join(map(str, row)))

    """
    M = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    A=one(M)
    M = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    B=two(M)
    print("one:")
    print_matrix(A)
    print("two:")
    print_matrix(B)
    if equivalent(A,B):
        print("equivalent")
    else:
        print("not equivalent")
    """

if __name__ == "__main__":
    app = question1()
    app.mainloop()