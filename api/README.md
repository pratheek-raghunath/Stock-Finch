# API Information

## Authentication

Reference - https://www.youtube.com/watch?v=8-W2O_R95Pk

There are two endpoints for authentication: 
1) POST /api/register - For User Signup
2) POST /api/token - For User Login

1) POST /api/register

    Requires firstname, lastname, email, password in request body

    Returns 401 with appropriate error message if: request body is empty or incomplete, user with email already exists
    Returns empty 201 if user was successfully registered

    Eg request:

    const opts = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            first_name: 'test',
            last_name: 'test, 
            email: 'test',
            password: 'test'
        })
    };

    fetch(" https://stockfinch.herokuapp.com/api/register", opts)
    .then()

2) POST /api/token

    Requires email and password in request body

    Returns 401 with appropriate error message if: request body is empty or incomplete, login credentials incorrect
    Returns the jwt access token if user was successfully authenticated- 
    Eg: {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0MzY0OTMzMSwianRpIjoiZThhNDhiODAtYWEyNS00ZjJkLWJlYjgtMzEzN2U0MzdhNjcxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjQzNjQ5MzMxLCJleHAiOjE2NDM2NTAyMzF9.-c7kkWEFP3inPI0itIL-dcbMKnjtjy4khKlWqdelyV4"
}

    Eg request:

    const opts = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: 'test',
            password: 'test'
        })
    };

    fetch(" https://stockfinch.herokuapp.com/api/token", opts)
    .then()


    The access token has to be stored in the react application context and the session storage/local storage for future api requests

## Data

All requests to the api need to contain the jwt access token.
This should be placed in the request headers.
Eg: Authorization: bearer <access_token>

Eg request:

const opts = {
    headers: {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0MzY0OTMzMSwianRpIjoiZThhNDhiODAtYWEyNS00ZjJkLWJlYjgtMzEzN2U0MzdhNjcxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjQzNjQ5MzMxLCJleHAiOjE2NDM2NTAyMzF9.-c7kkWEFP3inPI0itIL-dcbMKnjtjy4khKlWqdelyV4'
    }
};

fetch(" https://stockfinch.herokuapp.com/api/stock_news", opts)
.then()

1) GET /api/stock_news 

    Structure:
    data - list of stock news items
    has_prev - boolean - previous page available?
    prev - url of previous page
    has_next - boolean - next page available?
    next - url of next page

    Pagination parameters:
    ?offset - default 0
    ?limit - default 10

    Eg: 
    GET https://stockfinch.herokuapp.com/api/stock_news?limit=5 
    Returns the first page with 5 news items