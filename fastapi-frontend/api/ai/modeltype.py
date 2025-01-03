from config.enums import ApiMethod
from utils.request import api_request


class ModeltypeApi:
    """
    模型分类管理模块相关接口
    """

    @classmethod
    def list_modeltype(cls, query: dict):
        """
        查询模型分类列表接口

        :param query: 查询模型分类参数
        :return:
        """
        return api_request(
            url='/ai/modeltype/list',
            method=ApiMethod.GET,
            params=query,
        )

    @classmethod
    def get_modeltype(cls, type_id: int):
        """
        查询模型分类详情接口

        :param type_id: 模型分类id
        :return:
        """
        return api_request(
            url=f'/ai/modeltype/{type_id}',
            method=ApiMethod.GET,
        )

    @classmethod
    def add_modeltype(cls, json: dict):
        """
        新增模型分类接口

        :param json: 新增模型分类参数
        :return:
        """
        return api_request(
            url='/ai/modeltype',
            method=ApiMethod.POST,
            json=json,
        )

    @classmethod
    def update_modeltype(cls, json: dict):
        """
        修改模型分类接口

        :param json: 修改模型分类参数
        :return:
        """
        return api_request(
            url='/ai/modeltype',
            method=ApiMethod.PUT,
            json=json,
        )

    @classmethod
    def del_modeltype(cls, type_id: str):
        """
        删除模型分类接口

        :param type_id: 模型分类id
        :return:
        """
        return api_request(
            url=f'/ai/modeltype/{type_id}',
            method=ApiMethod.DELETE,
        )

