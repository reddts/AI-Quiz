import os
from datetime import datetime
from fastapi import APIRouter, Depends,  Query, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.service.login_service import LoginService
from module_admin.service.modeltype_service import ModeltypeService
from module_admin.entity.vo.modeltype_vo import DeleteModeltypeModel, ModeltypeModel, ModeltypePageQueryModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil



modeltypeController = APIRouter(prefix='/ai/modeltype', dependencies=[Depends(LoginService.get_current_user)])


@modeltypeController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('ai:modeltype:list'))]
)
async def get_modeltype_list(
    request: Request,
    modeltype_page_query: ModeltypePageQueryModel = Query(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    modeltype_page_query_result = await ModeltypeService.get_modeltype_list_services(query_db, modeltype_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=modeltype_page_query_result)


@modeltypeController.post('', dependencies=[Depends(CheckUserInterfaceAuth('ai:modeltype:add'))])
@ValidateFields(validate_model='add_modeltype')
@Log(title='模型分类管理', business_type=BusinessType.INSERT)
async def add_modeltype(
    request: Request,
    add_modeltype: ModeltypeModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_modeltype.create_by = current_user.user.user_name
    add_modeltype.create_time = datetime.now()
    add_modeltype.update_by = current_user.user.user_name
    add_modeltype.update_time = datetime.now()
    add_modeltype_result = await ModeltypeService.add_modeltype_services(query_db, add_modeltype)
    logger.info(add_modeltype_result.message)

    return ResponseUtil.success(msg=add_modeltype_result.message)


@modeltypeController.put('', dependencies=[Depends(CheckUserInterfaceAuth('ai:modeltype:edit'))])
@ValidateFields(validate_model='edit_modeltype')
@Log(title='模型分类管理', business_type=BusinessType.UPDATE)
async def edit_modeltype(
    request: Request,
    edit_modeltype: ModeltypeModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_modeltype.update_by = current_user.user.user_name
    edit_modeltype.update_time = datetime.now()
    edit_modeltype_result = await ModeltypeService.edit_modeltype_services(query_db, edit_modeltype)
    logger.info(edit_modeltype_result.message)

    return ResponseUtil.success(msg=edit_modeltype_result.message)


@modeltypeController.delete('/{type_ids}', dependencies=[Depends(CheckUserInterfaceAuth('ai:modeltype:remove'))])
@Log(title='模型分类管理', business_type=BusinessType.DELETE)
async def delete_modeltype(request: Request, type_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_modeltype = DeleteModeltypeModel(modeltype_ids=type_ids)
    delete_modeltype_result = await ModeltypeService.delete_modeltype_services(query_db, delete_modeltype)
    logger.info(delete_modeltype_result.message)

    return ResponseUtil.success(msg=delete_modeltype_result.message)


@modeltypeController.get(
    '/{type_id}', response_model=ModeltypeModel, dependencies=[Depends(CheckUserInterfaceAuth('ai:modeltype:query'))]
)
async def query_detail_modeltype(request: Request, type_id: int, query_db: AsyncSession = Depends(get_db)):
    modeltype_detail_result = await ModeltypeService.modeltype_detail_services(query_db, type_id)
    logger.info(f'获取type_id为{type_id}的信息成功')

    return ResponseUtil.success(data=modeltype_detail_result)


