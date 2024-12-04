from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime


class Member(Base):
    """
    用户信息表
    """
    __tablename__ = 'member'

    user_id = Column(Integer, primary_key=True, autoincrement=True, comment='用户ID')
    name = Column(String(100), default=None, comment='用户姓名')
    age = Column(Integer, default=None, comment='用户年龄')
    gender = Column(Enum('M', 'F'), default=None, comment='用户性别')
    email = Column(String(100), default=None, comment='用户邮箱')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    
    # Relationships
    recommendations = relationship("MemberAIRecommendations", back_populates="member")
    scale_answers = relationship("MemberScaleAnswers", back_populates="member")