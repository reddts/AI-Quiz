from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.aimodel_do import AiModel
from module_admin.entity.vo.aimodel_vo import AiModelModel, AiModelPageQueryModel
from utils.page_util import PageUtil


class AiModelDao:
    """
    ai模型管理模块数据库操作层
    """

    @classmethod
    async def get_aimodel_by_id(cls, db: AsyncSession, aimodel_id: int):
        """
        根据ai模型id获取在用ai模型详细信息

        :param db: orm对象
        :param aimodel_id: ai模型id
        :return: 在用ai模型信息对象
        """
        aimodel_info = (
            (await db.execute(select(AiModel).where(AiModel.aimodel_id == aimodel_id, AiModel.status == '0')))
            .scalars()
            .first()
        )

        return aimodel_info

    @classmethod
    async def get_aimodel_detail_by_id(cls, db: AsyncSession, aimodel_id: int):
        """
        根据ai模型id获取ai模型详细信息

        :param db: orm对象
        :param aimodel_id: ai模型id
        :return: ai模型信息对象
        """
        aimodel_info = (await db.execute(select(AiModel).where(AiModel.aimodel_id == aimodel_id))).scalars().first()

        return aimodel_info

    @classmethod
    async def get_aimodel_detail_by_info(cls, db: AsyncSession, aimodel: AiModelModel):
        """
        根据ai模型参数获取ai模型信息

        :param db: orm对象
        :param aimodel: ai模型参数对象
        :return: ai模型信息对象
        """
        aimodel_info = (
            (
                await db.execute(
                    select(AiModel).where(
                        AiModel.aimodel_name == aimodel.aimodel_name if aimodel.aimodel_name else True,
                        AiModel.aimodel_alias == aimodel.aimodel_alias if aimodel.aimodel_alias else True,
                    )
                )
            )
            .scalars()
            .first()
        )

        return aimodel_info

    @classmethod
    async def get_aimodel_list(cls, db: AsyncSession, query_object: AiModelPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取ai模型列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: ai模型列表信息对象
        """
        query = (
            select(AiModel)
            .where(
                AiModel.aimodel_alias.like(f'%{query_object.aimodel_alias}%') if query_object.aimodel_alias else True,
                AiModel.aimodel_name.like(f'%{query_object.aimodel_name}%') if query_object.aimodel_name else True,
                AiModel.status == query_object.status if query_object.status else True,
            )
            .order_by(AiModel.aimodel_id)
            .distinct()
        )
        aimodel_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return aimodel_list

    @classmethod
    async def add_aimodel_dao(cls, db: AsyncSession, aimodel: AiModelModel):
        """
        新增ai模型数据库操作

        :param db: orm对象
        :param aimodel: ai模型对象
        :return:
        """
        db_aimodel = AiModel(**aimodel.model_dump())
        db.add(db_aimodel)
        await db.flush()

        return db_aimodel

    @classmethod
    async def edit_aimodel_dao(cls, db: AsyncSession, aimodel: dict):
        """
        编辑ai模型数据库操作

        :param db: orm对象
        :param aimodel: 需要更新的ai模型字典
        :return:
        """
        await db.execute(update(AiModel), [aimodel])

    @classmethod
    async def edit_aimodel_dao_byid(cls, db: AsyncSession, aimodel_id: int):
        """
        根据ai模型id将其他数据的nowused字段修改为N

        :param db: orm对象
        :param aimodel_id: ai模型id
        :return:
        """
        await db.execute(
            update(AiModel)
            .where(AiModel.aimodel_id != aimodel_id)
            .values(nowused='N')
        )
        await db.commit()



    @classmethod
    async def delete_aimodel_dao(cls, db: AsyncSession, aimodel: AiModelModel):
        """
        删除ai模型数据库操作

        :param db: orm对象
        :param aimodel: ai模型对象
        :return:
        """
        await db.execute(delete(AiModel).where(AiModel.aimodel_id.in_([aimodel.aimodel_id])))


