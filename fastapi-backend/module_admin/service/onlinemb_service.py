import jwt
from fastapi import Request
from config.enums import RedisInitKeyConfig
from config.env import JwtConfig
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.entity.vo.onlinemb_vo import DeleteOnlinembModel, OnlinembQueryModel


class OnlinembService:
    """
    在线会员管理模块服务层
    """

    @classmethod
    async def get_onlinemb_list_services(cls, request: Request, query_object: OnlinembQueryModel):
        """
        获取在线会员表信息service

        :param request: Request对象
        :param query_object: 查询参数对象
        :return: 在线会员列表信息
        """
        member_access_token_keys = await request.app.state.redis.keys(f'{RedisInitKeyConfig.MEMBER_ACCESS_TOKEN.key}*')
        if not member_access_token_keys:
            member_access_token_keys = []
        member_access_token_values_list = [await request.app.state.redis.get(key) for key in member_access_token_keys]
        member_online_info_list = []
        for item in member_access_token_values_list:
            payload = jwt.decode(item, JwtConfig.jwt_secret_key, algorithms=[JwtConfig.jwt_algorithm])
            member_online_dict = dict(
                token_id=payload.get('session_id'),
                member_name=payload.get('member_name'),
                visit_name=payload.get('visit_name'),
                ipaddr=payload.get('member_login_info').get('ipaddr'),
                login_location=payload.get('member_login_info').get('login_location'),
                browser=payload.get('member_login_info').get('browser'),
                os=payload.get('member_login_info').get('os'),
                login_time=payload.get('member_login_info').get('login_time'),
            )
            if query_object.member_name and not query_object.ipaddr:
                if query_object.member_name == payload.get('member_login_info').get('ipaddr'):
                    member_online_info_list = [member_online_dict]
                    break
            elif not query_object.member_name and query_object.ipaddr:
                if query_object.ipaddr == payload.get('ipaddr'):
                    member_online_info_list = [member_online_dict]
                    break
            elif query_object.member_name and query_object.ipaddr:
                if query_object.member_name == payload.get('member_name') and query_object.ipaddr == payload.get(
                    'member_login_info'
                ).get('ipaddr'):
                    member_online_info_list = [member_online_dict]
                    break
            else:
                member_online_info_list.append(member_online_dict)

        return member_online_info_list

    @classmethod
    async def delete_onlinemb_services(cls, request: Request, page_object: DeleteOnlinembModel):
        """
        强退在线会员信息service

        :param request: Request对象
        :param page_object: 强退在线会员对象
        :return: 强退在线会员校验结果
        """
        if page_object.token_ids:
            token_id_list = page_object.token_ids.split(',')
            for token_id in token_id_list:
                await request.app.state.redis.delete(f'{RedisInitKeyConfig.MEMBER_ACCESS_TOKEN.key}:{token_id}')
            return CrudResponseModel(is_success=True, message='强退成功')
        else:
            raise ServiceException(message='传入session_id为空')
