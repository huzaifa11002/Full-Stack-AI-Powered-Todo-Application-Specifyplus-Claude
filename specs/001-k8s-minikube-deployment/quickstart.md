# Quickstart: Deploy Todo Chatbot to Minikube

**Feature**: 001-k8s-minikube-deployment
**Date**: 2026-01-20
**Estimated Time**: 30-45 minutes

## Prerequisites

- Local machine with 4 CPU cores, 8GB RAM, 20GB disk space
- Docker installed and running
- Internet connectivity for downloading tools and images
- Administrative privileges for tool installation

## Quick Start (TL;DR)

```bash
# 1. Install tools
brew install minikube helm  # macOS
# OR: choco install minikube kubernetes-helm  # Windows
# OR: See detailed installation below for Linux

# 2. Start Minikube
minikube start --cpus=4 --memory=8192 --driver=docker

# 3. Enable addons
minikube addons enable ingress
minikube addons enable metrics-server

# 4. Create namespace
kubectl create namespace todo-app

# 5. Create secrets (replace with actual values)
kubectl create secret generic frontend-secrets \
  --from-literal=BETTER_AUTH_SECRET="your-secret-key" \
  -n todo-app

kubectl create secret generic backend-secrets \
  --from-literal=DATABASE_URL="postgresql://user:pass@host:5432/db" \
  --from-literal=BETTER_AUTH_SECRET="your-secret-key" \
  --from-literal=OPENAI_API_KEY="sk-..." \
  -n todo-app

# 6. Deploy with Helm (from k8s/helm/ directory)
helm install todo-backend ./todo-backend -n todo-app
helm install todo-frontend ./todo-frontend -n todo-app

# 7. Configure local DNS
echo "$(minikube ip) todo.local" | sudo tee -a /etc/hosts

# 8. Access application
open http://todo.local
```

## Detailed Installation Guide

### Step 1: Install Minikube

**macOS**:
```bash
# Using Homebrew
brew install minikube

# Verify installation
minikube version
```

**Linux**:
```bash
# Download and install
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Verify installation
minikube version
```

**Windows**:
```powershell
# Using Chocolatey (run as Administrator)
choco install minikube

# Verify installation
minikube version
```

### Step 2: Install Helm

**macOS**:
```bash
brew install helm
helm version
```

**Linux**:
```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm version
```

**Windows**:
```powershell
choco install kubernetes-helm
helm version
```

### Step 3: Install kubectl-ai (Optional)

**npm**:
```bash
npm install -g kubectl-ai
kubectl-ai --version
```

**pip**:
```bash
pip install kubectl-ai
kubectl-ai --version
```

**Configure API Key**:
```bash
export OPENAI_API_KEY="sk-..."
# OR
export GEMINI_API_KEY="your-gemini-key"
```

### Step 4: Install Kagent (Optional)

```bash
# Check official documentation for latest installation method
pip install kagent
# OR download binary from GitHub releases

kagent version
```

### Step 5: Start Minikube Cluster

```bash
# Start cluster with recommended resources
minikube start --cpus=4 --memory=8192 --disk-size=20g --driver=docker

# Verify cluster is running
minikube status

# Check kubectl connection
kubectl cluster-info
kubectl get nodes
```

**Expected Output**:
```
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   1m    v1.28.x
```

### Step 6: Enable Required Addons

```bash
# Enable NGINX Ingress Controller
minikube addons enable ingress

# Enable Metrics Server (for HPA)
minikube addons enable metrics-server

# Optional: Enable Dashboard
minikube addons enable dashboard

# Verify addons
minikube addons list | grep enabled
```

**Wait for Ingress Controller**:
```bash
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s
```

### Step 7: Create Namespace

```bash
# Create dedicated namespace
kubectl create namespace todo-app

# Set as default namespace (optional)
kubectl config set-context --current --namespace=todo-app

# Verify namespace
kubectl get namespaces
```

### Step 8: Create Kubernetes Secrets

**Important**: Replace placeholder values with actual credentials.

**Frontend Secrets**:
```bash
kubectl create secret generic frontend-secrets \
  --from-literal=BETTER_AUTH_SECRET="your-secret-key-here" \
  -n todo-app
```

**Backend Secrets**:
```bash
kubectl create secret generic backend-secrets \
  --from-literal=DATABASE_URL="postgresql://user:password@host:5432/dbname" \
  --from-literal=BETTER_AUTH_SECRET="your-secret-key-here" \
  --from-literal=OPENAI_API_KEY="sk-your-openai-key" \
  -n todo-app
```

**Verify Secrets**:
```bash
kubectl get secrets -n todo-app
```

### Step 9: Deploy Backend with Helm

