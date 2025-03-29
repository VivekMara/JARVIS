package main

import (
	"bytes"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"
	"io"
	"encoding/json"

	"github.com/joho/godotenv"
)

func main(){
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading api key")
	}
	apiKey := os.Getenv("deepseek_api_key")
	url := os.Getenv("url")

	payload := map[string]interface{}{
		"model": "deepseek-chat",
		"messages": []map[string]string{
			{
				"role":    "system",
				"content": "You are a helpful assistant.",
			},
			{
				"role":    "user",
				"content": "Hello!",
			},
		},
		"stream": false,
	}
	jsonPayload, err := json.Marshal(payload)
	if err != nil {
		fmt.Println("Error marshaling JSON:", err)
		return
	}

	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonPayload))
	if err != nil {
		log.Fatal("Error making request", err)
		return
	}
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", fmt.Sprintf("Bearer %s", apiKey))

	client := &http.Client{
		Timeout:  10 * time.Second,
	}

	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error sending request:", err)
		return
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Error reading response:", err)
		return
	}

	fmt.Println("Status:", resp.Status)
	fmt.Println("Response:", string(body))


}