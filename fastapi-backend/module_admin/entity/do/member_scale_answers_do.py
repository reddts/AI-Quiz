from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime
from sqlalchemy.dialects.mysql import JSON


class MemberScaleAnswers(Base):
    """
    用户对量表的回答
    """
    __tablename__ = 'member_scale_answers'

    answer_id = Column(Integer, primary_key=True, autoincrement=True, comment='回答ID')
    user_id = Column(Integer, ForeignKey('member.user_id'), nullable=True, comment='关联到用户表 (member)')
    scale_id = Column(Integer, ForeignKey('scales.scale_id'), nullable=True, comment='关联到量表表 (scales)')
    answer_data = Column(JSON, default=None, comment='用户回答数据')
    completed_at = Column(DateTime, default=datetime.utcnow, comment='完成时间')

    # Relationships
    member = relationship("Member", back_populates="scale_answers")
