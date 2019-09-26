import hashlib
import random
import math

#isPoweroftwo is from geeks to geeks
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
        self.entry = entry

    def printNodePointers(self):
        node = self.entry.value
        if self.parent == None:
            p = "no pointer"
            rs = "none"
            ls = "none"
            gp = 'none'
        else:
            if self.parent.right == None:
                rs = 'none'
            else:
                rs = self.parent.right.entry.value
            if self.parent.left == None:
                ls = 'none'
            else:
                ls = self.parent.left.entry.value
            if self.parent.parent == None:
                gp = 'none'
            else:
                gp = self.parent.parent.entry.value
            p = self.parent.entry.value
        if self.right == None:
            r = "no pointer"
        else:
            r = self.right.entry.value
        if self.left == None:
            l = "no pointer"
        else:
            l = self.left.entry.value
        sibs = (". Right sib: " + rs + ". Left Sib: " + ls + ". grandparent: " + gp)
        essential = ("This is node: " + node + ". Parent: " + p + ". Right: " + r + ". Left: " + l)
        print(essential + sibs)

    def teachParentMyName(self, is_right):
        if self.parent:
            if is_right:
                self.parent.right = self
            else:
                self.parent.left = self

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
        self.RootHash = None #hex decimal hash
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

#            new_nd.makeEntry(new_nd_h, new_val)
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

    def getRightMostNode(self):
        #returns right most node
        right_nd = self.RootNode
        while right_nd.is_leaf != True:
            right_nd = right_nd.right
        return right_nd

    def removeRightMostNode(self, right_nd):
        '''
        Removes right most node from its spot and returns it
        '''
        if right_nd.parent == self.RootNode:
            #special case 2 leafs
            self.RootNode = right_nd.parent.left
            self.RootNode.parent = None

        else:
            grandparent = right_nd.parent.parent
            grandparent.right = right_nd.parent.left
            right_nd.parent.left.parent = grandparent
        parent_to_delete = right_nd.parent.entry.key
        del self.node_map[parent_to_delete]
        return right_nd

    def deleteLeafFromMaps(self, node):
        del self.entries_map[node.entry]
        del self.node_map[node.entry.key]
        self.entries.remove(node.entry)

    def Delete(self, entry):
        '''
        The Delete function takes a key (Entry) as argument, traverses the
        Merkle Tree and finds that key. If the key exists, delete the
        corresponding Entry and re-balance the tree if necessary. Delete
        function will return updated root hash if the key was found otherwise
        "path_not_found” if the key doesn't exist.
        '''
        if entry not in self.entries_map:
            return 'path_not_found'

        delete_nd = self.entries_map[entry]
        right_nd = self.getRightMostNode()

        '''
        Below is logic block for special cases.
        Special case 1: only one node in tree prior to delete.
        Special case: 2: leafs in tree prior to delete.
        '''
        if len(self.entries_map) == 1:
            self.RootHash = None
            self.RootNode = None
            self.deleteLeafFromMaps(delete_nd)
            return self.RootNode
        elif len(self.entries_map) == 2:
            parent_to_delete = right_nd.parent.entry.key
            if right_nd == delete_nd:
                self.RootNode = right_nd.parent.left
            else:
                self.RootNode = right_nd
            self.RootNode.left, self.RootNode.right, self.RootNode.parent = None, None, None
            self.RootHash = self.RootNode.entry.key
            self.deleteLeafFromMaps(delete_nd)
            del self.node_map[parent_to_delete]
            return self.RootNode

        right_nd = self.removeRightMostNode(right_nd)
        temp_node = None
        if right_nd == delete_nd:
            #deleting the farthest right node
            temp_node = delete_nd.parent.left
        else:
            temp_node, temp_node.parent = right_nd, delete_nd.parent
            if delete_nd == delete_nd.parent.right:
                temp_node.parent.right = temp_node
            else:
                temp_node.parent.left = temp_node
        self.deleteLeafFromMaps(delete_nd)
        while temp_node != self.RootNode:
            is_right = True
            if temp_node.parent.parent:
                #check what side for teaching parent later
                if temp_node.parent == temp_node.parent.parent.right:
                    is_right = True
                if temp_node.parent == temp_node.parent.parent.left:
                    is_right = False

            node_to_delete_key = temp_node.parent.entry.key
            if temp_node == temp_node.parent.right:
                sibling = temp_node.parent.left
                str = sibling.entry.key + temp_node.entry.key
                new_val = sibling.entry.value + temp_node.entry.value
                new_nd_h = hashlib.sha512(str.encode()).hexdigest()

                new_nd = Node(temp_node.parent.left, temp_node)
                new_nd.makeEntry(new_nd_h, new_val)
                self.checkIfGranparentRoot(temp_node, new_nd)
                new_nd.teachKids(temp_node.parent.left, temp_node)
                #new_nd.teachParentMyName(is_right)

            elif temp_node == temp_node.parent.left:
                sibling = temp_node.parent.right
                str = temp_node.entry.key + sibling.entry.key
                new_val = temp_node.entry.value + sibling.entry.value
                new_nd_h = hashlib.sha512(str.encode()).hexdigest()

                new_nd = Node(temp_node, temp_node.parent.right)
                new_nd.makeEntry(new_nd_h, new_val)
                self.checkIfGranparentRoot(temp_node, new_nd)
                #above sets to new_nd to root if applicable
                new_nd.teachKids(temp_node, temp_node.parent.right)

            new_nd.teachParentMyName(is_right)
            self.node_map[new_nd_h] = new_nd
            del self.node_map[node_to_delete_key] #delete old parent
            temp_node = new_nd
            #if new_nd is root then loop stops
        return self.RootHash

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
            if parent_hash not in self.node_map:
                #check if right or left
                return False
            if self.node_map[parent_hash] == self.node_map[parent_hash].parent.left:
                str = parent_hash + merkle_path[i]
            else:
                str = merkle_path[i] + parent_hash
            parent_hash = hashlib.sha512(str.encode()).hexdigest()
        return parent_hash == self.RootHash
