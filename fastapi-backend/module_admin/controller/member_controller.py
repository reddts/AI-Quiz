import os
from datetime import datetime
from fastapi import APIRouter, Depends, File, Form, Query, Request, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal, Optional, Union
from pydantic_validation_decorator import ValidateFields
from config.get_db import get_db
from config.env import UploadConfig
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.member_vo import (
    MemberPageQueryModel,
    CreateMemberModel,
    EditMemberModel,
    DeleteMemberModel,
    MemberModel,
)

from module_admin.entity.vo.user_vo import  CurrentUserModel
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
#memberController = APIRouter(prefix='/member', tags=["Member"])
memberController = APIRouter(prefix='/member', dependencies=[Depends(LoginService.get_current_user)])

@memberController.get("/list", response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('member:list'))])
async def get_all_members(
    request: Request,
    member_page_query: MemberPageQueryModel = Query(),
    query_db: AsyncSession = Depends(get_db),
):
    """
    获取所有会员信息
    :param query_db: 数据库会话
    :return: 成员列表
    """
    # 获取分页数据
    member_page_query_result = await MemberService.get_member_list_services(
        query_db, member_page_query, is_page=True
    )
    logger.info('获取成功')

    return ResponseUtil.success(model_content=member_page_query_result)
    #return await MemberService.get_all_members(db)


@memberController.post('', dependencies=[Depends(CheckUserInterfaceAuth('member:add'))])
@ValidateFields(validate_model='add_member')
@Log(title='会员管理', business_type=BusinessType.INSERT)
async def add_member(
    request: Request,
    add_member: CreateMemberModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_member.password = PwdUtil.get_password_hash(add_member.password)
    add_member.create_by = current_user.user.user_name
    add_member.create_at = datetime.now()
    add_member.update_by = current_user.user.user_name
    add_member.update_at = datetime.now()
    add_member_result = await MemberService.add_member_services(query_db, add_member)
    logger.info(add_member_result.message)

    return ResponseUtil.success(msg=add_member_result.message)



@memberController.put('', dependencies=[Depends(CheckUserInterfaceAuth('member:edit'))])
@ValidateFields(validate_model='edit_member')
@Log(title='会员管理', business_type=BusinessType.UPDATE)
async def edit_member(
    request: Request,
    edit_member: EditMemberModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
   
    edit_member.update_by = current_user.user.user_name
    edit_member.update_at = datetime.now()
    edit_member_result = await MemberService.edit_member_services(query_db, edit_member)
    logger.info(edit_member_result.message)

    return ResponseUtil.success(msg=edit_member_result.message)



@memberController.delete('/{member_ids}', dependencies=[Depends(CheckUserInterfaceAuth('member:remove'))])
@Log(title='会员管理', business_type=BusinessType.DELETE)
async def delete_member(
    request: Request,
    member_ids: str,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
       
    delete_member = DeleteMemberModel(member_ids=member_ids, update_by=current_user.user.user_name, update_time=datetime.now())
    delete_member_result = await MemberService.delete_member_services(query_db, delete_member)
    logger.info(delete_member_result.message)

    return ResponseUtil.success(msg=delete_member_result.message)

#修改状态
@memberController.put('/changeStatus', dependencies=[Depends(CheckUserInterfaceAuth('member:edit'))])
@Log(title='会员管理', business_type=BusinessType.UPDATE)
async def change_system_user_status(
    request: Request,
    change_member: EditMemberModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):    
    edit_member = EditMemberModel(
        member_id=change_member.member_id,
        status=change_member.status,
        update_by=current_user.user.user_name,
        update_at=datetime.now(),
        type='status',
    )
    edit_member_result = await MemberService.edit_member_services(query_db, edit_member)
    logger.info(edit_member_result.message)

    return ResponseUtil.success(msg=edit_member_result.message)

#重置密码
@userController.put('/resetPwd', dependencies=[Depends(CheckUserInterfaceAuth('member:resetPwd'))])
@Log(title='用户管理', business_type=BusinessType.UPDATE)
async def reset_system_user_pwd(
    request: Request,
    reset_user: EditUserModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
    data_scope_sql: str = Depends(GetDataScope('SysUser')),
):
    await UserService.check_user_allowed_services(reset_user)
    if not current_user.user.admin:
        await UserService.check_user_data_scope_services(query_db, reset_user.user_id, data_scope_sql)
    edit_user = EditUserModel(
        user_id=reset_user.user_id,
        password=PwdUtil.get_password_hash(reset_user.password),
        update_by=current_user.user.user_name,
        update_time=datetime.now(),
        type='pwd',
    )
    edit_user_result = await UserService.edit_user_services(query_db, edit_user)
    logger.info(edit_user_result.message)

    return ResponseUtil.success(msg=edit_user_result.message)

#获取会员信息
@memberController.get(
    '/{member_id}', response_model=MemberModel, dependencies=[Depends(CheckUserInterfaceAuth('member:query'))]
)
@memberController.get(
    '/', response_model=MemberModel, dependencies=[Depends(CheckUserInterfaceAuth('member:query'))]
)
async def query_detail_member(
    request: Request,
    member_id: Optional[Union[int, Literal['']]] = '',
    query_db: AsyncSession = Depends(get_db),
):
    
    detail_member_result = await MemberService.member_detail_services(query_db, member_id)
    logger.info(f'获取member_id为{member_id}的信息成功')

    return ResponseUtil.success(data=detail_member_result)