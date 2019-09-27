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

def printNodeMap(t):
    for key in t.node_map.keys():
        print (t.node_map[key].entry.toString())

def printEntryMap(t):
    for key in t.entries_map.keys():
        print (t.entries_map[key].entry.toString())

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
#    print('below is merkle path')
    for key in merklepath:
        print(t.node_map[key].entry.value)


def deleteTest1():
    t = MerkleTree()
    a = Entry("a")
    a.makeKey()
    print(a.key)
    b = Entry("b")
    b.makeKey()
    c = Entry("c")
    c.makeKey()

    t.Insert(a)
    print("insert a test 1____________________________________")
    print2D(t.RootNode)

    t.Insert(b)
    print("insert b test 2_____________________________________________")
    print2D(t.RootNode)

    t.Insert(c)
    print("insert c test 3_____________________________________________")
    print2D(t.RootNode)

    t.Delete(a)
    print("delete a test 4_____________________________________________")
    print2D(t.RootNode)

def largeDeleteTest():
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
    t.Insert(f)
    t.Insert(g)
    print("insert g test 7_____________________________________________")
    print2D(t.RootNode)

    t.Delete(g)
    print("delete g test 8_____________________________________________")
    print2D(t.RootNode)

    t.Delete(a)
    print("delete a test 9_____________________________________________")
    print2D(t.RootNode)

    t.Delete(c)
    print("delete c test 10_____________________________________________")
    print2D(t.RootNode)

    t.Delete(b)
    print("delete b test 11_____________________________________________")
    print2D(t.RootNode)

    t.Delete(d)
    print("delete d test 12_____________________________________________")
    print2D(t.RootNode)

    print("___Below is entry map before deleting f___")
    printEntryMap(t)
    t.Delete(f)
    print("delete f test 13_____________________________________________")
    print2D(t.RootNode)

    t.Delete(e)
    print("delete e test 13_____________________________________________")
    print2D(t.RootNode)

def verifyTest():
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

    pathA = t.generateMerklePath(a.key)
    print("a's merkle path")
    printMerklePath(t, pathA)
    print("a verification", t.VerifyMerklePath(a, 0, pathA))

    pathB = t.generateMerklePath(b.key)
    print("b merkle path below")
    printMerklePath(t, pathB)
    print("b verification", t.VerifyMerklePath(b,1, pathB))

    pathC = t.generateMerklePath(c.key)
    print("c path")
    printMerklePath(t, pathC)
    print("c verification", t.VerifyMerklePath(c,2, pathC))

    pathD = t.generateMerklePath(d.key)
    print("d path")
    printMerklePath(t, pathD)
    print("d verification", t.VerifyMerklePath(d, 3, pathD))

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

    pathA = t.generateMerklePath(a.key)
    #print("a's merkle path")
    #printMerklePath(t, pathA)
    print("a verification", t.VerifyMerklePath(a, 0, pathA))

    pathB = t.generateMerklePath(b.key)
    #print("b merkle path below")
    #printMerklePath(t, pathB)
    print("b verification", t.VerifyMerklePath(b,1, pathB))

    pathC = t.generateMerklePath(c.key)
    # print("c path")
    # printMerklePath(t, path)
    print("c verification", t.VerifyMerklePath(c,2, pathC))

    pathE = t.generateMerklePath(e.key)
    #print("e path")
    #printMerklePath(t, pathE)
    print("e verification", t.VerifyMerklePath(e, 4, pathE))

    pathG = t.generateMerklePath(g.key)
    print("g path")
    printMerklePath(t, pathG)
    print("g verification", t.VerifyMerklePath(g, 6, pathG))

    fake_node = Entry("fake_node")
    fake_node.makeKey()
    print("fake node verification with a's merkle path", t.VerifyMerklePath(fake_node, pathA))

    #printNodeMap(t)

#test()
#largeTest()
#deleteTest1()
#verifyTest()
largeDeleteTest()
