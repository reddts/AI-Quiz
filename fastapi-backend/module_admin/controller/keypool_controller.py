import os
from datetime import datetime
from fastapi import APIRouter, Depends, File, Form, Query, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.service.login_service import LoginService
from module_admin.service.keypool_service import KeypoolService
from module_admin.entity.vo.keypool_vo import DeleteKeypoolModel, KeypoolModel, KeypoolPageQueryModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


keypoolController = APIRouter(prefix='/ai/keypool', dependencies=[Depends(LoginService.get_current_user)])


@keypoolController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('ai:keypool:list'))]
)
async def get_keypool_list(
    request: Request,
    keypool_page_query: KeypoolPageQueryModel = Query(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    keypool_page_query_result = await KeypoolService.get_keypool_list_services(query_db, keypool_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=keypool_page_query_result)


@keypoolController.post('', dependencies=[Depends(CheckUserInterfaceAuth('ai:keypool:add'))])
@ValidateFields(validate_model='add_keypool')
@Log(title='key池管理', business_type=BusinessType.INSERT)
async def add_keypool(
    request: Request,
    add_keypool: KeypoolModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_keypool.create_by = current_user.user.user_name
    add_keypool.create_time = datetime.now()
    add_keypool.update_by = current_user.user.user_name
    add_keypool.update_time = datetime.now()
    add_keypool_result = await KeypoolService.add_keypool_services(query_db, add_keypool)
    logger.info(add_keypool_result.message)

    return ResponseUtil.success(msg=add_keypool_result.message)


@keypoolController.put('', dependencies=[Depends(CheckUserInterfaceAuth('ai:keypool:edit'))])
@ValidateFields(validate_model='edit_keypool')
@Log(title='key池管理', business_type=BusinessType.UPDATE)
async def edit_keypool(
    request: Request,
    edit_keypool: KeypoolModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_keypool.update_by = current_user.user.user_name
    edit_keypool.update_time = datetime.now()
    edit_keypool_result = await KeypoolService.edit_keypool_services(query_db, edit_keypool)
    logger.info(edit_keypool_result.message)

    return ResponseUtil.success(msg=edit_keypool_result.message)


@keypoolController.delete('/{key_ids}', dependencies=[Depends(CheckUserInterfaceAuth('ai:keypool:remove'))])
@Log(title='key池管理', business_type=BusinessType.DELETE)
async def delete_keypool(request: Request, key_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_keypool = DeleteKeypoolModel(key_ids=key_ids)
    delete_keypool_result = await KeypoolService.delete_keypool_services(query_db, delete_keypool)
    logger.info(delete_keypool_result.message)

    return ResponseUtil.success(msg=delete_keypool_result.message)


@keypoolController.get(
    '/{key_id}', response_model=KeypoolModel, dependencies=[Depends(CheckUserInterfaceAuth('ai:keypool:query'))]
)
async def query_detail_keypool(request: Request, key_id: int, query_db: AsyncSession = Depends(get_db)):
    keypool_detail_result = await KeypoolService.keypool_detail_services(query_db, key_id)
    logger.info(f'获取key_id为{key_id}的信息成功')

    return ResponseUtil.success(data=keypool_detail_result)


@keypoolController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('ai:keypool:export'))])
@Log(title='key池管理', business_type=BusinessType.EXPORT)
async def export_keypool_list(
    request: Request,
    keypool_page_query: KeypoolPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    keypool_query_result = await KeypoolService.get_keypool_list_services(query_db, keypool_page_query, is_page=False)
    keypool_export_result = await KeypoolService.export_keypool_list_services(keypool_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(keypool_export_result))
