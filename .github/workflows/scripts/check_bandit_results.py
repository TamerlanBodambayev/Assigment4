#!/usr/bin/env python3
"""
Bandit Results Checker for GitHub Actions
Fails the build if high severity issues are found
"""

import json
import sys
import os

def check_bandit_results():
    try:
        with open('bandit-results.json', 'r') as f:
            data = json.load(f)
        
        # Count issues by severity
        high_issues = 0
        medium_issues = 0
        low_issues = 0
        
        for result in data.get('results', []):
            severity = result.get('issue_severity', '').lower()
            if severity == 'high':
                high_issues += 1
            elif severity == 'medium':
                medium_issues += 1
            elif severity == 'low':
                low_issues += 1
        
        print(f"📊 Bandit Scan Results:")
        print(f"   High Severity Issues: {high_issues}")
        print(f"   Medium Severity Issues: {medium_issues}")
        print(f"   Low Severity Issues: {low_issues}")
        
        # Fail if high severity issues found
        if high_issues > 0:
            print("❌ Build failed: High severity security issues detected!")
            sys.exit(1)
        elif medium_issues > 0:
            print("⚠️  Medium severity issues found. Review recommended.")
        else:
            print("✅ No high severity issues found.")
            
    except FileNotFoundError:
        print("❌ Bandit results file not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print("❌ Error parsing Bandit results")
        sys.exit(1)

if __name__ == "__main__":
    check_bandit_results()