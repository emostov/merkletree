import hashlib
import random
import math


#from poweroftwo is from geeks to geeks
# Function to check
# Log base 2
def Log2(x):
    if x == 0:
        return false;

    return (math.log10(x) /
            math.log10(2));

# Function to check
# if x is power of 2
def isPowerOfTwo(n):
    return (math.ceil(Log2(n)) ==
            math.floor(Log2(n)));

class Node:
    def __init__(self, left, right, is_leaf=False):
        self.left = left
        self.right = right
        self.parent = None
        self.is_leaf = is_leaf
        self.entry = None

    def teachKids(self, left, right):
        self.left.parent = self
        self.right.parent = self

    def makeEntry(self, key, value):
        entry = Entry(value, key)
        #entry.key = new_root_hash
        self.entry = entry

class Entry:
    def __init__(self, value, key=None):
        self.value = value
        self.key = key

    def makeKey(self):
        #makes key from value, should only be used when making a leaf
        hash = hashlib.sha512(self.value.encode()).hexdigest()
        self.key = hash

    def toString(self):
        return "{key: "+self.key+", value: "+self.value+"}"


class MerkleTree:

    def __init__(self):
        self.RootNode = None #node class
        self.RootHash = None
        self.entries = [] #list of entries
        self.entries_map = {} #map entry to node
        self.node_map = {} #map hash to node

    def makeLeafNode(self, entry):
        #makes a leaf node and updates the entries
        #entry.makeKey()
        self.entries.append(entry)
        #hash = entry.key#hashlib.sha512(entry.value.encode()).hexdigest()
        new_node = Node( None, None, True)
        new_node.entry = entry
        self.entries_map[entry] = new_node
        self.node_map[entry.key] = new_node
        return new_node

    def updateRoot(self, node):
        self.RootNode = node
        self.RootHash = node.entry.key
        return self.RootHash

    def checkIfGranparentRoot(self, node, new_nd):
        #check if grandparent is root, if not asigns proper parent to relevant node
        if node.parent.parent != None: #parent is not root
            new_nd.parent = node.parent.parent
        else:
            self.updateRoot(new_nd)

    def Insert(self, entry):

        new_leaf_node = self.makeLeafNode(entry)
        #check if node is about to have only 1 leaf
        if len(self.entries) == 1: # first insert
            return self.updateRoot(new_leaf_node)

        #tree is perfect before insert or is about to have 2 leaves
        elif isPowerOfTwo(len(self.entries)-1) or len(self.entries) == 2:
            future_sib = self.RootNode
            str = future_sib.entry.key + new_leaf_node.entry.key
#            str = future_sib.entry.toString() + new_leaf_node.entry.toString()
            new_root_hash = hashlib.sha512(str.encode()).hexdigest()
            new_val = future_sib.entry.value + new_leaf_node.entry.value
            new_root = Node(future_sib, new_leaf_node)
            new_root.makeEntry(new_root_hash, new_val)

            new_root.teachKids(future_sib, new_leaf_node)
            self.node_map[new_root_hash] = new_root

            return self.updateRoot(new_root)

        second_to_last_entry = self.entries[-2]
        temp_root = self.entries_map[second_to_last_entry]

        #initial insert and there is no lonely leaf but not balance
        if temp_root.parent.left.is_leaf and temp_root.is_leaf:
            str = temp_root.parent.entry.key + new_leaf_node.entry.key
#            str = temp_root.parent.entry.toString() + new_leaf_node.entry.toString()
            new_nd_h = hashlib.sha512(str.encode()).hexdigest()

            new_val = temp_root.parent.entry.value + new_leaf_node.entry.value
            new_nd = Node(temp_root.parent, new_leaf_node)
            new_nd.makeEntry(new_nd_h, new_val)

            new_nd.makeEntry(new_nd_h, new_val)
            self.checkIfGranparentRoot(temp_root, new_nd)
            new_nd.teachKids(temp_root.parent, new_leaf_node)
            self.node_map[new_nd_h] = new_nd

            temp_root = new_nd

        #initial insert of leaf and there is already a lonely leaf
        elif temp_root.parent.left.is_leaf == False and temp_root.is_leaf:
            str = temp_root.entry.key + new_leaf_node.entry.key
#            str = temp_root.entry.toString() + new_leaf_node.entry.toString()
            new_nd_h = hashlib.sha512(str.encode()).hexdigest()

            new_val = temp_root.entry.value + new_leaf_node.entry.value
            new_nd = Node(temp_root, new_leaf_node)
            new_nd.makeEntry(new_nd_h, new_val)

            new_nd.parent = temp_root.parent
            new_nd.teachKids(temp_root, new_leaf_node)
            self.node_map[new_nd_h] = new_nd

            temp_root = new_nd

        #inserts after the initial insert
        while temp_root != self.RootNode:
            node_to_delete_key = temp_root.parent.entry.key
            str = temp_root.parent.left.entry.key + temp_root.entry.key
#            str = temp_root.parent.left.entry.toString() + new_leaf_node.entry.toString()
            new_nd_h = hashlib.sha512(str.encode()).hexdigest()

            new_val = temp_root.parent.left.entry.value + temp_root.entry.value
            new_nd = Node(temp_root.parent.left, temp_root)
            new_nd.makeEntry(new_nd_h, new_val)

            self.checkIfGranparentRoot(temp_root, new_nd)
            new_nd.teachKids(temp_root.parent.left, temp_root)
            self.node_map[new_nd_h] = new_nd
            del self.node_map[node_to_delete_key] #delete old parent

            temp_root = new_nd
        self.updateRoot(temp_root)
        return temp_root.entry.key

    def generateMerklePath(self, key):
        merkle_path = []
        if key in self.node_map:
            node = self.node_map[key]
        else:
            return "path_not_found"

        while node is not self.RootNode:
            if node.parent.right == node: #is right nodes
                merkle_path.append(node.parent.left.entry.key)
            else:
                merkle_path.append(node.parent.right.entry.key)
            node = node.parent
        return merkle_path

    def Delete(self, entry: Entry):
        """
        The Delete function takes a key (Entry) as argument, traverses the
        Merkle Tree and finds that key. If the key exists, delete the
        corresponding Entry and re-balance the tree if necessary. Delete
        function will return updated root hash if the key was found otherwise
        return empty string (or ‘’path_not_found”) if the key doesn't exist.
        """
        if entry not in self.entries_map.keys():
            return 'path_not_found'
        #TODO check if tree is balanced and then go balance it

    def VerifyMerklePath(self, entry, merkle_path):
        '''
        The VerifyMerklePath function takes a key (Entry) and its Merkle path,
        the ordered list of sibling hashes as argument. It computes all the
        hashes on the path from the given Entry to the root using the location
        and the MerklePath. The newly computed root hash is compared to the
        stored root for verification. Function returns true if the
        verification succeeds (if the newly computed root hash is equal to
        the stored root hash) otherwise return false.
        Arguments: Entry object, location (or index) of this Entry object in
        the Merkle Tree, and the list/array of hashes on Merkle Path
        Return: bool
        '''
        if entry not in self.entries_map.keys():
            return False
        node = self.entries_map[entry]
        parent_hash = node.entry.key
        for i in range(len(merkle_path)):
            #check if right or left
            if parent_hash not in self.node_map:
                return False
            if self.node_map[parent_hash] == self.node_map[parent_hash].parent.left:
                str = parent_hash + merkle_path[i]
            else:
                str = merkle_path[i] + parent_hash
            parent_hash = hashlib.sha512(str.encode()).hexdigest()

        return parent_hash == self.RootHash
