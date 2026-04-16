package main

import (
	"context"
	"myproject/backend/database"

	"github.com/OwlWorksInnovations/go-packages/configpath"
)

const CONFIG_FILE_PATH = ".owlsafe"
const CONFIG_FILE_NAME = "owlsafe"

func initialSetup(db *database.Database) {
	configpath.CreateConfigPath(CONFIG_FILE_PATH)
	err := database.CreateDatabase(CONFIG_FILE_NAME, configpath.GetConfigPath(CONFIG_FILE_PATH))
	if err != nil {
		panic(err)
	}

	database.CreateTable(db, "entries", database.Column{
		Name: "id",
		Type: database.Integer,
		Constraints: []database.Constraint{
			database.PrimaryKey,
			database.AutoIncrement,
		},
	}, database.Column{
		Name: "username",
		Type: database.Text,
		Constraints: []database.Constraint{
			database.NotNull,
		},
	}, database.Column{
		Name: "password",
		Type: database.Text,
		Constraints: []database.Constraint{
			database.NotNull,
		},
	}, database.Column{
		Name: "source",
		Type: database.Text,
		Constraints: []database.Constraint{
			database.NotNull,
		},
	})
}

// App struct
type App struct {
	ctx context.Context
	db  *database.Database
}

// NewApp creates a new App application struct
func NewApp() *App {
	return &App{}
}

// startup is called when the app starts. The context is saved
// so we can call the runtime methods
func (a *App) startup(ctx context.Context) {
	a.ctx = ctx
	db, err := database.OpenDatabase(CONFIG_FILE_NAME, configpath.GetConfigPath(CONFIG_FILE_PATH))
	if err != nil {
		panic(err)
	}
	a.db = db
}

func (a *App) shutdown() {
	a.db.Close()
}

func (a *App) Initialize() {
	initialSetup(a.db)
}
