# Head's Out 

## Overview
**Head's Out** is an quiz game where users guess famous travel destinations based on clues. The game tracks user scores and allows them to challenge friends. The backend is built with Python (FastAPI) and uses MongoDB for storing user data. The frontend is deployed on Vercel, while the backend is hosted separately.

## Tech Stack

### Frontend
- HTML, CSS, JavaScript (very very basic)
- Hosted on **Vercel**

### Backend
- **FastAPI** (Python-based framework)
- **MongoDB** 
- Hosted on **Render**
- Runs inside **Docker** for portability 

## Features
- Users enter their name and start playing.
- Multiple-choice format with real-time feedback.
- If a user answers incorrectly, the game ends, showing an option to restart or challenge a friend.
- User scores are stored and can be tracked.
- Deployed for public access with backend API hosting.

---

## Setup Instructions

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Docker (if running MongoDB locally)

### Clone the Repository
```bash
 git clone <repo-url>
 cd heads-out
```

### Backend Setup

1. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run MongoDB via Docker (if local):**
```bash
docker run -d --name mongo -p 27017:27017 mongo
```

4. **Run the FastAPI server:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

5. **Access API Docs:**
Navigate to `http://127.0.0.1:8000/docs` for interactive API documentation.

### Frontend Setup

1. Navigate to the `frontend` directory (if structured separately) or modify `index.html`.
2. Update the backend API URL in the JavaScript file:
```js
const backendUrl = "https://your-backend-url.com";
```
3. Deploy frontend to Vercel:
```bash
npm install -g vercel
vercel
```

### Deployment
- **Backend:** Deployed on Render.com, AWS, or another cloud service.
- **Frontend:** Deployed on Vercel (`vercel --prod`).

---

## API Endpoints

### Fetch Question
**GET** `/question`
```json
{
  "question_id": 1,
  "clues": ["A famous city known for its Eiffel Tower"],
  "choices": ["Paris", "London", "Rome"]
}
```

### Submit Answer
**POST** `/answer`
```json
{
  "question_id": 1,
  "user_answer": "Paris"
}
```
Response:
```json
{
  "correct": true,
  "message": "Paris is the capital of France!"
}
```

---

## Future Enhancements
- Add a leaderboard for top players.
- Add unit tests to test the API calls.
- Implement OAuth-based login (Google/Facebook).
- Use in-memory database like Redis for caching usernames , user scores.
- Optimize MongoDB queries for faster response.
- Migrate backend to a Kubernetes setup for scalability.




