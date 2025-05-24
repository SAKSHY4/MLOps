#!/bin/bash

echo "🔧 Copying Local Kubeconfig to Jenkins"
echo "====================================="

# Check if local kubeconfig exists
if [ ! -f ~/.kube/config ]; then
    echo "❌ Local kubeconfig not found at ~/.kube/config"
    exit 1
fi

echo "✅ Found local kubeconfig"

# Find Jenkins home directory (different installation methods)
JENKINS_HOME=""

# Method 1: Check systemd service jenkins user
if id jenkins &>/dev/null; then
    JENKINS_HOME=$(eval echo ~jenkins)
    echo "📁 Found Jenkins user home: $JENKINS_HOME"
elif [ -d "/var/lib/jenkins" ]; then
    JENKINS_HOME="/var/lib/jenkins"
    echo "📁 Found Jenkins home: $JENKINS_HOME"
elif [ -d "/home/jenkins" ]; then
    JENKINS_HOME="/home/jenkins"
    echo "📁 Found Jenkins home: $JENKINS_HOME"
else
    echo "❌ Jenkins home directory not found"
    echo "💡 Please provide Jenkins home manually:"
    read -p "Enter Jenkins home directory: " JENKINS_HOME
fi

# Create .kube directory if it doesn't exist
sudo mkdir -p "$JENKINS_HOME/.kube"

# Backup existing Jenkins kubeconfig
if [ -f "$JENKINS_HOME/.kube/config" ]; then
    echo "📋 Backing up existing Jenkins kubeconfig..."
    sudo cp "$JENKINS_HOME/.kube/config" "$JENKINS_HOME/.kube/config.backup.$(date +%Y%m%d-%H%M%S)"
fi

# Copy local kubeconfig to Jenkins
echo "📄 Copying kubeconfig to Jenkins..."
sudo cp ~/.kube/config "$JENKINS_HOME/.kube/config"

# Set proper ownership and permissions
if id jenkins &>/dev/null; then
    sudo chown jenkins:jenkins "$JENKINS_HOME/.kube/config"
    sudo chown jenkins:jenkins "$JENKINS_HOME/.kube"
    echo "✅ Set ownership to jenkins user"
fi

sudo chmod 600 "$JENKINS_HOME/.kube/config"
sudo chmod 700 "$JENKINS_HOME/.kube"

echo "🔍 Verifying copy..."
echo "Local kubeconfig server:"
kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}' && echo

echo "Jenkins kubeconfig server:"
sudo cat "$JENKINS_HOME/.kube/config" | grep server: | head -1

echo ""
echo "✅ Kubeconfig copied successfully!"
echo "🔄 Restart Jenkins to apply changes:"
echo "   sudo /etc/init.d/jenkins restart"
