from flask import Flask,jsonify
from src.orders_handlers import orders_bp
from src.food_handlers import food_bp
from src.delivery_handlers import delivery_bp
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

app.register_blueprint(orders_bp)
app.register_blueprint(food_bp, url_prefix="/foods")
app.register_blueprint(delivery_bp, url_prefix="/delivery")

@app.route("/",methods=["POST","GET"])
def index():
    return jsonify("Welcome to Holy Grills.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)