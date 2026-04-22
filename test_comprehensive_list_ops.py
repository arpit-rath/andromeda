#!/usr/bin/env python3
"""
Comprehensive test suite for list operations.
Tests sum of even/odd numbers, filtering, and other list operations.
"""

import json
import sys
from app import app

def run_comprehensive_tests():
    """Run comprehensive test suite with various list operations."""
    
    test_cases = [
        # (query, expected_answer, category)
        # ─── Sum Even Numbers ───
        ("Numbers: 2,5,8,11. Sum even numbers.", "10", "sum_even"),
        ("Sum the even numbers from: 1,2,3,4,5,6.", "12", "sum_even"),
        ("Add up all even numbers: 10,15,20,25,30.", "60", "sum_even"),
        ("What is the sum of even numbers? 2,4,6,8", "20", "sum_even"),
        ("Find the sum of even values: 3,6,9,12,15,18.", "36", "sum_even"),
        ("Sum of even numbers in: 1,3,5,7,9,10.", "10", "sum_even"),
        
        # ─── Sum Odd Numbers ───
        ("Numbers: 2,5,8,11. Sum odd numbers.", "16", "sum_odd"),
        ("Sum the odd numbers from: 1,2,3,4,5,6.", "9", "sum_odd"),
        ("Add up all odd numbers: 10,15,20,25,30.", "40", "sum_odd"),
        ("What is the sum of odd numbers? 2,4,6,8,9,11.", "20", "sum_odd"),
        ("Find the sum of odd values: 1,3,5,7,9,11.", "36", "sum_odd"),
        ("Sum of odd numbers in: 2,4,6,8,10,15.", "15", "sum_odd"),
        
        # ─── Sum All Numbers ───
        ("Sum these numbers: 5,10,15,20.", "50", "sum_all"),
        ("What is the total of: 1,2,3,4,5.", "15", "sum_all"),
        ("Find the sum: 100,200,300.", "600", "sum_all"),
        
        # ─── Count Operations ───
        ("How many numbers are there? 1,2,3,4,5.", "5", "count"),
        ("Count the items in: 10,20,30,40.", "4", "count"),
        
        # ─── Max/Min Operations ───
        ("Find the maximum from: 5,2,8,1,9.", "9", "max"),
        ("Find the largest number in: 50,100,75,25.", "100", "max"),
        ("Find the minimum from: 5,2,8,1,9.", "1", "min"),
        ("Find the smallest number in: 50,100,75,25.", "25", "min"),
        
        # ─── Average ───
        ("Find the average of: 2,4,6,8.", "5", "average"),
        ("What is the mean of: 10,20,30.", "20", "average"),
        
        # ─── Reverse ───
        ("Reverse the list: 1,2,3,4,5.", "5,4,3,2,1", "reverse"),
        
        # ─── Sort ───
        ("Sort these numbers: 5,2,8,1,9.", "1,2,5,8,9", "sort"),
        
        # ─── Product of numbers ───
        ("Product of: 2,3,4.", "24", "product"),
    ]
    
    client = app.test_client()
    
    results = {
        "total": len(test_cases),
        "passed": 0,
        "failed": 0,
        "by_category": {},
        "failures": []
    }
    
    print("=" * 90)
    print("COMPREHENSIVE LIST OPERATIONS TEST SUITE")
    print("=" * 90)
    
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
        
        # Check if output contains expected answer (case-insensitive, handle period)
        is_correct = expected.lower() in output.lower().replace(".", "").strip()
        
        if is_correct:
            print(f"✓ [{category.upper()}] {query}")
            print(f"  → {output}")
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
    print("\n" + "=" * 90)
    print("TEST SUMMARY")
    print("=" * 90)
    print(f"Total Tests: {results['total']}")
    print(f"Passed: {results['passed']} ✓")
    print(f"Failed: {results['failed']} ❌")
    accuracy = (results['passed'] / results['total'] * 100) if results['total'] > 0 else 0
    print(f"Overall Accuracy: {accuracy:.1f}%")
    
    print("\n" + "-" * 90)
    print("ACCURACY BY CATEGORY")
    print("-" * 90)
    for category in sorted(results["by_category"].keys()):
        cat_data = results["by_category"][category]
        total_cat = cat_data["passed"] + cat_data["failed"]
        cat_accuracy = (cat_data["passed"] / total_cat * 100) if total_cat > 0 else 0
        status = "✓" if cat_accuracy == 100.0 else "⚠"
        print(f"{status} {category.upper():20} {cat_data['passed']:2}/{total_cat:2}  ({cat_accuracy:5.1f}%)")
    
    if results["failures"]:
        print("\n" + "-" * 90)
        print("FAILURES")
        print("-" * 90)
        for failure in results["failures"]:
            print(f"\n❌ Query: {failure['query']}")
            print(f"   Category: {failure['category']}")
            print(f"   Expected: {failure['expected']}")
            print(f"   Got: {failure['got']}")
    
    print("\n" + "=" * 90)
    return results

if __name__ == "__main__":
    results = run_comprehensive_tests()
    sys.exit(0 if results["failed"] == 0 else 1)
