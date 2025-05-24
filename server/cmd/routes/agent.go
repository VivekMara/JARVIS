package routes

import (
	"context"
	"encoding/json"
	"net/http"
	"time"

	"server/cmd/helpers"
	agent "server/proto/ai_agent"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)



func GrpcDeepseek(w http.ResponseWriter, r *http.Request){
	if r.Method != http.MethodPost {
		helpers.SendErrorResponse(w, "Wrong http method", nil, http.StatusMethodNotAllowed)
		return
	}

	var input struct {
		Query string `json:"query"`
	}
	
	err := json.NewDecoder(r.Body).Decode(&input)
	if err != nil {
        helpers.SendErrorResponse(w, "Error decoding request", err, http.StatusBadRequest)
        return
    }

	if input.Query == "" {
        helpers.SendErrorResponse(w, "All fields are required", nil, http.StatusBadRequest)
        return
    }

	conn, err := grpc.NewClient("localhost:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		helpers.SendErrorResponse(w, "Could not connect to the grpc server", err, http.StatusInternalServerError)
	}
	defer conn.Close()

	client := agent.NewAgentClient(conn)

	ctx, cancel := context.WithTimeout(context.Background(), 200*time.Second)
	defer cancel()

	res, err := client.QueryDeepseek(ctx, &agent.Input{Query: input.Query})
	if err != nil {
		helpers.SendErrorResponse(w, "Could not talk with deepseek", err, http.StatusInternalServerError)
	}

	helpers.SendSuccessResponse(w, "Deepseek: ", res.Response)
}