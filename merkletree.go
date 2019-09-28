package main

import (
	"crypto/sha512"
	"encoding/hex"
	"fmt"
	"math"
)

// General utils
func getHash(str string) string {
	h := sha512.New()
	h.Write([]byte(str))
	out_hash := hex.EncodeToString(h.Sum(nil))
	return out_hash
}

func isPowerOfTwo(n int) bool {
	x := float64(n)
	if n == 0 {
		return false
	}
	return math.Ceil(math.Log2(x)) == math.Floor(math.Log2(x))
}

func removeEntry(l []*Entry, item *Entry) []*Entry {
	for i, other := range l {
		if other == item {
			return append(l[:i], l[i+1:]...)
		}
	}
	return nil
}

// Structs followed by there methods

type Node struct {
	left    *Node
	right   *Node
	is_leaf bool
	parent  *Node
	entry   *Entry
}

func NewNode(left *Node, right *Node, is_leaf bool) Node {
	new_nd := Node{left: left, right: right, is_leaf: is_leaf}
	return new_nd
}

func makeNilNode() *Node {
	nil_node := &Node{left: nil, right: nil, parent: nil}
	nil_node.makeEntry("", "")
	return nil_node
}

func (n *Node) makeEntry(key string, value string) {
	entry := &Entry{key: key, value: value}
	n.entry = entry
}

func (self *Node) printNodePointers() {
	node := self.entry.value
	var p, rs, ls, gp, r, l string
	if self.parent == nil {
		p = "no pointer"
		rs = "none"
		ls = "none"
		gp = "none"
	} else {
		if self.parent.right == nil {
			rs = "none"
		} else {
			rs = self.parent.right.entry.value
		}
		if self.parent.left == nil {
			ls = "none"
		} else {
			ls = self.parent.left.entry.value
		}
		if self.parent.parent == nil {
			gp = "none"
		} else {
			gp = self.parent.parent.entry.value
		}
		p = self.parent.entry.value
	}
	if self.right == nil {
		r = "no pointer"
	} else {
		r = self.right.entry.value
	}
	if self.left == nil {
		l = "no pointer"
	} else {
		l = self.left.entry.value
	}
	sibs := (". Right sib: " + rs + ". Left Sib: " + ls + ". grandparent: " + gp)
	essential := ("This is node: " + node + ". Parent: " + p + ". Right: " + r + ". Left: " + l)
	// name := ("I am node: " + self.entry.value + ". ")
	fmt.Println(essential + sibs)
}

func (nd *Node) teachKids() {
	// check if actually need those inputs
	nd.left.parent = nd
	nd.right.parent = nd
}

func (nd *Node) teachParentMyName(is_right bool) {
	if nd.parent != nil {
		if is_right == true {
			nd.parent.right = nd
		} else {
			nd.parent.left = nd
		}
	}
}

type Entry struct {
	key   string
	value string
}

func PublicNewEntry(value string) *Entry {
	h := sha512.New()
	h.Write([]byte(value))
	key := hex.EncodeToString(h.Sum(nil))
	e := Entry{key: key, value: value}
	return &e
}

type MerkleTree struct {
	RootNode  *Node
	RootHash  string
	entries   []*Entry
	entry_map map[*Entry]*Node
	node_map  map[string]*Node
}

func NewMerkleTree() *MerkleTree {
	t := new(MerkleTree)
	t.entry_map = make(map[*Entry]*Node)
	t.node_map = make(map[string]*Node)
	t.RootNode = nil
	t.RootHash = ""
	return t
}

func (t *MerkleTree) makeLeafNode(entry *Entry) *Node {
	t.entries = append(t.entries, entry)
	new_nd := Node{left: nil, right: nil, is_leaf: true}
	new_nd.entry = entry
	t.entry_map[entry] = &new_nd
	t.node_map[entry.key] = &new_nd
	return &new_nd
}

func (t *MerkleTree) updateRoot(nd *Node) string {
	t.RootNode = nd
	t.RootHash = nd.entry.key
	return t.RootHash
}

