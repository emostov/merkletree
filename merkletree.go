package main

import (
	"crypto/sha512"
	"encoding/hex"
	"fmt"
	"math"
)

//	"crypto/sha512"
//	"encoding/hex"
//	"encoding/json"
//	"fmt"
func isPowerOfTwo(n int) bool {
	x := float64(n)
	if n == 0 {
		return false
	}
	return math.Ceil(math.Log2(x)) == math.Floor(math.Log2(x))
}

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

func (n *Node) makeEntry(key string, value string) {
	entry := &Entry{key: key, value: value}
	n.entry = entry
}

func (n *Node) teachKids() {
	// check if actually need those inputs
	n.left.parent = n
	n.right.parent = n
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

func (e *Entry) MakeKey() string {
	h := sha512.New()
	h.Write([]byte(e.value))
	sha512_hash := hex.EncodeToString(h.Sum(nil))
	return sha512_hash
}

// func (e *Entry) toJson() []byte {
// 	b, err := json.Marshal(e)
// 	if err != nil {
// 		fmt.Println(err)
// 		return
// 	}
// 	return b
// }

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

func getHash(str string) string {
	h := sha512.New()
	h.Write([]byte(str))
	out_hash := hex.EncodeToString(h.Sum(nil))
	return out_hash
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
		t.node_map[new_root_hash] = &new_root
		return t.updateRoot(&new_root)
	}
	second_to_last_entry := t.entries[len(t.entries)-2]
	temp_root := t.entry_map[second_to_last_entry]

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
		t.RootNode.parent = nil
	} else {
		grandparent := right_nd.parent.parent
		grandparent.right = right_nd.parent.left
		right_nd.parent.left.parent = grandparent
	}
	parent_to_delete := right_nd.parent.entry.key
	delete(t.node_map, parent_to_delete)
	return right_nd
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

func main() {
	insertTest1()
}