**Navigate to Helm Charts Directory**:
```bash
cd k8s/helm
```

**Validate Backend Chart**:
```bash
# Lint chart
helm lint todo-backend

# Dry-run deployment
helm install todo-backend ./todo-backend --dry-run --debug -n todo-app
```

**Deploy Backend**:
```bash
helm install todo-backend ./todo-backend -n todo-app
```

**Verify Backend Deployment**:
```bash
# Watch pods come up
kubectl get pods -n todo-app -w

# Check deployment status
kubectl get deployments -n todo-app

# Check HPA
kubectl get hpa -n todo-app

# View logs
kubectl logs -f deployment/todo-backend -n todo-app
```

**Expected Output**:
```
NAME           READY   UP-TO-DATE   AVAILABLE   AGE
todo-backend   1/1     1            1           30s
```

### Step 10: Deploy Frontend with Helm

**Validate Frontend Chart**:
```bash
# Lint chart
helm lint todo-frontend

# Dry-run deployment
helm install todo-frontend ./todo-frontend --dry-run --debug -n todo-app
```

**Deploy Frontend**:
```bash
helm install todo-frontend ./todo-frontend -n todo-app
```

**Verify Frontend Deployment**:
```bash
# Check pods
kubectl get pods -n todo-app

# Check deployment
kubectl get deployments -n todo-app

# View logs
kubectl logs -f deployment/todo-frontend -n todo-app
```

**Expected Output**:
```
NAME            READY   UP-TO-DATE   AVAILABLE   AGE
todo-frontend   2/2     2            2           30s
```

### Step 11: Verify Services

```bash
# List services
kubectl get services -n todo-app

# Check service endpoints
kubectl get endpoints -n todo-app

# Describe services
kubectl describe service todo-frontend -n todo-app
kubectl describe service todo-backend -n todo-app
```

**Expected Output**:
```
NAME            TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
todo-backend    ClusterIP   10.96.xxx.xxx   <none>        8000/TCP   1m
todo-frontend   ClusterIP   10.96.xxx.xxx   <none>        3000/TCP   1m
```

### Step 12: Configure Ingress

**Check Ingress Resource**:
```bash
kubectl get ingress -n todo-app
kubectl describe ingress todo-frontend -n todo-app
```

**Configure Local DNS**:

**macOS/Linux**:
```bash
# Get Minikube IP
MINIKUBE_IP=$(minikube ip)

# Add to /etc/hosts
echo "$MINIKUBE_IP todo.local" | sudo tee -a /etc/hosts

# Verify
ping todo.local
```

**Windows** (run as Administrator):
```powershell
# Get Minikube IP
$MINIKUBE_IP = minikube ip

# Add to hosts file
Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value "$MINIKUBE_IP todo.local"

# Verify
ping todo.local
```

### Step 13: Access Application

**Via Ingress** (recommended):
```bash
# Open in browser
open http://todo.local

# Or use curl
curl http://todo.local
```

**Via Port-Forward** (alternative):
```bash
# Forward frontend port
kubectl port-forward service/todo-frontend 3000:3000 -n todo-app

# Access via localhost
open http://localhost:3000
```

### Step 14: Test Application

**Health Checks**:
```bash
# Frontend health
curl http://todo.local/api/health

# Backend health (via port-forward)
kubectl port-forward service/todo-backend 8000:8000 -n todo-app
curl http://localhost:8000/health
```

**API Endpoints**:
```bash
# List tasks
curl http://todo.local/api/1/tasks

# Create task
curl -X POST http://todo.local/api/1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "completed": false}'
```

**Chat Interface**:
```bash
# Test chat endpoint
curl -X POST http://todo.local/api/1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me my tasks"}'
```

## Using kubectl-ai (Optional)

**Deployment Verification**:
```bash
kubectl-ai "show me all pods in todo-app namespace"
kubectl-ai "are all pods running and healthy?"
kubectl-ai "describe the frontend deployment"
```

**Troubleshooting**:
```bash
kubectl-ai "why is the backend pod failing?"
kubectl-ai "show me the logs of the frontend pod"
kubectl-ai "check connectivity from frontend to backend"
```

**Scaling**:
```bash
kubectl-ai "scale the frontend to 3 replicas"
kubectl-ai "show me the HPA status for backend"
```

## Using Kagent (Optional)

**Cluster Health Analysis**:
```bash
kagent "analyze the cluster health"
kagent "show me resource utilization"
kagent "analyze the todo-app namespace for issues"
```

**Optimization**:
```bash
kagent "optimize resource allocation for todo-app"
kagent "what resources are being wasted?"
kagent "should I scale up or down any deployments?"
```

**Troubleshooting**:
```bash
kagent "why are my pods restarting?"
kagent "diagnose network connectivity issues"
kagent "identify performance bottlenecks"
```

