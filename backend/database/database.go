package database

import (
	"database/sql"
	"fmt"
	"log"
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
	db, err := sql.Open("sqlite", path+"/"+name+".db?_busy_timeout=5000")
	if err != nil {
		return nil, err
	}
	db.SetMaxOpenConns(1)
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
	Default     string
}

func CreateTable(db *Database, tableName string, column ...Column) {
	query := "CREATE TABLE IF NOT EXISTS " + tableName + " ("
	for i, col := range column {
		query += col.Name + " " + string(col.Type)
		for _, constraint := range col.Constraints {
			query += " " + string(constraint)
		}
		if col.Default != "" {
			query += " DEFAULT '" + col.Default + "'"
		}
		if i < len(column)-1 {
			query += ", "
		}
	}
	query += ")"
	if _, err := db.DB.Exec(query); err != nil {
		log.Fatal(err)
	}
}

type RowValue struct {
	Column string
	Value  any
}

func CreateRow(db *Database, tableName string, values ...RowValue) {
	cols := ""
	placeholders := ""
	args := make([]any, len(values))
	for i, v := range values {
		if i > 0 {
			cols += ", "
			placeholders += ", "
		}
		cols += v.Column
		placeholders += "?"
		args[i] = v.Value
	}
	query := "INSERT INTO " + tableName + " (" + cols + ") VALUES (" + placeholders + ")"
	if _, err := db.DB.Exec(query, args...); err != nil {
		log.Fatal(err)
	}
}

type Filter struct {
	Column string
	Value  any
}

// Most complex part of this entire package as of 4/29/2026
func FindRows(db *Database, tableName string, filters ...Filter) ([]map[string]any, error) {
	query := "SELECT * FROM " + tableName
	args := make([]any, len(filters))

	if len(filters) > 0 {
		query += " WHERE "
		for i, f := range filters {
			if i > 0 {
				query += " AND "
			}
			query += f.Column + " = ?"
			args[i] = f.Value
		}
	}

	rows, err := db.DB.Query(query, args...)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	cols, err := rows.Columns()
	if err != nil {
		return nil, err
	}

	var results []map[string]any

	for rows.Next() {
		scanTargets := make([]any, len(cols))
		scanValues := make([]any, len(cols))
		for i := range scanValues {
			scanTargets[i] = &scanValues[i]
		}

		if err := rows.Scan(scanTargets...); err != nil {
			return nil, err
		}

		row := make(map[string]any, len(cols))
		for i, col := range cols {
			row[col] = scanValues[i]
		}
		results = append(results, row)
	}

	return results, rows.Err()
}

func DeleteRows(db *Database, tableName string, filters ...Filter) error {
	if len(filters) == 0 {
		return fmt.Errorf("refusing to delete without filters")
	}
	query := "DELETE FROM " + tableName + " WHERE "
	args := make([]any, len(filters))
	for i, f := range filters {
		if i > 0 {
			query += " AND "
		}
		query += f.Column + " = ?"
		args[i] = f.Value
	}
	_, err := db.DB.Exec(query, args...)
	return err
}

func (db *Database) exec(query string, args ...any) {
	if _, err := db.DB.Exec(query, args...); err != nil {
		log.Fatal(err)
	}
}

func (db *Database) Close() error {
	return db.DB.Close()
}
