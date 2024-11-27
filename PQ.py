class MinHeap:
    def __init__(self):
        self.heap=[]
    def insert(self,node):
        self.heap.append(node)
        self.percolate_up(len(self.heap)-1)
    def extract_min(self):
        if len(self.heap)==0:
            return None
        if len(self.heap)==1:
            return self.heap.pop()
        root=self.heap[0]
        self.heap[0]=self.heap.pop()
        self.percolate_down(0)
        return root
    def percolate_up(self,i):
        parent=(i-1)//2
        if i>0 and self.heap[i].frequency<self.heap[parent].frequency:
            self.heap[i],self.heap[parent]=self.heap[parent],self.heap[i]
            self.percolate_up(parent)
    def percolate_down(self,i):
        smallest=i
        l=2*i+1
        r=2*i+2
        if l<len(self.heap) and self.heap[l].frequency<self.heap[smallest].frequency:
            smallest=l
        if r<len(self.heap) and self.heap[r].frequency<self.heap[smallest].frequency:
            smallest=r
        if smallest!=i:
            self.heap[i],self.heap[smallest]=self.heap[smallest],self.heap[i]
            self.percolate_down(smallest)


class Node:
    def __init__(self,pixel,frequency):
        self.pixel=pixel
        self.frequency=frequency
        self.left=None
        self.right=None
    def __lt__(self,other):
        return self.frequency<other.frequency