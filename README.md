# Simple Fastapi
This is simple fastapi project with PosgreSQL.

# Project Structure
```sh
simple-fastapi
    ├── src
    │   ├── app
    │   │   ├── api
    │   │   │    ├── __init__.py
    │   │   │    ├── account.py
    │   │   │    ├── crud.py
    │   │   │    ├── customer.py
    │   │   │    ├── models.py
    │   │   │    └── ping.py
    │   │   ├── __init__.py
    │   │   ├── db.py
    │   │   └── main.py
    │   ├── tests
    │   │   ├── __init__.py
    │   │   ├── conftest.py
    │   │   ├── test_accounts.py
    │   │   └── test_ping.py
    │   ├── Dockerfile
    │   └── requirements.txt
    ├── .gitignore
    ├── docker-compose.yml
    └── README.md
```

# How To Use

## Docker

Build the images and run the containers:

```sh
docker-compose up -d --build
```

# Testing
Using Starlette's TestClient, which uses the Requests library to make requests against the FastAPI app.
```sh
docker-compose exec web pytest .
```

Result
```sh
ubuntu@kali-playground:~$ docker-compose exec web pytest .
========================== test session starts ===========================
platform linux -- Python 3.9.4, pytest-6.2.3, py-1.11.0, pluggy-0.13.1
rootdir: /usr/src/app
collected 8 items

tests/test_accounts.py .......                                     [ 87%]
tests/test_ping.py .                                               [100%]

=========================== 8 passed in 0.33s ============================
```

# Available Routes

## METHOD GET /customer
This route will fetch all customers data
```sh
curl --location --request GET 'http://localhost:8002/customer'
```

If the data doesn't exists, then it will return empty array
```sh
ubuntu@kali-playground:~$ curl --location --request GET 'http://localhost:8002/customer' | json_pp
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100     2  100     2    0     0    285      0 --:--:-- --:--:-- --:--:--   285
[]
```

If the data exists, it will return all the customers data
```sh
ubuntu@kali-playground:~$ curl --location --request GET 'http://localhost:8002/customer' | json_pp
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100    47  100    47    0     0   6714      0 --:--:-- --:--:-- --:--:--  6714
[
   {
      "customer_number" : 1001,
      "id" : 1,
      "name" : "hehe"
   }
]
```

## METHOD GET /account
This route will fetch all accounts data
```sh
curl --location --request GET 'http://localhost:8002/account'
```

If the data doesn't exists, then it will return empty array
```sh
ubuntu@kali-playground:~$ curl --location --request GET 'http://localhost:8002/account' | json_pp
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100     2  100     2    0     0    285      0 --:--:-- --:--:-- --:--:--   285
[]
```

If the data exists, it will return all the accounts data
```sh
ubuntu@kali-playground:~$ curl --location --request GET 'http://localhost:8002/account' | json_pp
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    72  100    72    0     0  12000      0 --:--:-- --:--:-- --:--:-- 14400
[
   {
      "account_number" : 555001,
      "balance" : 1000,
      "customer_number" : 1001,
      "id" : 1
   }
]
```

## METHOD POST /account/create_data
This route will create account and customer data
```sh
curl --location --request POST 'http://localhost:8002/account/create_data' \
--header 'Content-Type: application/json' \
--data-raw '{
    "account_number": 555002,
    "customer_number": 1002,
    "name": "test1002",
    "balance": 1000
}'
```

Result
```sh
ubuntu@kali-playground:~$ curl --location --request POST 'http://localhost:8002/account/create_data' --header 'Content-Type: application/json' --data-raw '{
    "account_number": 555002,
    "customer_number": 1002,
    "name": "test1002",
    "balance": 1000
}' | json_pp
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   194  100    88  100   106   9777  11777 --:--:-- --:--:-- --:--:-- 21555
{
   "account_number" : 555002,
   "balance" : 1000,
   "customer_number" : 1002,
   "id" : 1,
   "name" : "test1002"
}
```

## METHOD GET /account/{account_number}
This route will return the detail of the account number
```sh
curl --location --request GET 'http://localhost:8002/account/555001' \
--header 'Content-Type: application/json' \
--data-raw ''
```

Result
```sh
ubuntu@kali-playground:~$ curl --location --request GET 'http://localhost:8002/account/555001' \
> --header 'Content-Type: application/json' \
> --data-raw '' | json_pp
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100    65  100    65    0     0   6500      0 --:--:-- --:--:-- --:--:--  6500
{
   "account_number" : "555001",
   "balance" : 1000,
   "customer_name" : "hehe"
}
```

## METHOD GET /account/{from_account_number}/transfer
This route will transfer the balance between account numbers that included in json data.

Body JSON
```json
{
    "to_account_number": "555001",
    "amount": 500
}
```
Curl 
```sh
curl --location --request POST 'http://localhost:8002/account/555002/transfer' \
--header 'Content-Type: application/json' \
--data-raw '{
    "to_account_number": "555001",
    "amount": 500
}'
```

Result
```sh
ubuntu@kali-playground:~$ curl --location --request POST 'http://localhost:8002/account/555002/transfer' \
> --header 'Content-Type: application/json' \
> --data-raw '{
>     "to_account_number": "555001",
>     "amount": 500
> }' | json_pp
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    99  100    43  100    56   2529   3294 --:--:-- --:--:-- --:--:--  6187
{
   "amount" : 500,
   "to_account_number" : "555001"
}
```