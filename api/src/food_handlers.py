from flask import Blueprint, request, jsonify
from config import db
from .models import FoodItem
import uuid

food_bp = Blueprint("foods", __name__)

COLLECTION_NAME = "foods"

@food_bp.route("/all", methods=["GET"])
def get_fooditems():
    """
    Get All Food Items
    ---
    tags:
      - Foods
    responses:
      200:
        description: List of all food items
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                data:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: string
                        example: "uuid"
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
    """
    try:
        foods_ref = db.collection(COLLECTION_NAME).stream()

        foods = []
        for doc in foods_ref:
            food = doc.to_dict()
            food["id"] = doc.id   # include document ID
            foods.append(food)

        return jsonify({
            "success": True,
            "data": foods
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@food_bp.route("/foods", methods=["POST"])
def create_food():
    """
    Create a Food Item
    ---
    tags:
      - Foods
    requestBody:
      required: true
      content:
        application/json:
          schema:
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
    responses:
      201:
        description: Food created successfully
      400:
        description: Missing required fields
    """
    try:
        data = request.get_json()

        food_name = data.get("food_name")
        addins = data.get("addins", [])
        size = data.get("size")
        price = data.get("price")

        if not food_name or not size or price is None:
            return jsonify({"error": "Missing required fields"}), 400

        food = FoodItem(food_name, addins, size, price)

        doc_id = str(uuid.uuid4())

        db.collection(COLLECTION_NAME).document(doc_id).set(food.to_dict())

        return jsonify({
            "success": True,
            "message": "Food created successfully",
            "id": doc_id
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@food_bp.route("/foods/<food_id>", methods=["PUT"])
def update_food(food_id):
    """
    Update a Food Item
    ---
    tags:
      - Foods
    parameters:
      - in: path
        name: food_id
        schema:
          type: string
        required: true
        description: UUID of the food item
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              food_name:
                type: string
              addins:
                type: array
                items:
                  type: string
              size:
                type: string
              price:
                type: number
    responses:
      200:
        description: Food updated successfully
      404:
        description: Food not found
    """
    try:
        data = request.get_json()

        food_ref = db.collection(COLLECTION_NAME).document(food_id)

        if not food_ref.get().exists:
            return jsonify({"error": "Food not found"}), 404

        food_ref.update(data)

        return jsonify({
            "success": True,
            "message": "Food updated successfully"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@food_bp.route("/foods/<food_id>", methods=["DELETE"])
def delete_food(food_id):
    """
    Delete a Food Item
    ---
    tags:
      - Foods
    parameters:
      - in: path
        name: food_id
        schema:
          type: string
        required: true
        description: UUID of the food item
    responses:
      200:
        description: Food deleted successfully
      404:
        description: Food not found
    """
    try:
        food_ref = db.collection(COLLECTION_NAME).document(food_id)

        if not food_ref.get().exists:
            return jsonify({"error": "Food not found"}), 404

        food_ref.delete()

        return jsonify({
            "success": True,
            "message": "Food deleted successfully"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

