package main

import (
	"crypto/sha512"
	"encoding/hex"
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

func (n *Node) teachKids(left *Node, right *Node) {
	// check if actually need those inputs
	n.left.parent = n
	n.right.parent = n
}

type Entry struct {
	key   string
	value string
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
		new_root.teachKids(future_sib, new_leaf_nd)
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
		new_nd.teachKids(temp_root.parent, new_leaf_nd)
		t.node_map[new_nd_h] = &new_nd
		temp_root = &new_nd
	} else if temp_root.parent.left.is_leaf == false && temp_root.is_leaf == true {
		str := temp_root.entry.key + new_leaf_nd.entry.key
		new_nd_h := getHash(str)
	}

	//initial insert of leaf and there is already a lonely leaf

	return t.RootHash
}

func main() {

}
