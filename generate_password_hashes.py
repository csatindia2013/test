#!/usr/bin/env python3
"""
Password Hash Generator for EasyBill Admin Dashboard
Run this script to generate secure password hashes for your environment variables.
"""

from werkzeug.security import generate_password_hash
import os

def generate_password_hashes():
    print("=== EasyBill Admin Dashboard - Password Hash Generator ===\n")
    
    # Get passwords from user input
    admin_password = input("Enter admin password (default: admin123): ").strip() or "admin123"
    user1_password = input("Enter user1 password (default: user123): ").strip() or "user123"
    
    # Generate hashes
    admin_hash = generate_password_hash(admin_password)
    user1_hash = generate_password_hash(user1_password)
    
    print("\n=== Environment Variables for Render/Production ===")
    print(f"ADMIN_USERNAME=admin")
    print(f"ADMIN_PASSWORD_HASH={admin_hash}")
    print(f"USER1_USERNAME=user1")
    print(f"USER1_PASSWORD_HASH={user1_hash}")
    
    print("\n=== Environment Variables for Local Development ===")
    print(f"set ADMIN_USERNAME=admin")
    print(f"set ADMIN_PASSWORD_HASH={admin_hash}")
    print(f"set USER1_USERNAME=user1")
    print(f"set USER1_PASSWORD_HASH={user1_hash}")
    
    print("\n=== For Linux/Mac ===")
    print(f"export ADMIN_USERNAME=admin")
    print(f"export ADMIN_PASSWORD_HASH={admin_hash}")
    print(f"export USER1_USERNAME=user1")
    print(f"export USER1_PASSWORD_HASH={user1_hash}")
    
    print("\n=== Security Notes ===")
    print("✅ Passwords are now hashed using Werkzeug's secure hashing")
    print("✅ Default passwords are: admin123 and user123")
    print("✅ Change these passwords in production!")
    print("✅ Store these environment variables securely")
    
    # Save to .env file for local development
    env_content = f"""# EasyBill Admin Dashboard Environment Variables
# Generated on {os.popen('date').read().strip()}

ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH={admin_hash}
USER1_USERNAME=user1
USER1_PASSWORD_HASH={user1_hash}

# Firebase Configuration (add your Firebase credentials here)
# FIREBASE_PROJECT_ID=your-project-id
# FIREBASE_PRIVATE_KEY_ID=your-private-key-id
# FIREBASE_PRIVATE_KEY="your-private-key"
# FIREBASE_CLIENT_EMAIL=your-client-email
# FIREBASE_CLIENT_ID=your-client-id
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print(f"\n✅ Environment variables saved to .env file")
    print("📝 Add .env to your .gitignore to keep credentials secure!")

if __name__ == "__main__":
    generate_password_hashes()
