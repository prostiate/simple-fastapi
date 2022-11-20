import json
from app.api import crud


def test_create_data(test_app, monkeypatch):
    test_request_payload = {
        "account_number": 555001,
        "customer_number": 1001,
        "name": "hehe1001",
        "balance": 1000
    }
    test_response_payload = {
        "id": 1,
        "account_number": 555001,
        "customer_number": 1001,
        "name": "hehe1001",
        "balance": 1000
    }

    async def mock_create_data(payload):
        return 1

    monkeypatch.setattr(crud, "create_data", mock_create_data)

    response = test_app.post("/account/create_data", data=json.dumps(test_request_payload))

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_data_invalid_json(test_app):
    response = test_app.post("/account/create_data", data=json.dumps({"account_number": "100"}))
    assert response.status_code == 422

    response = test_app.post("/account/create_data", data=json.dumps({"customer_number": "1"}))
    assert response.status_code == 422


def test_read_all_accounts(test_app, monkeypatch):
    test_data = [
        {
            "id": 1,
            "account_number": 555001,
            "customer_number": 1001,
            "name": "hehe1001",
            "balance": 1000
        },
        {
            "id": 2,
            "account_number": 555002,
            "customer_number": 1002,
            "name": "hehe1002",
            "balance": 1000
        }
    ]
    test_response_data = [
        {
            "id": 1,
            "account_number": 555001,
            "customer_number": 1001,
            "balance": 1000
        },
        {
            "id": 2,
            "account_number": 555002,
            "customer_number": 1002,
            "balance": 1000
        }
    ]

    async def mock_get_all_account():
        return test_data

    monkeypatch.setattr(crud, "get_all_account", mock_get_all_account)

    response = test_app.get("/account/")
    assert response.status_code == 200
    assert response.json() == test_response_data


def test_check_balance(test_app, monkeypatch):
    test_response_data = {
        "account_number": "555001",
        "customer_name": "hehe1001",
        "balance": 1000
    }

    async def mock_check_balance(account_number):
        return test_response_data

    monkeypatch.setattr(crud, "check_balance", mock_check_balance)
    
    response = test_app.get("/account/555001")
    assert response.status_code == 200
    assert response.json() == test_response_data


def test_check_balance_invalid_account(test_app):
    response = test_app.get("/account/testing123")
    assert response.status_code == 422

    response = test_app.get("/account/99219201")
    assert response.status_code == 404


def test_transfer_invalid_json(test_app):
    response = test_app.post("/account/testing123/transfer")
    assert response.status_code == 422

    test_data = {
        "account_number": "100"
    }
    response = test_app.post("/account/awt555001/transfer", data=json.dumps(test_data))
    assert response.status_code == 422

    response = test_app.post("/account/555001/transfer", data=json.dumps(test_data))
    assert response.status_code == 422

    test_data = {
        "to_account_number": "555001",
        "amount": 100
    }
    response = test_app.post("/account/555001/transfer", data=json.dumps(test_data))
    assert response.status_code == 404


def test_transfer(test_app, monkeypatch):
    test_data = {
        "to_account_number": "555002",
        "amount": 100000
    }

    async def mock_transfer(from_account_number, payload):
        return True

    monkeypatch.setattr(crud, "transfer", mock_transfer)

    response = test_app.post("/account/555001/transfer", data=json.dumps(test_data))
    print(response.json())
    assert response.status_code == 201
