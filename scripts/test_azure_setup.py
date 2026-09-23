#!/usr/bin/env python3
"""
Test Azure Setup - Verify your configuration works
Run: python test_azure_setup.py
"""

import os
import sys
import subprocess
from pathlib import Path

# Try to load .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("WARNING: python-dotenv not installed. Run: pip install python-dotenv")
    print("Continuing without .env loading...")


def test_azure_cli_login():
    """Verify Azure CLI is logged in (optional if using API key)"""
    print("\n[1] Testing Azure CLI Login...")
    try:
        result = subprocess.run(
            ["az", "account", "show", "--output", "json"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            import json
            account = json.loads(result.stdout)
            user = account.get("user", {}).get("name", "Unknown")
            subscription = account.get("name", "Unknown")
            print(f"   OK: Azure CLI login verified")
            print(f"      User: {user}")
            print(f"      Subscription: {subscription}")
            return True
        else:
            print(f"   SKIP: Azure CLI not logged in (OK if using API key)")
            return True

    except FileNotFoundError:
        print(f"   SKIP: Azure CLI not in PATH (OK if using API key from .env)")
        return True
    except subprocess.TimeoutExpired:
        print(f"   SKIP: Azure CLI command timed out (OK if using API key)")
        return True
    except Exception as e:
        print(f"   SKIP: Could not verify CLI (OK if using API key)")
        return True


def test_foundry_connection():
    """Test connection to AI Foundry (Azure OpenAI)"""
    print("\n[2] Testing AI Foundry Connection...")

    try:
        from openai import AzureOpenAI

        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-5.4-mini")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2025-04-01-preview")

        if not endpoint:
            print(f"   ERROR: AZURE_OPENAI_ENDPOINT not set in .env")
            return False

        print(f"   Endpoint: {endpoint}")
        print(f"   Deployment: {deployment}")

        # Create client (will use Azure CLI auth if no API key)
        client = AzureOpenAI(
            api_version=api_version,
            azure_endpoint=endpoint,
            api_key=api_key if api_key else None,
        )

        # Simple test call
        print(f"   Calling LLM...")
        response = client.chat.completions.create(
            model=deployment,
            messages=[{"role": "user", "content": "Say: WORKING"}],
            max_completion_tokens=10,
            temperature=0
        )

        content = response.choices[0].message.content
        print(f"   OK: AI Foundry connection verified")
        print(f"      LLM responded: {content}")
        return True

    except ModuleNotFoundError:
        print(f"   ERROR: OpenAI SDK not installed")
        print(f"      Fix: Run 'pip install openai'")
        return False
    except Exception as e:
        print(f"   ERROR: AI Foundry connection failed")
        print(f"      Details: {str(e)}")
        if "Unauthorized" in str(e) or "401" in str(e):
            print(f"      Fix: Check your API key or run 'az login'")
        return False


def test_env_file():
    """Verify .env file exists and is configured"""
    print("\n[0] Checking .env File...")

    env_path = Path(".env")

    if not env_path.exists():
        print(f"   ERROR: .env file not found")
        print(f"      Fix: Run 'cp .env.example .env' and fill in your values")
        return False

    # Check for required keys
    required_keys = [
        "AZURE_SUBSCRIPTION_ID",
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_VERSION",
    ]

    with open(env_path, encoding='utf-8') as f:
        env_content = f.read()

    missing_keys = [k for k in required_keys if k not in env_content]

    if missing_keys:
        print(f"   ERROR: Missing keys in .env: {', '.join(missing_keys)}")
        return False

    print(f"   OK: .env file found and configured")
    return True


def main():
    print("=" * 70)
    print("AZURE SETUP VERIFICATION")
    print("=" * 70)

    tests = [
        ("Environment File", test_env_file),
        ("Azure CLI Login", test_azure_cli_login),
        ("AI Foundry Connection", test_foundry_connection),
    ]

    results = []
    for name, test_fn in tests:
        try:
            result = test_fn()
            results.append((name, result))
        except KeyboardInterrupt:
            print(f"\nInterrupted by user")
            return 1
        except Exception as e:
            print(f"   ERROR: Unexpected error: {str(e)}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    for name, result in results:
        status = "OK" if result else "FAIL"
        print(f"[{status}] {name}")

    # Check if critical tests passed
    critical_tests = results[:2]  # .env and Azure CLI
    all_critical_ok = all(r for _, r in critical_tests)

    print("\n" + "=" * 70)
    if all_critical_ok and results[2][1]:
        print("SUCCESS: ALL TESTS PASSED - Ready to code!")
        return 0
    elif all_critical_ok:
        print("PARTIAL: Critical tests passed but LLM connection failed")
        print("         Check your credentials or network")
        return 1
    else:
        print("FAILURE: Some critical tests failed")
        print("         Fix the errors above before proceeding")
        return 1


if __name__ == "__main__":
    sys.exit(main())
