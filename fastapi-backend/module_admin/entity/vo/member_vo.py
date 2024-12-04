from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class MemberVO(BaseModel):
    """
    会员表对应pydantic模型
    """

    user_id: Optional[int] = Field(None, description="用户ID")
    name: Optional[str] = Field(None, max_length=100, description="用户姓名")
    age: Optional[int] = Field(None, description="用户年龄")
    gender: Optional[str] = Field(None, description="用户性别", regex="^(M|F)$")
    email: Optional[EmailStr] = Field(None, description="用户邮箱")
    created_at: Optional[datetime] = Field(None, description="创建时间")

    class Config:
        orm_mode = True

class CreateMemberVO(BaseModel):
    """
    创建会员对应pydantic模型
    """
    name: Optional[str] = Field(None, max_length=100, description="用户姓名")
    age: Optional[int] = Field(None, description="用户年龄")
    gender: Optional[str] = Field(None, description="用户性别", regex="^(M|F)$")
    email: Optional[EmailStr] = Field(None, description="用户邮箱")

    class Config:
        orm_mode = True

class UpdateMemberVO(BaseModel):
    """
    更新会员对应pydantic模型
    """    
    name: Optional[str] = Field(None, max_length=100, description="用户姓名")
    age: Optional[int] = Field(None, description="用户年龄")
    gender: Optional[str] = Field(None, description="用户性别", regex="^(M|F)$")
    email: Optional[EmailStr] = Field(None, description="用户邮箱")

    class Config:
        orm_mode = True