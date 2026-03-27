from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

products = [
{"id":1,"name":"Wireless Mouse","price":499,"category":"Electronics","in_stock":True},
{"id":2,"name":"Notebook","price":99,"category":"Stationery","in_stock":True},
{"id":3,"name":"USB Hub","price":799,"category":"Electronics","in_stock":False},
{"id":4,"name":"Pen Set","price":49,"category":"Stationery","in_stock":True}
]

cart = []
orders = []

def find_product(product_id):
    for p in products:
        if p["id"] == product_id:
            return p
    return None

#Q1,Q3,Q4
@app.post("/cart/add")
def add_to_cart(product_id:int, quantity:int=1):

    product = find_product(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if not product["in_stock"]:
        raise HTTPException(status_code=400, detail=f"{product['name']} is out of stock")

    # check if already in cart
    for item in cart:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            item["subtotal"] = item["quantity"] * item["unit_price"]

            return {
                "message":"Cart updated",
                "cart_item":item
            }

    subtotal = product["price"] * quantity

    new_item = {
        "product_id":product_id,
        "product_name":product["name"],
        "quantity":quantity,
        "unit_price":product["price"],
        "subtotal":subtotal
    }

    cart.append(new_item)

    return {
        "message":"Added to cart",
        "cart_item":new_item
    }

# Q2
@app.get("/cart")
def view_cart():

    if not cart:
        return {"message":"Cart is empty"}

    total = sum(item["subtotal"] for item in cart)

    return {
        "items":cart,
        "item_count":len(cart),
        "grand_total":total
    }

# Q5
@app.delete("/cart/{product_id}")
def remove_item(product_id:int):

    for item in cart:
        if item["product_id"] == product_id:
            cart.remove(item)
            return {"message":"Item removed from cart"}

    raise HTTPException(status_code=404, detail="Item not found in cart")

class Checkout(BaseModel):
    customer_name:str
    delivery_address:str

# Q5 + BONUS
@app.post("/cart/checkout")
def checkout(data:Checkout):

    if not cart:
        raise HTTPException(status_code=400, detail="CART_EMPTY")

    grand_total = sum(item["subtotal"] for item in cart)

    for item in cart:
        order = {
            "order_id":len(orders)+1,
            "customer_name":data.customer_name,
            "product":item["product_name"],
            "quantity":item["quantity"],
            "subtotal":item["subtotal"],
            "delivery_address":data.delivery_address
        }

        orders.append(order)

    cart.clear()

    return {
        "message":"Checkout successful",
        "orders_placed":len(orders),
        "grand_total":grand_total
    }


@app.get("/orders")
def get_orders():

    return {
        "orders":orders,
        "total_orders":len(orders)
    }