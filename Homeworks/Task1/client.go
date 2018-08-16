package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
)

func main() {
	conn, _ := net.Dial("tcp", "127.0.0.1:8083")
	fmt.Println("Available Operators: +, -, /, *, ^, sqrt")
	fmt.Println("Use: number_a number_b operator")
	fmt.Println("Example: 10 3 ^")
	for {
		reader := bufio.NewReader(os.Stdin)
		fmt.Print("Text to send: ")
		text, err := reader.ReadString('\n')
		if err != nil {
			break
		}
		fmt.Fprint(conn, text+"\n")
		message, err := bufio.NewReader(conn).ReadString('\n')
		if err != nil {
			break
		}
		fmt.Print("Message from server: " + message)
	}
	conn.Close()
}
