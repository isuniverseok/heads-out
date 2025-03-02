from fastapi import FastAPI, HTTPException, Depends
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel
import random
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["headout"]
collection = db["test"]
users_collection = db["users"]  # New collection for users

# User Model
class User(BaseModel):
    username: str

# Register User
@app.post("/register")
def register_user(user: User):
    existing_user = users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    users_collection.insert_one({"username": user.username, "score": 0})
    return {"message": "User registered successfully", "username": user.username}

# Get Random Question
@app.get("/question")
def get_question():
    try:
        city = list(collection.aggregate([{ "$sample": { "size": 1 } }]))[0]
        possible_answers = [city["city"]]
        all_cities = list(collection.distinct("city"))
        wrong_answers = random.sample([c for c in all_cities if c != city["city"]], 2)
        choices = possible_answers + wrong_answers
        random.shuffle(choices) 
        return {
            "clues": city["clues"],
            "choices": choices,  
            "question_id": str(city["_id"])  
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Answer Submission
class AnswerRequest(BaseModel):
    question_id: str
    user_answer: str
    username: str  # Add username to track scores

@app.post("/answer")
def check_answer(data: AnswerRequest):
    try:
        city = collection.find_one({"_id": ObjectId(data.question_id)})
        if not city:
            raise HTTPException(status_code=404, detail="Question not found")
        is_correct = data.user_answer == city["city"]
        message = random.choice(city["fun_fact"])
        feedback = "🎉 Correct!" if is_correct else "😢 Incorrect!"
        
        # Update user score if correct
        if is_correct:
            users_collection.update_one({"username": data.username}, {"$inc": {"score": 1}})
        return {
            "correct": is_correct,
            "message": f"{message}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get User Score
@app.get("/score/{username}")
def get_score(username: str):
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": username, "score": user["score"]}

# Trivia Fact for City
@app.get("/trivia/{city}")
def get_trivia(city: str):
    city_data = collection.find_one({"city": city})
    if not city_data:
        raise HTTPException(status_code=404, detail="City not found")
    return {"trivia": random.choice(city_data["trivia"])}

# Challenge a Friend (Generate Invite Link)
@app.get("/challenge/{username}")
def challenge_friend(username: str):
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    invite_link = f"http://127.0.0.1:8000/play?invited_by={username}"
    return {"message": f"Challenge your friend!", "invite_link": invite_link, "score": user["score"]}

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
