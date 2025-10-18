#!/usr/bin/env python3
"""
Safety Results Checker for GitHub Actions
Fails the build if critical vulnerabilities are found
"""

import json
import sys

def check_safety_results():
    try:
        with open('safety-results.json', 'r') as f:
            data = json.load(f)
        
        critical_vulns = 0
        high_vulns = 0
        medium_vulns = 0
        
        for vuln in data.get('vulnerabilities', []):
            cvss_score = vuln.get('cvssv3', {}).get('baseScore', 0)
            if cvss_score >= 9.0:
                critical_vulns += 1
            elif cvss_score >= 7.0:
                high_vulns += 1
            elif cvss_score >= 4.0:
                medium_vulns += 1
        
        print(f"📊 Safety Scan Results:")
        print(f"   Critical Vulnerabilities: {critical_vulns}")
        print(f"   High Vulnerabilities: {high_vulns}")
        print(f"   Medium Vulnerabilities: {medium_vulns}")
        
        # Fail if critical vulnerabilities found
        if critical_vulns > 0:
            print("❌ Build failed: Critical vulnerabilities detected!")
            sys.exit(1)
        elif high_vulns > 0:
            print("⚠️  High vulnerabilities found. Update recommended.")
        else:
            print("✅ No critical vulnerabilities found.")
            
    except FileNotFoundError:
        print("❌ Safety results file not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print("❌ Error parsing Safety results")
        sys.exit(1)

if __name__ == "__main__":
    check_safety_results()