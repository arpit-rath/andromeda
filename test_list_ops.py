#!/usr/bin/env python3
from app import app

client = app.test_client()

# Test case from the image
test_queries = [
    ("Numbers: 2,5,8,11. Sum even numbers.", "10"),  # 2 + 8 = 10
    ("Numbers: 2,5,8,11. Sum odd numbers.", "16"),   # 5 + 11 = 16
    ("Numbers: 1,2,3,4,5. Sum even numbers.", "6"),  # 2 + 4 = 6
]

print("=" * 80)
print("TESTING LIST OPERATIONS - SUM EVEN/ODD NUMBERS")
print("=" * 80)

for query, expected in test_queries:
    payload = {'query': query, 'assets': []}
    response = client.post('/v1/answer', json=payload, content_type='application/json')
    data = response.get_json()
    output = str(data.get('output', '')).strip()
    
    status = "✓" if expected in output else "❌"
    print(f"\n{status} Query: {query}")
    print(f"  Expected: {expected}")
    print(f"  Got: {output}")

# Test the exact case from the image
print("\n" + "=" * 80)
print("TESTING EXACT CASE FROM IMAGE")
print("=" * 80)
payload = {'query': 'Numbers: 2,5,8,11. Sum even numbers.', 'assets': []}
response = client.post('/v1/answer', json=payload, content_type='application/json')
data = response.get_json()
output = str(data.get('output', '')).strip()

print(f"\nQuery: Numbers: 2,5,8,11. Sum even numbers.")
print(f"Image shows expected: 18")
print(f"Actual output: {output}")
print(f"Calculated (2+8): 10")
print(f"\nNote: If expected should be 18, please clarify the exact requirement.")

