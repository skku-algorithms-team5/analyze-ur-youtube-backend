PROMPT = """
Analyze YouTube video comments to determine public opinion. This involves counting positive and negative comments to calculate their respective ratios. Weight the comments based on their nuance and the number of "likes" each comment receives. Use a greedy algorithm approach for analysis to reflect the majority viewpoint. Provide advice for YouTubers on producing their next video based on this analysis. If negative comments are absent or minimal, select comments offering constructive opinions for the next video.

Response Format:
The response should be in a JSON object format (Korean language) with the following keys (including an optional field):

pos_ratio: The ratio of positive comments (float).
neg_ratio: The ratio of negative comments (float).
pos_comments: A list of 10 representative positive comments (List of strings).
neg_comments: A list of 10 representative negative comments (List of strings).
repre_comments: A list of 10 representative comments offering constructive opinions for the next video (Optional, List of strings).
analysis: Your analysis of the comments' overall opinion (string).
advice: Advice for YouTubers to assist in producing their next video (string).


Example:
{
  "pos_ratio": 0.8,
  "neg_ratio": 0.2,
  "pos_comments": [
    "혜인님 시험기간 브이로그 나의 비타민 같은 존재…😙 항상 보면서 너무 좋은 자극 받구 있어여!!! 종강까지 힘내봐여💗🤍",
    "같은 단대생이라 영상 뒤에 나오는 배경이 너무나도 반갑다능거죠 ㅎㅡㅎ 전 시험만 6개 보는데 커뮤니 역시 진짜 팀플 진짜 많네요...🥹 보면서 항상 대단하시구 정말 바쁘게 사시는 것 같아서 항상 챙겨보게 되는 것 같아요 같이 종강까지 파이팅해요 ❤",
    "혜인님 .. 영상 너무 재밌어요 😘😘 전 지금 팀플끝나고 통학러라 버스타고 집가면서 짬짬이 혜인님 브이로그 보고 있는데요.. 혜인님 영상은 바쁜 일상 사이에 빛나는 보석이랄까요.. 게다가 힐링까지ㅜㅠ 너무 감사합니다 이번주도 화이팅 기말도 화이팅입니다 !",
    "시들어간다니 15학번 8학년 재학중인 화석 입장에선 신입생과 다를바가 없네요...ㅋㅋㅋㅋㅋㅋ 시험기간 잘 버티셨군여 굳굿!!",
    "혠이님영상백번봤어요!현역고등한ㄱ생인데언니ㅠㅠㅠㅠㅠㅠㅠㅠ언니영상보고오늘도동기부여얻어가요오늘도내일도모레도언니영상만계속올려주시면계속볼게요~~~~항상좋아요구독백번씩누르겠습니다!!!!",
    "꺅!! 혠님 시험기간 브이로그 최고😍😍😍😍😍 늘 응원해용",
    "혹시 아이패드가 있는데 안쇄해서 보시는 이유가 있을까요?!! 전 패드로 보면 머리에 잘 안 들어오는 느낌이라 막상 패드에 필기해도 잘 안 보게 되는데.. 같은 이유인지 무게때문인건지??? 궁그매용",
    "위로도 받고 동기부여도 받았어요", "고등학생 때도 대학생 때도 시험 기간 브이로그는 혜인님이 최고다🫶🏻",
    "진짜 존경..",
    "기말고사를 앞둔 대학생 1학년인데 혜인님 영상 보면서 동기부여가 너무나도 돼서 시험공부 열심히 할 수 있을 거 같아요!! 🤍"
  ],
  "neg_comments": [
    "밑힌…. 셤 기간 과제팀플 쁘라쓰 , 지필공부 쁘라쓰… 편집까지G 눈물 흘리자마자 제 모습보는 줄요…😭 어떡해 해야지 뭐 “ 이렇게 사는 중… 제가 F였다면… 혠님처럼 벅벅 울었을 듯 … 완전 공감 ㅠㅠ",
    "혜인아 너 브이로그를 보면서 내가 공부를 얼마나 안 하는지 깨닫고 간다... (이제 깨닫기만 하는,),",
    "눈물나는거 보고 저도 울컥... 저도 너무 힘들면 눈물나거든요 ㅜㅜ 그래도 열심히 하시는 모습 보고 자극 받아서 같이 파이팅 하려구요! 그나저나 투명안경 정보도 궁금해요 !!",
    "혠이 님 하이 추천영상이 떠서 왔… 쩝 내 이름은 不良敎生, 썰렁 멘트의 달인이죠! 【나약함】을 이겨낼 【나】를 【약】속【함】! …응? 썰렁 꾸벅 후다닥",
    "이번 브이로그는 과제와 시험으로 인한 약간의 광기를 본것같기도 하네욬ㅋㅋㅋㅅㅋㅅㅋㅋ 그래도 브이로그 마지막쯤에는 자격증도 따서 행복해하는 모습이 보여서 저도 같이 웃었어요 ㅋㅋㅋㅋㅌ 축하해용❤",
    "후엥 저도 최근에 팀플 개빡센거 하나에 자잘자잘 팀플 4개, 시험공부, 과제 등등.. 해서 너무 번아웃이 와서 광광 울었어요..넘 피곤해서 발목도 다치고..그래서 한 4일동안 밖에 안나가니까 넘 좋더라구요..? 근데 언제까지 집에만 있을 순 없으니 다시...기말 공부하러 ㅌㅌ...",
    "어제 단국대 면접보고 왔는데 꼭 붙어서 언니 학교에서 보고싶어요🥹 언니 영상때문에 단국대 가고싶어졌었는데 꼭 갈수있었으면 좋겠어요 으아앙아아아아아으앙",
    "저도 잘하고 싶은데 마음처럼 잘 안되는 상황에 속상해서 눈물흘리다가 언니 영상 보고 웃고있어요...😊너무 공감되는 당황스러운 감정선..",
    "언니 울먹하는 게 너무 귀여운데 또 너무 공감ㅜㅜ… 전 1학년 2학기 들어왔는데 갑자기 공부량이 늘어서 미리미리 한 것 같은데 조급하고 그래요🥲 혹시 정리는 수업 끝날 때마다 하시나요???",
    "요즈 혠이님 새로운 영상 보고싶다 많이 생각했는데 이렇게 짜잔 중2~3 혠이님 시험기간 영상 보며 나도 고등학생때 공부 열심히 해야지 하며 빨리 고등학교 가길 바랬는데 .. 어느새 내년에 고3 😭 항상 시험기간이 올때마다 빠짐없이 혠이님 영상 보면서 힐링도 하고 기운도 얻어가요 !! 팬들의 힐링천사 🫶🏻 항상 좋은 영상 감사합니다ㅏ 🥰🥰"
  ],
  "repre_comments": [
    "혹시 가능하다면 제가 미컴 진학을 지망하는 예비고3인데 대학 Q&A 된다면 한 번 찍어주세요ㅜㅜ!!"
  ],
  "analysis": "대다수의 댓글이 긍정적인 의견을 가지고 있으며, 혜인님의 영상이 자극제나 힐링 도구로 작용하고 있음을 나타냅니다. 보는 이들에게 좋은 영향을 미치고 있으며 동기부여와 위로를 주고 있습니다. 부정적인 댓글은 드물며, 대부분의 부정적 의견은 시청자들의 자신의 상황에 대한 공감이나 힘든 점을 표현한 것으로 영상 자체의 문제를 짚는 것은 아닙니다.",
  "advice": "혜인님이 제공하고 있는 동기부여 및 공감대 형성 콘텐츠는 많은 구독자에게 긍정적인 영향을 미치고 있습니다. 시청자들이 원하는 대학생활 Q&A처럼 교육적이면서도 상호작용적인 요소를 갖춘 콘텐츠를 추가로 제작하여 시청자들의 정보욕구를 충족시키고 교류를 강화하는 것이 좋아 보입니다. 또한, 대학생활과 관련된 고민상담, 시험기간 극복법 공유 등을 주제로 한 콘텐츠를 만들어 시청자 참여를 높이는 전략을 채택할 수도 있습니다."
}
"""
