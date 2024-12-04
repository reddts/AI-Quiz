from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from services.member_service import MemberService
from schemas.member_vo import CreateMemberVO, UpdateMemberVO, MemberVO
from database import get_db
from typing import List

# 初始化 router 实例
router = APIRouter(prefix="/members", tags=["Members"])

@router.get("/", response_model=List[MemberVO])
async def get_all_members(db: AsyncSession = Depends(get_db)):
    """
    获取所有成员信息
    :param db: 数据库会话
    :return: 成员列表
    """
    return await MemberService.get_all_members(db)

@router.get("/{user_id}", response_model=MemberVO)
async def get_member_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    根据用户ID获取单个成员信息
    :param user_id: 用户ID
    :param db: 数据库会话
    :return: 成员信息
    """
    return await MemberService.get_member_by_id(db, user_id)

@router.post("/", response_model=MemberVO)
async def create_member(member: CreateMemberVO, db: AsyncSession = Depends(get_db)):
    """
    创建新的成员
    :param member: 新成员数据
    :param db: 数据库会话
    :return: 创建的成员信息
    """
    return await MemberService.create_member(db, member)

@router.put("/{user_id}", response_model=MemberVO)
async def update_member(user_id: int, member: UpdateMemberVO, db: AsyncSession = Depends(get_db)):
    """
    更新成员信息
    :param user_id: 用户ID
    :param member: 更新的成员数据
    :param db: 数据库会话
    :return: 更新后的成员信息
    """
    return await MemberService.update_member(db, user_id, member)

@router.delete("/{user_id}")
async def delete_member(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    删除成员
    :param user_id: 用户ID
    :param db: 数据库会话
    :return: 删除成功的提示信息
    """
    await MemberService.delete_member(db, user_id)
    return {"detail": "Member deleted successfully"}
