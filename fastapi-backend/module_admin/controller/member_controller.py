import os
from datetime import datetime
from fastapi import APIRouter, Depends, File, Form, Query, Request, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal, Optional, Union
from pydantic_validation_decorator import ValidateFields
from config.get_db import get_db
from config.env import UploadConfig
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.data_scope import GetDataScope
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.member_vo import (
    MemberModel,
    MemberPageQueryModel,
    CreateMemberVO,
    UpdateMemberVO,
    UserDetailModel,
)
from module_admin.service.login_service import LoginService
from module_admin.service.member_service import MemberService
from config.enums import BusinessType
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.pwd_util import PwdUtil
from utils.response_util import ResponseUtil
from utils.upload_util import UploadUtil

# 初始化 router 实例
#router = APIRouter(prefix="/member", tags=["Members"])
memberController = APIRouter(prefix='/member', tags=["Member"])

@memberController.get("/list", response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('member:list'))])
async def get_all_members(request: Request,member_page_query: MemberPageQueryModel = Query(),query_db: AsyncSession = Depends(get_db),):
    """
    获取所有会员信息
    :param query_db: 数据库会话
    :return: 成员列表
    """
    # 获取分页数据
    member_page_query_result = await MemberService.get_all_members(
        query_db, member_page_query, is_page=True
    )
    logger.info('获取成功')

    return ResponseUtil.success(model_content=member_page_query_result)
    #return await MemberService.get_all_members(db)



@memberController.get("/{user_id}", response_model=MemberModel)
async def get_member_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    根据用户ID获取单个成员信息
    :param membeer_id: 用户ID
    :param db: 数据库会话
    :return: 成员信息
    """
    return await MemberService.get_member_by_id(db, user_id)

@memberController.post("/", response_model=MemberModel)
async def create_member(member: CreateMemberVO, db: AsyncSession = Depends(get_db)):
    """
    创建新的成员
    :param member: 新成员数据
    :param db: 数据库会话
    :return: 创建的成员信息
    """
    return await MemberService.create_member(db, member)

@memberController.put("/{user_id}", response_model=MemberModel)
async def update_member(user_id: int, member: UpdateMemberVO, db: AsyncSession = Depends(get_db)):
    """
    更新成员信息
    :param user_id: 用户ID
    :param member: 更新的成员数据
    :param db: 数据库会话
    :return: 更新后的成员信息
    """
    return await MemberService.update_member(db, user_id, member)

@memberController.delete("/{user_id}")
async def delete_member(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    删除成员
    :param user_id: 用户ID
    :param db: 数据库会话
    :return: 删除成功的提示信息
    """
    await MemberService.delete_member(db, user_id)
    return {"detail": "Member deleted successfully"}