func (t *MerkleTree) checkIfGrandParentRoot(nd *Node, new_nd *Node) {
	if nd.parent.parent != nil {
		new_nd.parent = nd.parent.parent
	} else {
		t.updateRoot(new_nd)
	}
}

func (t *MerkleTree) Insert(entry *Entry) string {
	new_leaf_nd := t.makeLeafNode(entry)
	if len(t.entry_map) == 1 {
		return t.updateRoot(new_leaf_nd)
	} else if isPowerOfTwo(len(t.entry_map)-1) || len(t.entry_map) == 2 {
		future_sib := t.RootNode
		str := future_sib.entry.key + new_leaf_nd.entry.key
		new_root_hash := getHash(str)
		new_val := future_sib.entry.value + new_leaf_nd.entry.value
		new_root := NewNode(future_sib, new_leaf_nd, false)
		new_root.makeEntry(new_root_hash, new_val)
		// new_root.teachKids(future_sib, new_leaf_nd)
		new_root.teachKids()
		//new_leaf_nd.parent = new_root
		t.node_map[new_root_hash] = &new_root
		fmt.Print("line 186")
		new_root.printNodePointers()
		fmt.Print("line 188")
		new_leaf_nd.printNodePointers()

		return t.updateRoot(&new_root)
	}
	second_to_last_entry := t.entries[len(t.entries)-2]
	temp_root := t.entry_map[second_to_last_entry]
	fmt.Print("line 191")
	temp_root.printNodePointers()

	// initial insert and there is no lonely leaf but not balance
	if temp_root.parent.left.is_leaf == true && temp_root.is_leaf == true {
		str := temp_root.parent.entry.key + new_leaf_nd.entry.key
		new_nd_h := getHash(str)
		new_val := temp_root.parent.entry.value + new_leaf_nd.entry.value
		new_nd := NewNode(temp_root.parent, new_leaf_nd, false)
		new_nd.makeEntry(new_nd_h, new_val)
		t.checkIfGrandParentRoot(temp_root, &new_nd)
		//new_nd.teachKids(temp_root.parent, new_leaf_nd)
		new_nd.teachKids()
		t.node_map[new_nd_h] = &new_nd
		fmt.Print("line 204")
		t.RootNode.printNodePointers()
		temp_root = &new_nd
	} else if temp_root.parent.left.is_leaf == false && temp_root.is_leaf == true {
		str := temp_root.entry.key + new_leaf_nd.entry.key
		new_nd_h := getHash(str)
		new_val := temp_root.entry.value + new_leaf_nd.entry.value
		new_nd := NewNode(temp_root, new_leaf_nd, false)
		new_nd.makeEntry(new_nd_h, new_val)
		new_nd.parent = temp_root.parent
		//new_nd.teachKids(temp_root, new_leaf_nd)
		new_nd.teachKids()
		t.node_map[new_nd_h] = &new_nd
		fmt.Print("line 216")
		t.RootNode.printNodePointers()
		temp_root = &new_nd
	}

	//inserts after the initial insert
	for temp_root != t.RootNode {
		node_to_delete_key := temp_root.parent.entry.key
		str := temp_root.parent.left.entry.key + temp_root.entry.key
		new_nd_h := getHash(str)
		new_val := temp_root.parent.left.entry.value + temp_root.entry.value
		new_nd := NewNode(temp_root.parent.left, temp_root, false)
		new_nd.makeEntry(new_nd_h, new_val)
		t.checkIfGrandParentRoot(temp_root, &new_nd)
		new_nd.teachKids()
		t.node_map[new_nd_h] = &new_nd
		delete(t.node_map, node_to_delete_key)
		temp_root = &new_nd
	}
	// t.RootNode.teachKids()

	return t.updateRoot(temp_root)
}

func (t *MerkleTree) GenerateMerklePath(key string) []string {
	var merkle_path []string
	node, ok := t.node_map[key]
	if !ok {
		err := []string{"path_not_found"}
		return err
	}
	for node != t.RootNode {
		if node.parent.right == node {
			merkle_path = append(merkle_path, node.parent.left.entry.key)
		} else {
			merkle_path = append(merkle_path, node.parent.right.entry.key)
		}
		node = node.parent
	}
	return merkle_path
}

