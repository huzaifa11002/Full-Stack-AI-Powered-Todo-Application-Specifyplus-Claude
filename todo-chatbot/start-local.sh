#!/bin/bash

# Start local access to TODO app on Minikube
# This script sets up port-forwarding for frontend and backend services

echo "Starting TODO App on Minikube..."

# Kill any existing port-forward processes
pkill -f "kubectl port-forward" 2>/dev/null

# Wait for pods to be ready
echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/part-of=todo-chatbot -n todo-app --timeout=60s 2>/dev/null || true

# Start port-forward for frontend (port 30080)
echo "Starting frontend port-forward on http://localhost:30080"
kubectl port-forward -n todo-app svc/todo-app-todo-chatbot-frontend 30080:3000 --address 0.0.0.0 &
FRONTEND_PID=$!

# Start port-forward for backend (port 30081)
echo "Starting backend port-forward on http://localhost:30081"
kubectl port-forward -n todo-app svc/todo-app-todo-chatbot-backend 30081:8000 --address 0.0.0.0 &
BACKEND_PID=$!

echo ""
echo "=========================================="
echo "TODO App is now accessible:"
echo "  Frontend: http://localhost:30080"
echo "  Backend:  http://localhost:30081"
echo "=========================================="
echo ""
echo "Press Ctrl+C to stop"

# Wait for user to press Ctrl+C
wait $FRONTEND_PID $BACKEND_PID
