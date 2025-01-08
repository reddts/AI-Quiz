from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.dao.keypool_dao import KeypoolDao
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.entity.vo.keypool_vo import DeleteKeypoolModel, KeypoolModel, KeypoolPageQueryModel
from utils.common_util import export_list2excel, SqlalchemyUtil


class KeypoolService:
    """
    key池管理模块服务层
    """

    @classmethod
    async def get_keypool_list_services(
        cls, query_db: AsyncSession, query_object: KeypoolPageQueryModel, is_page: bool = False
    ):
        """
        获取key池列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: key池列表信息对象
        """
        keypool_list_result = await KeypoolDao.get_keypool_list(query_db, query_object, is_page)

        return keypool_list_result

    @classmethod
    async def check_keypool_name_unique_services(cls, query_db: AsyncSession, page_object: KeypoolModel):
        """
        检查key池名称是否唯一service

        :param query_db: orm对象
        :param page_object: key池对象
        :return: 校验结果
        """
        key_id = -1 if page_object.key_id is None else page_object.key_id
        keypool = await KeypoolDao.get_keypool_detail_by_info(query_db, KeypoolModel(key_name=page_object.key_name))
        if keypool and keypool.key_id != key_id:
            return CommonConstant.NOT_UNIQUE
        return CommonConstant.UNIQUE

    @classmethod
    async def add_keypool_services(cls, query_db: AsyncSession, page_object: KeypoolModel):
        """
        新增key池信息service

        :param query_db: orm对象
        :param page_object: 新增key池对象
        :return: 新增key池校验结果
        """
        if not await cls.check_keypool_name_unique_services(query_db, page_object):
            raise ServiceException(message=f'新增Key{page_object.key_name}失败，Key名称已存在')
        else:
            try:
                await KeypoolDao.add_keypool_dao(query_db, page_object)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='新增成功')
            except Exception as e:
                await query_db.rollback()
                raise e

    @classmethod
    async def edit_keypool_services(cls, query_db: AsyncSession, page_object: KeypoolModel):
        """
        编辑key池信息service

        :param query_db: orm对象
        :param page_object: 编辑key池对象
        :return: 编辑key池校验结果
        """
        edit_keypool = page_object.model_dump(exclude_unset=True)
        keypool_info = await cls.keypool_detail_services(query_db, page_object.key_id)
        if keypool_info.key_id:
            if not await cls.check_keypool_name_unique_services(query_db, page_object):
                raise ServiceException(message=f'修改Key{page_object.key_name}失败，Key名称已存在')           
            else:
                try:
                    await KeypoolDao.edit_keypool_dao(query_db, edit_keypool)
                    await query_db.commit()
                    return CrudResponseModel(is_success=True, message='更新成功')
                except Exception as e:
                    await query_db.rollback()
                    raise e
        else:
            raise ServiceException(message='key池不存在')

    @classmethod
    async def delete_keypool_services(cls, query_db: AsyncSession, page_object: DeleteKeypoolModel):
        """
        删除key池信息service

        :param query_db: orm对象
        :param page_object: 删除key池对象
        :return: 删除key池校验结果
        """
        if page_object.key_ids:
            keypool_id_list = page_object.key_ids.split(',')
            try:
                for key_id in keypool_id_list:
                    await KeypoolDao.delete_keypool_dao(query_db, KeypoolModel(key_id=key_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入key池id为空')

    @classmethod
    async def keypool_detail_services(cls, query_db: AsyncSession, key_id: int):
        """
        获取key池详细信息service

        :param query_db: orm对象
        :param key_id: key池id
        :return: key池id对应的信息
        """
        keypool = await KeypoolDao.get_keypool_detail_by_id(query_db, key_id=key_id)
        if keypool:
            result = KeypoolModel(**SqlalchemyUtil.serialize_result(keypool))
        else:
            result = KeypoolModel(**dict())

        return result

    @staticmethod
    async def export_keypool_list_services(keypool_list: List):
        """
        导出key池信息service

        :param keypool_list: key池信息列表
        :return: key池信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'key_id': 'key编号',
            'key_name': 'key名称',
            'key_token': 'keyTOKEN',
            'key_typeid': 'key分类',
            'status': '状态',
            'disablereason': '停用原因',
            'create_by': '创建者',
            'create_time': '创建时间',
            'update_by': '更新者',
            'update_time': '更新时间',
            'remark': '备注',
        }

        data = keypool_list

        for item in data:
            if item.get('status') == '0':
                item['status'] = '正常'
            else:
                item['status'] = '停用'
        new_data = [
            {mapping_dict.get(key): value for key, value in item.items() if mapping_dict.get(key)} for item in data
        ]
        binary_data = export_list2excel(new_data)

        return binary_data