func (t *MerkleTree) VerifyMerklePath(entry *Entry, location int, merkle_path []string) bool {
	return true
}

func (t *MerkleTree) getRightMostNode() *Node {
	right_nd := t.RootNode
	for right_nd.is_leaf == false {
		right_nd = right_nd.right
	}
	return right_nd
}

func (t *MerkleTree) removeRightMostNode(right_nd *Node) *Node {
	if right_nd.parent == t.RootNode {
		t.RootNode = right_nd.parent.left
		//t.RootNode.parent = nil
	} else {
		grandparent := right_nd.parent.parent
		grandparent.right = right_nd.parent.left
		right_nd.parent.left.parent = grandparent
	}
	parent_to_delete := right_nd.parent.entry.key
	delete(t.node_map, parent_to_delete)
	return right_nd
}

func (t *MerkleTree) deleteLeafFromMaps(node *Node) {
	delete(t.entry_map, node.entry)
	delete(t.node_map, node.entry.key)
	removeEntry(t.entries, node.entry)
}

func (t *MerkleTree) Delete(entry *Entry) string {
	delete_nd, ok := t.entry_map[entry]
	fmt.Print("line 299")
	delete_nd.parent.printNodePointers()
	if !ok {
		return "path_not_found"
	}
	right_nd := t.getRightMostNode()
	fmt.Print("line 303")
	right_nd.printNodePointers()
	// Special case 1: only one node in tree prior to delete.
	if len(t.entry_map) == 1 {
		t.RootHash = ""
		t.RootNode = nil
		t.deleteLeafFromMaps(delete_nd)
		return t.RootHash
	} else if len(t.entry_map) == 2 { //Special case 2: 2 leafs in tree prior to delete.
		parent_to_delete := right_nd.parent.entry.key
		if right_nd == delete_nd {
			t.RootNode = right_nd.parent.left
		} else {
			t.RootNode = right_nd
		}
		t.RootNode.left, t.RootNode.right, t.RootNode.parent = nil, nil, nil
		t.RootHash = t.RootNode.entry.key
		t.deleteLeafFromMaps(delete_nd)
		delete(t.node_map, parent_to_delete)
		return t.RootHash
	}

	right_nd = t.removeRightMostNode(right_nd)
	fmt.Print("line 327")
	delete_nd.parent.printNodePointers()

	var temp_node *Node
	if right_nd == delete_nd { // Special case 3: deleting farthest right node and more then 2 entrys
		temp_node = delete_nd.parent.left
	} else {
		temp_node = right_nd
		temp_node.parent = delete_nd.parent
		if delete_nd == delete_nd.parent.right {
			temp_node.parent.right = temp_node
		} else {
			temp_node.parent.left = temp_node
		}
	}
	fmt.Print("line 339")
	temp_node.printNodePointers()
	fmt.Print("line 341")
	delete_nd.parent.printNodePointers()
	for temp_node != t.RootNode {
		var is_right bool
		fmt.Print("line 351")
		temp_node.printNodePointers()
		if temp_node.parent.parent != nil {
			if temp_node.parent.parent == temp_node.parent.parent.right {
				is_right = true
			} else if temp_node.parent == temp_node.parent.parent.left {
				is_right = false
			}
		}
		node_to_delete_key := temp_node.parent.entry.key
		var new_nd Node
		var str string
		var new_val string
		if temp_node == temp_node.parent.right {
			sibling := temp_node.parent.left
			str = sibling.entry.key + temp_node.entry.key
			new_val = sibling.entry.value + temp_node.entry.value
			new_nd = NewNode(temp_node.parent.left, temp_node, false)
		} else if temp_node == temp_node.parent.left {
			sibling := temp_node.parent.right
			str = temp_node.entry.key + sibling.entry.key
			new_val = temp_node.entry.value + sibling.entry.value
			new_nd = NewNode(temp_node, temp_node.parent.right, false)
		}
		new_nd_h := getHash(str)
		new_nd.makeEntry(new_nd_h, new_val)
		t.checkIfGrandParentRoot(temp_node, &new_nd)
		new_nd.teachKids()
		if temp_node.parent != t.RootNode {
			new_nd.teachParentMyName(is_right)
		} else {
			t.RootNode = &new_nd
		}
		t.node_map[new_nd_h] = &new_nd
		delete(t.node_map, node_to_delete_key) //del old parent
		temp_node = &new_nd                    // if new_nd is root level then stop
	}
	return t.RootHash
}

