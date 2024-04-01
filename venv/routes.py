from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import app, db
from models import User, Product, CartItem
from schemas import ProductSchema, CartItemSchema

@app.route('/products')
def get_products():
    products = Product.query.all()
    product_schema = ProductSchema(many=True)
    return jsonify(product_schema.dump(products))

@app.route('/products/<int:product_id>')
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    product_schema = ProductSchema()
    return jsonify(product_schema.dump(product))

@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

@app.route('/cart/add/<int:product_id>', methods=['POST'])
@jwt_required()
def add_to_cart(product_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"msg": "Product not found"}), 404

    cart_item = CartItem.query.filter_by(user_id=user.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        new_cart_item = CartItem(user_id=user.id, product_id=product_id, quantity=1)
        db.session.add(new_cart_item)

    db.session.commit()
    return jsonify({"msg": "Product added to cart"}), 200

@app.route('/cart')
@jwt_required()
def view_cart():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    cart_items = CartItem.query.filter_by(user_id=user.id).all()
    cart_item_schema = CartItemSchema(many=True)
    return jsonify(cart_item_schema.dump(cart_items))

@app.route('/cart/remove/<int:product_id>', methods=['POST'])
@jwt_required()
def remove_from_cart(product_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    cart_item = CartItem.query.filter_by(user_id=user.id, product_id=product_id).first()
    if not cart_item:
        return jsonify({"msg": "Product not in cart"}), 404

    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({"msg": "Product removed from cart"}), 200

@app.route('/cart/clear', methods=['POST'])
@jwt_required()
def clear_cart():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    CartItem.query.filter_by(user_id=user.id).delete()
    db.session.commit()
    return jsonify({"msg": "Cart cleared"}), 200