from config.enums import ApiMethod
from utils.request import api_request


class TagsApi:
    """
    标签管理模块相关接口
    """

    @classmethod
    def list_tags(cls, query: dict):
        """
        查询标签列表接口

        :param query: 查询标签参数
        :return:
        """
        return api_request(
            url='/scales/tags/list',
            method=ApiMethod.GET,
            params=query,
        )

    @classmethod
    def get_tags(cls, tags_id: int):
        """
        查询标签详情接口

        :param tags_id: 标签id
        :return:
        """
        return api_request(
            url=f'/scales/tags/{tags_id}',
            method=ApiMethod.GET,
        )

    @classmethod
    def add_tags(cls, json: dict):
        """
        新增标签接口

        :param json: 新增标签参数
        :return:
        """
        return api_request(
            url='/scales/tags',
            method=ApiMethod.POST,
            json=json,
        )

    @classmethod
    def update_tags(cls, json: dict):
        """
        修改标签接口

        :param json: 修改标签参数
        :return:
        """
        return api_request(
            url='/scales/tags',
            method=ApiMethod.PUT,
            json=json,
        )

    @classmethod
    def del_tags(cls, tags_id: str):
        """
        删除标签接口

        :param tags_id: 标签id
        :return:
        """
        return api_request(
            url=f'/scales/tags/{tags_id}',
            method=ApiMethod.DELETE,
        )

    @classmethod
    def export_tags(cls, data: dict):
        """
        导出标签接口

        :param data: 导出标签参数
        :return:
        """
        return api_request(
            url='/scales/tags/export',
            method=ApiMethod.POST,
            data=data,
            stream=True,
        )
    
    @classmethod
    def upload_avatar(cls, tags_id: str,files: dict):
        """
        图标上传接口

        :param files: 图标参数
        :return:
        """
        return api_request(
            url=f'/scales/tags/avatar/{tags_id}',
            method=ApiMethod.POST,
            files=files,
        )
