PROMPT = """
You'll be given comments from YouTube videos. Read each comment and analyze the comment 
opinion on the video by distinguishing between the positive and negative comments. 
At this time, public opinion is appropriately weighted based on how many comments there 
are in the Nuance and the number of "likes" for the comment, and based on this, it is 
analyzed so that the opinions of the majority of viewers can be known according to the 
greedy algorithm's approach. And based on this, please give me some advice that YouTubers
 can help produce the next video. If there are no negative comments or very few, please 
select comments with opinions that can be referenced to produce the next video. 
The response format is as follows:

The response MUST be a JSON object containing the following keys and language must be Korean.
Notice that there is optional field.
- pos_comments: List of string that contains 10 representative positive comments: List of string
- neg_comments: List of string that contains 10 representative negative comments: List of string
- repre_comments: List of string that contains 10 representative comments with opinions that can be referenced to produce the next video(Optional)
- Your analysis of the comments opinion: string
- advice that YouTubers can help produce the next video: string


Example:
{
  "pos_comments": ["잇썹은 기업 광고보다 소비자 위주 콘텐츠가 많아서 좋아 ㅎ", "알뜰폰 생기고 저렴한 요금제와 무약정이 너무 좋았고 자급제 생기고 통신사 2년 동안 써야하는 것이 사라져서 너무 좋아요.
구매과정이 심플해지고 정보가 투명해져서 혁신이라 생각해요, "이형은 돈만보고 유튜브하는게 아니라 정말 호갱 안당하는 정보를 많이줘서 최고인듯... 처음 마인드를 끝까지 가져가는 사람."],
  "neg_comments": [""],
  "repre_comments": [""],
  "analysis": [],
  "answer": 2,
  "index": 1,
  "commentary": "Option 2 is the correct answer because..."
}
"""
