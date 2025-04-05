package main

import (
	"fmt"
	"log"
	"primary_backend/cmd/handlers"
)

func main(){
	db, err := handlers.DB_connect()
	if err != nil {
		log.Fatal("Error connecting to db")
	} else {
		fmt.Println("Connected to db")
	}


	err = handlers.Create_table(db)
	if err != nil {
		log.Fatal("Error creating a table")
	} else {
		fmt.Println("Created the table")
	}

	
	resp,err := handlers.Create_task(db, "second task")
	if err != nil {
		log.Fatal("Error inserting data:", err)
	} else {
		fmt.Println("Task inserted successfully")
	}
	fmt.Println(resp)
}