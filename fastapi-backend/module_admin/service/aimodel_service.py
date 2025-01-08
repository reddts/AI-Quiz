from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.dao.aimodel_dao import AiModelDao
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.entity.vo.aimodel_vo import DeleteAiModelModel, AiModelModel, AiModelPageQueryModel
from utils.common_util import export_list2excel, SqlalchemyUtil


class AiModelService:
    """
    ai模型管理模块服务层
    """

    @classmethod
    async def get_aimodel_list_services(
        cls, query_db: AsyncSession, query_object: AiModelPageQueryModel, is_page: bool = False
    ):
        """
        获取ai模型列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: ai模型列表信息对象
        """
        aimodel_list_result = await AiModelDao.get_aimodel_list(query_db, query_object, is_page)

        return aimodel_list_result

    @classmethod
    async def check_aimodel_name_unique_services(cls, query_db: AsyncSession, page_object: AiModelModel):
        """
        检查ai模型名称是否唯一service

        :param query_db: orm对象
        :param page_object: ai模型对象
        :return: 校验结果
        """
        aimodel_id = -1 if page_object.aimodel_id is None else page_object.aimodel_id
        aimodel = await AiModelDao.get_aimodel_detail_by_info(query_db, AiModelModel(aimodel_name=page_object.aimodel_name))
        if aimodel and aimodel.aimodel_id != aimodel_id:
            return CommonConstant.NOT_UNIQUE
        return CommonConstant.UNIQUE

    @classmethod
    async def check_aimodel_alias_unique_services(cls, query_db: AsyncSession, page_object: AiModelModel):
        """
        检查ai模型别名是否唯一service

        :param query_db: orm对象
        :param page_object: ai模型对象
        :return: 校验结果
        """
        aimodel_id = -1 if page_object.aimodel_id is None else page_object.aimodel_id
        aimodel = await AiModelDao.get_aimodel_detail_by_info(query_db, AiModelModel(aimodel_alias=page_object.aimodel_alias))
        if aimodel and aimodel.aimodel_id != aimodel_id:
            return CommonConstant.NOT_UNIQUE
        return CommonConstant.UNIQUE

    @classmethod
    async def add_aimodel_services(cls, query_db: AsyncSession, page_object: AiModelModel):
        """
        新增ai模型信息service

        :param query_db: orm对象
        :param page_object: 新增ai模型对象
        :return: 新增ai模型校验结果
        """
        if not await cls.check_aimodel_name_unique_services(query_db, page_object):
            raise ServiceException(message=f'新增AI模型{page_object.aimodel_name}失败，AI模型调用名称已存在')
        elif not await cls.check_aimodel_alias_unique_services(query_db, page_object):
            raise ServiceException(message=f'新增AI模型{page_object.aimodel_alias}失败，AI模型显示名已存在')
        else:
            try:
                await AiModelDao.add_aimodel_dao(query_db, page_object)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='新增成功')
            except Exception as e:
                await query_db.rollback()
                raise e

    @classmethod
    async def edit_aimodel_services(cls, query_db: AsyncSession, page_object: AiModelModel):
        """
        编辑ai模型信息service

        :param query_db: orm对象
        :param page_object: 编辑ai模型对象
        :return: 编辑ai模型校验结果
        """
        edit_aimodel = page_object.model_dump(exclude_unset=True)
        aimodel_info = await cls.aimodel_detail_services(query_db, page_object.aimodel_id)
        if aimodel_info.aimodel_id:
            if not await cls.check_aimodel_name_unique_services(query_db, page_object):
                raise ServiceException(message=f'修改AI模型{page_object.aimodel_name}失败，AI模型调用名称已存在')
            elif not await cls.check_aimodel_alias_unique_services(query_db, page_object):
                raise ServiceException(message=f'修改AI模型{page_object.aimodel_alias}失败，AI模型显示名称已存在')
            else:
                try:
                    #先修改基础字段
                    await AiModelDao.edit_aimodel_dao(query_db, edit_aimodel)
                    await query_db.commit()
                    #当修改了当前模型时，将其他模型置为非当前模型
                    if aimodel_info.nowused == 'Y':
                        await AiModelDao.edit_aimodel_dao(query_db, aimodel_info.aimodel_id)
                        await query_db.commit()
                    return CrudResponseModel(is_success=True, message='更新成功')
                except Exception as e:
                    await query_db.rollback()
                    raise e
        else:
            raise ServiceException(message='AI模型不存在')
        

    @classmethod
    async def delete_aimodel_services(cls, query_db: AsyncSession, page_object: DeleteAiModelModel):
        """
        删除ai模型信息service

        :param query_db: orm对象
        :param page_object: 删除ai模型对象
        :return: 删除ai模型校验结果
        """
        if page_object.aimodel_ids:
            aimodel_id_list = page_object.aimodel_ids.split(',')
            try:
                for aimodel_id in aimodel_id_list:
                    aimodel = await cls.aimodel_detail_services(query_db, int(aimodel_id))
                    if aimodel.nowused == 'Y':
                        raise ServiceException(message=f'{aimodel.aimodel_name}是当前模型，不能删除')
                    await AiModelDao.delete_aimodel_dao(query_db, AiModelModel(aimodel_id=aimodel_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入AI模型id为空')

    @classmethod
    async def aimodel_detail_services(cls, query_db: AsyncSession, aimodel_id: int):
        """
        获取ai模型详细信息service

        :param query_db: orm对象
        :param aimodel_id: ai模型id
        :return: ai模型id对应的信息
        """
        aimodel = await AiModelDao.get_aimodel_detail_by_id(query_db, aimodel_id=aimodel_id)
        if aimodel:
            result = AiModelModel(**SqlalchemyUtil.serialize_result(aimodel))
        else:
            result = AiModelModel(**dict())

        return result

    @staticmethod
    async def export_aimodel_list_services(aimodel_list: List):
        """
        导出ai模型信息service

        :param aimodel_list: ai模型信息列表
        :return: ai模型信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'aimodel_id': 'ai模型编号',
            'aimodel_name': 'ai模型调用名称',
            'aimodel_alias': 'ai模型显示名称',
            'type_id': '模型分类编号',
            'type_name': '模型分类名',
            'nowused': '当前模型标记',
            'context_num': '上下文数量',
            'maxtoken': '最大输入token',
            'temperature': '随机性',
            'top_p': '多样性',
            'frequency': '重复性',
            'presence': '创新性',
            'status': '状态',
            'create_by': '创建者',
            'create_time': '创建时间',
            'update_by': '更新者',
            'update_time': '更新时间',
            'remark': '备注',
        }

        data = aimodel_list

        for item in data:
            if item.get('status') == '0':
                item['status'] = '正常'
            else:
                item['status'] = '停用'
            if item.get('nowused') == 'Y':
                item['nowused'] = '当前'
            else:
                item['nowused'] = '非当前'
        new_data = [
            {mapping_dict.get(key): value for key, value in item.items() if mapping_dict.get(key)} for item in data
        ]
        binary_data = export_list2excel(new_data)

        return binary_data
