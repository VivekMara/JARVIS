package handlers

import (
	"database/sql"
	"fmt"

	_ "github.com/lib/pq"
	"github.com/google/uuid"
)

type Task struct {
	ID uuid.UUID `json:"id"`
	NAME string `json:"name"`
	STATUS bool `json:"status"`
}

func DB_connect() (*sql.DB , error) {
	connStr := "postgres://darthman:darthman05@localhost:5432/go_backend_db?sslmode=disable"
	db, err := sql.Open("postgres", connStr)
	return db,err
}
func Create_table(db *sql.DB) error {
	_, err := db.Exec(`
	CREATE TABLE IF NOT EXISTS tasks (
		id UUID PRIMARY KEY,
		name TEXT NOT NULL,
		status BOOLEAN NOT NULL
	);`)

	return err
}
func Create_task(db *sql.DB,name string) (Task,error) {
	defer db.Close()

	var task = Task{
		ID: uuid.New(),
		NAME: name,
		STATUS: false,
	}


	_, err := db.Exec(`
	INSERT INTO tasks (id, name, status) VALUES ($1, $2, $3)`, task.ID, task.NAME, task.STATUS)

	return task,err
}

func Read_task(){
	
}

func Read_tasks(){
	fmt.Println("Read tasks")
}

func Update_task(){
	fmt.Println("Update a task")
}

func Delete_task(){
	fmt.Println("Delete a task")
}