## Monitoring and Debugging

**View Pod Logs**:
```bash
# Frontend logs
kubectl logs -f deployment/todo-frontend -n todo-app

# Backend logs
kubectl logs -f deployment/todo-backend -n todo-app

# All pods
kubectl logs -l app=todo-frontend -n todo-app --tail=100
```

**Check Resource Usage**:
```bash
# Node resources
kubectl top nodes

# Pod resources
kubectl top pods -n todo-app
```

**Describe Resources**:
```bash
kubectl describe pod <pod-name> -n todo-app
kubectl describe deployment todo-backend -n todo-app
kubectl describe hpa todo-backend -n todo-app
```

**Access Kubernetes Dashboard** (optional):
```bash
minikube dashboard
```

## Testing HPA Scaling

**Generate Load**:
```bash
# Run load generator
kubectl run -it --rm load-generator --image=busybox --restart=Never -- /bin/sh -c "while true; do wget -q -O- http://todo-backend:8000/health; done"

# Watch HPA scale
kubectl get hpa -n todo-app -w
```

**Expected Behavior**:
- Backend pods scale up when CPU > 70% or Memory > 80%
- Scaling happens within 30-60 seconds
- Pods scale down after 5 minutes of low utilization

## Updating Deployments

**Update Image Version**:
```bash
# Frontend
helm upgrade todo-frontend ./todo-frontend \
  --set image.tag=v1.1.0 \
  -n todo-app

# Backend
helm upgrade todo-backend ./todo-backend \
  --set image.tag=v1.1.0 \
  -n todo-app
```

**Update Replica Count**:
```bash
helm upgrade todo-frontend ./todo-frontend \
  --set replicaCount=3 \
  -n todo-app
```

**Rollback**:
```bash
# View release history
helm history todo-frontend -n todo-app

# Rollback to previous version
helm rollback todo-frontend 1 -n todo-app
```

## Cleanup

**Uninstall Helm Releases**:
```bash
helm uninstall todo-frontend -n todo-app
helm uninstall todo-backend -n todo-app
```

**Delete Secrets**:
```bash
kubectl delete secret frontend-secrets -n todo-app
kubectl delete secret backend-secrets -n todo-app
```

**Delete Namespace**:
```bash
kubectl delete namespace todo-app
```

**Stop Minikube**:
```bash
# Stop cluster (preserves state)
minikube stop

# Delete cluster (removes all data)
minikube delete
```

**Remove DNS Entry**:
```bash
# macOS/Linux
sudo sed -i '' '/todo.local/d' /etc/hosts

# Windows (run as Administrator)
# Manually edit C:\Windows\System32\drivers\etc\hosts
```

## Troubleshooting

### Pods Not Starting

**Check pod status**:
```bash
kubectl get pods -n todo-app
kubectl describe pod <pod-name> -n todo-app
```

**Common issues**:
- Image pull errors: Verify image exists in registry
- Resource constraints: Check Minikube has sufficient resources
- Secret missing: Verify secrets are created

### Ingress Not Working

**Check ingress controller**:
```bash
kubectl get pods -n ingress-nginx
```

**Verify ingress resource**:
```bash
kubectl describe ingress todo-frontend -n todo-app
```

**Fallback to port-forward**:
```bash
kubectl port-forward service/todo-frontend 3000:3000 -n todo-app
```

### HPA Not Scaling

**Check metrics server**:
```bash
kubectl get deployment metrics-server -n kube-system
kubectl top nodes
kubectl top pods -n todo-app
```

**Enable metrics server**:
```bash
minikube addons enable metrics-server
```

### Database Connection Issues

**Verify secrets**:
```bash
kubectl get secret backend-secrets -n todo-app -o yaml
```

**Check backend logs**:
```bash
kubectl logs -f deployment/todo-backend -n todo-app
```

**Test database connectivity**:
```bash
kubectl exec -it deployment/todo-backend -n todo-app -- /bin/sh
# Inside pod: test database connection
```

## Next Steps

1. **Customize Configuration**: Edit Helm values files for your environment
2. **Set Up CI/CD**: Automate deployment with GitHub Actions or similar
3. **Add Monitoring**: Install Prometheus and Grafana for metrics
4. **Implement Logging**: Set up centralized logging with ELK or Loki
5. **Production Deployment**: Deploy to cloud Kubernetes (DOKS, EKS, GKE)

## Additional Resources

- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [kubectl-ai GitHub](https://github.com/sozercan/kubectl-ai)
- [Kagent Documentation](https://kagent.ai/docs/)

---

**Quickstart Status**: Complete
**Date**: 2026-01-20
**Estimated Completion Time**: 30-45 minutes
