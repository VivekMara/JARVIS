package main

import (
	"fmt"
	"log"
	"primary_backend/cmd/handlers"

	"github.com/google/uuid"
)

func main(){
	//connect db
	db, err := handlers.DB_connect()
	if err != nil {
		log.Fatal("Error connecting to db")
	} else {
		fmt.Println("Connected to db")
	}

	//create table
	err = handlers.Create_table(db)
	if err != nil {
		log.Fatal("Error creating a table")
	} else {
		fmt.Println("Created the table")
	}

	//create a task
	resp,err := handlers.Create_task(db, "second task")
	if err != nil {
		log.Fatal("Error inserting data:", err)
	} else {
		fmt.Println("Task inserted successfully")
	}
	fmt.Println(resp)

	//retrieve a task from db using it's name
	task, err := handlers.Read_task(db, "first task")
	if err != nil {
		log.Fatal("Error retrieving data:", err)
	} else {
		fmt.Println("Task retrieved successfully")
	}
	fmt.Println(task)

	//retrieve all the tasks
	tasks, err := handlers.Read_tasks(db)
	if err != nil {
		log.Fatal("Error retrieving data:", err)
	} else {
		fmt.Println("Tasks retrieved successfully")
	}
	fmt.Println(tasks)

	//update a task with new values
	UpdatedTask := handlers.Task{
		ID: uuid.MustParse("c062c7e9-9c01-488a-9830-3f998ada1d56"),
		NAME: "first task",
		STATUS: true,
	}
	err = handlers.Update_task(db, UpdatedTask)
	if err != nil {
		log.Fatal("Error updating task", err)
	} else {
		fmt.Println("Successfully updated the task")
	}

	//delete a task using it's id
	id := uuid.MustParse("c062c7e9-9c01-488a-9830-3f998ada1d56")
	affectedRows, err1, err2 := handlers.Delete_task(db, id)
	if affectedRows == 0 {
		fmt.Println("No task found with the id ", id)
	} else {
		fmt.Println("Task deleted successfully")
	}
	if err1 != nil {
		log.Fatal("Error deleting the task", err)
	} else {
		fmt.Println("Successfully deleted the task")
	}
	if err2 != nil {
		log.Fatal("Error fetching the affected rows", err)
	} else {
		fmt.Println("Successfully fetched the updated rows")
	}
}