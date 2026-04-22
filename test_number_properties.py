#!/usr/bin/env python3
"""
Local testing suite for number property questions.
Tests odd/even, prime, divisibility, positive/negative questions.
"""

import json
import sys

# Import the Flask app
from app import app

def run_test_cases():
    """Run test cases and calculate accuracy."""
    
    test_cases = [
        # (query, expected_answer, category)
        ("Is 9 an odd number?", "YES", "odd"),
        ("Is 8 an odd number?", "NO", "odd"),
        ("Is 15 odd?", "YES", "odd"),
        ("Is 2 odd?", "NO", "odd"),
        ("Is 101 an odd number?", "YES", "odd"),
        
        ("Is 8 an even number?", "YES", "even"),
        ("Is 9 an even number?", "NO", "even"),
        ("Is 24 even?", "YES", "even"),
        ("Is 77 even?", "NO", "even"),
        ("Is 100 an even number?", "YES", "even"),
        
        ("Is 7 prime?", "YES", "prime"),
        ("Is 11 a prime number?", "YES", "prime"),
        ("Is 13 prime?", "YES", "prime"),
        ("Is 17 prime?", "YES", "prime"),
        ("Is 4 prime?", "NO", "prime"),
        ("Is 9 prime?", "NO", "prime"),
        ("Is 15 prime?", "NO", "prime"),
        ("Is 1 prime?", "NO", "prime"),
        
        ("Is 5 positive?", "YES", "positive"),
        ("Is 100 positive?", "YES", "positive"),
        ("Is -5 positive?", "NO", "positive"),
        ("Is -100 positive?", "NO", "positive"),
        ("Is 0 positive?", "NO", "positive"),
        
        ("Is -5 negative?", "YES", "negative"),
        ("Is -100 negative?", "YES", "negative"),
        ("Is 5 negative?", "NO", "negative"),
        ("Is 0 negative?", "NO", "negative"),
        
        ("Is 0 zero?", "YES", "zero"),
        ("Is 5 zero?", "NO", "zero"),
        ("Is -5 zero?", "NO", "zero"),
        
        ("Is 12 divisible by 3?", "YES", "divisibility"),
        ("Is 15 divisible by 5?", "YES", "divisibility"),
        ("Is 20 divisible by 4?", "YES", "divisibility"),
        ("Is 10 divisible by 2?", "YES", "divisibility"),
        ("Is 13 divisible by 5?", "NO", "divisibility"),
        ("Is 7 divisible by 2?", "NO", "divisibility"),
        ("Is 100 divisible by 7?", "NO", "divisibility"),
        ("Is 50 divisible by 10?", "YES", "divisibility"),
    ]
    
    # Create Flask test client
    client = app.test_client()
    
    results = {
        "total": len(test_cases),
        "passed": 0,
        "failed": 0,
        "by_category": {},
        "failures": []
    }
    
    print("=" * 80)
    print("TESTING NUMBER PROPERTY QUESTIONS")
    print("=" * 80)
    
    for query, expected, category in test_cases:
        payload = {
            "query": query,
            "assets": []
        }
        
        response = client.post(
            "/v1/answer",
            json=payload,
            content_type="application/json"
        )
        
        if response.status_code != 200:
            print(f"❌ [{category.upper()}] {query}")
            print(f"   HTTP Error: {response.status_code}")
            results["failed"] += 1
            results["failures"].append({
                "query": query,
                "expected": expected,
                "got": f"HTTP {response.status_code}",
                "category": category
            })
            if category not in results["by_category"]:
                results["by_category"][category] = {"passed": 0, "failed": 0}
            results["by_category"][category]["failed"] += 1
            continue
        
        try:
            data = response.get_json()
            output = str(data.get("output", "")).strip()
        except Exception as e:
            print(f"❌ [{category.upper()}] {query}")
            print(f"   Parse Error: {e}")
            results["failed"] += 1
            results["failures"].append({
                "query": query,
                "expected": expected,
                "got": str(e),
                "category": category
            })
            if category not in results["by_category"]:
                results["by_category"][category] = {"passed": 0, "failed": 0}
            results["by_category"][category]["failed"] += 1
            continue
        
        # Check if output contains expected answer (case-insensitive)
        is_correct = expected.upper() in output.upper()
        
        if is_correct:
            print(f"✓ [{category.upper()}] {query}")
            print(f"  → Output: {output}")
            results["passed"] += 1
        else:
            print(f"❌ [{category.upper()}] {query}")
            print(f"  Expected: {expected}")
            print(f"  Got: {output}")
            results["failed"] += 1
            results["failures"].append({
                "query": query,
                "expected": expected,
                "got": output,
                "category": category
            })
        
        # Track by category
        if category not in results["by_category"]:
            results["by_category"][category] = {"passed": 0, "failed": 0}
        
        if is_correct:
            results["by_category"][category]["passed"] += 1
        else:
            results["by_category"][category]["failed"] += 1
    
    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {results['total']}")
    print(f"Passed: {results['passed']} ✓")
    print(f"Failed: {results['failed']} ❌")
    accuracy = (results['passed'] / results['total'] * 100) if results['total'] > 0 else 0
    print(f"Overall Accuracy: {accuracy:.1f}%")
    
    print("\n" + "-" * 80)
    print("ACCURACY BY CATEGORY")
    print("-" * 80)
    for category in sorted(results["by_category"].keys()):
        cat_data = results["by_category"][category]
        total_cat = cat_data["passed"] + cat_data["failed"]
        cat_accuracy = (cat_data["passed"] / total_cat * 100) if total_cat > 0 else 0
        print(f"{category.upper():15} {cat_data['passed']:2}/{total_cat:2}  ({cat_accuracy:5.1f}%)")
    
    if results["failures"]:
        print("\n" + "-" * 80)
        print("FAILURES")
        print("-" * 80)
        for failure in results["failures"]:
            print(f"Query: {failure['query']}")
            print(f"  Expected: {failure['expected']}")
            print(f"  Got: {failure['got']}")
            print()
    
    return results

if __name__ == "__main__":
    results = run_test_cases()
    sys.exit(0 if results["failed"] == 0 else 1)
