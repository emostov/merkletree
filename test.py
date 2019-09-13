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

def tpname(t):
    print("start")
    print("root is: ", t.RootNode)
    for hash, node in t.node_map.items():
        print("node", node, "left", node.left, "right", node.right)
        print("name: ", node.name)
        if node.entry != None:
            print("entry val: ", node.entry.value)

def tpname(t):
    print("start")
    print("root is: ", t.RootNode.name)
    for hash, node in t.node_map.items():
        print("node", node.name, node, "left:", node.left, "right:", node.right)
        if node.entry != None:
            print("entry val: ", node.entry.value)


def test4():
    t = MerkleTree()

    a = Entry("a")
    b = Entry("b")

    c = Entry("c")
    d = Entry("d")
    t.Insert(a)

    #tp(t)
    t.Insert(b)
    #print("Test 2")
    #print2D(t.RootNode)
    #tp(t)
    t.Insert(c)
    #tpname(t)
    print("Test 3_________")
    print2D(t.RootNode)
    t.Insert(d)
    print("Test 4_________")
    print2D(t.RootNode)

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

def pnm():
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
    print("test 2_________")
    print2D(t.RootNode)

    t.Insert(c)
    print("test 3_________")
    print2D(t.RootNode)

    t.Insert(d)
    print("test 4_________")
    print2D(t.RootNode)


    t.Insert(e)
    print("test 5_________")
    print2D(t.RootNode)

    t.Insert(f)


    print("test 6_________")
    print2D(t.RootNode)

    t.Insert(g)

    print("test 7_________")
    print2D(t.RootNode)

    path = t.generateMerklePath(a.key)
    printMerklePath(t, path)

    #print("Merkle Path a", t.generateMerklePath(a.key))
    #print("a merkle_path length", len(t.generateMerklePath(a.key)))


    #print(t.node_map)




#test()
pnm()
