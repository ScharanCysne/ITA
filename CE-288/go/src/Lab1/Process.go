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
var status map[int]string

// Possible States
const RELEASED = 0
const WANTED = 1
const HELD = 2

// Send a message msg to a certain address
func sendMessage(conn *net.UDPConn, msg string) {
	// Append Process Id and Clock value in Msg
	msg = idStr + " " + strconv.Itoa(clock.value) + " " + msg
	// Load in buffer
	buf := []byte(msg)
	_, err := conn.Write(buf)
	utils.CheckError(err)
}

// Represents an internal action
func internalAction() {
	clock.mu.Lock()
	clock.value++
	fmt.Println("State:", status[state.value], "Clock:", clock.value)
	clock.mu.Unlock()
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
	resourcePort = ":10001" // Resource Port
	resourceAddr, err := net.ResolveUDPAddr("udp", "127.0.0.1"+resourcePort)
	utils.CheckError(err)
	resourceConn, err = net.DialUDP("udp", nil, resourceAddr)
	utils.CheckError(err)
	fmt.Println("Resource port: " + resourcePort[1:])

	// Configure it's own listening port
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
	for { // Keeps forever checking for new inputs
		select {
		case x, valid := <-ch: // Wait until channel has received a command to request/free resource
			if valid { // If command is valid, act upon it
				if x == idStr {
					go internalAction() // Internal action (increment clock)
				} else if x == "request" { // Request access to resource
					// Lock state to process request
					state.mu.Lock()
					if state.value == WANTED {
						fmt.Println("[500] Invalid Request: Process already awaiting for resource.")
					}
					if state.value == HELD {
						fmt.Println("[500] Invalid Request: Process already holds resource.")
					}
					if state.value == RELEASED {
						state.value = WANTED        // Change State to WANTED
						time.Sleep(time.Second * 2) // Delay of 2s for testing purposes
						// Clear reply list
						rep.mu.Lock()
						rep.value = make([]int, 0)
						rep.mu.Unlock()
						// Update clock once and send request messages to all clients
						clock.mu.Lock()
						clock.value++
						// Send Request to all other processes
						for j := 0; j < nClients; j++ {
							sendMessage(clientConn[clientIds[j]], "request")
						}
						clock.mu.Unlock()
					}
					state.mu.Unlock()
				} else if x == "free" { // Free held resource and answer to queued requests
					// Lock state to process request
					state.mu.Lock()
					clock.mu.Lock()
					clock.value++ // Added this increase in clock to emulate an action occurring
					// Free held resource before answering queue
					sendMessage(resourceConn, "free")
					clock.mu.Unlock()
					if state.value == WANTED || state.value == RELEASED {
						fmt.Println("[500] Invalid Command: Process don't hold resource.")
					}
					if state.value == HELD {
						state.value = RELEASED // Change State to RELEASED
						// Lock queue to answer all requests
						queue.mu.Lock()
						for len(queue.value) > 0 { // Send message until queue is empty
							queueId := queue.value[0]                 // Pop first element in queue
							queue.value = queue.value[1:]             // Update queue
							sendMessage(clientConn[queueId], "reply") // Send message
						}
						queue.mu.Unlock()
						fmt.Println("State:", status[state.value], "Clock:", clock.value)
					}
					state.mu.Unlock()
				} else {
					fmt.Println("[500] Invalid Command: " + x)
				}

			} else {
				fmt.Println("[500] Closed Channel")
			}
		default:
			time.Sleep(time.Second * 1)
		}
		time.Sleep(time.Second * 1)
	}
}

func doServerJob(ch chan string) {
	// Listens to requests from other precesses
	fmt.Println("\nListening...\n")
	fmt.Println("State:", status[state.value], "Clock:", clock.value)
	// Buffer
	buf := make([]byte, 1024)

	for {
		// Check if received any message
		n, addr, err := servConn.ReadFromUDP(buf)
		utils.CheckError(err)
		// Store Message
		msg := string(buf[0:n])
		// Parse Message - "id clock msg"
		s := strings.Split(msg, " ")
		processId, _ := strconv.Atoi(s[0])
		processClock, _ := strconv.Atoi(s[1])
		processMsg := s[2]

		// Print received message - "Addr Msg Id Clock"
		fmt.Println(addr, processMsg, "Id:", processId, "Incoming Clock:", processClock)
		// Lock clock and state to process received message
		state.mu.Lock()
		clock.mu.Lock()
		// Handles Request/Replies
		if processMsg == "request" {
			if state.value == HELD ||
				(state.value == WANTED && clock.value < processClock) ||
				(state.value == WANTED && clock.value == processClock && id < processId) {
				// If STATE = HELD or (state = WANTED and (Tj, pj) < (Ti, pi)) -> queue request from pi without replying
				queue.mu.Lock()
				queue.value = append(queue.value, processId)
				queue.mu.Unlock()
			} else {
				// Reply immeaditely to pi
				sendMessage(clientConn[processId], "reply")
			}
		}
		if processMsg == "reply" {
			// Add to list of replies
			if state.value == WANTED {
				rep.mu.Lock()
				// Append reply
				rep.value = append(rep.value, processId)
				// If got enough replies, access the resource
				if len(rep.value) == nClients {
					state.value = HELD
					sendMessage(resourceConn, "held")
				}
				rep.mu.Unlock()
			} else {
				// discard message for it is already HELD or RELEASED
			}
		}
		// Update clock
		clock.value = utils.Max(clock.value, processClock) + 1 // Update clock

		fmt.Println("State:", status[state.value], "Clock:", clock.value)
		clock.mu.Unlock()
		state.mu.Unlock()
	}
}

func main() {
	//  Init and defer connections
	initConnections()
	defer servConn.Close()
	for i := 0; i < nClients; i++ {
		defer clientConn[clientIds[i]].Close()
	}

	// Status map for Terminal Output
	status = make(map[int]string)
	status[RELEASED] = "RELEASED"
	status[WANTED] = "WANTED"
	status[HELD] = "HELD"

	// Init State Mutex as RELEASED
	state.mu.Lock()
	state.value = RELEASED
	state.mu.Unlock()

	// Init Clock Mutex as Zero
	clock.mu.Lock()
	clock.value = 0
	clock.mu.Unlock()

	// Init empty Replies list
	rep.mu.Lock()
	rep.value = make([]int, 0)
	rep.mu.Unlock()

	// Init empty Queue
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
		// eternal loop... :)
	}
}
