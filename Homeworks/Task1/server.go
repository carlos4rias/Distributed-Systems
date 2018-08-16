package main

import (
	"bufio"
	"fmt"
	"math"
	"net"
	"strconv"
	"strings"
)

type HandleFunc func(a int, b int) string

func eval(message string) string {
	// var handler map[string]HandleFunc
	// handler["sum"] = handleSum
	values := strings.Split(message, " ")
	if len(values) != 3 {
		return "is not a valid operation"
	}
	a, err1 := strconv.Atoi(values[0])
	b, err2 := strconv.Atoi(values[1])
	if err1 != nil || err2 != nil {
		return "is not a valid operation"
	}

	values[2] = strings.TrimRight(values[2], "\n")
	switch {
	case values[2] == "+":
		return strconv.Itoa(a + b)
	case values[2] == "-":
		return strconv.Itoa(a - b)
	case values[2] == "*":
		return strconv.Itoa(a * b)
	case values[2] == "/":
		return strconv.Itoa(a / b)
	case values[2] == "^":
		return strconv.FormatFloat(math.Pow(float64(a), float64(b)), 'f', 6, 64)
	case values[2] == "sqrt":
		return strconv.FormatFloat(math.Pow(float64(a), 1.0/float64(b)), 'f', 6, 64)
	}
	return "Not a valid operation"
}

func main() {
	fmt.Println("Launching server...")

	ln, _ := net.Listen("tcp", ":8083")
	conn, _ := ln.Accept()

	for {
		message, err := bufio.NewReader(conn).ReadString('\n')
		if err != nil {
			break
		}
		fmt.Print("Message Received: ", string(message))
		newmessage := strings.ToUpper("The operation result is: " + eval(message))
		conn.Write([]byte(newmessage + "\n"))
	}
	conn.Close()
}
