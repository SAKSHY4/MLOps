#!/bin/bash

echo "🚀 Complete MLOps Project Startup Verification"
echo "=============================================="

echo "1. Docker Desktop:"
docker --version

echo -e "\n2. Minikube Cluster:"
kubectl get nodes

echo -e "\n3. ELK Stack (External):"
docker-compose -f elk-docker-compose.yml ps

echo -e "\n4. Jenkins:"
curl -s -o /dev/null -w "%{http_code}" http://localhost:8080
echo " - Jenkins HTTP Status"


export VAULT_TOKEN='hvs.EmgA3FiBLZ72bLiDleC7TgM8'
export VAULT_ADDR='http://127.0.0.1:8200'

echo -e "\n5. Vault:"
vault status | head -3

echo -e "\n5.5. Ensuring metrics-server is available..."
minikube addons enable metrics-server
kubectl wait --for=condition=ready pod -l k8s-app=metrics-server -n kube-system --timeout=120s

echo -e "\n6. MLOps Application:"
kubectl get pods -l app=mlops-demo

echo -e "\n7. HPA Status:"
kubectl get hpa mlops-demo-hpa

echo -e "\n8. Monitoring Stack:"
kubectl get pods -n kube-system -l k8s-app=filebeat
kubectl get pods -n kube-system -l k8s-app=metricbeat

echo -e "\n9. ELK Integration:"
curl -s "http://localhost:9200/_cat/indices?v" | grep -E "(filebeat|metricbeat)" | wc -l
echo " indices found"

echo -e "\n10. Service URL:"
minikube service mlops-demo --url

echo -e "\n✅ Startup Verification Complete!"
echo "📊 Access Points:"
echo "   - Jenkins: http://localhost:8080"
echo "   - Kibana: http://localhost:5601"
echo "   - Elasticsearch: http://localhost:9200"
echo "   - MLOps App: $(minikube service mlops-demo --url)"
