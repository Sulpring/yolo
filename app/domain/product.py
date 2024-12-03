from sqlalchemy import Column, BigInteger, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Product(Base):
    __tablename__ = "product"  # 이미 생성된 테이블 이름
    __table_args__ = {'extend_existing': True}  # 기존 테이블 확장 설정


    user_id = Column(BigInteger, ForeignKey("users.id"))  # product 테이블의 user_id 필드
    name = Column(String(255), nullable=False)  # product 테이블의 name 필드
    code = Column(BigInteger, primary_key=True)  # product 테이블의 code 필드
    img_url = Column(String(255))  # product 테이블의 img_url 필드
    human_text = Column(String(255))  # product 테이블의 human_text 필드
    ai_text = Column(JSON, nullable=True)  # product 테이블의 ai_text 필드

    # 관계 설정
    user = relationship("User", back_populates="products")

