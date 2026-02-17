import uuid
from datetime import datetime


class FoodItem:
    def __init__(self, food_name, addins, size, price):
        self.food_name = food_name
        self.addins = addins
        self.size = size
        self.price = price

    def to_dict(self):
        return {
            "food_name": self.food_name,
            "addins": self.addins,
            "size": self.size,
            "price": self.price
        }


class Order:
    def __init__(
        self,
        items,
        customer_name,
        customer_phone,
        delivery_mode,
        estimated_delivery_time=None,
    ):
        self.order_id = str(uuid.uuid4())  # auto generated
        self.items = items
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.delivery_mode = delivery_mode
        self.order_status = "Pending"
        self.estimated_delivery_time = estimated_delivery_time
        self.created_at = datetime.now()
        self.full_price = self.calculate_total()

    def calculate_total(self):
        return sum(item.price for item in self.items)

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "items": [item.to_dict() for item in self.items],
            "customer_name": self.customer_name,
            "customer_phone": self.customer_phone,
            "delivery_mode": self.delivery_mode,
            "order_status": self.order_status,
            "estimated_delivery_time": self.estimated_delivery_time,
            "created_at": self.created_at,
            "full_price": self.full_price,
        }


class PickupDelivery:
    def __init__(
        self,
        order_id,
        customer_name,
        customer_phone,
        rider_name,
        order_time,
        restaurant_address
    ):
        self.delivery_id = str(uuid.uuid4())
        self.order_id = order_id
        self.type = "pickup"
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.rider_name = rider_name
        self.order_time = order_time
        self.restaurant_address = restaurant_address
        self.created_at = datetime.now()

    def to_dict(self):
        return self.__dict__


class DoorstepDelivery:
    def __init__(
        self,
        order_id,
        street,
        zone,
        lodge_name,
        delivery_time,
        additional_info=None
    ):
        self.delivery_id = str(uuid.uuid4())
        self.order_id = order_id
        self.type = "doorstep"
        self.street = street
        self.zone = zone
        self.lodge_name = lodge_name
        self.delivery_time = delivery_time
        self.additional_info = additional_info
        self.created_at = datetime.now()

    def to_dict(self):
        return self.__dict__
