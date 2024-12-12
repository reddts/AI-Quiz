from typing import Union
from config.enums import ApiMethod
from utils.request import api_request


class MemberApi:
    """
    会员管理模块相关接口
    """

    @classmethod
    def list_member(cls, query: dict):
        """
        查询会员列表接口

        :param query: 查询会员参数
        :return:
        """
        return api_request(
            url='/member/list',
            method=ApiMethod.GET,
            params=query,
        )

    @classmethod
    def get_member(cls, member_id: Union[int, str]):
        """
        查询会员详情接口

        :param member_id: 会员id
        :return:
        """
        return api_request(
            url=f'/member/{member_id}',
            method=ApiMethod.GET,
        )

    @classmethod
    def add_member(cls, json: dict):
        """
        新增会员接口

        :param json: 新增会员参数
        :return:
        """
        return api_request(
            url='/member',
            method=ApiMethod.POST,
            json=json,
        )

    @classmethod
    def update_member(cls, json: dict):
        """
        修改会员接口

        :param json: 修改会员参数
        :return:
        """
        return api_request(
            url='/member',
            method=ApiMethod.PUT,
            json=json,
        )

    @classmethod
    def del_member(cls, member_id: str):
        """
        删除会员接口

        :param user_id: 会员id
        :return:
        """
        return api_request(
            url=f'/member/{member_id}',
            method=ApiMethod.DELETE,
        )

    @classmethod
    def download_template(cls):
        """
        下载会员导入模板接口

        :return:
        """
        return api_request(
            url='/member/importTemplate',
            method=ApiMethod.POST,
            stream=True,
        )

    @classmethod
    def import_member(cls, file: bytes, update_support: bool):
        """
        导入会员接口

        :param file: 导入模板文件
        :param update_support: 是否更新已存在的会员数据
        :return:
        """
        return api_request(
            url='/member/importData',
            method=ApiMethod.POST,
            files={'file': file},
            params={'update_support': update_support},
        )

    @classmethod
    def export_member(cls, data: dict):
        """
        导出会员接口

        :param data: 导出会员参数
        :return:
        """
        return api_request(
            url='/member/export',
            method=ApiMethod.POST,
            data=data,
            stream=True,
        )

    @classmethod
    def reset_member_pwd(cls, member_id: int, password: str):
        """
        会员密码重置接口

        :param member_id: 会员id
        :param password: 会员密码
        :return:
        """
        return api_request(
            url='/member/resetPwd',
            method=ApiMethod.PUT,
            json=dict(member_id=member_id, password=password),
        )

    @classmethod
    def change_member_status(cls, member_id: int, status: str):
        """
        会员状态修改接口

        :param member_id: 会员id
        :param password: 会员状态
        :return:
        """
        return api_request(
            url='/member/changeStatus',
            method=ApiMethod.PUT,
            json=dict(member_id=member_id, status=status),
        )

    @classmethod
    def get_member_profile(cls):
        """
        查询会员个人信息接口

        :return:
        """
        return api_request(
            url='/member/profile',
            method=ApiMethod.GET,
        )

    @classmethod
    def update_member_profile(cls, json: dict):
        """
        修改会员个人信息接口

        :param json: 修改会员个人信息参数
        :return:
        """
        return api_request(
            url='/member/profile',
            method=ApiMethod.PUT,
            json=json,
        )

    @classmethod
    def update_member_pwd(cls, old_password: str, new_password: str):
        """
        会员个人密码重置接口

        :param old_password: 会员旧密码
        :param new_password: 会员新密码
        :return:
        """
        return api_request(
            url='/member/profile/updatePwd',
            method=ApiMethod.PUT,
            params=dict(old_password=old_password, new_password=new_password),
        )

    @classmethod
    def upload_avatar(cls, files: dict):
        """
        会员头像上传接口

        :param files: 会员头像参数
        :return:
        """
        return api_request(
            url='/member/profile/avatar',
            method=ApiMethod.POST,
            files=files,
        )

