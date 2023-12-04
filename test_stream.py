import requests

localhost_url = "http://localhost:8000/stream_analyze/?url=https://www.youtube.com/watch?v=tnSUTDcKhPU"
deploy_url = "https://port-0-analyze-ur-youtube-backend-3szcb0g2blp9bp0ek.sel5.cloudtype.app/stream_analyze/?url=https://www.youtube.com/watch?v=tnSUTDcKhPU"
mocking_url = "http://localhost:8000/mocking_stream_analyze"
with requests.get(mocking_url, stream=True) as r:
    for chunk in r.iter_content(None, decode_unicode=True):
        if chunk:
            print(chunk, end="", flush=True)
