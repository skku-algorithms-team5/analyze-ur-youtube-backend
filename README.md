# analyze-ur-youtube-backend

Analyze your YouYube video.

# Runtimes and Package Managers

- runtime version 정보는 `.tool-versions` 파일에 명시되어 있습니다.

## Backend

- python version: `3.11.6`
- package manager: `pip`
- framework: `fastapi`

# How to Run

## Backend

```zsh
pip install -r requirements.txt
uvicorn main:app --host=0.0.0.0 --port=8000
```

# How to Run Stress Test with Locust

```zsh
pip install -r requirements.txt
uvicorn main:app --host=0.0.0.0 --port=8000
locust -f test.py
```
