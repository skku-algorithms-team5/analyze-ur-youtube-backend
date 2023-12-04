from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
import os
from youtube_processing import extract_video_id, get_comments, initialize_youtube_client
from analyzer import CommentAnalyzer
from starlette.middleware.cors import CORSMiddleware
import prompt
import asyncio, time

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()

origins = [
    "https://analyze-ur-youtube-frontend.vercel.app",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080",
]

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


@app.get("/async_will_block")
async def async_will_block():
    time.sleep(10)
    return []


@app.get("/analyze")
def analyze_youtube_comments(url: str):
    video_id = extract_video_id(url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    comments_with_likes = get_comments(youtube, video_id)

    if not comments_with_likes:
        raise HTTPException(status_code=404, detail="No comments found for this video")

    combined_text = "\n".join(comments_with_likes)
    print(combined_text)
    write_to_file("comments2.txt", combined_text)

    result = comment_analyzer.get_answer(combined_text)
    print(result)
    write_to_file("answer2.txt", result)

    return {"result": result}


@app.get("/stream_analyze")
def stream_analyze_youtube_comments(url: str):
    video_id = extract_video_id(url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    comments_with_likes = get_comments(youtube, video_id)

    if not comments_with_likes:
        raise HTTPException(status_code=404, detail="No comments found for this video")

    combined_text = "\n".join(comments_with_likes)
    print(combined_text)
    write_to_file("comments2.txt", combined_text)

    return StreamingResponse(
        comment_analyzer.stream_answer(combined_text), media_type="text/event-stream"
    )


@app.get("/mocking_analyze")
async def mocking_analyze():
    print("openai api mocking...waiting")
    # IO Bound 작업을 mocking
    await asyncio.sleep(130)
    print("openai api mocked successfully")
    return {"result": "mocking api test"}


@app.get("/mocking_stream_analyze")
async def mocking_stream_analyze():
    TEST_STREAM_RESULT = """
    ```json
    {
    "pos_ratio": 0.9,
    "neg_ratio": 0.1,
    "pos_comments": [
        "좋은 영상 감사합니다 항상 잘보고 있어요 (likes=0)",
        "그냥 몬가 좋다.. (likes=0)",
        "판뚜님... 배경음악으로 자막내용 나오는게 너무 좋네요 ㅋㅋㅋㅋㅋㅋㅋ 오늘은 평소보다 많아서 더 좋아요 😂 (likes=0)",
        "ㅋㅋㅋㅋㅋ 구독은 꽤 전에 해놨는데 바빠서 못오다가 오랫만에 봤는데 너무 재밌어요 ㅋㅋㅋ 두 분이서 티키타카 너무 재밌고 다른 분야의 일을 집에서 볼 수 있다니 너무 신기해요!ㅎㅎㅎ 자주자주 놀러오겠습니다 >< (likes=0)",
        "주말에 머하시는지도 찍어주세요 ㅋㅋ (likes=0)",
        "ㅋㅋㅋㅋ 브이로그 영상 또한 매우 stable하군요! (likes=0)",
        "새롭게 빡 추천할 가게가 없어서 너무 슬프니다... (likes=0)",
        "역시 모든 직장인들은 같군요.. 오늘의 식단!!! (likes=0)",
        "편안하게 재밌는 느낌... 누워서 보는게 힐링이네요 (likes=1)",
        "판뚜님 영상 기다리고 있었습니다 ㅋㅋ 즐거워요 그냥 일상이 소소하게 재미있습니다 (likes=0)"
    ],
    "neg_comments": [
        "Fault 버거에서 무너졌습니다 ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ (likes=0)",
        "아침: 너무 일찍 왔는데? 따다다다담다다다다 (likes=0)",
        "이제 아예 재택 안하시나요? (likes=0)",
        "출근이 꿈입니다 (likes=0)",
        "아니 밥 왤케 잘나와요 (likes=0)",
        "아... 내일 월요일이네 (likes=0)",
        "아씨.. 내일 출근해야 하는데 왜 퇴근하고 싶지.. (likes=0)",
        "뭔가 새롭게 빡 추천할 가게가 없어서 너무 슬프니다... (likes=0)",
        "오늘의 식단!!! (likes=0)",
        "먼 미래에는 판뚜님 얼공한 영상을 꼭 보길!!! (likes=0)"
    ],
    "analysis": "영상에 대한 대다수의 댓글이 긍정적인 반응을 보이고 있으며, 구독자들이 즐겁게 시청하고 있음을 나타냅니다. 부정적인 댓글들은 특정한 문제점을 지적하기보다는 개인의 일상적인 불만이나 농담을 담고 있는 경우가 대부분입니다.",
    "advice": "구독자들이 영상의 일상적인 내용과 잔잔한 유머를 즐겨보는 것 같으니, 이 특징을 유지하면서 다양한 일상의 순간들을 포착해 시청자들과 공유하는 콘텐츠 전략을 지속하는 것이 좋을 것 같습니다. 구독자들이 관심있어 하는 평범한 브이로그 콘텐츠에 소소한 서비스나 정보를 추가하여 가치를 더할 수 있습니다."
    }
    ```
    """

    async def stream_event_generator():
        for line in TEST_STREAM_RESULT.splitlines():
            for char in line:
                yield "data: " + char + "\n\n"
                await asyncio.sleep(0.1)

    return StreamingResponse(stream_event_generator(), media_type="text/event-stream")
