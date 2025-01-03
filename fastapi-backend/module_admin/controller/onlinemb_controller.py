from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.onlinemb_vo import DeleteOnlinembModel, OnlinembPageQueryModel, OnlinembQueryModel
from module_admin.service.login_service import LoginService
from module_admin.service.onlinemb_service import OnlinembService
from utils.log_util import logger
from utils.page_util import PageResponseModel, PageUtil
from utils.response_util import ResponseUtil


onlinembController = APIRouter(prefix='/member/online', dependencies=[Depends(LoginService.get_current_user)])


@onlinembController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('member:online:list'))]
)
async def get_monitor_onlinemb_list(request: Request, online_page_query: OnlinembQueryModel = Query()):
    # 获取全量数据
    online_query_result = await OnlinembService.get_onlinemb_list_services(request, online_page_query)
    logger.info('获取成功')

    return ResponseUtil.success(
        model_content=PageResponseModel(rows=online_query_result, total=len(online_query_result))
    )


@onlinembController.get(
    '/list/page',
    response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('member:online:list'))],
)
async def get_monitor_onlinemb_page_list(request: Request, online_page_query: OnlinembPageQueryModel = Query()):
    online_query = OnlinembQueryModel(**online_page_query.model_dump(by_alias=True))
    # 获取全量数据
    online_query_result = await OnlinembService.get_onlinemb_list_services(request, online_query)
    # 获取分页数据
    online_page_query_result = PageUtil.get_page_obj(
        online_query_result, online_page_query.page_num, online_page_query.page_size
    )
    logger.info('获取成功')

    return ResponseUtil.success(model_content=online_page_query_result)


@onlinembController.delete('/{token_ids}', dependencies=[Depends(CheckUserInterfaceAuth('member:online:forceLogout'))])
@Log(title='在线会员', business_type=BusinessType.FORCE)
async def delete_monitor_online(request: Request, token_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_online = DeleteOnlinembModel(token_ids=token_ids)
    delete_online_result = await OnlinembService.delete_onlinemb_services(request, delete_online)
    logger.info(delete_online_result.message)

    return ResponseUtil.success(msg=delete_online_result.message)
