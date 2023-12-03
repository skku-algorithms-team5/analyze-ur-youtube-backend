import openai


class CommentAnalyzer:
    def __init__(self, api_key, model="gpt-4-1106-preview", prompt=""):
        # client = OpenAI(
        #     api_key=api_key,
        # )
        openai.api_key = api_key
        self.model = model
        self.prompt = prompt

    def get_answer(self, comments_with_likes):
        comments_text = "\n".join(comments_with_likes)

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.prompt},
                    {"role": "user", "content": comments_text},
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error occurred: {e}")
            return ""

    def stream_answer(self, comments_with_likes):
        comments_text = "\n".join(comments_with_likes)

        try:
            response_stream = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.prompt},
                    {"role": "user", "content": comments_text},
                ],
                stream=True,
            )
            for event in response_stream:
                if "content" in event["choices"][0].delta:
                    current_response = event["choices"][0].delta.content
                    yield current_response
        except Exception as e:
            print(f"Error occurred: {e}")
            return ""
