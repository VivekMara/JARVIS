package main

import (
	"log"
	"net/http"
	"primary_backend/cmd/handlers"
)

func main(){
	//DB initialization
	handlers.InitDB()
	
	//routes
	http.HandleFunc("/", handlers.Root)
	http.HandleFunc("/create", handlers.Create_task)
	http.HandleFunc("/read", handlers.Read_task)
	http.HandleFunc("/readAll", handlers.Read_tasks)
	http.HandleFunc("/update", handlers.Update_task)
	http.HandleFunc("/delete", handlers.Delete_task)

	//server
	log.Println("Server starting on port 6969")
	log.Fatal(http.ListenAndServe(":6969", nil))
	
}