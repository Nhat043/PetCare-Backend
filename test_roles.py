#!/usr/bin/env python3
"""
Test script to verify roles query functionality
"""

import sys
import os

# Add the vendor directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "vendor"))

from packages.core.database.postgresql import get_db_connection, execute_query


def test_roles_query():
    """Test querying all roles from the database."""
    print("Testing roles query...")

    try:
        # Get database connection
        db = get_db_connection()

        # Test connection
        if db.test_connection():
            print("✅ Database connection successful!")
        else:
            print("❌ Database connection failed!")
            return

        # Query all roles
        print("\nQuerying all roles...")
        results = execute_query("SELECT * FROM roles")

        if results:
            print(f"✅ Found {len(results)} roles:")
            for row in results:
                role_id, role_name = row
                print(f"  - Role ID: {role_id}, Name: {role_name}")
        else:
            print("ℹ️  No roles found in the database.")

        # Test specific role query
        print("\nTesting specific role query...")
        if results:
            first_role_id = results[0][0]
            specific_result = execute_query(
                "SELECT * FROM roles WHERE role_id = %s", (first_role_id,)
            )
            if specific_result:
                role_id, role_name = specific_result[0]
                print(f"✅ Found role: ID {role_id}, Name: {role_name}")
            else:
                print("❌ Specific role query failed")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


def test_insert_role():
    """Test inserting a new role."""
    print("\n" + "=" * 50)
    print("Testing role insertion...")

    try:
        # Insert a test role
        result = execute_query(
            "INSERT INTO roles (role_name) VALUES (%s) RETURNING *", ("Test Role",)
        )

        if result:
            role_id, role_name = result[0]
            print(f"✅ Successfully inserted role: ID {role_id}, Name: {role_name}")

            # Clean up - delete the test role
            execute_query("DELETE FROM roles WHERE role_id = %s", (role_id,))
            print(f"✅ Cleaned up test role")
        else:
            print("❌ Failed to insert role")

    except Exception as e:
        print(f"❌ Error during insertion test: {e}")


if __name__ == "__main__":
    print("Roles Database Test")
    print("=" * 50)

    test_roles_query()
    test_insert_role()

    print("\n" + "=" * 50)
    print("Test completed!")
