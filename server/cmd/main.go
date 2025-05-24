package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
	"server/cmd/helpers"
	"server/cmd/routes"
	"time"

	"github.com/gorilla/mux"
)

func main() {
	//table creation and init
	tables := make([]string,0)
	users_table := `
	CREATE TABLE IF NOT EXISTS users (
		id SERIAL PRIMARY KEY,
		username VARCHAR(255) NOT NULL,
		email VARCHAR(255) NOT NULL UNIQUE,
		password_hash VARCHAR(255) NOT NULL,
		created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
		updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
	);`
	tables = append(tables, users_table)
	sessions_table := `
	CREATE TABLE IF NOT EXISTS sessions (
    	session_id UUID PRIMARY KEY,
    	user_id INTEGER REFERENCES users(id),
    	created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    	expires_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    	user_agent TEXT,
    	ip_address TEXT
	);
	`
	tables = append(tables, sessions_table)
	dbpool, err := helpers.CreateTables(tables)
	if err != nil {
		err_stmt := fmt.Sprintf("Failed to create tables!! with error: %s", err)
		log.Println(err_stmt)
	} else {
		log.Println("Database connection established and table created successfully")
	}
	helpers.Pool = dbpool
	defer helpers.Pool.Close()

	var wait time.Duration
	flag.DurationVar(&wait, "Graceful Shutdown", time.Second * 15, "the duration for which the server shutdowns")
	flag.Parse()
	
	r := mux.NewRouter()

	srv := &http.Server{
		Addr: "0.0.0.0:8989",
		WriteTimeout: time.Second * 15,
        ReadTimeout:  time.Second * 15,
        IdleTimeout:  time.Second * 60,
		Handler: r,
	}

	go func() {
        if err := srv.ListenAndServe(); err != nil {
            log.Println(err)
        }
    }()
	
	//routes
	r.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		resp := []byte("Hello Darthman")
		w.Write(resp)
	})

	//auth
	r.HandleFunc("/auth/register", routes.Register)
	r.HandleFunc("/auth/login", routes.Login)
	r.HandleFunc("/auth/logout", routes.Logout)

	r.HandleFunc("/query", routes.GrpcDeepseek)

	http.Handle("/", r)

	//server
	log.Println("Server starting on port 6969")
	log.Fatal(http.ListenAndServe(":6969", nil))
}
