from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

movies = [
    {"id":1,"title":"Leo","genre":"Action","language":"Tamil","duration_mins":160,"ticket_price":200,"seats_available":50},
    {"id":2,"title":"Jailer","genre":"Drama","language":"Tamil","duration_mins":150,"ticket_price":180,"seats_available":40},
    {"id":3,"title":"Avengers","genre":"Action","language":"English","duration_mins":180,"ticket_price":250,"seats_available":30},
    {"id":4,"title":"Interstellar","genre":"Drama","language":"English","duration_mins":170,"ticket_price":220,"seats_available":20},
    {"id":5,"title":"Conjuring","genre":"Horror","language":"English","duration_mins":120,"ticket_price":150,"seats_available":25},
    {"id":6,"title":"Doctor","genre":"Comedy","language":"Tamil","duration_mins":140,"ticket_price":170,"seats_available":35}
]

bookings = []
booking_counter = 1

holds = []
hold_counter = 1

class BookingRequest(BaseModel):
    customer_name: str = Field(min_length=2)
    movie_id: int = Field(gt=0)
    seats: int = Field(gt=0, le=10)
    phone: str = Field(min_length=10)
    seat_type: str = "standard"
    promo_code: str = ""

class NewMovie(BaseModel):
    title: str = Field(min_length=2)
    genre: str = Field(min_length=2)
    language: str = Field(min_length=2)
    duration_mins: int = Field(gt=0)
    ticket_price: int = Field(gt=0)
    seats_available: int = Field(gt=0)

def find_movie(movie_id):
    for m in movies:
        if m["id"] == movie_id:
            return m
    return None

def calculate_ticket_cost(price, seats, seat_type, promo_code):
    multiplier = 1
    if seat_type == "premium":
        multiplier = 1.5
    elif seat_type == "recliner":
        multiplier = 2

    original = price * seats * multiplier

    discount = original
    if promo_code == "SAVE10":
        discount = original * 0.9
    elif promo_code == "SAVE20":
        discount = original * 0.8

    return original, discount

@app.get("/")
def home():
    return {"message":"Welcome to CineStar Booking"}

@app.get("/movies")
def get_movies():
    return {
        "movies":movies,
        "total":len(movies),
        "total_seats_available":sum(m["seats_available"] for m in movies)
    }

@app.get("/movies/summary")
def summary():
    return {
        "total_movies":len(movies),
        "max_price":max(m["ticket_price"] for m in movies),
        "min_price":min(m["ticket_price"] for m in movies),
        "total_seats":sum(m["seats_available"] for m in movies),
        "genre_count":{g:len([m for m in movies if m["genre"]==g]) for g in set(m["genre"] for m in movies)}
    }

@app.get("/movies/filter")
def filter_movies(genre:Optional[str]=None,language:Optional[str]=None,max_price:Optional[int]=None,min_seats:Optional[int]=None):
    result = movies
    if genre is not None:
        result = [m for m in result if m["genre"]==genre]
    if language is not None:
        result = [m for m in result if m["language"]==language]
    if max_price is not None:
        result = [m for m in result if m["ticket_price"]<=max_price]
    if min_seats is not None:
        result = [m for m in result if m["seats_available"]>=min_seats]
    return result

@app.get("/movies/search")
def search(keyword:str):
    result=[m for m in movies if keyword.lower() in m["title"].lower() or keyword.lower() in m["genre"].lower() or keyword.lower() in m["language"].lower()]
    if not result:
        return {"message":"No results"}
    return {"results":result,"total":len(result)}

@app.get("/movies/sort")
def sort_movies(sort_by:str="ticket_price"):
    return sorted(movies,key=lambda x:x[sort_by])

@app.get("/movies/page")
def paginate(page:int=1,limit:int=3):
    start=(page-1)*limit
    end=start+limit
    total=len(movies)
    return {
        "data":movies[start:end],
        "total":total,
        "total_pages":(total+limit-1)//limit
    }

