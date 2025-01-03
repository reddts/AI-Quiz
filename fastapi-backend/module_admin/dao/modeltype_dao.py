from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.modeltype_do import Modeltype
from module_admin.entity.do.model_do import AiModel
from module_admin.entity.vo.modeltype_vo import ModeltypeModel, ModeltypePageQueryModel
from utils.page_util import PageUtil


class ModeltypeDao:
    """
    模型分类管理模块数据库操作层
    """

    @classmethod
    async def get_modeltype_by_id(cls, db: AsyncSession, type_id: int):
        """
        根据模型分类id获取在用模型分类详细信息

        :param db: orm对象
        :param type_id: 模型分类id
        :return: 在用模型分类信息对象
        """
        modeltype_info = (
            (await db.execute(select(Modeltype).where(Modeltype.type_id == type_id, Modeltype.status == '0')))
            .scalars()
            .first()
        )

        return modeltype_info

    @classmethod
    async def get_modeltype_detail_by_id(cls, db: AsyncSession, type_id: int):
        """
        根据模型分类id获取模型分类详细信息

        :param db: orm对象
        :param type_id: 模型分类id
        :return: 模型分类信息对象
        """
        modeltype_info = (await db.execute(select(Modeltype).where(Modeltype.type_id == type_id))).scalars().first()

        return modeltype_info

    @classmethod
    async def get_modeltype_detail_by_info(cls, db: AsyncSession, modeltype: ModeltypeModel):
        """
        根据模型分类参数获取模型分类信息

        :param db: orm对象
        :param Modeltype: 模型分类参数对象
        :return: 模型分类信息对象
        """
        modeltype_info = (
            (
                await db.execute(
                    select(Modeltype).where(
                        Modeltype.type_name == modeltype.type_name if modeltype.type_name else True,
                    )
                )
            )
            .scalars()
            .first()
        )

        return modeltype_info

    @classmethod
    async def get_modeltype_list(cls, db: AsyncSession, query_object: ModeltypePageQueryModel, is_page: bool = False):
        """
        根据查询参数获取模型分类列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 模型分类列表信息对象
        """
        query = (
            select(Modeltype)
            .where(
                Modeltype.type_name.like(f'%{query_object.type_name}%') if query_object.type_name else True,
                Modeltype.status == query_object.status if query_object.status else True,
            )
            .order_by(Modeltype.type_id)
            .distinct()
        )
        modeltype_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return modeltype_list

    @classmethod
    async def add_modeltype_dao(cls, db: AsyncSession, modeltype: ModeltypeModel):
        """
        新增模型分类数据库操作

        :param db: orm对象
        :param modeltype: 模型分类对象
        :return:
        """
        db_modeltype = Modeltype(**modeltype.model_dump())
        db.add(db_modeltype)
        await db.flush()

        return db_modeltype

    @classmethod
    async def edit_modeltype_dao(cls, db: AsyncSession, modeltype: dict):
        """
        编辑模型分类数据库操作

        :param db: orm对象
        :param modeltype: 需要更新的模型分类字典
        :return:
        """
        await db.execute(update(Modeltype), [modeltype])

    @classmethod
    async def delete_modeltype_dao(cls, db: AsyncSession, modeltype: ModeltypeModel):
        """
        删除模型分类数据库操作

        :param db: orm对象
        :param modeltype: 模型分类对象
        :return:
        """
        await db.execute(delete(Modeltype).where(Modeltype.type_id.in_([modeltype.type_id])))

    @classmethod
    async def count_modeltype_dao(cls, db: AsyncSession, type_id: int):
        """
        根据模型分类id查询模型分类关联的量表数量

        :param db: orm对象
        :param modeltype_id: 模型分类id
        :return: 关联的量表数量
        """
        modeltype_count = (
            await db.execute(select(func.count('*')).select_from(AiModel).where(AiModel.type_id == type_id))
        ).scalar()

        return modeltype_count
