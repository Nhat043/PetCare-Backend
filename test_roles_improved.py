#!/usr/bin/env python3
"""
Test script to demonstrate improved result handling
"""

import sys
import os

# Add the vendor directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "vendor"))

from packages.core.database.postgresql import execute_query, execute_query_dict


def compare_old_vs_new():
    """Compare old tuple results vs new dictionary results."""
    print("Comparing Old vs New Result Handling")
    print("=" * 50)

    # Set environment variable
    os.environ["DATABASE_URL"] = (
        "postgresql://postgres.emjhisvkycbxckobfilk:PetCare123456789@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
    )

    try:
        # OLD WAY - Tuple results (confusing!)
        print("\n🔴 OLD WAY - Tuple Results:")
        old_results = execute_query("SELECT role_id, role_name FROM roles")
        print(f"Raw result: {old_results}")

        if old_results:
            first_row = old_results[0]
            print(f"First row: {first_row}")
            print(f"role_id: {first_row[0]}")  # What does [0] mean? Confusing!
            print(f"role_name: {first_row[1]}")  # What does [1] mean? Confusing!

        # NEW WAY - Dictionary results (clear!)
        print("\n🟢 NEW WAY - Dictionary Results:")
        new_results = execute_query_dict("SELECT role_id, role_name FROM roles")
        print(f"Raw result: {new_results}")

        if new_results:
            first_row = new_results[0]
            print(f"First row: {first_row}")
            print(f"role_id: {first_row['role_id']}")  # Clear! We know it's role_id
            print(
                f"role_name: {first_row['role_name']}"
            )  # Clear! We know it's role_name

        print("\n" + "=" * 50)
        print("✅ Dictionary results are much clearer and less error-prone!")

    except Exception as e:
        print(f"❌ Error: {e}")


def demonstrate_usage():
    """Show how to use the improved results."""
    print("\n📖 Usage Examples:")
    print("=" * 30)

    try:
        results = execute_query_dict("SELECT role_id, role_name FROM roles")

        print("Looping through results:")
        for row in results:
            # Much clearer than row[0], row[1]
            print(f"  Role ID: {row['role_id']}, Name: {row['role_name']}")

        print("\nAccessing specific fields:")
        if results:
            first_role = results[0]
            print(f"  First role ID: {first_role['role_id']}")
            print(f"  First role name: {first_role['role_name']}")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    compare_old_vs_new()
    demonstrate_usage()
