# main.py
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import openai
import io
import os

app = FastAPI()

# OpenAIのAPIキーを環境変数から取得
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/tts")
async def tts(request: Request):
    # リクエストの中身をJSONとして読み取る
    data = await request.json()
    text = data.get("text", "")

    if not text:
        return {"error": "No text provided"}

    # OpenAIのTTS APIにリクエストを送る
    response = openai.audio.speech.create(
        model="tts-1",         # TTSモデル（最新版）
        voice="nova",          # 音声（nova, alloy, shimmer, fable, echo, onyx）
        input=text,            # 読み上げたいテキスト
        response_format="mp3"  # 返却されるファイル形式
    )

    # バイナリの音声ファイルとして読み取り
    audio_data = io.BytesIO(response.read())

    # クライアントにMP3ファイルとして返す
    return StreamingResponse(audio_data, media_type="audio/mpeg")

# デバッグ用
@app.get("/")
def root():
    return {"message": "Server is alive!"}