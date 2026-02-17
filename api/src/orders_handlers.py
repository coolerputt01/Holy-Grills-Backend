from flask import Blueprint,request,jsonify
from config import db
from .models import Order, FoodItem
from datetime import datetime, timedelta


orders_bp = Blueprint("orders", __name__)
COLLECTION_NAME = "orders"

@orders_bp.route("/orders", methods=["POST"])
def create_order():
    """
    Create a new order
    ---
    tags:
      - Orders
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - items
              - customer_name
              - customer_phone
              - delivery_mode
            properties:
              items:
                type: array
                items:
                  type: object
                  required:
                    - food_name
                    - size
                    - price
                  properties:
                    food_name:
                      type: string
                      example: "Burger"
                    addins:
                      type: array
                      items:
                        type: string
                      example: ["Cheese", "Bacon"]
                    size:
                      type: string
                      example: "Large"
                    price:
                      type: number
                      example: 2500
              customer_name:
                type: string
                example: "John Doe"
              customer_phone:
                type: string
                example: "09012345678"
              delivery_mode:
                type: string
                enum: ["pickup", "doorstep"]
                example: "doorstep"
    responses:
      201:
        description: Order created successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Order confirmed"
                order_id:
                  type: string
                  example: "uuid"
                estimated_delivery_time:
                  type: string
                  example: "18:45"
      400:
        description: Invalid request
    """
    data = request.json

    items = [
        FoodItem(
            food_name=item["food_name"],
            addins=item.get("addins", []),
            size=item["size"],
            price=item["price"],
        )
        for item in data["items"]
    ]

    # Auto estimate delivery time (example: 45 minutes)
    estimated_time = (datetime.now() + timedelta(minutes=45)).strftime("%H:%M")

    order = Order(
        items=items,
        customer_name=data["customer_name"],
        customer_phone=data["customer_phone"],
        delivery_mode=data["delivery_mode"],
        estimated_delivery_time=estimated_time,
    )

    db.collection(COLLECTION_NAME).document(order.order_id).set(order.to_dict())

    return jsonify({
        "message": "Order confirmed",
        "order_id": order.order_id,
        "estimated_delivery_time": estimated_time
    }), 201


#  Get Order
@orders_bp.route("/orders/<order_id>", methods=["GET"])
def get_order(order_id):
    """
    Get a single order by ID
    ---
    tags:
      - Orders
    parameters:
      - in: path
        name: order_id
        schema:
          type: string
        required: true
        description: UUID of the order
    responses:
      200:
        description: Order details
        content:
          application/json:
            schema:
              type: object
      404:
        description: Order not found
    """
    doc = db.collection(COLLECTION_NAME).document(order_id).get()

    if not doc.exists:
        return jsonify({"error": "Order not found"}), 404

    return jsonify(doc.to_dict()), 200


#  Mark Order as Delivered
@orders_bp.route("/orders/<order_id>/deliver", methods=["PATCH"])
def mark_delivered(order_id):
    """
    Mark an order as delivered
    ---
    tags:
      - Orders
    parameters:
      - in: path
        name: order_id
        schema:
          type: string
        required: true
        description: UUID of the order
    responses:
      200:
        description: Order marked as delivered
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Order marked as delivered"
      404:
        description: Order not found
    """
    order_ref = db.collection(COLLECTION_NAME).document(order_id)
    doc = order_ref.get()

    if not doc.exists:
        return jsonify({"error": "Order not found"}), 404

    order_ref.update({
        "order_status": "Delivered",
        "delivered_at": datetime.now()
    })

    return jsonify({
        "message": "Order marked as delivered"
    }), 200
