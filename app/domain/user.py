from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"  # 이미 생성된 테이블 이름
    __table_args__ = {'extend_existing': True}  # 기존 테이블 확장 설정

    id = Column(String(255), primary_key=True)  # users 테이블의 id 필드
    password = Column(String(255), nullable=False)  # users 테이블의 password 필드

    # 관계 설정
    products = relationship("Product", back_populates="user")