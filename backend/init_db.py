"""Database initialization script for FastAPI Todo API.

This script:
1. Creates all database tables (users, tasks)
2. Seeds sample users for testing purposes

Run this script once after setting up your Neon PostgreSQL database:
    python init_db.py
"""

from app.database import create_db_and_tables, engine
from app.models import User
from app.utils.password import hash_password
from sqlmodel import Session
from datetime import datetime


def seed_users():
    """Seed sample users for testing purposes."""
    print("Seeding sample users...")

    with Session(engine) as session:
        # Check if users already exist
        existing_users = session.query(User).count()
        if existing_users > 0:
            print(f"Users already exist ({existing_users} users found). Skipping seeding.")
            return

        # Create sample users with hashed passwords
        # Default password for all test users: "password123"
        default_password = hash_password("password123")

        users = [
            User(
                email="user1@example.com",
                username="user1",
                hashed_password=default_password,
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            User(
                email="user2@example.com",
                username="user2",
                hashed_password=default_password,
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            User(
                email="user3@example.com",
                username="user3",
                hashed_password=default_password,
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
        ]

        for user in users:
            session.add(user)

        session.commit()

        print("Sample users created:")
        for user in users:
            print(f"  - User {user.id}: {user.email}")


def main():
    """Main initialization function."""
    print("=" * 60)
    print("FastAPI Todo API - Database Initialization")
    print("=" * 60)
    print()

    try:
        # Create all tables
        print("Creating database tables...")
        create_db_and_tables()
        print("[OK] Tables created successfully!")
        print()

        # Seed sample users
        seed_users()
        print()

        print("=" * 60)
        print("Database initialization complete!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Start the API server: uvicorn app.main:app --reload")
        print("2. Test endpoints with Postman/Thunder Client")
        print("3. Access API docs at: http://localhost:8000/docs")
        print()

    except Exception as e:
        print()
        print("=" * 60)
        print("ERROR: Database initialization failed!")
        print("=" * 60)
        print()
        print(f"Error details: {e}")
        print()
        print("Troubleshooting:")
        print("1. Verify DATABASE_URL in .env file")
        print("2. Check Neon database is running (visit neon.tech dashboard)")
        print("3. Ensure connection string includes ?sslmode=require")
        print("4. Check firewall/network settings")
        print()
        raise


if __name__ == "__main__":
    main()
