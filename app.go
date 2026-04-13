package main

import (
	"context"
	"encoding/json"
	"os"
	"path/filepath"
)

type Entry struct {
	Id       int
	Username string
	Email    string
	Password string
}

type Vault struct {
	Version int
	Entries []Entry
}

func getVaultPath() string {
	homeDir, err := os.UserHomeDir()
	if err != nil {
		panic(err)
	}

	return homeDir + "/.owl-safe/vault.json"
}

func vaultExists() bool {
	vaultPath := getVaultPath()
	vaultFile := filepath.Base(vaultPath)

	_, err := os.Stat(vaultFile)
	if err == nil {
		return true
	}

	return false
}

func createVault() {
	vaultPath := getVaultPath()

	dir := filepath.Dir(vaultPath)
	err := os.MkdirAll(dir, 0755)
	if err != nil {
		panic(err)
	}

	vaultFile, err := os.Create(vaultPath)
	if err != nil {
		panic(err)
	}
	defer vaultFile.Close()

	vault := Vault{
		Version: 1,
		Entries: []Entry{},
	}

	data, err := json.Marshal(vault)
	if err != nil {
		panic(err)
	}

	_, err = vaultFile.Write(data)
	if err != nil {
		panic(err)
	}
}

func readVault() Vault {
	vaultPath := getVaultPath()

	data, err := os.ReadFile(vaultPath)
	if err != nil {
		panic(err)
	}

	var vault Vault
	err = json.Unmarshal(data, &vault)
	if err != nil {
		panic(err)
	}

	return vault
}

func createEntry() {
	vaultPath := getVaultPath()
	vault := readVault()

	vaultFile, err := os.OpenFile(vaultPath, os.O_WRONLY|os.O_TRUNC, 0644)
	if err != nil {
		panic(err)
	}
	defer vaultFile.Close()

	entry := Entry{
		Id:       0,
		Username: "Example",
		Email:    "example@example.com",
		Password: "Example",
	}

	vault.Entries = append(vault.Entries, entry)

	data, err := json.Marshal(vault)
	if err != nil {
		panic(err)
	}

	_, err = vaultFile.Write(data)
	if err != nil {
		panic(err)
	}
}

func importVault() {
	vaultPath := getVaultPath()
	vault := readVault()

	const numEntries = 1000000
	newEntries := make([]Entry, numEntries)
	entry := Entry{
		Id:       0,
		Username: "Example",
		Email:    "example@example.com",
		Password: "Example",
	}

	for i := 0; i < numEntries; i++ {
		newEntries[i] = entry
	}
	vault.Entries = append(vault.Entries, newEntries...)

	vaultFile, err := os.OpenFile(vaultPath, os.O_WRONLY|os.O_TRUNC, 0644)
	if err != nil {
		panic(err)
	}
	defer vaultFile.Close()

	data, err := json.Marshal(vault)
	if err != nil {
		panic(err)
	}

	_, err = vaultFile.Write(data)
	if err != nil {
		panic(err)
	}
}

// App struct
type App struct {
	ctx context.Context
}

// NewApp creates a new App application struct
func NewApp() *App {
	return &App{}
}

// startup is called when the app starts. The context is saved
// so we can call the runtime methods
func (a *App) startup(ctx context.Context) {
	a.ctx = ctx
}

func (a *App) InitialSetup() {
	if !vaultExists() {
		createVault()
	}
}

func (a *App) CreateEntry() {
	createEntry()
}

func (a *App) ImportVault() {
	importVault()
}
