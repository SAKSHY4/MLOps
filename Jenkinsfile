pipeline {
  agent any

  environment {
    VAULT_ADDR = 'http://127.0.0.1:8200' 
    KUBECONFIG = '/var/lib/jenkins/.kube/config'
    DOCKER_HUB_CREDS = credentials('DockerHubCred')
    APP_NAME         = 'mlops-demo'
    IMAGE_NAME       = "sakshya4/${APP_NAME}"
    IMAGE_TAG        = "${env.BUILD_NUMBER}"
    KUBERNETES_SERVER = sh(script: "kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}'", returnStdout: true).trim()
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Retrieve Secrets from Vault') {
      steps {
        script {
          echo "Retrieving all secrets from Vault..."

          withCredentials([string(credentialsId: 'vault-root-token', variable: 'VAULT_TOKEN')]) {
            
              // Get Docker Hub credentials
              def dockerUser = sh(
                script: "VAULT_TOKEN='${VAULT_TOKEN}' /usr/bin/vault kv get -field=username secret/docker-hub",
                returnStdout: true
              ).trim()
              
              def dockerPassword = sh(
                script: "VAULT_TOKEN='${VAULT_TOKEN}' /usr/bin/vault kv get -field=password secret/docker-hub",
                returnStdout: true
              ).trim()
              
              // Get Kubernetes server
              def kubernetesServer = sh(
                script: "VAULT_TOKEN='${VAULT_TOKEN}' /usr/bin/vault kv get -field=server secret/kubernetes",
                returnStdout: true
              ).trim()
            
            env.DOCKER_HUB_USER = dockerUser
            env.DOCKER_HUB_PASSWORD = dockerPassword
            env.VAULT_KUBERNETES_SERVER = kubernetesServer
            
            echo "All secrets retrieved successfully from Vault!"
            echo "   Docker Hub User: ${dockerUser}"
            echo "   Kubernetes Server: ${kubernetesServer}"
            echo "   Docker Hub Password: [HIDDEN]"
          }
        }
      }
    }
    
    stage('Verify Vault Integration') {
      steps {
        script {
          echo "Verifying Vault secrets integration..."

          // Test connectivity using Vault-retrieved credentials
          sh """
            echo "Testing Docker Hub connectivity..."
            echo '${DOCKER_HUB_PASSWORD}' | docker login -u '${DOCKER_HUB_USER}' --password-stdin
            docker logout
            
            echo "Testing Kubernetes connectivity..."
            curl -k ${VAULT_KUBERNETES_SERVER}/healthz || echo "Kubernetes health check"
          """
          
          echo "Vault integrations verified!"
        }
      }
    }

    stage('Verify K8s Configuration') {
      steps {
        echo "Verifying kubectl configuration..."
        sh '''
          echo "Using kubeconfig: ${KUBECONFIG}"
          echo "Kubernetes server from Vault: ${VAULT_KUBERNETES_SERVER}"
          echo "Original server: ${KUBERNETES_SERVER}"
          kubectl config current-context
        '''
      }
    }

    stage('Check K8s Connectivity') {
      steps {
        echo "Using kubeconfig at: ${env.KUBECONFIG}"
        echo "Connecting to Kubernetes server: ${env.KUBERNETES_SERVER}"
        sh 'kubectl get nodes' 
        sh 'kubectl cluster-info'
      }
    }

    stage('Provision Infrastructure') {
      agent any
      steps {
        sh '''
          ansible-galaxy collection install kubernetes.core community.kubernetes
          ansible-playbook -i inventory/hosts.ini deploy-app.yml --tags common,docker,k8s_setup
        '''
      }
    }

    stage('Build Docker Image') {
      steps {
        sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
        sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest"
      }
    }

    stage('Test') {
      agent {
        docker {
          image "${IMAGE_NAME}:${IMAGE_TAG}"
        }
      }
      steps {
        sh 'pytest tests/'
      }
    }

    stage('Push to Docker Hub with Vault Secrets') {
      steps {
        script {
          echo "Pushing to Docker Hub using Vault-managed credentials..."
          echo "   Using Docker Hub user: ${env.DOCKER_HUB_USER}"
          echo "   Using server from Vault: ${env.VAULT_KUBERNETES_SERVER}"
          
          sh """
            echo '${DOCKER_HUB_PASSWORD}' | docker login -u '${DOCKER_HUB_USER}' --password-stdin
            docker push ${IMAGE_NAME}:${IMAGE_TAG}
            docker push ${IMAGE_NAME}:latest
          """
          
          echo "Images pushed successfully using Vault secrets!"
        }
      }
    }

    stage('Deploy Application') {
      agent any
      steps {
        sh '''
          ansible-playbook \
            -i inventory/hosts.ini \
            deploy-app.yml \
            --tags k8s_setup,mlops_app
        '''
      }
    }

    stage('Verify Deployment') {
      steps {
        echo "Verifying Kubernetes deployment..."
        sh '''
          kubectl get pods -l app=mlops-app
          kubectl get svc
          kubectl get hpa
        '''
      }
    }

    stage('Monitor Deployment') {
      steps {
        echo "Checking deployment status..."
        sh '''
          kubectl rollout restart deployment/mlops-demo
          kubectl rollout status deployment/mlops-demo --timeout=300s
          kubectl describe deployment mlops-demo
        '''
      }
    }
  }

  post {
    always {
      echo 'Pipeline completed!'
      sh 'docker logout'
    }
    success {
      echo 'Pipeline succeeded! Application deployed successfully.'
    }
    failure {
      echo 'Pipeline failed! Check logs for details.'
      sh 'kubectl get events --sort-by=.metadata.creationTimestamp'
    }
  }
}