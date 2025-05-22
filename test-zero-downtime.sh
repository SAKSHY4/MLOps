#!/bin/bash

echo "=== Zero Downtime Test Started ==="
echo "Testing endpoint: $1"
echo "Press Ctrl+C to stop"

SUCCESS_COUNT=0
FAILURE_COUNT=0

while true; do
    # Fixed: Get HTTP code separately from response
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$1/health" 2>/dev/null)
    RESPONSE_TIME=$(curl -s -o /dev/null -w "%{time_total}" "$1/health" 2>/dev/null)
    TIMESTAMP=$(date '+%H:%M:%S.%3N')
    
    if [ "$HTTP_CODE" == "200" ]; then
        echo "[$TIMESTAMP] ✅ SUCCESS: HTTP $HTTP_CODE (${RESPONSE_TIME}s)"
        ((SUCCESS_COUNT++))
    else
        echo "[$TIMESTAMP] ❌ FAILURE: HTTP $HTTP_CODE (${RESPONSE_TIME}s)"
        ((FAILURE_COUNT++))
    fi
    
    sleep 0.5  # Test every 500ms
done