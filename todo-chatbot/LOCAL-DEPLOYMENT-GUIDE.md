# Local Deployment Guide for TODO Application

This guide explains how to deploy the TODO application locally using Helm charts on Minikube.

## Prerequisites

- [Minikube](https://minikube.sigs.k8s.io/docs/start/) installed
- [kubectl](https://kubernetes.io/docs/tasks/tools/) installed
- [Helm](https://helm.sh/docs/intro/install/) installed
- Docker images for frontend and backend built locally

## Setup Instructions

### 1. Start Minikube

```bash
minikube start
```

### 2. Enable Ingress Controller

```bash
minikube addons enable ingress
```

### 3. Build Docker Images

Make sure you have built the Docker images locally:

```bash
# From the project root directory
cd frontend
docker build -t todo-app-frontend .

cd ../backend
docker build -t todo-app-backend .
```

Or if using Docker Compose:

```bash
docker-compose build
```

### 4. Deploy Using Helm

```bash
# Navigate to the helm chart directory
cd todo-chatbot

# Install the chart
helm install todo-app .
```

### 5. Access the Application

#### Option 1: Using NodePorts (Default)
- Frontend: http://localhost:30080
- Backend: http://localhost:30081

#### Option 2: Using Minikube Tunnel
In a separate terminal, run:
```bash
minikube tunnel
```

Then access the application via the external IP:
```bash
minikube ip
```

#### Option 3: Using Ingress
With the ingress enabled, you can access the application at:
- http://localhost/

### 6. Verify Deployment

Check that all pods are running:
```bash
kubectl get pods
```

Check the services:
```bash
kubectl get services
```

View application logs:
```bash
kubectl logs -f deployment/$(kubectl get deployments -o jsonpath='{.items[0].metadata.name}' -l app.kubernetes.io/component=frontend)
kubectl logs -f deployment/$(kubectl get deployments -o jsonpath='{.items[0].metadata.name}' -l app.kubernetes.io/component=backend)
```

## Troubleshooting

### Common Issues

1. **Images not found**: Ensure Docker images are built locally with the correct names
2. **Port conflicts**: Check that ports 30080 and 30081 are not in use
3. **Insufficient resources**: Increase Minikube resources if pods are stuck in Pending state

### Useful Commands

```bash
# Check status of all resources
kubectl get all

# Describe a specific pod for detailed information
kubectl describe pod <pod-name>

# Port forward for debugging (alternative to NodePort)
kubectl port-forward svc/$(kubectl get svc -o jsonpath='{.items[0].metadata.name}' -l app.kubernetes.io/component=frontend) 3000:3000

# Uninstall the release
helm uninstall todo-app
```

## Configuration

The default configuration in `values.yaml` is optimized for local development:

- NodePort services for easy access
- Local image pull policy (`IfNotPresent`)
- Development environment variables
- Local PostgreSQL database
- Increased resource limits for local development

## Scaling

To scale the frontend or backend:

```bash
kubectl scale deployment/$(kubectl get deployments -o jsonpath='{.items[0].metadata.name}' -l app.kubernetes.io/component=frontend) --replicas=2
kubectl scale deployment/$(kubectl get deployments -o jsonpath='{.items[0].metadata.name}' -l app.kubernetes.io/component=backend) --replicas=2
```