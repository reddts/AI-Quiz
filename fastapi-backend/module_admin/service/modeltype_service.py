from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.dao.modeltype_dao import ModeltypeDao
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.entity.vo.modeltype_vo import DeleteModeltypeModel, ModeltypeModel, ModeltypePageQueryModel
from utils.common_util import SqlalchemyUtil


class ModeltypeService:
    """
    模型分类管理模块服务层
    """

    @classmethod
    async def get_modeltype_list_services(
        cls, query_db: AsyncSession, query_object: ModeltypePageQueryModel, is_page: bool = False
    ):
        """
        获取模型分类列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 模型分类列表信息对象
        """
        modeltype_list_result = await ModeltypeDao.get_modeltype_list(query_db, query_object, is_page)

        return modeltype_list_result

    @classmethod
    async def check_modeltype_name_unique_services(cls, query_db: AsyncSession, page_object: ModeltypeModel):
        """
        检查模型分类名称是否唯一service

        :param query_db: orm对象
        :param page_object: 模型分类对象
        :return: 校验结果
        """
        type_id = -1 if page_object.type_id is None else page_object.type_id
        modeltype = await ModeltypeDao.get_modeltype_detail_by_info(query_db, ModeltypeModel(type_name=page_object.type_name))
        if modeltype and modeltype.type_id != type_id:
            return CommonConstant.NOT_UNIQUE
        return CommonConstant.UNIQUE

    @classmethod
    async def add_modeltype_services(cls, query_db: AsyncSession, page_object: ModeltypeModel):
        """
        新增模型分类信息service

        :param query_db: orm对象
        :param page_object: 新增模型分类对象
        :return: 新增模型分类校验结果
        """
        if not await cls.check_modeltype_name_unique_services(query_db, page_object):
            raise ServiceException(message=f'新增模型分类{page_object.type_name}失败，模型分类名称已存在')
        else:
            try:
                await ModeltypeDao.add_modeltype_dao(query_db, page_object)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='新增成功')
            except Exception as e:
                await query_db.rollback()
                raise e

    @classmethod
    async def edit_modeltype_services(cls, query_db: AsyncSession, page_object: ModeltypeModel):
        """
        编辑模型分类信息service

        :param query_db: orm对象
        :param page_object: 编辑模型分类对象
        :return: 编辑模型分类校验结果
        """
        edit_modeltype = page_object.model_dump(exclude_unset=True)
        modeltype_info = await cls.modeltype_detail_services(query_db, page_object.type_id)
        if modeltype_info.type_id:
            if not await cls.check_modeltype_name_unique_services(query_db, page_object):
                raise ServiceException(message=f'修改模型分类{page_object.type_name}失败，模型分类名称已存在')
            else:
                try:
                    await ModeltypeDao.edit_modeltype_dao(query_db, edit_modeltype)
                    await query_db.commit()
                    return CrudResponseModel(is_success=True, message='更新成功')
                except Exception as e:
                    await query_db.rollback()
                    raise e
        else:
            raise ServiceException(message='模型分类不存在')
        

    @classmethod
    async def delete_modeltype_services(cls, query_db: AsyncSession, page_object: DeleteModeltypeModel):
        """
        删除模型分类信息service

        :param query_db: orm对象
        :param page_object: 删除模型分类对象
        :return: 删除模型分类校验结果
        """
        if page_object.type_ids:
            modeltype_id_list = page_object.type_ids.split(',')
            try:
                for type_id in modeltype_id_list:
                    modeltype = await cls.modeltype_detail_services(query_db, int(type_id))
                    if (await ModeltypeDao.count_modeltype_dao(query_db, int(type_id))) > 0:
                        raise ServiceException(message=f'{modeltype.type_name}已分配，不能删除')
                    await ModeltypeDao.delete_modeltype_dao(query_db, ModeltypeModel(type_id=type_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入模型分类id为空')

    @classmethod
    async def modeltype_detail_services(cls, query_db: AsyncSession, type_id: int):
        """
        获取模型分类详细信息service

        :param query_db: orm对象
        :param type_id: 模型分类id
        :return: 模型分类id对应的信息
        """
        modeltype = await ModeltypeDao.get_modeltype_detail_by_id(query_db, type_id=type_id)
        if modeltype:
            result = ModeltypeModel(**SqlalchemyUtil.serialize_result(modeltype))
        else:
            result = ModeltypeModel(**dict())

        return result

