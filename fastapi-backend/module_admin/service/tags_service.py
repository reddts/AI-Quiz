from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.dao.tags_dao import TagsDao
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.entity.vo.tags_vo import DeleteTagsModel, TagsModel, TagsPageQueryModel
from utils.common_util import export_list2excel, SqlalchemyUtil


class TagsService:
    """
    标签管理模块服务层
    """

    @classmethod
    async def get_tags_list_services(
        cls, query_db: AsyncSession, query_object: TagsPageQueryModel, is_page: bool = False
    ):
        """
        获取标签列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 标签列表信息对象
        """
        tags_list_result = await TagsDao.get_tags_list(query_db, query_object, is_page)

        return tags_list_result

    @classmethod
    async def check_tags_name_unique_services(cls, query_db: AsyncSession, page_object: TagsModel):
        """
        检查标签名称是否唯一service

        :param query_db: orm对象
        :param page_object: 标签对象
        :return: 校验结果
        """
        tags_id = -1 if page_object.tags_id is None else page_object.tags_id
        tags = await TagsDao.get_tags_detail_by_info(query_db, TagsModel(tags_name=page_object.tags_name))
        if tags and tags.tags_id != tags_id:
            return CommonConstant.NOT_UNIQUE
        return CommonConstant.UNIQUE

    @classmethod
    async def check_tags_code_unique_services(cls, query_db: AsyncSession, page_object: TagsModel):
        """
        检查标签编码是否唯一service

        :param query_db: orm对象
        :param page_object: 标签对象
        :return: 校验结果
        """
        tags_id = -1 if page_object.tags_id is None else page_object.tags_id
        tags = await TagsDao.get_tags_detail_by_info(query_db, TagsModel(tags_code=page_object.tags_code))
        if tags and tags.tags_id != tags_id:
            return CommonConstant.NOT_UNIQUE
        return CommonConstant.UNIQUE

    @classmethod
    async def add_tags_services(cls, query_db: AsyncSession, page_object: TagsModel):
        """
        新增标签信息service

        :param query_db: orm对象
        :param page_object: 新增标签对象
        :return: 新增标签校验结果
        """
        if not await cls.check_tags_name_unique_services(query_db, page_object):
            raise ServiceException(message=f'新增标签{page_object.tags_name}失败，标签名称已存在')
        elif not await cls.check_tags_code_unique_services(query_db, page_object):
            raise ServiceException(message=f'新增标签{page_object.tags_name}失败，标签编码已存在')
        else:
            try:
                await TagsDao.add_tags_dao(query_db, page_object)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='新增成功')
            except Exception as e:
                await query_db.rollback()
                raise e

    @classmethod
    async def edit_tags_services(cls, query_db: AsyncSession, page_object: TagsModel):
        """
        编辑标签信息service

        :param query_db: orm对象
        :param page_object: 编辑标签对象
        :return: 编辑标签校验结果
        """
        edit_tags = page_object.model_dump(exclude_unset=True)
        tags_info = await cls.tags_detail_services(query_db, page_object.tags_id)
        if tags_info.tags_id:
            if not await cls.check_tags_name_unique_services(query_db, page_object):
                raise ServiceException(message=f'修改标签{page_object.tags_name}失败，标签名称已存在')
            elif not await cls.check_tags_code_unique_services(query_db, page_object):
                raise ServiceException(message=f'修改标签{page_object.tags_name}失败，标签编码已存在')
            else:
                try:
                    await TagsDao.edit_tags_dao(query_db, edit_tags)
                    await query_db.commit()
                    return CrudResponseModel(is_success=True, message='更新成功')
                except Exception as e:
                    await query_db.rollback()
                    raise e
        else:
            raise ServiceException(message='标签不存在')
        
    @classmethod
    async def edit_tags_avatar_services(cls, query_db: AsyncSession, page_object: TagsModel):
        """
        编辑标签图标service

        :param query_db: orm对象
        :param page_object: 编辑标签对象
        :return: 编辑标签校验结果
        """
        edit_tags = page_object.model_dump(exclude_unset=True)
        tags_info = await cls.tags_detail_services(query_db, page_object.tags_id)
        if tags_info.tags_id:            
            try:
                await TagsDao.edit_tags_dao(query_db, edit_tags)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新图标成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='标签不存在')

    @classmethod
    async def delete_tags_services(cls, query_db: AsyncSession, page_object: DeleteTagsModel):
        """
        删除标签信息service

        :param query_db: orm对象
        :param page_object: 删除标签对象
        :return: 删除标签校验结果
        """
        if page_object.tags_ids:
            tags_id_list = page_object.tags_ids.split(',')
            try:
                for tags_id in tags_id_list:
                    tags = await cls.tags_detail_services(query_db, int(tags_id))
                    if (await TagsDao.count_scales_post_dao(query_db, int(tags_id))) > 0:
                        raise ServiceException(message=f'{tags.tags_name}已分配，不能删除')
                    await TagsDao.delete_tags_dao(query_db, TagsModel(tags_id=tags_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入标签id为空')

    @classmethod
    async def tags_detail_services(cls, query_db: AsyncSession, tags_id: int):
        """
        获取标签详细信息service

        :param query_db: orm对象
        :param tags_id: 标签id
        :return: 标签id对应的信息
        """
        tags = await TagsDao.get_tags_detail_by_id(query_db, tags_id=tags_id)
        if tags:
            result = TagsModel(**SqlalchemyUtil.serialize_result(tags))
        else:
            result = TagsModel(**dict())

        return result

    @staticmethod
    async def export_tags_list_services(tags_list: List):
        """
        导出标签信息service

        :param tags_list: 标签信息列表
        :return: 标签信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'tags_id': '标签编号',
            'tags_code': '标签编码',
            'tags_name': '标签名称',
            'tags_sort': '显示顺序',
            'position': '展示位置',
            'avatar': '标签图标地址',
            'status': '状态',
            'create_by': '创建者',
            'create_time': '创建时间',
            'update_by': '更新者',
            'update_time': '更新时间',
            'remark': '备注',
        }

        data = tags_list

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
