import requests

localhost_test_url = "http://localhost:8000/stream_analyze/?url=https://www.youtube.com/watch?v=tnSUTDcKhPU"
deploy_test_url = "https://port-0-analyze-ur-youtube-backend-3szcb0g2blp9bp0ek.sel5.cloudtype.app/stream_analyze/?url=https://www.youtube.com/watch?v=tnSUTDcKhPU"
with requests.get(localhost_test_url, stream=True) as r:
    for chunk in r.iter_content(None, decode_unicode=True):
        if chunk:
            print(chunk, end="", flush=True)
