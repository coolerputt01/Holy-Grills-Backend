# Holy Grills API

## Overview
The Holy Grills API is a robust backend system built with Python and Flask, leveraging Google Cloud Firestore as its primary NoSQL database. It provides comprehensive functionalities for managing food items, processing customer orders, and handling various delivery types, all exposed through a well-documented RESTful interface.

## Features
-   **Food Item Management**: Full CRUD operations for managing menu items, including details like name, add-ins, size, and price.
-   **Order Processing**: Allows customers to create new orders with multiple food items, specifying delivery preferences.
-   **Order Tracking**: Enables retrieval of individual order details and status updates.
-   **Delivery Management**: Supports two distinct delivery modes:
    -   **Pickup Delivery**: Facilitates orders to be picked up at a specified restaurant address.
    -   **Doorstep Delivery**: Manages deliveries to specific customer addresses, including street, zone, and lodge information.
-   **Real-time Database**: Utilizes Google Cloud Firestore for efficient and scalable data storage and retrieval.
-   **Integrated API Documentation**: Automatically generates and serves OpenAPI (Swagger) documentation for all endpoints using Flasgger.

## Getting Started
### Installation
<!-- User opted out of Installation Instructions -->

### Environment Variables
For secure and flexible configuration, the following environment-related setup is required:

*   **`sk.json`**: This file contains the Firebase service account credentials. It must be placed in the project's root directory. `config.py` directly references this file for Firebase initialization. Ensure its contents are correctly configured for your Firebase project.

## API Documentation
### Base URL
`http://localhost:5000`

### Endpoints
#### GET /
**Overview**: Checks the API status and returns a welcome message.
**Request**:
This endpoint does not require any request body.

**Response**:
```json
"Welcome to Holy Grills."
```

**Errors**:
-   `500 Internal Server Error`: An unexpected error occurred on the server.

#### POST /orders
**Overview**: Creates a new customer order with specified food items and delivery details.
**Request**:
```json
{
  "items": [
    {
      "food_name": "Burger",
      "addins": ["Cheese", "Bacon"],
      "size": "Large",
      "price": 2500
    }
  ],
  "customer_name": "John Doe",
  "customer_phone": "09012345678",
  "delivery_mode": "doorstep"
}
```
**Required fields**: `items`, `customer_name`, `customer_phone`, `delivery_mode`.
For each `item`: `food_name`, `size`, `price`.

**Response**:
```json
{
  "message": "Order confirmed",
  "order_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "estimated_delivery_time": "18:45"
}
```

**Errors**:
-   `400 Bad Request`: Invalid or missing required fields in the request body.

#### GET /orders/{order_id}
**Overview**: Retrieves the details of a specific order by its ID.
**Request**:
This endpoint does not require any request body.
**Parameters**:
-   `order_id` (path): The unique identifier of the order.

**Response**:
```json
{
  "created_at": "2024-01-01T10:00:00.000000",
  "customer_name": "John Doe",
  "customer_phone": "09012345678",
  "delivery_mode": "doorstep",
  "estimated_delivery_time": "18:45",
  "full_price": 2500,
  "items": [
    {
      "addins": ["Cheese", "Bacon"],
      "food_name": "Burger",
      "price": 2500,
      "size": "Large"
    }
  ],
  "order_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "order_status": "Pending"
}
```

**Errors**:
-   `404 Not Found`: The order with the specified ID was not found.

#### PATCH /orders/{order_id}/deliver
**Overview**: Updates the status of an order to 'Delivered'.
**Request**:
This endpoint does not require any request body.
**Parameters**:
-   `order_id` (path): The unique identifier of the order.

**Response**:
```json
{
  "message": "Order marked as delivered"
}
```

**Errors**:
-   `404 Not Found`: The order with the specified ID was not found.

