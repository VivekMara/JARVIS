package handlers

import (
	"database/sql"
	"encoding/json"
	"log"
	"net/http"
	"time"

	"github.com/google/uuid"
	_ "github.com/lib/pq"
)


type Task struct {
	ID uuid.UUID `json:"id"`
	NAME string `json:"name"`
	STATUS bool `json:"status"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

type ApiResponse struct{
	Status string `json:"status"`
	Message string `json:"message"`
	Data any `json:"data,omitempty"`
	Error error `json:"error,omitempty"`
}

func sendSuccessResponse(w http.ResponseWriter, message string, data interface{}) {
    response := ApiResponse{
        Status:  "success",
        Message: message,
        Data:    data,
    }
    
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

func sendErrorResponse(w http.ResponseWriter,message string, err error, statusCode int) {
    response := ApiResponse{
        Status: "error",
		Message: message,
        Error:  err,
    }
    
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(statusCode)
    json.NewEncoder(w).Encode(response)
}

var db *sql.DB

func InitDB() error {
    connStr := "postgres://darthman:darthman05@localhost:5432/go_backend_db?sslmode=disable"
    
    var err error
    db, err = sql.Open("postgres", connStr)
    if err != nil {
        log.Println("Error connecting to DB:", err)
        return err
    }
    
    log.Println("Connected to db")
    
    err = db.Ping()
    if err != nil {
        log.Println("No response from the db:", err)
        db.Close()
        return err
    }
    
    _, err = db.Exec(`
    CREATE TABLE IF NOT EXISTS tasks (
        id UUID PRIMARY KEY,
        name TEXT NOT NULL,
        status BOOLEAN NOT NULL DEFAULT FALSE,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL
    );`)
    if err != nil {
        log.Println("Error creating a table in DB:", err)
        db.Close()
        return err
    }
    
    return nil
}

func Root(w http.ResponseWriter, r *http.Request) {
	if r.Method != "GET" {
		sendErrorResponse(w, "Invalid http method", nil, http.StatusMethodNotAllowed)
	} else {
		sendSuccessResponse(w, "Hello darthman", nil)
		log.Println(r.RemoteAddr)
	}
}

func Create_task(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		sendErrorResponse(w, "Invalid HTTP method", nil, http.StatusMethodNotAllowed)
	} else {
		var input struct{
			Name string `json:"name"`
		}
		err := json.NewDecoder(r.Body).Decode(&input)
		if err != nil {
			sendErrorResponse(w, "Error decoding request", err, http.StatusBadRequest)
			return
		}
		if input.Name == "" {
			sendErrorResponse(w, "Task name is required", nil, http.StatusBadRequest)
			return
		}
		current_time := time.Now()
		var task = Task{
			ID: uuid.New(),
			NAME: input.Name,
			STATUS: false,
			CreatedAt: current_time,
			UpdatedAt: current_time,
		}
		_, err = db.Exec(`
		INSERT INTO tasks (id, name, status, created_at, updated_at) VALUES ($1, $2, $3, $4, $5)`, task.ID, task.NAME, task.STATUS, task.CreatedAt, task.UpdatedAt)
		if err != nil {
			sendErrorResponse(w, "Error creating task", err, http.StatusInternalServerError)
		} else {
			sendSuccessResponse(w, "Task created successfully", task)
			log.Println("Task inserted successfully ", task)
		}
	}
}


func Read_task(w http.ResponseWriter, r *http.Request) {
	if r.Method != "GET" {
		sendErrorResponse(w, "Invalid http method", nil, http.StatusMethodNotAllowed)
	} else {
		query := r.URL.Query()
		id := query.Get("id")
		err := uuid.Validate(id)
		if err != nil {
			sendErrorResponse(w, "Invalid uuid", err, http.StatusBadRequest)
			log.Println(err)
			return
		}
		row := db.QueryRow("SELECT * FROM tasks WHERE id = $1", id)
		var task Task
		err = row.Scan(&task.ID, &task.NAME, &task.STATUS, &task.CreatedAt, &task.UpdatedAt)
		if err != nil {
			sendErrorResponse(w, "Error scanning db", err, http.StatusInternalServerError)
		} else {
			sendSuccessResponse(w, "Task Retrieved successfully", task)
		}
	}
}


func Read_tasks(w http.ResponseWriter, r *http.Request) {
	if r.Method != "GET" {
		sendErrorResponse(w, "Invalid http method", nil, http.StatusMethodNotAllowed)
	} else {
		rows, err := db.Query("SELECT * FROM tasks")
		if err != nil {
			log.Println("Error querying data ", err)
			defer rows.Close()
			sendErrorResponse(w, "Error querying data", err, http.StatusInternalServerError)
		} else {
			tasks := make([]Task, 0)
			for rows.Next(){
				var task Task
				err = rows.Scan(&task.ID, &task.NAME, &task.STATUS, &task.CreatedAt, &task.UpdatedAt)
				if err != nil {
					log.Println("Scan error: ", err)
					sendErrorResponse(w, "Error in scanning rows", err, http.StatusInternalServerError)
					continue
				} else {
					tasks = append(tasks, task)
				}
			}
			sendSuccessResponse(w, "Successfully retrieved data", tasks)
		}
	}
}


func Update_task(w http.ResponseWriter, r *http.Request) {
	if r.Method != "PUT" {
		sendErrorResponse(w, "Invalid http method", nil, http.StatusMethodNotAllowed)
	} else {
		var UpdatedTask struct {
			ID uuid.UUID `json:"id"`
			NAME string `json:"name"`
			STATUS bool `json:"status"`
			CreatedAt time.Time `json:"created_at"`
			UpdatedAt time.Time `json:"updated_at"`
		}
		err := json.NewDecoder(r.Body).Decode(&UpdatedTask)
		if err != nil {
			sendErrorResponse(w, "Error decoding request", err, http.StatusBadRequest)
			return
		}
		err = uuid.Validate(UpdatedTask.ID.String())
		if err != nil {
			sendErrorResponse(w, "Task id is required", nil, http.StatusBadRequest)
			return
		}
		current_time := time.Now()
		res, err := db.Exec("UPDATE tasks SET name = $1, status = $2, updated_at = $3 WHERE id = $4", UpdatedTask.NAME, UpdatedTask.STATUS, current_time, UpdatedTask.ID)
		if err != nil {
			sendErrorResponse(w, "Error updating task", err, http.StatusInternalServerError)
		} else {
			sendSuccessResponse(w, "Task created successfully", []any{UpdatedTask, res})
		}
	}
}


func Delete_task(w http.ResponseWriter, r *http.Request) {
	if r.Method != "DELETE" {
		sendErrorResponse(w, "Invalid http method", nil, http.StatusMethodNotAllowed)
	} else {
		query := r.URL.Query()
		id := query.Get("id")
		err := uuid.Validate(id)
		if err != nil {
			sendErrorResponse(w, "Invalid uuid", err, http.StatusBadRequest)
			log.Println(err)
			return
		}
		res, err := db.Exec("DELETE FROM tasks WHERE id = $1", id)
		if err != nil {
			sendErrorResponse(w, "Error executing command", err, http.StatusInternalServerError)
			return
		}
		affectedRows, err := res.RowsAffected()
		if affectedRows == 0 {
			sendErrorResponse(w, "No task found with the given id", nil, http.StatusBadRequest)
		} else {
			sendSuccessResponse(w, "Task deleted successfully", []any{res, affectedRows})
		}
	}
}
