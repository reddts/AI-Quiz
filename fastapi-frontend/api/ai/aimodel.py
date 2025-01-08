from config.enums import ApiMethod
from utils.request import api_request


class AiModelApi:
    """
    ai模型管理模块相关接口
    """

    @classmethod
    def list_aimodel(cls, query: dict):
        """
        查询ai模型列表接口

        :param query: 查询ai模型参数
        :return:
        """
        return api_request(
            url='/ai/aimodel/list',
            method=ApiMethod.GET,
            params=query,
        )

    @classmethod
    def get_aimodel(cls, aimodel_id: int):
        """
        查询ai模型详情接口

        :param aimodel_id: ai模型id
        :return:
        """
        return api_request(
            url=f'/ai/aimodel/{aimodel_id}',
            method=ApiMethod.GET,
        )

    @classmethod
    def add_aimodel(cls, json: dict):
        """
        新增ai模型接口

        :param json: 新增ai模型参数
        :return:
        """
        return api_request(
            url='/ai/aimodel',
            method=ApiMethod.POST,
            json=json,
        )

    @classmethod
    def update_aimodel(cls, json: dict):
        """
        修改ai模型接口

        :param json: 修改ai模型参数
        :return:
        """
        return api_request(
            url='/ai/aimodel',
            method=ApiMethod.PUT,
            json=json,
        )

    @classmethod
    def del_aimodel(cls, aimodel_id: str):
        """
        删除ai模型接口

        :param aimodel_id: ai模型id
        :return:
        """
        return api_request(
            url=f'/ai/aimodel/{aimodel_id}',
            method=ApiMethod.DELETE,
        )

    @classmethod
    def export_aimodel(cls, data: dict):
        """
        导出ai模型接口

        :param data: 导出ai模型参数
        :return:
        """
        return api_request(
            url='/ai/aimodel/export',
            method=ApiMethod.POST,
            data=data,
            stream=True,
        )
    

    