import os
from datetime import datetime
from fastapi import APIRouter, Depends, File, Form, Query, Request, UploadFile
from typing import Literal, Optional, Union
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.service.login_service import LoginService
from module_admin.service.tags_service import TagsService
from module_admin.entity.vo.tags_vo import DeleteTagsModel, TagsModel, TagsPageQueryModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil
from utils.upload_util import UploadUtil
from config.env import UploadConfig


tagsController = APIRouter(prefix='/scales/tags', dependencies=[Depends(LoginService.get_current_user)])


@tagsController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('scales:tags:list'))]
)
async def get_tags_list(
    request: Request,
    tags_page_query: TagsPageQueryModel = Query(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    tags_page_query_result = await TagsService.get_tags_list_services(query_db, tags_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=tags_page_query_result)


@tagsController.post('', dependencies=[Depends(CheckUserInterfaceAuth('scales:tags:add'))])
@ValidateFields(validate_model='add_tags')
@Log(title='标签管理', business_type=BusinessType.INSERT)
async def add_tags(
    request: Request,
    add_tags: TagsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_tags.create_by = current_user.user.user_name
    add_tags.create_time = datetime.now()
    add_tags.update_by = current_user.user.user_name
    add_tags.update_time = datetime.now()
    add_tags_result = await TagsService.add_tags_services(query_db, add_tags)
    logger.info(add_tags_result.message)

    return ResponseUtil.success(msg=add_tags_result.message)


@tagsController.put('', dependencies=[Depends(CheckUserInterfaceAuth('scales:tags:edit'))])
@ValidateFields(validate_model='edit_tags')
@Log(title='标签管理', business_type=BusinessType.UPDATE)
async def edit_tags(
    request: Request,
    edit_tags: TagsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_tags.update_by = current_user.user.user_name
    edit_tags.update_time = datetime.now()
    edit_tags_result = await TagsService.edit_tags_services(query_db, edit_tags)
    logger.info(edit_tags_result.message)

    return ResponseUtil.success(msg=edit_tags_result.message)


@tagsController.delete('/{tags_ids}', dependencies=[Depends(CheckUserInterfaceAuth('scales:tags:remove'))])
@Log(title='标签管理', business_type=BusinessType.DELETE)
async def delete_tags(request: Request, tags_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_tags = DeleteTagsModel(tags_ids=tags_ids)
    delete_tags_result = await TagsService.delete_tags_services(query_db, delete_tags)
    logger.info(delete_tags_result.message)

    return ResponseUtil.success(msg=delete_tags_result.message)


@tagsController.get(
    '/{tags_id}', response_model=TagsModel, dependencies=[Depends(CheckUserInterfaceAuth('scales:tags:query'))]
)
async def query_detail_tags(request: Request, tags_id: int, query_db: AsyncSession = Depends(get_db)):
    tags_detail_result = await TagsService.tags_detail_services(query_db, tags_id)
    logger.info(f'获取tags_id为{tags_id}的信息成功')

    return ResponseUtil.success(data=tags_detail_result)


@tagsController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('scales:tags:export'))])
@Log(title='标签管理', business_type=BusinessType.EXPORT)
async def export_tags_list(
    request: Request,
    tags_page_query: TagsPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    tags_query_result = await TagsService.get_tags_list_services(query_db, tags_page_query, is_page=False)
    tags_export_result = await TagsService.export_tags_list_services(tags_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(tags_export_result))


#更新图标
@tagsController.post('/avatar/{tags_id}', dependencies=[Depends(CheckUserInterfaceAuth('scales:tags:edit'))])
@Log(title='更新图标', business_type=BusinessType.UPDATE)
async def change_tags_avatar(
    request: Request,
    tags_id: str,
    avatarfile: bytes = File(),
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    if not tags_id:
        return ResponseUtil.failure(msg='标签ID不能为空')
    if avatarfile:
        relative_path = (
            f'tags/{datetime.now().strftime("%Y")}/{datetime.now().strftime("%m")}/{datetime.now().strftime("%d")}'
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
        edit_tags = TagsModel(
            tags_id=tags_id,
            avatar=f'{UploadConfig.UPLOAD_PREFIX}/{relative_path}/{avatar_name}',
            update_by=current_user.user.user_name,
            update_time=datetime.now(),
        )
        edit_tags_result = await TagsService.edit_tags_avatar_services(query_db, edit_tags)
        logger.info(edit_tags_result.message)

        return ResponseUtil.success(dict_content={'imgUrl': edit_tags.avatar}, msg=edit_tags_result.message)
    return ResponseUtil.failure(msg='上传图标异常，请联系管理员')
