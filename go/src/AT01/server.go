package main

import (
	"fmt"
	"net"
	"os"
)

func CheckError(err error) {
	if err != nil {
		fmt.Println("Error: ", err)
		os.Exit(0)
	}
}

func main() {
	address, err := net.ResolveUDPAddr("udp", ":10001")
	CheckError(err)

	conn, err := net.ListenUDP("udp", address)
	CheckError(err)
	defer conn.Close()

	buffer := make([]byte, 1024)

	for {
		n, addr, err := conn.ReadFromUDP(buffer)
		fmt.Println("Received ", string(buffer[0:n]), " from ", addr)

		if err != nil {
			fmt.Println("Error ", err)
		}
	}
}
