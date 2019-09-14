# merkletree
September 13, 2019
6:0pm
Summary:
First try at implementing a merkle tree that supports insertion and finding the
trees merkle path. The implementation also supports printing tree, display the
combination of leaf nodes that make up that node. merkletree.py includes 3
classes: Node, Entry, and MerkleTree. The merkletree supports look ups by keys
(hash value of node) through the attribute node_map. Additionally, it can
map an Entry object that was initially inserted to the corresponding leaf nodes
with the entries_map, using the Entry object as a key. Nodes maintain pointers
to there parent, left child, and right child. The Entry object stores a key
and value, both in string form.

Note: the entry field of a Node stores the entry and is equivalent to LeafValue

Example:
An example of how to use Insertion() and generateMerklePath():
    import merkletree
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

Testing:
Additional utilities are available in test.py. There is a function to print the
entire tree and one print the merkle path with readable values. Large test
inserts 7 values into a tree and prints the tree horizontally after each
insertion (root left), showing the node value as its name. It then generates
and prints a readable version of the MerklePaths for leaf nodes
a, b, c, e, and g.
