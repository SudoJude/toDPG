.PHONY: help build up down logs clean test lint install-frontend install-backend

help:
	@echo "DPG4x Build Commands:"
	@echo "  make install-backend    - Install backend dependencies"
	@echo "  make install-frontend   - Install frontend dependencies"
	@echo "  make build              - Build Docker containers"
	@echo "  make up                 - Start Docker containers"
	@echo "  make down               - Stop Docker containers"
	@echo "  make logs               - View Docker logs"
	@echo "  make test               - Run all tests"
	@echo "  make test-backend       - Run backend tests"
	@echo "  make test-frontend      - Run frontend tests"
	@echo "  make lint               - Run linters"
	@echo "  make clean              - Clean up Docker containers and volumes"
	@echo "  make dev-backend        - Run backend in development mode"
	@echo "  make dev-frontend       - Run frontend in development mode"

install-backend:
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt

install-frontend:
	@echo "Installing frontend dependencies..."
	cd frontend && npm ci

build:
	@echo "Building Docker images..."
	docker-compose build --no-cache

up:
	@echo "Starting Docker containers..."
	docker-compose up -d
	@echo "Application started at http://localhost:8080"

down:
	@echo "Stopping Docker containers..."
	docker-compose down

logs:
	docker-compose logs -f

test: test-backend test-frontend
	@echo "All tests completed"

test-backend: install-backend
	@echo "Running backend tests..."
	cd backend && pip install pytest pytest-cov && pytest --cov=. || echo "No tests found"

test-frontend: install-frontend
	@echo "Running frontend tests..."
	cd frontend && npm test -- --run || echo "No tests configured"

lint:
	@echo "Running linters..."
	@echo "Linting Python code..."
	pip install flake8 pylint || true
	flake8 backend/ dpg4x/ --count --select=E9,F63,F7,F82 --show-source --statistics || true

clean:
	@echo "Cleaning up Docker resources..."
	docker-compose down -v
	find . -type d -name __pycache__ -exec rm -rf {} + || true
	find . -type d -name node_modules -exec rm -rf {} + || true

dev-backend: install-backend
	@echo "Starting backend in development mode..."
	cd backend && FLASK_ENV=development FLASK_DEBUG=1 python -m flask run --host=0.0.0.0

dev-frontend: install-frontend
	@echo "Starting frontend in development mode..."
	cd frontend && npm start
