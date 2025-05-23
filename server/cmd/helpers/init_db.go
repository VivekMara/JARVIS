package helpers

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/joho/godotenv"
)

func CreateTables(tables []string) (*pgxpool.Pool, error) {
	err := godotenv.Load()
	if err != nil {
		return nil, err
	}
	dbName := os.Getenv("DB_NAME")
	dbUser := os.Getenv("DB_USER")
	dbPassword := os.Getenv("DB_PASSWORD")

	connStr := fmt.Sprintf("postgres://%s:%s@127.0.0.1:5432/%s?sslmode=disable", dbUser, dbPassword, dbName)
	ctx := context.Background()

	dbpool, err := pgxpool.New(ctx, connStr)
	if err != nil {
		return nil, fmt.Errorf("unable to create connection pool: %w", err)
	}

	for _, query := range tables {
		_, err := dbpool.Exec(ctx, query)
		if err != nil {
			return nil, fmt.Errorf("error executing query %q: %w", query, err)
		}
		log.Printf("Migrated table with query: %s\n", query)
	}

	return dbpool, nil
}

