import hashlib
import random

import math

#froom poweroftwo is from geeks to geeks
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
    def __init__(self, hash, left, right, is_leaf=False):
        self.left = left
        self.right = right
        self.parent = None
        self.hash = hash
        self.is_leaf = is_leaf
        self.entry = None
        self.name = random.randint(1,101)

    def teachKids(self, left, right):
        self.left.parent = self
        self.right.parent = self

class Entry:
    def __init__(self, value):
        self.value = value

class MerkleTree:

    def __init__(self):
        self.RootNode = None #node class
        self.entries = [] #list of entries
        self.entries_map = {} #map entry to node
        self.node_map = {} #map hash to node


    def makeLeafNode(self, entry):
        #makes a leaf node and updates the entries
        #entry = Entry(val)
        self.entries.append(entry)
        hash = hashlib.sha512(entry.value.encode()).hexdigest()
        new_node = Node(hash, None, None, True)
        new_node.entry = entry
        self.entries_map[entry] = new_node
        self.node_map[hash] = new_node
        return new_node

    # def checkIfFirst(self, leaf_node):
    #     if len(self.entries) == 1:
    #         updateRoot(leaf_node)
    #         #self.RootNode = leaf_node
    #         #leaf_node.parent = leaf_node
    #         return True
    #     return False

    def updateRoot(self, node):
        self.RootNode = node
        self.RootHash = node.hash
        return self.RootHash

    def checkIfGranparentRoot(self, node, new_nd):
        #check if grandparent is root, if not asigns proper parent to relevant node
        if node.parent.parent != None: #parent is not root
            new_nd.parent = node.parent.parent
        else:
            self.updateRoot(new_nd)

    def Insert(self, entry):
        new_leaf_node = self.makeLeafNode(entry)

        if len(self.entries) < 3:
        #check if there is 0 or 1 nodes in the tree
            if len(self.entries) == 1: #if first insert
                return self.updateRoot(new_leaf_node)
            else: #second insertion
                future_sib = self.RootNode
                str = future_sib.hash + new_leaf_node.hash
                parent_hash = hashlib.sha512(str.encode()).hexdigest()
                parent = Node(parent_hash, future_sib, new_leaf_node)
                parent.teachKids(future_sib, new_leaf_node)
                self.node_map[parent_hash] = parent
                return self.updateRoot(parent)

        elif isPowerOfTwo(len(self.entries)-1): #tree perfectly balance
            future_sib = self.RootNode
            str = future_sib.hash + new_leaf_node.hash
            new_root_hash = hashlib.sha512(str.encode()).hexdigest()
            new_root = Node(new_root_hash, future_sib, new_leaf_node)
            new_root.teachKids(future_sib, new_leaf_node)
            self.node_map[new_root_hash] = new_root
            return self.updateRoot(new_root)

        second_to_last_entry = self.entries[-2]
        farthest_right_leaf = self.entries_map[second_to_last_entry]

        def recurse(temp_root):
            print("in recurse")
            #recurse deals with initial insertion and then percolates up
            #if the tree is at least 2 nodes big do the initial insertion
            #Within each call to recursive function to percolate up inserts

            if temp_root == self.RootNode: #given is already at root
                self.updateRoot(temp_root)
                return temp_root.hash

            #initial insert and there is no lonely leaf but not balance
            elif temp_root.parent.left.is_leaf and temp_root.is_leaf:
                str = temp_root.parent.hash + new_leaf_node.hash
                new_nd_h = hashlib.sha512(str.encode()).hexdigest()
                new_nd = Node(new_nd_h, temp_root.parent, new_leaf_node)
                self.checkIfGranparentRoot(temp_root, new_nd)
                new_nd.teachKids(temp_root.parent, new_leaf_node)
                print("new node hash:", new_nd_h)
                self.node_map[new_nd_h] = new_nd
                recurse(new_nd)

            #initial insert of leaf and there is already a lonely leaf
            elif temp_root.parent.left.is_leaf == False and temp_root.is_leaf:
                #new_nd_h = hash(temp_root.hash + new_leaf_node.hash)
                str = temp_root.hash + new_leaf_node.hash
                new_nd_h = hashlib.sha512(str.encode()).hexdigest()

                new_nd = Node(new_nd_h, temp_root, new_leaf_node)
                new_nd.parent = temp_root.parent
                new_nd.teachKids(temp_root, new_leaf_node)
                recurse(new_nd)
            #percolating up after an insert
            elif temp_root.parent.left.is_leaf == False and temp_root.is_leaf == False:
                #new_nd_h = hash(temp_root.parent.left.hash + temp_root.hash)
                str = temp_root.parent.left.hash + new_leaf_node.hash
                new_nd_h = hashlib.sha512(str.encode()).hexdigest()

                node_to_delete_key = temp_root.parent.hash
                new_nd = Node(new_nd_h, temp_root.parent.left, temp_root)
                self.checkIfGranparentRoot(temp_root, new_nd)
                new_nd.teachKids(temp_root.parent.left, temp_root)
                del self.node_map[node_to_delete_key]
                recurse(new_nd)

        recurse(farthest_right_leaf)
