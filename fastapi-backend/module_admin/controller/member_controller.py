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
    MemberProfileModel,
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

#获取会员列表
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

#新增会员
@memberController.post('', dependencies=[Depends(CheckUserInterfaceAuth('member:add'))])
@ValidateFields(validate_model='add_member')
@Log(title='会员管理', business_type=BusinessType.INSERT)
async def add_member(
    request: Request,
    add_member: CreateMemberModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    """
    新增会员
    :param query_db: 数据库会话
    :param current_user: 当前登陆用户
    :return: 成员列表
    """
    add_member.password = PwdUtil.get_password_hash(add_member.password)
    add_member.create_by = current_user.user.user_name
    add_member.create_at = datetime.now()
    add_member.update_by = current_user.user.user_name
    add_member.update_at = datetime.now()
    add_member_result = await MemberService.add_member_services(query_db, add_member)
    logger.info(add_member_result.message)

    return ResponseUtil.success(msg=add_member_result.message)


#编辑会员
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


#删除会员
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
@memberController.put('/resetPwd', dependencies=[Depends(CheckUserInterfaceAuth('member:resetPwd'))])
@Log(title='会员管理', business_type=BusinessType.UPDATE)
async def reset_member_pwd(
    request: Request,
    reset_member: EditMemberModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):

    edit_member = EditMemberModel(
        member_id=reset_member.member_id,
        password=PwdUtil.get_password_hash(reset_member.password),
        update_by=current_user.user.user_name,
        update_time=datetime.now(),
        type='pwd',
    )
    edit_member_result = await MemberService.edit_member_services(query_db, edit_member)
    logger.info(edit_member_result.message)

    return ResponseUtil.success(msg=edit_member_result.message)

#导入数据
@memberController.post('/importData', dependencies=[Depends(CheckUserInterfaceAuth('member:import'))])
@Log(title='会员管理', business_type=BusinessType.IMPORT)
async def batch_import_member(
    request: Request,
    file: UploadFile = File(...),
    update_support: bool = Query(),
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    batch_import_result = await MemberService.batch_import_member_services(
        request, query_db, file, update_support, current_user
    )
    logger.info(batch_import_result.message)

    return ResponseUtil.success(msg=batch_import_result.message)

#导入数据模板
@memberController.post('/importTemplate', dependencies=[Depends(CheckUserInterfaceAuth('member:import'))])
async def export_member_template(request: Request, query_db: AsyncSession = Depends(get_db)):
    member_import_template_result = await MemberService.get_member_import_template_services()
    logger.info('获取成功')

    return ResponseUtil.streaming(data=bytes2file_response(member_import_template_result))

#导出数据
@memberController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('member:export'))])
@Log(title='会员管理', business_type=BusinessType.EXPORT)
async def export_member_list(
    request: Request,
    member_page_query: MemberPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    member_query_result = await MemberService.get_member_list_services(
        query_db, member_page_query, is_page=False
    )
    member_export_result = await MemberService.export_member_list_services(member_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(member_export_result))

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

#################################以下是会员详细信息管理功能##############################


#更新会员头像
@memberController.post('/profile/avatar')
@Log(title='会员信息', business_type=BusinessType.UPDATE)
async def change_member_profile_avatar(
    request: Request,
    member_id: Optional[Union[int, Literal['']]] = '',
    avatarfile: bytes = File(),
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    if avatarfile:
        relative_path = (
            f'avatar/member/{datetime.now().strftime("%Y")}/{datetime.now().strftime("%m")}/{datetime.now().strftime("%d")}'
        )
        dir_path = os.path.join(UploadConfig.UPLOAD_PATH, relative_path)
        try:
            os.makedirs(dir_path)
        except FileExistsError:
            pass
        avatar_name = f'avatar_{datetime.now().strftime("%Y%m%d%H%M%S")}{UploadConfig.UPLOAD_MACHINE}{UploadUtil.generate_random_number()}.png'
        avatar_path = os.path.join(dir_path, avatar_name)
        with open(avatar_path, 'wb') as f:
            f.write(avatarfile)
        edit_member = EditMemberModel(
            member_id=member_id,
            avatar=f'{UploadConfig.UPLOAD_PREFIX}/{relative_path}/{avatar_name}',
            update_by=current_user.user.user_name,
            update_at=datetime.now(),
            type='avatar',
        )
        edit_member_result = await MemberService.edit_member_services(query_db, edit_member)
        logger.info(edit_member_result.message)

        return ResponseUtil.success(dict_content={'imgUrl': edit_member.avatar}, msg=edit_member_result.message)
    return ResponseUtil.failure(msg='上传图片异常，请联系管理员')