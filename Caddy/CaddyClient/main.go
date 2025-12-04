package main

import (
	//"fmt"
	"github.com/SmigorX/ProjectGneiss/Caddy/CaddyClient/cryptography"
	//"log"
	"crypto/rsa"
	"flag"
	//"net/http"
	"os"
)

type environ struct {
	KeyPath string
	Key     *rsa.PrivateKey
}

var environment = environ{}

func init() {
	flag.StringVar(&environment.KeyPath, "keyPath", "", "Path to a file to save the key")
}

func main() {
	flag.Parse()

	if environment.KeyPath == "" {
		os.Getenv("KEY_PATH")
	}

	if environment.KeyPath == "" {
		os.Exit(1)
	}

	environment.Key = cryptography.GetKeys(environment.KeyPath)

	//http.HandleFunc("/", handler)
	//log.Fatal(http.ListenAndServe(":8080", nil))
}
