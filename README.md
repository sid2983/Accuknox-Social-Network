# Social Network API

This project is a social networking application API built using Django Rest Framework. The application includes user authentication and various social networking functionalities such as sending, accepting, and rejecting friend requests, as well as searching for users.

## Installation

Follow these steps to set up and run the project on your local machine:

### Prerequisites

- Python 3.10+
- Docker
- Docker Compose

### Steps

1. **Clone the repository:**

```bash
git clone <repository_url>
cd <repository_directory>
```

2. **Create or modify the  `.env` file in the project root :**
```
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True
POSTGRES_DB=social_network
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```
- Replace `your_secret_key`, `your_username`, and `your_password` with your own values.




3. **Build and run the Docker containers:**

```bash
docker-compose up --build
```
This command will build the Docker containers and run the Django application on `http://localhost:8000` after applying the migrations.

You can create a superuser by running the following command:
```bash
docker-compose exec web python manage.py createsuperuser
```    
And then you can access the Django admin panel at `http://localhost:8000/admin`.

<br>
<br>
<br>

## API Endpoints

### Authentication

1. **Register a new user:**
   
    - **URL:** `/signup/`
    - **Method:** `POST`
    - **Request Body:**
      ```json
      {
            "username": "new_user",
            "email": "email",
            "password": "password"
        }
        ```    
    - **Response:** 
    - **Status Code:** 201
    - **Response Body:**
      ```json
      {
           "refresh": "refresh_token",
              "access": "access_token"            
        }
        ```   
     Here access and refresh tokens are generated , in order to log in the user automatically after sign up.
<br>

2. **Login:**
       
    - **URL:** `/login/`
    - **Method:** `POST`
    - **Request Body:**
      ```json
      {
            "username": "username",
            "password": "password"
        }
        ```    
    - **Response:** 
    - **Status Code:** 200
    - **Response Body:**
      ```json
      {
           "refresh": "refresh_token",
              "access": "access_token"            
        }
        ```   
     Here access and refresh tokens are generated , in order to log in the user. Access token is valid for 10 minutes and refresh token is valid for 1 day.<br>
     **Acces token is needed to access the protected endpoints.**

<br>

3. **Logout:**
       
    - **URL:** `/logout/`
    - **Method:** `POST`
    - **Request Header:**
      ```json
      {
            "Authorization": "Bearer access_token"
        }
        ```
    - **Request Body:**
        ```json
        {
                "refresh": "refresh_token"
            }
            ```
    - **Response:**
    - **Status Code:** 205
    - **Response Body:**
        ```json
        {
                "message": "Logout successful"
            }
            ```
    - **Note:** The refresh token is needed to be sent in the request body to invalidate it.
    - **Note:** The refresh token is blacklisted and can no longer be used to obtain a new access token.

<br>
<br>
<br>

### User Endpoints

1. **Search Users:**
   
    - **URL:** `/users/?search_keyword=<search_query>`
    - **Method:** `GET`
    - **Request Header:**
      ```json
      {
        "Authorization": "Bearer access_token"
        }
        ```
    - **Response:**
    - **Status Code:** 200
    - **Response Body:**
      ```json
      [
            {
                "username": "user1",
                "email": "email1"
            },
            ...
        ]
    
        ```
    - **Note:** The search query is case-insensitive and can be a partial match of the username.
    - **Note:** The search query is case-insensitive and can be a partial match of the username.

<br>

2. **Send Friend Request:**
       
    - **URL:** `/send_friend_request/`
    - **Method:** `POST`
    - **Request Header:**
      ```json
        {
        "Authorization": "Bearer access_token"
        }
        ```
    - **Request Body:**
        ```json
        {
            "receiver_username": "actual_receiver_username"
        }    
        ```
    - **Response:**
    - **Status Code:** 201
    - **Response Body:**
        ```json
        {
            "message": "Friend request sent"
        }
        ```
    - **Note:** The receiver username should be a valid user in the system.
    - **Note:** The sender and receiver cannot be the same user.
  
<br>

3. **Accept Friend Request:**
       
    - **URL:** `/accept_friend_request/<request_id>/`
    - **Method:** `POST`
    - **Request Header:**
      ```json
        {
        "Authorization": "Bearer access_token"
        }
        ```
    - **Response:**
    - **Status Code:** 200
    - **Response Body:**
        ```json
        {
            "message": "Friend request accepted"
        }
        ```
    
    - **Note:** The request id should be a valid friend request id.
  
<br>

4. **Reject Friend Request:**
       
    - **URL:** `/reject_friend_request/<request_id>/`
    - **Method:** `POST`
    - **Request Header:**
      ```json
        {
            "Authorization": "Bearer access_token"
        }
        ```
    - **Response:**
    - **Status Code:** 200
    - **Response Body:**
        ```json
        {
            "message": "Friend request rejected"
        }
        ```
    - **Note:** The request id should be a valid friend request id.
    - **Note:** The request should be in the pending state to in order to get rejected.
  
<br>

5. **List Friends:**
       
    - **URL:** `/list_friends/`
    - **Method:** `GET`
    - **Request Header:**
      ```json
        {
            "Authorization": "Bearer access_token"
        }
        ```
    - **Response:**
    - **Status Code:** 200
    - **Response Body:**
        ```json
        [
            {
                "username": "friend1",
                "email": "email1"
            },
            ...
        ]
        ```    
    - **Note:** The list of friends includes users who have accepted the friend request.

<br>

6. **List Pending Friend Requests:**
       
    - **URL:** `/list_pending_friend_requests/`
    - **Method:** `GET`
    - **Request Header:**
      ```json
        {
            "Authorization": "Bearer access_token"
        }
        ```
    - **Response:**
    - **Status Code:** 200
    - **Response Body:**
        ```json
        [
            {
                "id": 1,
                "sender": "sender_username",
                "receiver": "receiver_username"
            },
            ...
        ]
        ```


## Postman Collection :



### Run in Postman button : 

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/26249030-8108e2c2-5b56-4e16-9dc6-6280c51799de?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D26249030-8108e2c2-5b56-4e16-9dc6-6280c51799de%26entityType%3Dcollection%26workspaceId%3D58058a67-e0ee-409b-b778-3ec746370577)



**Note: Postman Collection File is also provided in the root directory. So one have to import the file in the postman app and start testing** 