#### GET /foods/all
**Overview**: Retrieves a list of all available food items.
**Request**:
This endpoint does not require any request body.

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": "food-uuid-1",
      "food_name": "Burger",
      "addins": ["Cheese", "Bacon"],
      "size": "Large",
      "price": 2500
    },
    {
      "id": "food-uuid-2",
      "food_name": "Fries",
      "addins": [],
      "size": "Medium",
      "price": 800
    }
  ]
}
```

**Errors**:
-   `500 Internal Server Error`: An unexpected error occurred on the server.

#### POST /foods/foods
**Overview**: Creates a new food item in the menu.
**Request**:
```json
{
  "food_name": "Burger",
  "addins": ["Cheese", "Bacon"],
  "size": "Large",
  "price": 2500
}
```
**Required fields**: `food_name`, `size`, `price`. `addins` is optional.

**Response**:
```json
{
  "success": true,
  "message": "Food created successfully",
  "id": "food-uuid-3"
}
```

**Errors**:
-   `400 Bad Request`: Missing required fields in the request body.
-   `500 Internal Server Error`: An unexpected error occurred on the server.

#### PUT /foods/foods/{food_id}
**Overview**: Updates an existing food item's details.
**Request**:
```json
{
  "food_name": "Updated Burger",
  "price": 2800
}
```
**Parameters**:
-   `food_id` (path): The unique identifier of the food item to update.
Any combination of `food_name`, `addins`, `size`, or `price` can be provided to update.

**Response**:
```json
{
  "success": true,
  "message": "Food updated successfully"
}
```

**Errors**:
-   `404 Not Found`: The food item with the specified ID was not found.
-   `500 Internal Server Error`: An unexpected error occurred on the server.

#### DELETE /foods/foods/{food_id}
**Overview**: Deletes a food item from the menu.
**Request**:
This endpoint does not require any request body.
**Parameters**:
-   `food_id` (path): The unique identifier of the food item to delete.

**Response**:
```json
{
  "success": true,
  "message": "Food deleted successfully"
}
```

**Errors**:
-   `404 Not Found`: The food item with the specified ID was not found.
-   `500 Internal Server Error`: An unexpected error occurred on the server.

#### POST /delivery/pickup
**Overview**: Creates a new pickup delivery record.
**Request**:
```json
{
  "order_id": "12345",
  "customer_name": "John Doe",
  "customer_phone": "09012345678",
  "rider_name": "David",
  "order_time": "6:30 PM",
  "restaurant_address": "Campus Main Gate"
}
```
**Required fields**: `order_id`, `customer_name`, `customer_phone`, `rider_name`, `order_time`, `restaurant_address`.

**Response**:
```json
{
  "success": true,
  "delivery_id": "delivery-uuid-1"
}
```

**Errors**:
-   `400 Bad Request`: Missing required fields in the request body.
-   `500 Internal Server Error`: An unexpected error occurred on the server.

#### POST /delivery/doorstep
**Overview**: Creates a new doorstep delivery record.
**Request**:
```json
{
  "order_id": "12345",
  "street": "Off Campus Road",
  "zone": "Zone B",
  "lodge_name": "Divine Lodge",
  "delivery_time": "7:00 PM",
  "additional_info": "Call on arrival"
}
```
**Required fields**: `order_id`, `street`, `zone`, `lodge_name`, `delivery_time`. `additional_info` is optional.

**Response**:
```json
{
  "success": true,
  "delivery_id": "delivery-uuid-2"
}
```

**Errors**:
-   `400 Bad Request`: Missing required fields in the request body.
-   `500 Internal Server Error`: An unexpected error occurred on the server.

## Usage
To run the Holy Grills API locally:

1.  **Clone the repository**:
    ```bash
    git clone <your-repository-url>
    cd Holy-Grills-Backend/api
    ```
2.  **Set up the environment**:
    Ensure you have `sk.json` with your Firebase service account credentials in the root directory of the project.
3.  **Install dependencies**:
    It is recommended to use a virtual environment.
    ```bash
    python -m venv pyenv
    source pyenv/bin/activate
    pip install -r requirements.txt
    ```
4.  **Run the Flask application**:
    ```bash
    python app.py
    ```
    The API will start running on `http://localhost:5000`.

### Interacting with the API
You can use tools like `curl` or Postman to interact with the endpoints.

**Example: Creating a New Order**
```bash
curl -X POST \
  http://localhost:5000/orders \
  -H 'Content-Type: application/json' \
  -d '{
    "items": [
      {
        "food_name": "Spicy Chicken Sandwich",
        "addins": ["Extra Mayo"],
        "size": "Regular",
        "price": 3200
      }
    ],
    "customer_name": "Jane Smith",
    "customer_phone": "08098765432",
    "delivery_mode": "pickup"
  }'
```

**Example: Getting All Food Items**
```bash
curl http://localhost:5000/foods/all
```

**Example: Accessing API Documentation**
Once the server is running, you can access the interactive API documentation (Swagger UI) by navigating to `http://localhost:5000/apidocs` in your web browser.

## Technologies Used

| Technology             | Description                                          | Link                                                  |
| :--------------------- | :--------------------------------------------------- | :---------------------------------------------------- |
| Python                 | Primary programming language.                        | [Python](https://www.python.org/)                     |
| Flask                  | Lightweight web framework for API development.       | [Flask](https://flask.palletsprojects.com/)           |
| Google Cloud Firestore | NoSQL cloud database for data persistence.           | [Firestore](https://firebase.google.com/docs/firestore) |
| Flasgger               | Integrates Swagger UI for API documentation.         | [Flasgger](https://github.com/flasgger/flasgger)      |
| Firebase Admin SDK     | Python client library for Firebase services.         | [Firebase Admin](https://firebase.google.com/docs/admin/setup/python) |

## Contributing
We welcome contributions to the Holy Grills API! To contribute:

*   ✨ Fork the repository.
*   🌿 Create a new branch for your feature or bug fix.
*   🛠️ Make your changes and test thoroughly.
*   📝 Write clear, concise commit messages.
*   🚀 Push your branch and open a pull request.

Please ensure your code adheres to the existing style and standards of the project.

## Author Info
-   **LinkedIn**: [Your LinkedIn Profile](https://www.linkedin.com/in/yourusername)
-   **X (formerly Twitter)**: [@YourXUsername](https://x.com/YourXUsername)

---

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask 3.1.2](https://img.shields.io/badge/Flask-3.1.2-black?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Firebase Firestore](https://img.shields.io/badge/Firestore-Database-orange?logo=firebase&logoColor=white)](https://firebase.google.com/docs/firestore)
[![Flasgger 0.9.7.1](https://img.shields.io/badge/Flasgger-0.9.7.1-blueviolet?logo=swagger&logoColor=white)](https://github.com/flasgger/flasgger)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen)](https://github.com/yourusername/yourrepository/actions)

[![Readme was generated by Dokugen](https://img.shields.io/badge/Readme%20was%20generated%20by-Dokugen-brightgreen)](https://www.npmjs.com/package/dokugen)