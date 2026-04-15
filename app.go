package main

import (
	"context"
	"myproject/backend/database"

	"github.com/OwlWorksInnovations/go-packages/configpath"
)

const CONFIG_FILE_PATH = ".owlsafe"
const CONFIG_FILE_NAME = "owlsafe"

func initialSetup() {
	configpath.CreateConfigPath(CONFIG_FILE_PATH)
	err := database.NewDatabase(CONFIG_FILE_NAME, configpath.GetConfigPath(CONFIG_FILE_PATH))
	if err != nil {
		panic(err)
	}

	db, err := database.OpenDatabase(CONFIG_FILE_NAME, configpath.GetConfigPath(CONFIG_FILE_PATH))
	if err != nil {
		panic(err)
	}

	column := &database.Column{
		Name: "id",
		Type: "INTEGER",
		Constraints: []string{
			"PRIMARY",
			"KEY",
			"AUTOINCREMENT",
		},
	}
	database.CreateTable(db, "entries", column)
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

func (a *App) Initialize() {
	initialSetup()
}
