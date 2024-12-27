from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MemberAIRecommendationsVO(BaseModel):
    recommendation_id: Optional[int] = Field(None, description="主键，用于唯一标识每条建议记录")
    user_id: Optional[int] = Field(None, description="关联到用户表 (member)")
    scale_id: Optional[int] = Field(None, description="关联到量表表 (scales)")
    answer_id: Optional[int] = Field(None, description="关联到用户量表回答表")
    question: Optional[str] = Field(None, description="用户提出的问题内容")
    recommendation: Optional[str] = Field(None, description="AI 建议的答案")
    create_at: Optional[datetime] = Field(None, description="建议生成的时间")

    class Config:
        orm_mode = True
