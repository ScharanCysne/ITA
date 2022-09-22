// CE-288 - Programação Distribuída
// Lab 1 - Mutual Exclusion
// Nicholas Scharan Cysne (PMG)
//
// Process.go - Arquivo que representa um processo

package main

import (
	"fmt"
	"net"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
	"utils"
)

// Global Variables
var err string
var id int                          // Process Id as Int
var idStr string                    // Process Id as String
var port string                     // Process port
var nClients int                    // Number of processes
var clientIds []int                 // Array of processes' ids
var clientConn map[int]*net.UDPConn // Array of connections to different servers
var servConn *net.UDPConn           // Server Connection
var resourcePort string             // CS Resource Port
var resourceConn *net.UDPConn       // CS Resource Connection

// Clock Mutex
type Clock struct {
	mu    sync.Mutex
	value int
}

// State Mutex
type State struct {
	mu    sync.Mutex
	value int
}

// Replies Mutex
type Reply struct {
	mu    sync.Mutex
	value []int
}

// Queue Mutex
type Queue struct {
	mu    sync.Mutex
	value []int
}

var clock Clock // Process' Clock
var state State // Process' State
var rep Reply   // List of replies received after request
var queue Queue // Queue of requests to reply

// Possible States
const RELEASED = 0
const WANTED = 1
const HELD = 2

// Send a message msg to a certain address with the option of updating the clock or not
func sendMessage(conn *net.UDPConn, msg string, update bool) {
	clock.mu.Lock()
	if update { // Update current logical clock
		clock.value++
	}
	// Append Process Id and Clock value in Msg
	msg = idStr + " " + strconv.Itoa(clock.value) + " " + msg
	clock.mu.Unlock()
	// Load in buffer
	buf := []byte(msg)
	_, err := conn.Write(buf)
	utils.CheckError(err)
}

// Init all client and server connections
func initConnections() {
	idStr = os.Args[1]                      // Process Id as String
	id, _ = strconv.Atoi(idStr)             // Process Id as Int
	port = os.Args[id+1]                    // Process port
	nClients = len(os.Args) - 3             // Number of processes
	clientIds = make([]int, nClients)       // Array of processes' ids
	clientConn = make(map[int]*net.UDPConn) // Array of connections to different servers

	// Resource connection
	resourcePort = ":10001" // CS Resource Port
	resourceAddr, err := net.ResolveUDPAddr("udp", "127.0.0.1"+resourcePort)
	utils.CheckError(err)
	resourceConn, err = net.DialUDP("udp", nil, resourceAddr)
	utils.CheckError(err)
	fmt.Println("Resource port: " + resourcePort[1:])

	// Configure it's own connection
	serverAddr, err := net.ResolveUDPAddr("udp", "127.0.0.1"+port)
	utils.CheckError(err)
	servConn, err = net.ListenUDP("udp", serverAddr)
	utils.CheckError(err)
	fmt.Println("Process Port: " + port[1:])

	// Configure clients connections
	process := 1 // Port numbers in os.args
	for client := 0; client < nClients; client++ {
		if process == id {
			process++ // Avoid appending own connection
		}

		clientAddr, err := net.ResolveUDPAddr("udp", "127.0.0.1"+os.Args[process+1])
		utils.CheckError(err)
		Conn, err := net.DialUDP("udp", nil, clientAddr)
		clientIds[client] = process
		clientConn[process] = Conn
		utils.CheckError(err)
		fmt.Println("Client port: " + os.Args[process+1][1:])
		process++
	}
}

