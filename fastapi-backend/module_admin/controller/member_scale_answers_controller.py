from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from services.member_scale_answers_service import MemberScaleAnswerService
from schemas.member_scale_answers_vo import CreateAnswerVO, AnswerVO
from database import get_db
from typing import List

# 初始化 router 实例
router = APIRouter(prefix="/answers", tags=["Answers"])

@router.get("/", response_model=List[AnswerVO])
async def get_all_answers(db: AsyncSession = Depends(get_db)):
    """
    获取所有用户量表回答记录
    :param db: 数据库会话
    :return: 用户量表回答记录列表
    """
    return await MemberScaleAnswerService.get_all_answers(db)

@router.get("/{answer_id}", response_model=AnswerVO)
async def get_answer_by_id(answer_id: int, db: AsyncSession = Depends(get_db)):
    """
    根据回答ID获取单个量表回答记录
    :param answer_id: 回答记录ID
    :param db: 数据库会话
    :return: 量表回答记录
    """
    return await MemberScaleAnswerService.get_answer_by_id(db, answer_id)

@router.post("/", response_model=AnswerVO)
async def create_answer(answer: CreateAnswerVO, db: AsyncSession = Depends(get_db)):
    """
    创建新的量表回答记录
    :param answer: 新量表回答记录数据
    :param db: 数据库会话
    :return: 创建的量表回答记录
    """
    return await MemberScaleAnswerService.create_answer(db, answer)

@router.delete("/{answer_id}")
async def delete_answer(answer_id: int, db: AsyncSession = Depends(get_db)):
    """
    删除量表回答记录
    :param answer_id: 回答记录ID
    :param db: 数据库会话
    :return: 删除成功的提示信息
    """
    await MemberScaleAnswerService.delete_answer(db, answer_id)
    return {"detail": "Answer deleted successfully"}
