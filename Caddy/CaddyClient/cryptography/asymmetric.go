package cryptography

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	"encoding/pem"
	"errors"
	"fmt"
	"log"
	"os"
)

func generateRSAKeys() *rsa.PrivateKey {
	privateKey, err := rsa.GenerateKey(rand.Reader, 4096)
	if err != nil {
		fmt.Printf("Error generating private key: %v\n", err)
		return nil
	}

	return privateKey
}

func saveKeyToFile(privateKey *rsa.PrivateKey, filename string) error {
	privateKeyBytes := x509.MarshalPKCS1PrivateKey(privateKey)

	privateKeyPEM := pem.EncodeToMemory(&pem.Block{
		Type:  "RSA PRIVATE KEY",
		Bytes: privateKeyBytes,
	})

	err := os.WriteFile(filename, privateKeyPEM, 0600)
	if err != nil {
		return fmt.Errorf("failed to write private key to file: %v", err)
	}

	return nil
}

func loadKeyFromFile(filename string) (*rsa.PrivateKey, error) {
	privateKeyPEM, err := os.ReadFile(filename)
	if err != nil {
		return nil, fmt.Errorf("failed to read private key file: %v", err)
	}

	block, _ := pem.Decode(privateKeyPEM)
	if block == nil {
		return nil, fmt.Errorf("failed to decode PEM block")
	}

	privateKey, err := x509.ParsePKCS1PrivateKey(block.Bytes)
	if err != nil {
		key, err := x509.ParsePKCS8PrivateKey(block.Bytes)
		if err != nil {
			return nil, fmt.Errorf("failed to parse private key: %v", err)
		}
		var ok bool
		privateKey, ok = key.(*rsa.PrivateKey)
		if !ok {
			return nil, fmt.Errorf("private key is not an RSA private key")
		}
	}

	return privateKey, nil
}

func GetKeys(KeyPath string) *rsa.PrivateKey {
	info, err := os.Stat(KeyPath)

	if info.IsDir() {
		log.Fatal(errors.New("path is a directory, not a file: " + KeyPath))
		os.Exit(1)
	}

	if err != nil && !os.IsNotExist(err) {
		log.Fatal(err)
		os.Exit(1)
	}

	if os.IsNotExist(err) || info.Size() == 0 {
		keys := generateRSAKeys()
		if err := saveKeyToFile(keys, KeyPath); err != nil {
			log.Fatal(err)
			os.Exit(1)
		}
		return keys
	}

	keys, err := loadKeyFromFile(KeyPath)
	if err != nil {
		log.Fatal(err)
		os.Exit(1)
	}

	return keys
}
