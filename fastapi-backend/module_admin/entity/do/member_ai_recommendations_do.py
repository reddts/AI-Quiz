from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime

class MemberAIRecommendations(Base):
    """
    用户 AI 建议答案表
    """
    __tablename__ = 'member_ai_recommendations'

    recommendation_id = Column(Integer, primary_key=True, autoincrement=True, comment='主键，用于唯一标识每条建议记录')
    user_id = Column(Integer, ForeignKey('member.user_id'), nullable=True, comment='关联到用户表 (member)')
    scale_id = Column(Integer, ForeignKey('scales.scale_id'), nullable=True, comment='关联到量表表 (scales)')
    answer_id = Column(Integer, ForeignKey('member_scale_answers.answer_id'), nullable=True, comment='关联到用户量表回答表')
    question = Column(String, comment='用户提出的问题内容')
    recommendation = Column(String, comment='AI 建议的答案')
    created_at = Column(DateTime, default=datetime.utcnow, comment='建议生成的时间')

    # Relationships
    member = relationship("Member", back_populates="recommendations")