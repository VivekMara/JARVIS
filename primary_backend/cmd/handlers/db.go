package handlers

import (
	"database/sql"
	"log"

	"github.com/google/uuid"
	_ "github.com/lib/pq"
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


func Create_task(db *sql.DB, name string) (Task, error) {
	var task = Task{
		ID: uuid.New(),
		NAME: name,
		STATUS: false,
	}
	_, err := db.Exec(`
	INSERT INTO tasks (id, name, status) VALUES ($1, $2, $3)`, task.ID, task.NAME, task.STATUS)

	defer db.Close()
	return task,err
}


func Read_task(db *sql.DB, name string) (Task, error) {
	row := db.QueryRow("SELECT * FROM tasks WHERE name = $1", name)
	var task Task
	err := row.Scan(&task.ID, &task.NAME, &task.STATUS)
	return task, err
}


func Read_tasks(db *sql.DB) ([]Task, error) {
	rows, err := db.Query("SELECT * FROM tasks")
	defer rows.Close()
	tasks := make([]Task, 0)
	for rows.Next(){
		var task Task
		err = rows.Scan(&task.ID, &task.NAME, &task.STATUS)
		if err != nil {
			log.Fatal("Scan error: ", err)
			continue
		}
		tasks = append(tasks, task)

	}
	return tasks, err
}


func Update_task(db *sql.DB, task Task) error {
	_, err := db.Exec("UPDATE tasks SET name = $1, status = $2 WHERE id = $3", task.NAME, task.STATUS, task.ID)

	return err
}


func Delete_task(db *sql.DB, id uuid.UUID)(int64, error, error){
	res, err1 := db.Exec("DELETE FROM tasks WHERE id = $1", id)
	affectedRows, err2 := res.RowsAffected()

	return affectedRows, err1, err2
}
