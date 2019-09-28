# merkletree
September 27, 2019

Summary:
There are 2 implementations, 1 in python and one in go. The go version is not
work for deletion and I have not updated the verification function yet. The python
version is fully working.This is the first try at implementing a merkle tree
that supports insertion, deletion, finding
the merkle path and and merkle path verification using only the RootHash,
merkle_path, entry, and location of entry relative to other leaves.
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

    c = makeEntryFromValue("c") #new function added for easier interface
    #creates entry with value and key in one step
    t.Insert(c)

    b_path = t.generateMerklePath(b) #pass an Entry instance to the method
    #returns [hexDecSHA512(a)] which is the merkle path of b

    t.VerifyMerklePath(b, 1, b_path) #takes entry, location and merkle_path
    #outputs boolean, in this case true. Performed in lg (n) without the use
    #of the tree, other then for accesing root hash field for final comparison

Testing:
Additional utilities are available in test.py. There is a function to print the
entire tree and one print the merkle path with readable values. Large test
inserts 7 values into a tree and prints the tree horizontally after each
insertion (root left), showing the node value as its name. It then generates
and prints a readable version of the MerklePaths for leaf nodes
a, b, c, e, and g. Updated: there our now test for just deletion, verification.
