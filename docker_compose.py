version: "3.8"
services:
  db:
    image: postgres:latest
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: poker_db
    ports:
      - "5432:5432"

  redis:
    image: redis:latest
    ports:
      - "6379:6379"

  backend:
    build: .
    depends_on:
      - db
      - redis
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://user:password@db/poker_db
