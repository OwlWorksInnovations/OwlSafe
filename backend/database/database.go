package database

import (
	"database/sql"
	"os"

	_ "modernc.org/sqlite"
)

type Database struct {
	*sql.DB
}

func CreateDatabase(name string, path string) error {
	_, err := os.Stat(path + "/" + name + ".db")
	if os.IsNotExist(err) {
		os.Create(path + "/" + name + ".db")
		return nil
	} else if err != nil {
		return err
	}

	return nil
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
	NotNull       Constraint = "NOT NULL"
	Unique        Constraint = "UNIQUE"
)

type Column struct {
	Name        string
	Type        ColumnType
	Constraints []Constraint
}

func CreateTable(db *Database, tableName string, column ...Column) {
	query := "CREATE TABLE IF NOT EXISTS " + tableName + " ("
	for i, col := range column {
		query += col.Name + " " + string(col.Type)
		for _, constraint := range col.Constraints {
			query += " " + string(constraint)
		}
		if i < len(column)-1 {
			query += ", "
		}
	}
	query += ")"

	db.Exec(query)
}

func (db *Database) Close() error {
	return db.DB.Close()
}
