import unittest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_completed():
    response = client.post("/solution",
                           json={
                               "orders": [
                                   {"id": 1, "item": "Laptop", "quantity": 1, "price": 999.99,
                                    "status": "completed"},
                                   {"id": 2, "item": "Smartphone", "quantity": 2, "price": 499.95,
                                    "status": "pending"},
                                   {"id": 3, "item": "Headphones", "quantity": 3, "price": 99.90,
                                    "status": "completed"},
                                   {"id": 4, "item": "Mouse", "quantity": 4, "price": 24.99, "status": "canceled"}
                               ],
                               "criterion": "completed"
                           })
    assert response.status_code == 200
    assert float(response.content) == 1099.89


def test_all():
    response = client.post("/solution",
                           json={
                               "orders": [
                                   {"id": 1, "item": "Laptop", "quantity": 1, "price": 999.99,
                                    "status": "completed"},
                                   {"id": 2, "item": "Smartphone", "quantity": 2, "price": 499.95,
                                    "status": "pending"},
                                   {"id": 3, "item": "Headphones", "quantity": 3, "price": 99.90,
                                    "status": "completed"},
                                   {"id": 4, "item": "Mouse", "quantity": 4, "price": 24.99, "status": "canceled"}
                               ],
                               "criterion": "all"
                           })
    assert response.status_code == 200
    assert float(response.content) == 1624.83


def test_pending():
    response = client.post("/solution",
                           json={
                               "orders": [
                                   {"id": 1, "item": "Laptop", "quantity": 1, "price": 999.99,
                                    "status": "completed"},
                                   {"id": 2, "item": "Smartphone", "quantity": 2, "price": 499.95,
                                    "status": "pending"},
                                   {"id": 3, "item": "Headphones", "quantity": 3, "price": 99.90,
                                    "status": "completed"},
                                   {"id": 4, "item": "Mouse", "quantity": 4, "price": 24.99, "status": "canceled"}
                               ],
                               "criterion": "pending"
                           })
    assert response.status_code == 200
    assert float(response.content) == 499.95


def test_incorrectcriterion():
    response = client.post("/solution",
                           json={
                               "orders": [
                                   {"id": 1, "item": "Laptop", "quantity": 1, "price": 999.99,
                                    "status": "completed"},
                                   {"id": 2, "item": "Smartphone", "quantity": 2, "price": 499.95,
                                    "status": "pending"},
                                   {"id": 3, "item": "Headphones", "quantity": 3, "price": 99.90,
                                    "status": "completed"},
                                   {"id": 4, "item": "Mouse", "quantity": 4, "price": 24.99, "status": "canceled"}
                               ],
                               "criterion": "thisisbad"
                           })
    assert response.status_code == 200
    assert response.json() == {"message": "malformed input"}


def test_incorrectparameters():
    response = client.post("/solution",
                           json={
                               "orders": [
                                   {"id": 1, "item": "Laptop", "quantity": 1, "price": 999.99,
                                    "status": "completed"},
                                   {"id": 2, "item": "Smartphone", "quantity": 2, "price": -499.95,
                                    "status": "pending"},
                                   {"id": 3, "item": "Headphones", "quantity": 3, "price": 99.90,
                                    "status": "completed"},
                                   {"id": 4, "item": "Mouse", "quantity": 4, "price": 24.99, "status": "canceled"}
                               ],
                               "criterion": "all"
                           })
    assert response.status_code == 200
    assert response.json() == {"message": "malformed input"}


def test_incorrectorderstype():
    response = client.post("/solution",
                           json={
                               "orders": "this is a str",
                               "criterion": "all"
                           })
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body', 'orders'],
                                           'msg': 'value is not a valid list',
                                           'type': 'type_error.list'}]}
