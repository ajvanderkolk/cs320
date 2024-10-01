class Node():
    def __init__(self, key):
        self.key = key
        self.values = []
        self.left = None
        self.right = None
    
    # number of 'fruit' of each leaf in the tree (or loans in the tree)
    def __len__(self):
        size = len(self.values)
        if self.left != None:
            size += len(self.left)
        if self.right != None:
            size += len(self.right)
        return size
    
    def __getitem__(self, key):
        if key == self.key:
            return self.values
        elif key < self.key:
            if self.left != None:
                return self.left[key]
        elif key > self.key:
            if self.right != None:
                return self.right[key]
            else:
                return []
            
    def lookup(self, key):
        return self.__getitem__(key)
    
    def height(self):
        # TODO: handle direct Node.height() calls. specify to use 
        if self == None:
            return 0
        l_height = r_height = 0
        # get height of left 'branch'
        if self.left != None:
            l_height += 1
            l_height += self.left.height()
        
        # get height of right 'branch'
        if self.right != None:
            r_height += 1
            r_height += self.right.height()
        
        # compare
        if l_height > r_height:
            return l_height
        else:
            return r_height
    
    def num_leaves(self):
        count = 0
        if self.left == None and self.right == None:
            count += 1
        if self.left != None:
            count += self.left.num_leaves()
        if self.right != None:
            count += self.right.num_leaves()
        
        return count
        
    
    def num_nodes(self):
        if self == None:
            return 0
        else:
            num_nodes = 1
        if self.right != None:
            num_nodes += self.right.num_nodes()
        if self.left != None:
            num_nodes += self.left.num_nodes()
        return num_nodes
        
    def nlargest(self, n):
        assert self.num_nodes() >= n
        top_n = []
        
        def __nthlargest(node):
            nonlocal n
            nonlocal top_n
            
            if node == None:
                return
            
            if n > 0:
                __nthlargest(node.right)
                if n <= 0:
                    return
                top_n.append(node.key)
                n -= 1
                if n <= 0:
                    return
                if node.left == None:
                    return
                __nthlargest(node.left)
                if n <= 0:
                    return
                top_n.append(node.key)
                n -= 1
        
        if n != 0:
            __nthlargest(self)
        return top_n
    
    def nthlargest(self, k):
        #https://www.geeksforgeeks.org/kth-largest-element-bst-using-constant-extra-space/
        assert self.num_nodes() >= k
        curr = self
        klargest = None
        count = 0
        
        while (curr != None):
            if curr.right == None:
                count += 1
                if count == k:
                    klargest = curr
                curr = curr.left
            else:
                succ = curr.right
                
                while succ.left != None and succ.left != curr:
                    succ = succ.left
                if succ.left == None:
                    succ.left = curr
                    curr = curr.right
                else:
                    succ.left = None
                    count += 1
                    if count == k:
                        klargest = curr
                    curr = curr.left          
        return klargest.key

                    
class BST():
    def __init__(self):
        self.root = None

    def add(self, key, val):
        if self.root == None:
            self.root = Node(key)

        curr = self.root
        while True:
            if key < curr.key:
                # go left
                if curr.left == None:
                    curr.left = Node(key)
                curr = curr.left
            elif key > curr.key:
                 # go right
                if curr.right == None:
                    curr.right = Node(key)
                curr = curr.right
            else:
                # found it!
                assert curr.key == key
                break

        curr.values.append(val)

    def __dump(self, node):
        if node == None:
            return
        self.__dump(node.left)            # 3
        print(node.key, ":", node.values)  # 2
        self.__dump(node.right)             # 1

    def dump(self):
        self.__dump(self.root)
    
    def __getitem__(self, key):
        return self.root[key]
        
    def height(self):
        return self.root.height()
    
    def num_leaves(self):
        return self.root.num_leaves()
    
    # number of 'leaves' in the tree (or interest rates in the tree.)
    def __num_nodes(self, node):
        if node == None:
            return 0
        else:
            height = 1
        height += self.__num_nodes(node.left)
        height += self.__num_nodes(node.right)
        return height
    
    def num_nodes(self):
        return self.__num_nodes(self.root)
    
    def nlargest(self, n):
        if self.root == None:
            return []
        return self.root.nlargest(n)