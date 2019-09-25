package main

import (
	"crypto/sha512"
	"encoding/hex"
)

//	"crypto/sha512"
//	"encoding/hex"
//	"encoding/json"
//	"fmt"

type Node struct {
	left    *Node
	right   *Node
	parent  *Node
	is_leaf bool
	entry   *Entry
}

func initNode(left *Node, right *Node, is_leaf bool) Node {
	new_nd := Node{left: left, right: right, is_leaf: is_leaf}
	return new_nd
}

type Entry struct {
	value string
	key   string
}

func (e Entry) makeKey() string {
	h := sha512.New()
	h.Write([]byte(e.value))
	sha512_hash := hex.EncodeToString(h.Sum(nil))
	return string
}
