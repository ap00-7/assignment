#!/usr/bin/env python
"""End-to-end test for AI chat log transaction."""
import sys
sys.path.insert(0, '.')

from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

# Test the AI chat endpoint
prompt = "today i met with HCP Dr. Sarah. we discussed product X efficacy. The doctor responded positively. Please log this interaction"
print(f"Test prompt: {prompt}\n")

try:
    resp = client.post('/ai/chat', json={'prompt': prompt, 'force_log': True})
    
    print(f"Status: {resp.status_code}")
    
    if resp.status_code != 200:
        print(f"ERROR Response: {resp.text}")
        sys.exit(1)
    
    data = resp.json()
    print(f"Response keys: {list(data.keys())}")
    print(f"Tool: {data.get('tool')}")
    print(f"Has interaction: {'interaction' in data and data['interaction'] is not None}")
    
    if data.get('interaction'):
        print("\nInteraction created:")
        for key in ['id', 'hcp_name', 'topics', 'sentiment', 'outcomes', 'follow_up', 'ai_summary']:
            print(f"  {key}: {data['interaction'].get(key)}")
    else:
        print("\nWARNING: No interaction in response!")
        print(f"Full response:\n{json.dumps(data, indent=2)}")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
