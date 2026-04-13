"""Tests for registration only: API POST /users/ and /register page markup for base.js."""

from fastapi import status


def test_register_page_has_form_before_base_js(client):
    """So document.getElementById('registerForm') exists when base.js runs."""
    response = client.get("/register")
    assert response.status_code == status.HTTP_200_OK
    text = response.text
    assert 'id="registerForm"' in text
    assert "base.js" in text
    assert text.index('id="registerForm"') < text.index("base.js")


def test_post_users_creates_user(client):
    payload = {
        "email": "newuser@example.com",
        "username": "newuser",
        "fullname": "New User",
        "password": "secretpass123",
        "role": "user",
        "phone_number": "+15551234567",
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["username"] == payload["username"]
    assert data["fullname"] == payload["fullname"]
    assert data["role"] == payload["role"]
    assert data["phone_number"] == payload["phone_number"]
    assert "password" not in data


def test_post_users_duplicate_email_returns_409(client):
    payload = {
        "email": "dup@example.com",
        "username": "first",
        "fullname": "First User",
        "password": "secretpass123",
        "role": "user",
    }
    assert client.post("/users/", json=payload).status_code == status.HTTP_201_CREATED
    payload2 = {
        **payload,
        "username": "second",
        "fullname": "Second User",
    }
    response = client.post("/users/", json=payload2)
    assert response.status_code == status.HTTP_409_CONFLICT
