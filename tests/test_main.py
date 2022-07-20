import json
from app.db import schemas

# user can log in
def test_user_can_log_in(client, basic_user_schema):
    user_data = {}
    response = client.post("/login", data=user_data)
    assert response.status_code == 422

    user_data = {"username": "wrong", "password": "credentials"}

    response = client.post("/login", data=user_data)
    assert response.status_code == 401

    user_data = {"username": basic_user_schema.username, "password": basic_user_schema.password}

    response = client.post("/login", data=user_data)
    assert response.status_code == 200


# any user (authenticated or not) can access /books endpoint (GET)
def test_user_can_see_books(client):
    response = client.get("/books")
    assert response.status_code == 200


# authenticated user can CRUD (Create, read, update and delete)
def test_user_can_publish_a_book(client_authenticated, basic_user_schema):
    book_data = {
        "title": "Pinokio",
        "description": "Lies",
        "author": basic_user_schema.pseudonym,
        "cover": "https://images-na.ssl-images-amazon.com/images/I/715Uyyb6xiL.jpg",
        "price": 20_00,
    }

    response = client_authenticated.post("/books", data=json.dumps(book_data))
    assert response.status_code == 200


def test_user_can_read_a_book(client, basic_user_schema):
    response = client.get(f"/books/{basic_user_schema.pseudonym}/Pinokio")
    assert response.status_code == 200
    assert schemas.Book(**response.json())

# user can update/delete only their own books
def test_user_can_update_a_book(client_authenticated, basic_user_schema):
    update_data = {
        "title": "Pinokio",
        "description": "Lies",
        "author": basic_user_schema.pseudonym,
        "cover": "https://kbimages1-a.akamaihd.net/7e7f3381-d6b8-4a32-b01b-036895d0ec5a/353/569/90/False/pinocchio-148.jpg",
        "price": 40_00,
    }
    response = client_authenticated.put(f"/books", data=json.dumps(update_data))
    assert response.status_code == 200
    assert schemas.Book(**response.json())

def test_user_can_delete_a_book(client_authenticated, basic_user_schema):
    response = client_authenticated.delete(f"/books/{basic_user_schema.pseudonym}/Pinokio")
    assert response.status_code == 200

# Darth Vader is unable to publish his works
def test_darth_vader_cant_publish(client_authenticated_villain):
    book_data = {
        "title": "The Hobbit",
        "description": "There and Back Again",
        "author": "Darth Vader",
        "cover": "https://cdn.pastemagazine.com/www/articles/hobbit300.jpg",
        "price": 13_37,
    }

    response = client_authenticated_villain.post("/books", data=json.dumps(book_data))
    assert response.status_code == 401


def test_user_can_see_own_profile(client_authenticated):
    response = client_authenticated.get("/me")
    assert response.status_code == 200