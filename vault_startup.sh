#!/bin/bash

echo "🔐 Starting Persistent Vault After Restart"
echo "=========================================="

# Start vault server
echo "1. Starting Vault server..."
/usr/bin/vault server -config=vault-persistent.hcl &
VAULT_PID=$!

# Wait for startup
sleep 5

# Set environment
export VAULT_ADDR='http://127.0.0.1:8200'

# Check if sealed
echo "2. Checking Vault status..."
if /usr/bin/vault status | grep -q "Sealed.*true"; then
    echo "3. Unsealing Vault..."
    /usr/bin/vault operator unseal jQAeeDwG3oD3xq+B4Tg6CgKSUItUKZySTT7KgHuAGQA=
    echo "✅ Vault unsealed successfully!"
else
    echo "✅ Vault already unsealed"
fi

# Verify secrets are accessible
echo "4. Verifying secrets..."
export VAULT_TOKEN='hvs.EmgA3FiBLZ72bLiDleC7TgM8'
/usr/bin/vault kv list secret/ 2>/dev/null && echo "✅ Secrets accessible" || echo "⚠️  Secrets not accessible"

echo ""
echo "🎉 Vault ready for Jenkins!"
echo "📋 Process ID: $VAULT_PID"
echo "🛑 To stop: kill $VAULT_PID"

# chmod +x startup-vault.sh