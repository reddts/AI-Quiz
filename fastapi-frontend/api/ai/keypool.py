from config.enums import ApiMethod
from utils.request import api_request


class KeypoolApi:
    """
    key池管理模块相关接口
    """

    @classmethod
    def list_keypool(cls, query: dict):
        """
        查询key池列表接口

        :param query: 查询key池参数
        :return:
        """
        return api_request(
            url='/ai/keypool/list',
            method=ApiMethod.GET,
            params=query,
        )

    @classmethod
    def get_keypool(cls, key_id: int):
        """
        查询key池详情接口

        :param key_id: key池id
        :return:
        """
        return api_request(
            url=f'/ai/keypool/{key_id}',
            method=ApiMethod.GET,
        )

    @classmethod
    def add_keypool(cls, json: dict):
        """
        新增key池接口

        :param json: 新增key池参数
        :return:
        """
        return api_request(
            url='/ai/keypool',
            method=ApiMethod.POST,
            json=json,
        )

    @classmethod
    def update_keypool(cls, json: dict):
        """
        修改key池接口

        :param json: 修改key池参数
        :return:
        """
        return api_request(
            url='/ai/keypool',
            method=ApiMethod.PUT,
            json=json,
        )

    @classmethod
    def del_keypool(cls, key_id: str):
        """
        删除key池接口

        :param key_id: key池id
        :return:
        """
        return api_request(
            url=f'/ai/keypool/{key_id}',
            method=ApiMethod.DELETE,
        )

    @classmethod
    def export_keypool(cls, data: dict):
        """
        导出key池接口

        :param data: 导出key池参数
        :return:
        """
        return api_request(
            url='/ai/keypool/export',
            method=ApiMethod.POST,
            data=data,
            stream=True,
        )
    