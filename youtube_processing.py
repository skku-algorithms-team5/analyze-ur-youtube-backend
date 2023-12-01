from googleapiclient.discovery import build


def extract_video_id(url):
    parts = url.split("watch?v=")
    if len(parts) > 1:
        return parts[1].split("&")[0]
    return None


def get_comments(youtube, video_id):
    comments_with_likes = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        textFormat="plainText",
    )

    while request:
        response = request.execute()
        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            likes = item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
            comment_with_likes = f"{comment} (likes={likes})"
            comments_with_likes.append(comment_with_likes)
        request = youtube.commentThreads().list_next(request, response)

    return comments_with_likes


def initialize_youtube_client(api_key):
    return build("youtube", "v3", developerKey=api_key)
