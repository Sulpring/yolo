import time

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from io import BytesIO
from PIL import Image
import requests
from ultralytics import YOLO

from app.domain.product import Product
from app.database import SessionLocal

# AI 라우터 생성
ai_router = APIRouter()

# YOLO와 SAM 모델 로드
yolo_model = YOLO("yolov3.pt")  # YOLO 사전 학습된 가중치

# 요청 데이터 모델
class ImageRequest(BaseModel):
    name: str
    image_url: str  # 이미지 URL

# 데이터베이스 세션 종속성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# AI 프로세싱 엔드포인트
import logging

logging.basicConfig(level=logging.INFO)


@ai_router.post("/yolo-only")
async def process_image(request_data: ImageRequest, db: Session = Depends(get_db)):
    try:
        # 데이터베이스에서 img_url 검색
        print(f"Looking for img_url: {request_data.image_url}")
        product = db.query(Product).filter(Product.img_url == request_data.image_url).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product with the given img_url not found.")

        # 이미지 다운로드
        print("Downloading image...")
        response = requests.get(request_data.image_url, timeout=10)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch image from URL")

        # 이미지 변환 및 크기 조정
        print("Converting and resizing image...")
        image = Image.open(BytesIO(response.content)).convert("RGB")
        print(f"Original Image size: {image.size}, Image type: {type(image)}")  # 원본 이미지 로그

        # YOLO로 객체 탐지
        print("Processing with YOLO...")
        start_time = time.time()
        yolo_results = yolo_model(image)
        print(f"YOLO processing time: {time.time() - start_time} seconds")

        # YOLO 탐지 결과 처리
        results = []
        for box in yolo_results[0].boxes.data.cpu().numpy():
            x1, y1, x2, y2, confidence, class_id = box
            class_name = yolo_model.names[int(class_id)]
            bounding_box = [float(x1), float(y1), float(x2), float(y2)]

            # 결과 저장
            results.append({
                "class_name": class_name,
                "bounding_box": bounding_box,
                "confidence": float(confidence)
            })

        # 데이터베이스 업데이트
        product.ai_text = results
        db.commit()

        print(yolo_model.names)

        # 결과 반환
        return {"message": "YOLO processing complete", "results": results}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")










