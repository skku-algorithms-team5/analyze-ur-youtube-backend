from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
from youtube_processing import extract_video_id, get_comments, initialize_youtube_client
from analyzer import CommentAnalyzer
from starlette.middleware.cors import CORSMiddleware
import prompt
import asyncio

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

youtube = initialize_youtube_client(YOUTUBE_API_KEY)
comment_analyzer = CommentAnalyzer(api_key=OPENAI_API_KEY, prompt=prompt.PROMPT)


def write_to_file(filename, content):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)


@app.get("/analyze")
async def analyze_youtube_comments(url: str):
    video_id = extract_video_id(url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    comments_with_likes = get_comments(youtube, video_id)

    if not comments_with_likes:
        raise HTTPException(status_code=404, detail="No comments found for this video")

    combined_text = "\n".join(comments_with_likes)
    write_to_file("comments2.txt", combined_text)

    result = comment_analyzer.get_answer(combined_text)
    write_to_file("answer2.txt", result)

    return {"result": result}


@app.get("/test")
async def test():
    return {"result": "Hello, World!"}


@app.get("/mocking_analyze")
async def mocking_analyze():
    print("openai api mocking...waiting")
    # IO Bound 작업을 mocking
    await asyncio.sleep(130)
    print("openai api mocked successfully")
    return {"result": "mocking api test"}
