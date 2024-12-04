from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from pydantic.json import Json


class MemberScaleAnswersVO(BaseModel):
    answer_id: Optional[int] = Field(None, description="回答ID")
    user_id: Optional[int] = Field(None, description="关联到用户表 (member)")
    scale_id: Optional[int] = Field(None, description="关联到量表表 (scales)")
    answer_data: Optional[Json] = Field(None, description="用户回答数据")
    completed_at: Optional[datetime] = Field(None, description="完成时间")

    class Config:
        orm_mode = True
