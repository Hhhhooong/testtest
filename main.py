from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import os
import requests
import time
import hmac
import hashlib
import base64
from dotenv import load_dotenv
from pydantic import BaseModel

# 加载环境变量
load_dotenv()

# 初始化FastAPI应用
app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化Supabase客户端
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# 讯飞星火认知大模型配置
XUNFEI_APP_ID = os.getenv("XUNFEI_APP_ID")
XUNFEI_API_KEY = os.getenv("XUNFEI_API_KEY")
XUNFEI_API_SECRET = os.getenv("XUNFEI_API_SECRET")

# 定义请求模型
class QuestionRequest(BaseModel):
    question: str

# 生成讯飞星火API的认证头
def get_xunfei_auth_headers():
    timestamp = str(int(time.time()))
    signature_origin = f"host: api.xf-yun.com\ndate: {timestamp}\nPOST /v1/chat/completions HTTP/1.1"
    signature_sha = hmac.new(
        XUNFEI_API_SECRET.encode('utf-8'),
        signature_origin.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    signature = base64.b64encode(signature_sha).decode('utf-8')
    authorization_origin = f"api_key={XUNFEI_API_KEY}, algorithm=hmac-sha256, headers=host date request-line, signature={signature}"
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Appid": XUNFEI_APP_ID,
        "Date": timestamp,
        "Authorization": authorization_origin
    }

# 根路径
@app.get("/")
def read_root():
    return {"message": "Pet Knowledge API"}

# 获取养宠知识列表
@app.get("/api/knowledge")
def get_knowledge():
    try:
        response = supabase.table("pet_knowledge").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 获取单个养宠知识详情
@app.get("/api/knowledge/{id}")
def get_knowledge_detail(id: int):
    try:
        response = supabase.table("pet_knowledge").select("*").eq("id", id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Knowledge not found")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# AI问答端点
@app.post("/api/ask")
def ask_ai(request: QuestionRequest):
    try:
        url = "https://api.xf-yun.com/v1/chat/completions"
        headers = get_xunfei_auth_headers()
        payload = {
            "model": "ep-20260317134345-k76r5",  # 讯飞星火模型
            "messages": [
                {"role": "system", "content": "你是一个专业的宠物知识顾问，回答关于宠物饲养、健康、行为等方面的问题。"},
                {"role": "user", "content": request.question}
            ],
            "temperature": 0.7
        }
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        if "choices" in response_data and len(response_data["choices"]) > 0:
            return {"answer": response_data["choices"][0]["message"]["content"]}
        else:
            raise HTTPException(status_code=500, detail="AI response error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))