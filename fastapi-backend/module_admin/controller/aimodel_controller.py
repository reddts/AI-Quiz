from datetime import datetime
from fastapi import APIRouter, Depends,  Form, Query, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.service.login_service import LoginService
from module_admin.service.aimodel_service import AiModelService
from module_admin.entity.vo.aimodel_vo import DeleteAiModelModel, AiModelModel, AiModelPageQueryModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil
from utils.common_util import bytes2file_response



aimodelController = APIRouter(prefix='/ai/aimodel', dependencies=[Depends(LoginService.get_current_user)])


@aimodelController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('ai:aimodel:list'))]
)
async def get_aimodel_list(
    request: Request,
    aimodel_page_query: AiModelPageQueryModel = Query(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    aimodel_page_query_result = await AiModelService.get_aimodel_list_services(query_db, aimodel_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=aimodel_page_query_result)


@aimodelController.put('', dependencies=[Depends(CheckUserInterfaceAuth('ai:aimodel:edit'))])
@ValidateFields(validate_model='edit_aimodel')
@Log(title='模型管理', business_type=BusinessType.UPDATE)
async def edit_aimodel(
    request: Request,
    edit_aimodel: AiModelModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_aimodel.update_by = current_user.user.user_name
    edit_aimodel.update_time = datetime.now()
    edit_aimodel_result = await AiModelService.edit_aimodel_services(query_db, edit_aimodel)
    logger.info(edit_aimodel_result.message)

    return ResponseUtil.success(msg=edit_aimodel_result.message)


@aimodelController.post('', dependencies=[Depends(CheckUserInterfaceAuth('ai:aimodel:add'))])
@ValidateFields(validate_model='add_aimodel')
@Log(title='模型管理', business_type=BusinessType.INSERT)
async def add_aimodel(
    request: Request,
    add_aimodel: AiModelModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    """
    Add a new AI model.

    Args:
        request (Request): The request object.
        add_aimodel (AiModelModel): The AI model data to be added.
        query_db (AsyncSession): The database session.
        current_user (CurrentUserModel): The current logged-in user.

    Returns:
        JSONResponse: The response containing the result of the add operation.
    """
    add_aimodel.create_by = current_user.user.user_name
    add_aimodel.create_time = datetime.now()
    add_aimodel.update_by = current_user.user.user_name
    add_aimodel.update_time = datetime.now()
    add_aimodel_result = await AiModelService.add_aimodel_services(query_db, add_aimodel)
    logger.info(add_aimodel_result.message)

    return ResponseUtil.success(msg=add_aimodel_result.message)


@aimodelController.delete('/{aimodel_ids}', dependencies=[Depends(CheckUserInterfaceAuth('ai:aimodel:remove'))])
@Log(title='模型管理', business_type=BusinessType.DELETE)
async def delete_aimodel(request: Request, aimodel_ids: str, query_db: AsyncSession = Depends(get_db)):
    """
    根据模型ID删除AI模型。

    参数:
        request (Request): 请求对象。
        aimodel_ids (str): 要删除的模型ID，多个ID用逗号分隔。
        query_db (AsyncSession): 数据库会话。

    返回:
        JSONResponse: 包含删除操作结果的响应。
    """
    delete_aimodel = DeleteAiModelModel(aimodel_ids=aimodel_ids)
    delete_aimodel_result = await AiModelService.delete_aimodel_services(query_db, delete_aimodel)
    logger.info(delete_aimodel_result.message)

    return ResponseUtil.success(msg=delete_aimodel_result.message)


@aimodelController.get(
    '/{aimodel_id}', response_model=AiModelModel, dependencies=[Depends(CheckUserInterfaceAuth('ai:aimodel:query'))]
)
async def query_detail_aimodel(request: Request, aimodel_id: int, query_db: AsyncSession = Depends(get_db)):
    aimodel_detail_result = await AiModelService.aimodel_detail_services(query_db, aimodel_id)
    logger.info(f'获取aimodel_id为{aimodel_id}的信息成功')

    return ResponseUtil.success(data=aimodel_detail_result)


@aimodelController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('ai:aimodel:export'))])
@Log(title='模型管理', business_type=BusinessType.EXPORT)
async def export_aimodel_list(
    request: Request,
    aimodel_page_query: AiModelPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    aimodel_query_result = await AiModelService.get_aimodel_list_services(query_db, aimodel_page_query, is_page=False)
    aimodel_export_result = await AiModelService.export_aimodel_list_services(aimodel_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(aimodel_export_result))
