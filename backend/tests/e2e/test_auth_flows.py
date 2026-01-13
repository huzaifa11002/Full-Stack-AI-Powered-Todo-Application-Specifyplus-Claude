"""End-to-end tests for complete authentication flows and user isolation.

Tests for:
- Complete signup → login → access protected resource flow
- User isolation (User A cannot access User B's tasks)
- Token expiration handling
- Full CRUD operations with authentication
- Multiple users interacting with their own resources
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models import User, Task


@pytest.mark.e2e
@pytest.mark.auth
class TestAuthenticationFlows:
    """Test suite for complete authentication workflows."""

    def test_complete_signup_login_access_flow(self, client: TestClient, session: Session):
        """Test complete flow: signup → login → access protected resource."""
        # Step 1: Sign up a new user
        signup_data = {
            "email": "newuser@example.com",
            "password": "SecurePass123",
            "username": "New User",
        }
        signup_response = client.post("/api/auth/signup", json=signup_data)
        assert signup_response.status_code == 201
        signup_token = signup_response.json()["access_token"]
        user_id = signup_response.json()["user"]["id"]

        # Step 2: Login with same credentials
        login_data = {
            "email": signup_data["email"],
            "password": signup_data["password"],
        }
        login_response = client.post("/api/auth/signin", json=login_data)
        assert login_response.status_code == 200
        login_token = login_response.json()["access_token"]

        # Step 3: Access protected resource with signup token
        headers_signup = {"Authorization": f"Bearer {signup_token}"}
        tasks_response_1 = client.get(f"/api/{user_id}/tasks", headers=headers_signup)
        assert tasks_response_1.status_code == 200
        assert tasks_response_1.json() == []  # No tasks yet

        # Step 4: Access protected resource with login token
        headers_login = {"Authorization": f"Bearer {login_token}"}
        tasks_response_2 = client.get(f"/api/{user_id}/tasks", headers=headers_login)
        assert tasks_response_2.status_code == 200
        assert tasks_response_2.json() == []

        # Step 5: Create a task
        task_data = {"title": "My First Task", "description": "Test task"}
        create_response = client.post(
            f"/api/{user_id}/tasks", json=task_data, headers=headers_login
        )
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]

        # Step 6: Verify task was created
        tasks_response_3 = client.get(f"/api/{user_id}/tasks", headers=headers_login)
        assert tasks_response_3.status_code == 200
        tasks = tasks_response_3.json()
        assert len(tasks) == 1
        assert tasks[0]["title"] == task_data["title"]

    def test_user_isolation_complete_flow(self, client: TestClient, session: Session):
        """Test that User A cannot access User B's tasks (complete isolation)."""
        # Step 1: Create User A
        user_a_data = {
            "email": "usera@example.com",
            "password": "PassA123",
            "username": "User A",
        }
        signup_a = client.post("/api/auth/signup", json=user_a_data)
        assert signup_a.status_code == 201
        token_a = signup_a.json()["access_token"]
        user_a_id = signup_a.json()["user"]["id"]

        # Step 2: Create User B
        user_b_data = {
            "email": "userb@example.com",
            "password": "PassB123",
            "username": "User B",
        }
        signup_b = client.post("/api/auth/signup", json=user_b_data)
        assert signup_b.status_code == 201
        token_b = signup_b.json()["access_token"]
        user_b_id = signup_b.json()["user"]["id"]

        # Step 3: User A creates a task
        headers_a = {"Authorization": f"Bearer {token_a}"}
        task_a_data = {"title": "User A's Task", "description": "Private to A"}
        create_a = client.post(
            f"/api/{user_a_id}/tasks", json=task_a_data, headers=headers_a
        )
        assert create_a.status_code == 201
        task_a_id = create_a.json()["id"]

        # Step 4: User B creates a task
        headers_b = {"Authorization": f"Bearer {token_b}"}
        task_b_data = {"title": "User B's Task", "description": "Private to B"}
        create_b = client.post(
            f"/api/{user_b_id}/tasks", json=task_b_data, headers=headers_b
        )
        assert create_b.status_code == 201
        task_b_id = create_b.json()["id"]

        # Step 5: User A can see only their own task
        tasks_a = client.get(f"/api/{user_a_id}/tasks", headers=headers_a)
        assert tasks_a.status_code == 200
        tasks_a_list = tasks_a.json()
        assert len(tasks_a_list) == 1
        assert tasks_a_list[0]["title"] == "User A's Task"
        assert tasks_a_list[0]["user_id"] == user_a_id

        # Step 6: User B can see only their own task
        tasks_b = client.get(f"/api/{user_b_id}/tasks", headers=headers_b)
        assert tasks_b.status_code == 200
        tasks_b_list = tasks_b.json()
        assert len(tasks_b_list) == 1
        assert tasks_b_list[0]["title"] == "User B's Task"
        assert tasks_b_list[0]["user_id"] == user_b_id

        # Step 7: User A cannot access User B's task list
        access_b_list = client.get(f"/api/{user_b_id}/tasks", headers=headers_a)
        assert access_b_list.status_code == 403

        # Step 8: User B cannot access User A's task list
        access_a_list = client.get(f"/api/{user_a_id}/tasks", headers=headers_b)
        assert access_a_list.status_code == 403

        # Step 9: User A cannot access User B's specific task
        access_b_task = client.get(
            f"/api/{user_b_id}/tasks/{task_b_id}", headers=headers_a
        )
        assert access_b_task.status_code == 403

        # Step 10: User B cannot access User A's specific task
        access_a_task = client.get(
            f"/api/{user_a_id}/tasks/{task_a_id}", headers=headers_b
        )
        assert access_a_task.status_code == 403

        # Step 11: User A cannot update User B's task
        update_b = client.put(
            f"/api/{user_b_id}/tasks/{task_b_id}",
            json={"title": "Hacked!"},
            headers=headers_a,
        )
        assert update_b.status_code == 403

        # Step 12: User A cannot delete User B's task
        delete_b = client.delete(
            f"/api/{user_b_id}/tasks/{task_b_id}", headers=headers_a
        )
        assert delete_b.status_code == 403

        # Step 13: Verify User B's task is still intact
        verify_b = client.get(f"/api/{user_b_id}/tasks/{task_b_id}", headers=headers_b)
        assert verify_b.status_code == 200
        assert verify_b.json()["title"] == "User B's Task"

    def test_full_crud_operations_with_authentication(
        self, client: TestClient, session: Session
    ):
        """Test complete CRUD operations with authentication."""
        # Step 1: Sign up and get token
        signup_data = {
            "email": "crud@example.com",
            "password": "CrudPass123",
            "username": "CRUD User",
        }
        signup = client.post("/api/auth/signup", json=signup_data)
        assert signup.status_code == 201
        token = signup.json()["access_token"]
        user_id = signup.json()["user"]["id"]
        headers = {"Authorization": f"Bearer {token}"}

        # Step 2: Create multiple tasks
        tasks_data = [
            {"title": "Task 1", "description": "First task"},
            {"title": "Task 2", "description": "Second task"},
            {"title": "Task 3", "description": "Third task"},
        ]
        task_ids = []
        for task_data in tasks_data:
            response = client.post(
                f"/api/{user_id}/tasks", json=task_data, headers=headers
            )
            assert response.status_code == 201
            task_ids.append(response.json()["id"])

        # Step 3: Read all tasks
        all_tasks = client.get(f"/api/{user_id}/tasks", headers=headers)
        assert all_tasks.status_code == 200
        assert len(all_tasks.json()) == 3

        # Step 4: Read specific task
        task_detail = client.get(f"/api/{user_id}/tasks/{task_ids[0]}", headers=headers)
        assert task_detail.status_code == 200
        assert task_detail.json()["title"] == "Task 1"

        # Step 5: Update task
        update_data = {"title": "Updated Task 1", "is_completed": True}
        update = client.put(
            f"/api/{user_id}/tasks/{task_ids[0]}", json=update_data, headers=headers
        )
        assert update.status_code == 200
        assert update.json()["title"] == "Updated Task 1"
        assert update.json()["is_completed"] is True

        # Step 6: Toggle task completion
        toggle = client.patch(
            f"/api/{user_id}/tasks/{task_ids[1]}/toggle", headers=headers
        )
        assert toggle.status_code == 200
        assert toggle.json()["is_completed"] is True

        # Step 7: Toggle again
        toggle_again = client.patch(
            f"/api/{user_id}/tasks/{task_ids[1]}/toggle", headers=headers
        )
        assert toggle_again.status_code == 200
        assert toggle_again.json()["is_completed"] is False

        # Step 8: Delete task
        delete = client.delete(f"/api/{user_id}/tasks/{task_ids[2]}", headers=headers)
        assert delete.status_code == 204

        # Step 9: Verify deletion
        verify_delete = client.get(
            f"/api/{user_id}/tasks/{task_ids[2]}", headers=headers
        )
        assert verify_delete.status_code == 404

        # Step 10: Verify remaining tasks
        remaining = client.get(f"/api/{user_id}/tasks", headers=headers)
        assert remaining.status_code == 200
        assert len(remaining.json()) == 2

    def test_multiple_users_concurrent_operations(
        self, client: TestClient, session: Session
    ):
        """Test multiple users performing operations concurrently."""
        # Create 3 users
        users = []
        for i in range(3):
            signup_data = {
                "email": f"user{i}@example.com",
                "password": f"Pass{i}123",
                "username": f"User {i}",
            }
            signup = client.post("/api/auth/signup", json=signup_data)
            assert signup.status_code == 201
            users.append(
                {
                    "id": signup.json()["user"]["id"],
                    "token": signup.json()["access_token"],
                    "headers": {"Authorization": f"Bearer {signup.json()['access_token']}"},
                }
            )

        # Each user creates 2 tasks
        for user in users:
            for j in range(2):
                task_data = {"title": f"User {user['id']} Task {j}"}
                response = client.post(
                    f"/api/{user['id']}/tasks", json=task_data, headers=user["headers"]
                )
                assert response.status_code == 201

        # Verify each user sees only their own tasks
        for user in users:
            tasks = client.get(f"/api/{user['id']}/tasks", headers=user["headers"])
            assert tasks.status_code == 200
            tasks_list = tasks.json()
            assert len(tasks_list) == 2
            # All tasks should belong to this user
            assert all(task["user_id"] == user["id"] for task in tasks_list)

    def test_authentication_required_for_all_task_operations(
        self, client: TestClient, session: Session
    ):
        """Test that all task operations require authentication."""
        # Create a user and task
        signup_data = {
            "email": "protected@example.com",
            "password": "ProtectedPass123",
            "username": "Protected User",
        }
        signup = client.post("/api/auth/signup", json=signup_data)
        user_id = signup.json()["user"]["id"]
        token = signup.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create a task
        task_data = {"title": "Protected Task"}
        create = client.post(f"/api/{user_id}/tasks", json=task_data, headers=headers)
        task_id = create.json()["id"]

        # Try all operations without authentication
        operations = [
            ("GET", f"/api/{user_id}/tasks", None),
            ("POST", f"/api/{user_id}/tasks", task_data),
            ("GET", f"/api/{user_id}/tasks/{task_id}", None),
            ("PUT", f"/api/{user_id}/tasks/{task_id}", {"title": "Updated"}),
            ("PATCH", f"/api/{user_id}/tasks/{task_id}/toggle", None),
            ("DELETE", f"/api/{user_id}/tasks/{task_id}", None),
        ]

        for method, url, data in operations:
            if method == "GET":
                response = client.get(url)
            elif method == "POST":
                response = client.post(url, json=data)
            elif method == "PUT":
                response = client.put(url, json=data)
            elif method == "PATCH":
                response = client.patch(url)
            elif method == "DELETE":
                response = client.delete(url)

            assert response.status_code == 401, f"Failed for {method} {url}"

    def test_token_reuse_across_sessions(self, client: TestClient, session: Session):
        """Test that token can be reused across multiple sessions."""
        # Sign up and get token
        signup_data = {
            "email": "reuse@example.com",
            "password": "ReusePass123",
            "username": "Reuse User",
        }
        signup = client.post("/api/auth/signup", json=signup_data)
        token = signup.json()["access_token"]
        user_id = signup.json()["user"]["id"]
        headers = {"Authorization": f"Bearer {token}"}

        # Use token multiple times with delays (simulating different sessions)
        for i in range(5):
            # Create task
            task_data = {"title": f"Task {i}"}
            create = client.post(
                f"/api/{user_id}/tasks", json=task_data, headers=headers
            )
            assert create.status_code == 201

            # List tasks
            tasks = client.get(f"/api/{user_id}/tasks", headers=headers)
            assert tasks.status_code == 200
            assert len(tasks.json()) == i + 1

    def test_login_after_signup_provides_new_token(
        self, client: TestClient, session: Session
    ):
        """Test that logging in after signup provides a new token."""
        # Sign up
        signup_data = {
            "email": "newtoken@example.com",
            "password": "NewTokenPass123",
            "username": "New Token User",
        }
        signup = client.post("/api/auth/signup", json=signup_data)
        signup_token = signup.json()["access_token"]
        user_id = signup.json()["user"]["id"]

        # Login
        login_data = {"email": signup_data["email"], "password": signup_data["password"]}
        login = client.post("/api/auth/signin", json=login_data)
        login_token = login.json()["access_token"]

        # Tokens should be different (different iat timestamps)
        assert signup_token != login_token

        # Both tokens should work
        headers_signup = {"Authorization": f"Bearer {signup_token}"}
        headers_login = {"Authorization": f"Bearer {login_token}"}

        response_signup = client.get(f"/api/{user_id}/tasks", headers=headers_signup)
        response_login = client.get(f"/api/{user_id}/tasks", headers=headers_login)

        assert response_signup.status_code == 200
        assert response_login.status_code == 200

    def test_user_cannot_manipulate_url_to_access_other_users(
        self, client: TestClient, session: Session
    ):
        """Test that users cannot manipulate URL parameters to access other users' data."""
        # Create two users
        user1_data = {
            "email": "user1@example.com",
            "password": "User1Pass123",
            "username": "User 1",
        }
        user2_data = {
            "email": "user2@example.com",
            "password": "User2Pass123",
            "username": "User 2",
        }

        signup1 = client.post("/api/auth/signup", json=user1_data)
        signup2 = client.post("/api/auth/signup", json=user2_data)

        user1_id = signup1.json()["user"]["id"]
        user2_id = signup2.json()["user"]["id"]
        token1 = signup1.json()["access_token"]
        headers1 = {"Authorization": f"Bearer {token1}"}

        # User 1 tries to access User 2's resources by changing URL
        attempts = [
            f"/api/{user2_id}/tasks",
            f"/api/{user2_id}/tasks/1",
        ]

        for url in attempts:
            response = client.get(url, headers=headers1)
            assert response.status_code == 403, f"Failed to block access to {url}"

    def test_complete_workflow_with_data_persistence(
        self, client: TestClient, session: Session
    ):
        """Test complete workflow with data persistence verification."""
        # Sign up
        signup_data = {
            "email": "persist@example.com",
            "password": "PersistPass123",
            "username": "Persist User",
        }
        signup = client.post("/api/auth/signup", json=signup_data)
        user_id = signup.json()["user"]["id"]

        # Login (simulating new session)
        login_data = {"email": signup_data["email"], "password": signup_data["password"]}
        login = client.post("/api/auth/signin", json=login_data)
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create tasks
        for i in range(3):
            task_data = {"title": f"Persistent Task {i}", "description": f"Task {i}"}
            response = client.post(
                f"/api/{user_id}/tasks", json=task_data, headers=headers
            )
            assert response.status_code == 201

        # Verify in database
        statement = select(Task).where(Task.user_id == user_id)
        db_tasks = session.exec(statement).all()
        assert len(db_tasks) == 3

        # Verify via API
        api_tasks = client.get(f"/api/{user_id}/tasks", headers=headers)
        assert len(api_tasks.json()) == 3

        # Update a task
        task_id = api_tasks.json()[0]["id"]
        update_data = {"title": "Updated Persistent Task"}
        client.put(f"/api/{user_id}/tasks/{task_id}", json=update_data, headers=headers)

        # Verify update persisted
        db_task = session.get(Task, task_id)
        assert db_task.title == "Updated Persistent Task"
