from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
from youtube_processing import extract_video_id, get_comments, initialize_youtube_client
from analyzer import CommentAnalyzer
from starlette.middleware.cors import CORSMiddleware
import prompt

# Load environment variables
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")  # YouTube API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # OpenAI API Key

# Initialize FastAPI
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize YouTube and OpenAI clients
youtube = initialize_youtube_client(YOUTUBE_API_KEY)
comment_analyzer = CommentAnalyzer(api_key=OPENAI_API_KEY, prompt=prompt.PROMPT)


@app.get("/analyze")
async def analyze_youtube_comments(url: str):
    video_id = extract_video_id(url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    comments_with_likes = get_comments(youtube, video_id)
    if not comments_with_likes:
        raise HTTPException(status_code=404, detail="No comments found for this video")

    # Generate result using AnswerGenerator with comments and likes
    result = comment_analyzer.get_answer(comments_with_likes)

    print(result)

    return {"result": result}