func doClientJob(ch chan string) {
	// Everytime it identifies a new input, sends a request to access CS
	for {
		select {
		case x, valid := <-ch: // Wait receive the command to request resource
			if valid {
				if x == idStr { // Internal action
					clock.mu.Lock()
					clock.value++
					clock.mu.Unlock()
				} else if x == "request" { // Request access to CS
					state.mu.Lock()
					if state.value == WANTED || state.value == HELD {
						fmt.Println("[500] Invalid Request: Process already awaiting for resource.")
					}
					if state.value == RELEASED {
						state.value = WANTED // Change State to WANTED
						rep.mu.Lock()
						rep.value = make([]int, 0) // Empty reply list
						rep.mu.Unlock()
						for j := 0; j < nClients; j++ { // Send Request to all other processes
							sendMessage(clientConn[clientIds[j]], "request", true)
						}
					}
					state.mu.Unlock()
				} else if x == "free" {
					state.mu.Lock()
					if state.value == WANTED || state.value == RELEASED {
						fmt.Println("[500] Invalid Command: Process don't hold resource.")
					}
					if state.value == HELD {
						state.value = RELEASED
						queue.mu.Lock()
						for len(queue.value) > 0 {
							queueId := queue.value[0]
							queue.value = queue.value[1:]
							sendMessage(clientConn[queueId], "reply", true)
						}
						queue.mu.Unlock()
						rep.mu.Lock()
						rep.value = make([]int, 0) // Empty reply list
						rep.mu.Unlock()
						sendMessage(resourceConn, "free", true)
					}
					state.mu.Unlock()
				} else {
					fmt.Println("[500] Invalid Command: " + x)
				}

			} else {
				fmt.Println("Closed channel")
			}
		default:
			time.Sleep(time.Second * 1)
		}
		time.Sleep(time.Second * 1)
	}
}

// Listens to requests from other precesses
func doServerJob(ch chan string) {
	fmt.Println("\nListening...\n")
	// Buffer
	buf := make([]byte, 1024)

	for {
		// Check if received any message
		n, addr, err := servConn.ReadFromUDP(buf)
		utils.CheckError(err)
		// Store Message
		msg := string(buf[0:n])
		// Handle Request
		s := strings.Split(msg, " ") //[id, clock, msg]
		processId, _ := strconv.Atoi(s[0])
		processClock, _ := strconv.Atoi(s[1])
		processMsg := s[2]
		// Handles Request of Replies
		handleMessage(addr, processId, processClock, processMsg, ch)
	}
}

func handleMessage(addr *net.UDPAddr, processId int, processClock int, processMsg string, ch chan string) {
	state.mu.Lock()
	clock.mu.Lock()
	// Update clock
	clock.value = utils.Max(clock.value, processClock) + 1
	fmt.Println("State:", state.value, "Clock:", clock.value)
	fmt.Println(addr, processMsg, "Id:", processId, "Clock:", processClock)

	if processMsg == "request" {
		if state.value == HELD || (state.value == WANTED && clock.value < processClock) || (state.value == WANTED && clock.value == processClock && id < processId) {
			queue.mu.Lock()
			queue.value = append(queue.value, processId)
			queue.mu.Unlock()
		} else {
			sendMessage(clientConn[processId], "reply", false)
		}
	}
	if processMsg == "reply" {
		if state.value == WANTED {
			rep.mu.Lock()
			// Queue replies
			rep.value = append(rep.value, processId)
			// If got enough replies, access the resource
			if len(rep.value) == nClients {
				state.value = HELD
				sendMessage(resourceConn, "held", false)
				fmt.Println("State:", state.value, "Clock:", clock.value)
			}
			rep.mu.Unlock()
		} else {
			// discard message for it is already HELD or RELEASED
		}
	}
	clock.mu.Unlock()
	state.mu.Unlock()
}

func main() {
	//  Init and defer connections
	initConnections()
	defer servConn.Close()
	for i := 0; i < nClients; i++ {
		defer clientConn[clientIds[i]].Close()
	}

	// Init State Mutex as RELEASED
	state.mu.Lock()
	state.value = RELEASED
	state.mu.Unlock()

	// Init Clock Mutex as Zero
	clock.mu.Lock()
	clock.value = 0
	clock.mu.Unlock()

	// Replies
	rep.mu.Lock()
	rep.value = make([]int, 0)
	rep.mu.Unlock()

	// Queue
	queue.mu.Lock()
	queue.value = make([]int, 0)
	queue.mu.Unlock()

	// Input channel
	ch := make(chan string)
	go utils.ReadInput(ch)

	// Handle communication
	go doServerJob(ch)
	go doClientJob(ch)

	for {
		// eternal loop...
	}
}
