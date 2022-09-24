// CE-288 - Programação Distribuída
// Lab 1 - Mutual Exclusion
// Nicholas Scharan Cysne (PMG)
//
// SharedResource.go - Arquivo que representa o recurso compartilhado

package main

import (
	"fmt"
	"net"
	"strconv"
	"strings"
	"utils"
)

func main() {
	Address, err := net.ResolveUDPAddr("udp", ":10001")
	utils.CheckError(err)
	Connection, err := net.ListenUDP("udp", Address)
	utils.CheckError(err)
	defer Connection.Close()

	buf := make([]byte, 1024)
	for {
		n, addr, err := Connection.ReadFromUDP(buf)
		utils.CheckError(err)
		msg := string(buf[0:n])

		// Parse Message - "id clock msg"
		s := strings.Split(msg, " ")
		processId, _ := strconv.Atoi(s[0])
		processClock, _ := strconv.Atoi(s[1])
		processMsg := s[2]

		fmt.Println(addr, "Id:", processId, "Clock:", processClock, "Action:", processMsg)
	}
}
