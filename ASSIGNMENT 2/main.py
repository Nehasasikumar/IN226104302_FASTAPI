from fastapi import FastAPI
from pydantic import BaseModel,Field
from typing import Optional,List

app=FastAPI()

# Product list
products=[
{"id":1,"name":"Wireless Mouse","price":499,"category":"Electronics","in_stock":True},
{"id":2,"name":"Notebook","price":99,"category":"Stationery","in_stock":True},
{"id":3,"name":"Pen Set","price":49,"category":"Stationery","in_stock":True},
{"id":4,"name":"USB Cable","price":199,"category":"Electronics","in_stock":False},
{"id":5,"name":"Laptop Stand","price":1299,"category":"Electronics","in_stock":True},
{"id":6,"name":"Mechanical Keyboard","price":2499,"category":"Electronics","in_stock":True},
{"id":7,"name":"Webcam","price":1899,"category":"Electronics","in_stock":False}
]

#Q1
@app.get("/products/filter")
def filter_products(category:Optional[str]=None,max_price:Optional[int]=None,min_price:Optional[int]=None):

 result=products

 if category:
  result=[p for p in result if p["category"].lower()==category.lower()]

 if max_price:
  result=[p for p in result if p["price"]<=max_price]

 if min_price:
  result=[p for p in result if p["price"]>=min_price]

 return{
 "filtered_products":result,
 "count":len(result)
 }

#Q2
@app.get("/products/{product_id}/price")
def get_product_price(product_id:int):

 for product in products:
  if product["id"]==product_id:
   return{
   "name":product["name"],
   "price":product["price"]
   }

 return{"error":"Product not found"}

#Q3
feedback=[]

class CustomerFeedback(BaseModel):
 customer_name:str=Field(...,min_length=2)
 product_id:int=Field(...,gt=0)
 rating:int=Field(...,ge=1,le=5)
 comment:Optional[str]=Field(None,max_length=300)

@app.post("/feedback")
def submit_feedback(data:CustomerFeedback):

 feedback.append(data.dict())

 return{
 "message":"Feedback submitted successfully",
 "feedback":data.dict(),
 "total_feedback":len(feedback)
 }

#Q4
@app.get("/products/summary")
def product_summary():

 total_products=len(products)

 in_stock=[p for p in products if p["in_stock"]]
 out_stock=[p for p in products if not p["in_stock"]]

 most_expensive=max(products,key=lambda p:p["price"])
 cheapest=min(products,key=lambda p:p["price"])

 categories=list(set([p["category"] for p in products]))

 return{
 "total_products":total_products,
 "in_stock_count":len(in_stock),
 "out_of_stock_count":len(out_stock),
 "most_expensive":{"name":most_expensive["name"],"price":most_expensive["price"]},
 "cheapest":{"name":cheapest["name"],"price":cheapest["price"]},
 "categories":categories
 }

#Q5
orders=[]

class OrderItem(BaseModel):
 product_id:int=Field(...,gt=0)
 quantity:int=Field(...,ge=1,le=50)

class BulkOrder(BaseModel):
 company_name:str=Field(...,min_length=2)
 contact_email:str=Field(...,min_length=5)
 items:List[OrderItem]

@app.post("/orders/bulk")
def place_bulk_order(order:BulkOrder):

 confirmed=[]
 failed=[]
 grand_total=0

 for item in order.items:

  product=next((p for p in products if p["id"]==item.product_id),None)

  if not product:
   failed.append({"product_id":item.product_id,"reason":"Product not found"})
   continue

  if not product["in_stock"]:
   failed.append({"product_id":item.product_id,"reason":f"{product['name']} is out of stock"})
   continue

  subtotal=product["price"]*item.quantity

  confirmed.append({
  "product":product["name"],
  "qty":item.quantity,
  "subtotal":subtotal
  })

  grand_total+=subtotal

 return{
 "company":order.company_name,
 "confirmed":confirmed,
 "failed":failed,
 "grand_total":grand_total
 }

#BONUS
@app.post("/orders")
def create_order(product_id:int,quantity:int):

 order_id=len(orders)+1

 order={
 "order_id":order_id,
 "product_id":product_id,
 "quantity":quantity,
 "status":"pending"
 }

 orders.append(order)

 return order

@app.get("/orders/{order_id}")
def get_order(order_id:int):

 for order in orders:
  if order["order_id"]==order_id:
   return order

 return{"error":"Order not found"}

@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id:int):

 for order in orders:
  if order["order_id"]==order_id:
   order["status"]="confirmed"
   return order

 return{"error":"Order not found"}