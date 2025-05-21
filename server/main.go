package main

import (
	"context"
	"log"
	"time"

	pb "server/server/greeterpb"
	"google.golang.org/grpc"
)

func main() {
	conn, err := grpc.Dial("localhost:50051", grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		log.Fatalf("Could not connect: %v", err)
	}
	defer conn.Close()

	client := pb.NewGreeterClient(conn)

	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	res, err := client.SayHello(ctx, &pb.HelloRequest{Name: "Go Client"})
	if err != nil {
		log.Fatalf("Could not greet: %v", err)
	}

	log.Printf("Response from server: %s", res.Message)
}
