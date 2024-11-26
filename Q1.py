from math import sqrt, cos
import random
pi = 3.141592653589793
## CMPT 365 Project 3 Question 1 ## 

# constructor

# initialize

# take user input, N = x, create dialog box for inputting a NxN matrix (2 <= N <= 8)
# validate input as ints, or generate random matrix between 0,255

def generate_random_matrix(N):
    res=[[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            res[i][j]=random.randint(0,255)
    return res

def pow(x,n):
    p=1
    for i in range(n):
        p=p*x
    return p

def factorial(x):
    if (x==0):
        return 1
    return x*factorial(x-1)

def cosine(x):
    # flag = even (true)
    limit = 0.00000001
    i=2
    flag = True
    
    sum=1
    while flag:
        new_term=(pow(x,i))/(factorial(i))

        if new_term<limit:
            flag=False
        
    

    

print(pow(2,4))
print(factorial(3))

# helper math functions

# probably matrix operations
 
# (1) rows then columns
# i,j=0,...,N-1.
# c_{i,j} = a*cos((2j+1)*i*pi)
# if i == 0 : a = sqrt(1/n)
# if i > 0 : a = sqrt(2/n)
# construct T
# c[i][j] = a*cos(sqrt(1/N)*cos(((2j+1)*i*pi)/2N)

def dot_product(A,B):
    N=len(A[0])
    res=[[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            for k in range(N):
                res[i][j]+=A[i][k]*B[k][j]
    return res

def construct_transform_matrix(M):
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
            T[i][j]=a*cos(((2*j+1)*i*pi)/(2*N))
    return T

def transpose(M):
    N=len(M[0])
    transposed=[[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            transposed[j][i]=M[i][j]
    return transposed

def equivalent(A,B):
    N=len(A[0])
    # assumption, sizes are the same and square
    for i in range(N):
        for j in range(N):
            if A[i][j]!=B[i][j]:
                return False
    return True

def convert_to_int(A):
    N=len(A[0])
    for i in range(N):
        for j in range(N):
            A[i][j]=int(A[i][j])
    return A
def one(M):
    # row then column
    T=construct_transform_matrix(M)
    Y=dot_product(T,M)
    T=transpose(T)
    Y=dot_product(Y,T)
    Y=convert_to_int(Y)
    return Y

def two(M):
    # column then row
    T=construct_transform_matrix(M)
    Y=dot_product(M,transpose(T))
    Y=dot_product(T,Y)
    Y=convert_to_int(Y)
    return Y
    
# (2) columns then rows
        
# output on the canvas
# output difference, which is bigger, or equivalency

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(map(str, row)))


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