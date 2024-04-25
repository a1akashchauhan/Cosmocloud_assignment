from fastapi import FastAPI, HTTPException, Query,Request
from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import List, Optional
from pydantic import BaseModel
from redis import Redis
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse


app = FastAPI()

# Connecting with MongoDB


client = MongoClient("mongodb+srv://a1akashchauhanpersonal:heicuMmmOWSwt2hO@cluster0.jd1q1xj.mongodb.net/")
db = client["library_management"]
students_collection = db["students"]

#connecting with redis
redis_client = Redis(host='localhost', port=6379, db=0, decode_responses=True)



#middleware 
@app.middleware("http")
async def rate_limit(request: Request, call_next):
    user_id = request.headers.get('user_id')               #if userid is not provided
    if not user_id:
        error_message = {"error": "Header is Missing"}       
        return JSONResponse(status_code=429, content=error_message)

    
    today = datetime.now().strftime('%Y-%m-%d')
    key = f"{user_id}:{today}"

    current_count = int(redis_client.get(key) or 0)

    if current_count >= 5:                                 #condition to check no of rate limits
        error_message = {"error": "Rate Limit Exceeded"}
        return JSONResponse(status_code=429, content=error_message)

    # condition to check if requests happened yesterday
    if current_count == 0:
      
        tomorrow = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

        #TTL
        ttl = int((tomorrow - datetime.now()).total_seconds())
        redis_client.setex(key, ttl, 1)


    else:
        redis_client.incr(key)


    response = await call_next(request)
    return response


# Models
class Student(BaseModel):
    name: str
    age: int
    address: dict

class UpdateStudent(BaseModel):
    name: str = None
    age: int = None
    address: dict = None


@app.post("/students", status_code=201)
async def create_student(student: Student):

    result = students_collection.insert_one(student.model_dump())
    return {"id": str(result.inserted_id)}

@app.get("/students", status_code=200)
async def list_students(country: str = Query(None), age: int = Query(None)):

    query = {}
    if country:
        query["address.country"] = country
    if age is not None:
        query["age"] = {"$gte": age}


    students = students_collection.find(query, {"_id": 0})

    return {"data": list(students)}

@app.get("/students/{id}", status_code=200)
async def get_student(id: str):

    student = students_collection.find_one({"_id": ObjectId(id)}, {"_id": 0})

    if student:
        return student
    else:
        raise HTTPException(status_code=404, detail="Student not found")

@app.patch("/students/{id}", status_code=204)
async def update_student(id: str, student: UpdateStudent):

    update_fields = {}
    if student.name is not None:
        update_fields["name"] = student.name
    if student.age is not None:
        update_fields["age"] = student.age
    if student.address is not None:
        update_fields["address"] = student.address

    # Update student record in MongoDB
    students_collection.update_one({"_id": ObjectId(id)}, {"$set": update_fields})

@app.delete("/students/{id}", status_code=200)
async def delete_student(id: str):
    # Delete student record from MongoDB
    result = students_collection.delete_one({"_id": ObjectId(id)})
    
    if result.deleted_count == 1:
        return {"message": "Student deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Student not found")
    
