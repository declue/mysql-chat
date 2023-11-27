from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()

# SQLAlchemy 설정
SQLALCHEMY_DATABASE_URL = "mysql://root:testpassword@localhost/chat"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 채팅 메시지 모델
class ChatMessage(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), index=True)
    message = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

class ChatMessageRequest(BaseModel):
    message: str

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)


def get_client_ip(request: Request):
    if "x-forwarded-for" in request.headers:
        # 프록시를 통한 접속의 경우
        ip = request.headers["x-forwarded-for"]
        ip = ip.split(",")[0]  # X-Forwarded-For 헤더는 쉼표로 구분된 IP 리스트일 수 있음
    else:
        # 직접 접속의 경우
        ip = request.client.host
    return ip

# HTML 파일 제공
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open('index.html', 'r') as file:
        return file.read()


# 채팅 메시지 저장
@app.post("/chat/")
async def post_chat_message(request: Request, chat_message: ChatMessageRequest):
    user_id = get_client_ip(request)
    db = SessionLocal()
    db_message = ChatMessage(user_id=user_id, message=chat_message.message)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    db.close()
    return {"user_id": user_id, "message": chat_message.message}

# 채팅 메시지 가져오기
@app.get("/chat/")
async def get_chat_messages():
    db = SessionLocal()
    messages = db.query(ChatMessage).all()
    for message in messages:
        message.user_id = '*.*' + '.'.join(message.user_id.split('.')[2:])
    db.close()
    return messages

