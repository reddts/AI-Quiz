from config.enums import ApiMethod
from utils.request import api_request


class OnlineApi:
    """
    在线会员管理模块相关接口
    """

    @classmethod
    def list_online(cls, query: dict):
        """
        查询在线会员列表接口

        :param query: 查询在线会员参数
        :return:
        """
        return api_request(
            url='/member/online/list/page',
            method=ApiMethod.GET,
            params=query,
        )

    @classmethod
    def force_logout(cls, token_id: str):
        """
        强退会员接口

        :param token_id: 在线会员token
        :return:
        """
        return api_request(
            url=f'/member/online/{token_id}',
            method=ApiMethod.DELETE,
        )
