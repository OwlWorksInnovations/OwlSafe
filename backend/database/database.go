package database

import (
	"database/sql"
	"fmt"
	"os"

	_ "modernc.org/sqlite"
)

type Database struct {
	*sql.DB
}

func CreateDatabase(name string, path string) error {
	_, err := os.Stat(path + "/" + name + ".db")
	if err != nil {
		os.Create(path + "/" + name + ".db")
	}

	return err
}

func OpenDatabase(name string, path string) (*Database, error) {
	db, err := sql.Open("sqlite", path+"/"+name+".db")
	if err != nil {
		return nil, err
	}

	return &Database{db}, nil
}

type ColumnType string

const (
	Integer ColumnType = "INTEGER"
	Text    ColumnType = "TEXT"
	Real    ColumnType = "REAL"
	Blob    ColumnType = "BLOB"
)

type Constraint string

const (
	PrimaryKey    Constraint = "PRIMARY KEY"
	AutoIncrement Constraint = "AUTOINCREMENT"
)

type Column struct {
	Name        string
	Type        string
	Constraints []Constraint
}

func CreateTable(db *Database, tableName string, column *Column) {
	query := "CREATE TABLE IF NOT EXISTS " + tableName + " (" + column.Name + " " + column.Type
	for _, constraint := range column.Constraints {
		query += " " + constraint
	}
	query += ")"

	fmt.Println(query)
	// db.Exec(query)
}

func (db *Database) Close() error {
	return db.DB.Close()
}
