from merkletree import *

COUNT = [10]
def print2DUtil(root, space) :

    # Base case
    if (root == None) :
        return

    # Increase distance between levels
    space += COUNT[0]

    # Process right child first
    print2DUtil(root.right, space)

    # Print current node after space
    # count
    print()
    for i in range(COUNT[0], space):
        print(end = " ")
    print(root.entry.value)

    # Process left child
    print2DUtil(root.left, space)

# Wrapper over print2DUtil()
def print2D(root) :

    # space=[0]
    # Pass initial space count as 0
    print2DUtil(root, 0)

def example():
    t = MerkleTree() #create a MerkleTree instance
    a = Entry("a") #create an entry instance, initializing value to "a"
    a.makeKey() #create a key based on output of SHA512(value)
    t.Insert(a) #insert the complete entry into the tree
    #insert will return a string of the inserted nodes key in hexadecimal

    b = Entry("b") #create an entry instance, initializing value to "a"
    b.makeKey() #create a key based on output of SHA512(value)
    t.Insert(b)

    t.generateMerklePath(b) #pass an Entry instance to the method
    #returns [hexDecSHA512(a)] which is the merkle path of b


def test():
    t = MerkleTree()
    a = Entry("a")
    a.makeKey()
    print(a.key)
    b = Entry("b")
    b.makeKey()
    c = Entry("c")
    c.makeKey()
    d = Entry("d")
    d.makeKey()
    e = Entry("e")
    e.makeKey()
    f = Entry("f")
    f.makeKey()
    g = Entry("g")
    g.makeKey()

    t.Insert(a)
    t.Insert(b)
    t.Insert(c)
    t.Insert(d)
    t.Insert(e)
    print("Test 5 ")
    print2D(t.RootNode)
    t.Insert(f)
    print("Test 6 ")
    print2D(t.RootNode)
    t.Insert(g)
    print("test 7")
    print2D(t.RootNode)
    print("node map length: ", len(t.node_map))

def printMerklePath(t, merklepath):
    print('below is merkle path')
    for key in merklepath:
        print(t.node_map[key].entry.value)

def largeTest():
    t = MerkleTree()
    a = Entry("a")
    a.makeKey()
    print(a.key)
    b = Entry("b")
    b.makeKey()
    c = Entry("c")
    c.makeKey()
    d = Entry("d")
    d.makeKey()
    e = Entry("e")
    e.makeKey()
    f = Entry("f")
    f.makeKey()
    g = Entry("g")
    g.makeKey()

    t.Insert(a)
    print("insert a test 1____________________________________")
    print2D(t.RootNode)

    t.Insert(b)
    print("insert b test 2_____________________________________________")
    print2D(t.RootNode)

    t.Insert(c)
    print("insert c test 3_____________________________________________")
    print2D(t.RootNode)

    t.Insert(d)
    print("insert d test 4_____________________________________________")
    print2D(t.RootNode)


    t.Insert(e)
    print("insert e test 5_____________________________________________")
    print2D(t.RootNode)

    t.Insert(f)
    print("insert f test 6_____________________________________________")
    print2D(t.RootNode)

    t.Insert(g)
    print("insert g test 7_____________________________________________")
    print2D(t.RootNode)

    path = t.generateMerklePath(a.key)
    print("a path")
    printMerklePath(t, path)

    path = t.generateMerklePath(b.key)
    print("b path")
    printMerklePath(t, path)

    path = t.generateMerklePath(c.key)
    print("c path")
    printMerklePath(t, path)

    path = t.generateMerklePath(e.key)
    print("e path")
    printMerklePath(t, path)

    path = t.generateMerklePath(g.key)
    print("g path")
    printMerklePath(t, path)

#test()
largeTest()
