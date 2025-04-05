package main

import (
	"log"
	"primary_backend/cmd/handlers"

	"github.com/gofiber/fiber/v2"
)
type ReadTask struct{
	NAME string `json:"name"`
}

func main(){
	app := fiber.New()

	app.Get("/", func(c *fiber.Ctx) error {
		return c.SendString("Hello, World!")
	})

	//connect db
	db, _ := handlers.DB_connect()
	

	//create table
	handlers.Create_table(db)
	

	//create a task
	app.Post("/create_task", func(c *fiber.Ctx) error {
		task := new(handlers.Task)
		err := c.BodyParser(task)
		if err != nil {
			return err
		}
		resp, err := handlers.Create_task(db, task.NAME)
		if err != nil {
			return fiber.NewError(fiber.StatusInternalServerError, "Internal DB error")
		} else {
			return c.Send([]byte("Task added successfully " + resp.NAME))
		}
	})
	
	

	//retrieve a task from db using it's name
	app.Get("read_task", func(c * fiber.Ctx) error {
		task := new(ReadTask)
		err := c.BodyParser(task)
		if err != nil{
			return c.Status(fiber.StatusNotFound).JSON(fiber.Map{
				"error": err.Error(),
			})
		}
		resp, err := handlers.Read_task(db, task.NAME)
		if err != nil {
			return c.Status(fiber.StatusNotFound).JSON(fiber.Map{
				"error": err.Error(),
			})
		} else {
			return c.JSON(resp)
		}
	})

	

	// //retrieve all the tasks
	// handlers.Read_tasks(db)
	

	// //update a task with new values
	// UpdatedTask := handlers.Task{
	// 	ID: uuid.MustParse("c062c7e9-9c01-488a-9830-3f998ada1d56"),
	// 	NAME: "first task",
	// 	STATUS: true,
	// }
	// handlers.Update_task(db, UpdatedTask)
	

	// //delete a task using it's id
	// id := uuid.MustParse("c062c7e9-9c01-488a-9830-3f998ada1d56")
	// handlers.Delete_task(db, id)

	err := app.Listen(":6969")
	if err != nil {
		log.Fatal("Error listening on port 6969")
	}
	
}