@app.get("/movies/browse")
def browse(keyword:Optional[str]=None,genre:Optional[str]=None,language:Optional[str]=None,sort_by:str="ticket_price",order:str="asc",page:int=1,limit:int=3):
    result=movies

    if keyword:
        result=[m for m in result if keyword.lower() in m["title"].lower()]
    if genre:
        result=[m for m in result if m["genre"]==genre]
    if language:
        result=[m for m in result if m["language"]==language]

    result=sorted(result,key=lambda x:x[sort_by],reverse=(order=="desc"))

    start=(page-1)*limit
    end=start+limit

    return {
        "data":result[start:end],
        "total":len(result)
    }

@app.get("/movies/{movie_id}")
def get_movie(movie_id:int):
    movie = find_movie(movie_id)
    if not movie:
        raise HTTPException(404,"Movie not found")
    return movie

@app.get("/bookings")
def get_bookings():
    return {
        "bookings":bookings,
        "total":len(bookings),
        "total_revenue":sum(b["total_cost"] for b in bookings)
    }

@app.post("/bookings")
def create_booking(req:BookingRequest):
    global booking_counter

    movie = find_movie(req.movie_id)
    if not movie:
        raise HTTPException(404,"Movie not found")

    if movie["seats_available"] < req.seats:
        raise HTTPException(400,"Not enough seats")

    original, discounted = calculate_ticket_cost(movie["ticket_price"],req.seats,req.seat_type,req.promo_code)

    movie["seats_available"] -= req.seats

    booking = {
        "booking_id":booking_counter,
        "customer":req.customer_name,
        "movie":movie["title"],
        "seats":req.seats,
        "seat_type":req.seat_type,
        "original_cost":original,
        "total_cost":discounted
    }

    bookings.append(booking)
    booking_counter += 1

    return booking

@app.post("/movies")
def add_movie(req:NewMovie,response:Response):
    for m in movies:
        if m["title"].lower()==req.title.lower():
            raise HTTPException(400,"Duplicate movie")

    new_id = max(m["id"] for m in movies)+1
    movie = req.dict()
    movie["id"]=new_id
    movies.append(movie)

    response.status_code=201
    return movie

@app.put("/movies/{movie_id}")
def update_movie(movie_id:int,ticket_price:Optional[int]=None,seats_available:Optional[int]=None):
    movie = find_movie(movie_id)
    if not movie:
        raise HTTPException(404,"Not found")

    if ticket_price is not None:
        movie["ticket_price"]=ticket_price
    if seats_available is not None:
        movie["seats_available"]=seats_available

    return movie

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id:int):
    movie = find_movie(movie_id)
    if not movie:
        raise HTTPException(404,"Not found")

    for b in bookings:
        if b["movie"]==movie["title"]:
            raise HTTPException(400,"Movie has bookings")

    movies.remove(movie)
    return {"message":"Deleted"}

@app.post("/seat-hold")
def hold_seats(customer_name:str,movie_id:int,seats:int):
    global hold_counter

    movie = find_movie(movie_id)
    if not movie:
        raise HTTPException(404,"Movie not found")

    if movie["seats_available"]<seats:
        raise HTTPException(400,"Not enough seats")

    movie["seats_available"]-=seats

    hold={
        "hold_id":hold_counter,
        "customer":customer_name,
        "movie_id":movie_id,
        "seats":seats
    }

    holds.append(hold)
    hold_counter+=1

    return hold

@app.get("/seat-hold")
def get_holds():
    return holds

@app.post("/seat-confirm/{hold_id}")
def confirm_hold(hold_id:int):
    global booking_counter

    hold = next((h for h in holds if h["hold_id"]==hold_id),None)
    if not hold:
        raise HTTPException(404,"Hold not found")

    movie = find_movie(hold["movie_id"])

    booking={
        "booking_id":booking_counter,
        "customer":hold["customer"],
        "movie":movie["title"],
        "seats":hold["seats"],
        "total_cost":movie["ticket_price"]*hold["seats"]
    }

    bookings.append(booking)
    holds.remove(hold)
    booking_counter+=1

    return booking

@app.delete("/seat-release/{hold_id}")
def release_hold(hold_id:int):
    hold = next((h for h in holds if h["hold_id"]==hold_id),None)
    if not hold:
        raise HTTPException(404,"Hold not found")

    movie = find_movie(hold["movie_id"])
    movie["seats_available"]+=hold["seats"]

    holds.remove(hold)
    return {"message":"Released"}