// Below is testing
var COUNT int = 10

func print2DUtil(root *Node, space int) {
	if root == nil {
		return
	}

	space += COUNT
	print2DUtil(root.right, space)

	fmt.Printf("\n")
	for i := COUNT; i < space; i++ {
		fmt.Printf(" ")
	}
	fmt.Printf(root.entry.value)

	print2DUtil(root.left, space)
	println()
}

func print2D(root *Node) {
	print2DUtil(root, 0)
}

func insertTest1() {
	t := NewMerkleTree()
	a := PublicNewEntry("a")
	b := PublicNewEntry("b")
	c := PublicNewEntry("c")
	d := PublicNewEntry("d")
	e := PublicNewEntry("e")
	f := PublicNewEntry("f")
	g := PublicNewEntry("g")

	fmt.Println("test 1 insert a ________")
	t.Insert(a)
	print2D(t.RootNode)
	fmt.Println("test 2 insert b ________")
	t.Insert(b)
	print2D(t.RootNode)
	fmt.Println("test 3 insert c ________")
	t.Insert(c)
	print2D(t.RootNode)
	fmt.Println("test 4 insert d ________")
	t.Insert(d)
	print2D(t.RootNode)

	fmt.Println("test 5 insert e ________")
	t.Insert(e)
	print2D(t.RootNode)
	fmt.Println("test 6 insert f ________")
	t.Insert(f)
	print2D(t.RootNode)
	fmt.Println("test 7 insert g ________")
	t.Insert(g)
	print2D(t.RootNode)

}

func deleteTest0() {
	t := NewMerkleTree()
	a := PublicNewEntry("a")
	b := PublicNewEntry("b")
	c := PublicNewEntry("c")
	t.Insert(a)
	fmt.Println("insert a test 1____________________________________")
	print2D(t.RootNode)

	t.Insert(b)
	fmt.Println("insert b test 2_____________________________________________")
	print2D(t.RootNode)

	t.Insert(c)
	fmt.Println("insert c test 3_____________________________________________")
	print2D(t.RootNode)

	fmt.Println("delete a test 4_____________________________________________")
	t.Delete(a)
	print2D(t.RootNode)
}

func deleteTest1() {
	t := NewMerkleTree()
	a := PublicNewEntry("a")
	b := PublicNewEntry("b")
	c := PublicNewEntry("c")
	d := PublicNewEntry("d")
	e := PublicNewEntry("e")
	f := PublicNewEntry("f")
	g := PublicNewEntry("g")

	//  fmt.Println("test 1 insert a ________")
	t.Insert(a)
	//  fmt.Println("test 2 insert b ________")
	t.Insert(b)
	print2D(t.RootNode)
	//  fmt.Println("test 3 insert c ________")
	t.Insert(c)
	print2D(t.RootNode)
	//  fmt.Println("test 4 insert d ________")
	t.Insert(d)
	//  print2D(t.RootNode)
	fmt.Println("test 5 insert e ________")
	t.Insert(e)
	//  print2D(t.RootNode)
	fmt.Println("test 6 insert f ________")
	t.Insert(f)
	//  print2D(t.RootNode)
	fmt.Println("test 7 insert g ________")
	t.Insert(g)
	print2D(t.RootNode)

	t.Delete(g)
	fmt.Println("delete g test 8_____________________________________________")
	print2D(t.RootNode)
}
func main() {
	//insertTest1()
	//deleteTest1()
	deleteTest0()
}
