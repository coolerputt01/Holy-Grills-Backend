from flask import Blueprint, request, jsonify
from config import db
from .models import PickupDelivery, DoorstepDelivery

delivery_bp = Blueprint("delivery", __name__)
COLLECTION_NAME = "deliveries"

@delivery_bp.route("/pickup", methods=["POST"])
def create_pickup():
    """
    Create Pickup Delivery
    ---
    tags:
      - Delivery
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - order_id
              - customer_name
              - customer_phone
              - rider_name
              - order_time
              - restaurant_address
            properties:
              order_id:
                type: string
                example: "12345"
              customer_name:
                type: string
                example: "John Doe"
              customer_phone:
                type: string
                example: "09012345678"
              rider_name:
                type: string
                example: "David"
              order_time:
                type: string
                example: "6:30 PM"
              restaurant_address:
                type: string
                example: "Campus Main Gate"
    responses:
      201:
        description: Pickup delivery created successfully
      400:
        description: Missing required fields
    """
    try:
        data = request.get_json()

        required_fields = [
            "order_id",
            "customer_name",
            "customer_phone",
            "rider_name",
            "order_time",
            "restaurant_address"
        ]

        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"{field} is required"}), 400

        pickup = PickupDelivery(
            order_id=data["order_id"],
            customer_name=data["customer_name"],
            customer_phone=data["customer_phone"],
            rider_name=data["rider_name"],
            order_time=data["order_time"],
            restaurant_address=data["restaurant_address"]
        )

        db.collection(COLLECTION_NAME).document(pickup.delivery_id).set(
            pickup.to_dict()
        )

        return jsonify({
            "success": True,
            "delivery_id": pickup.delivery_id
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@delivery_bp.route("/doorstep", methods=["POST"])
def create_doorstep():
    """
    Create Doorstep Delivery
    ---
    tags:
      - Delivery
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - order_id
              - street
              - zone
              - lodge_name
              - delivery_time
            properties:
              order_id:
                type: string
                example: "12345"
              street:
                type: string
                example: "Off Campus Road"
              zone:
                type: string
                example: "Zone B"
              lodge_name:
                type: string
                example: "Divine Lodge"
              delivery_time:
                type: string
                example: "7:00 PM"
              additional_info:
                type: string
                example: "Call on arrival"
    responses:
      201:
        description: Doorstep delivery created successfully
      400:
        description: Missing required fields
    """
    try:
        data = request.get_json()

        required_fields = [
            "order_id",
            "street",
            "zone",
            "lodge_name",
            "delivery_time"
        ]

        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"{field} is required"}), 400

        doorstep = DoorstepDelivery(
            order_id=data["order_id"],
            street=data["street"],
            zone=data["zone"],
            lodge_name=data["lodge_name"],
            delivery_time=data["delivery_time"],
            additional_info=data.get("additional_info")
        )

        db.collection(COLLECTION_NAME).document(doorstep.delivery_id).set(
            doorstep.to_dict()
        )

        return jsonify({
            "success": True,
            "delivery_id": doorstep.delivery_id
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
