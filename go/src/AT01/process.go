package main

import (
	"fmt"
	"net"
	"os"
	"strconv"
	"time"
)

var ClientConn []*net.UDPConn
var ServerConn *net.UDPConn

var err string
var myPort string
var nClients int

func CheckError(err error) {
	if err != nil {
		fmt.Println("Error: ", err)
		os.Exit(0)
	}
}

func PrintError(err error) {
	if err != nil {
		fmt.Println("Error: ", err)
	}
}

func doServerJob() {
	for {
		var buffer []byte
		n, addr, err := ServerConn.ReadFromUDP(buffer)
		fmt.Println("Received ", string(buffer[0:n]), " from ", addr)
		CheckError(err)
	}
}

func doClientJob(otherProcess int, i int) {
	msg := strconv.Itoa(i)
	buf := []byte(msg)
	_, err := ClientConn[otherProcess].Write(buf)
	CheckError(err)
}

func initConnections() {
	myPort = os.Args[1]
	nClients = len(os.Args) - 2
	ClientConn = make([]*net.UDPConn, nClients)

	ServerAddr, err := net.ResolveUDPAddr("udp", "127.0.0.1"+myPort)
	CheckError(err)
	ServerConn, err = net.ListenUDP("udp", ServerAddr)
	CheckError(err)

	for client := 0; client < nClients; client++ {
		ClientAddr, err := net.ResolveUDPAddr("udp", "127.0.0.1"+os.Args[2+client])
		CheckError(err)
		conn, err := net.DialUDP("udp", nil, ClientAddr)
		ClientConn[client] = conn
		CheckError(err)
	}
}

func main() {
	initConnections()

	defer ServerConn.Close()
	for i := 0; i < nClients; i++ {
		defer ClientConn[i].Close()
	}

	go doServerJob()

	for i := 0; ; i++ {
		for j := 0; j < nClients; j++ {
			go doClientJob(j, i)
		}
		time.Sleep(time.Second * 1)
	}
}
