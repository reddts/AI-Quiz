from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.tags_do import Tags
from module_admin.entity.do.scales_do import ScalesTags
from module_admin.entity.vo.tags_vo import TagsModel, TagsPageQueryModel
from utils.page_util import PageUtil


class TagsDao:
    """
    标签管理模块数据库操作层
    """

    @classmethod
    async def get_tags_by_id(cls, db: AsyncSession, tags_id: int):
        """
        根据标签id获取在用标签详细信息

        :param db: orm对象
        :param tags_id: 标签id
        :return: 在用标签信息对象
        """
        tags_info = (
            (await db.execute(select(Tags).where(Tags.tags_id == tags_id, Tags.status == '0')))
            .scalars()
            .first()
        )

        return tags_info

    @classmethod
    async def get_tags_detail_by_id(cls, db: AsyncSession, tags_id: int):
        """
        根据标签id获取标签详细信息

        :param db: orm对象
        :param tags_id: 标签id
        :return: 标签信息对象
        """
        tags_info = (await db.execute(select(Tags).where(Tags.tags_id == tags_id))).scalars().first()

        return tags_info

    @classmethod
    async def get_tags_detail_by_info(cls, db: AsyncSession, tags: TagsModel):
        """
        根据标签参数获取标签信息

        :param db: orm对象
        :param tags: 标签参数对象
        :return: 标签信息对象
        """
        tags_info = (
            (
                await db.execute(
                    select(Tags).where(
                        Tags.tags_name == tags.tags_name if tags.tags_name else True,
                        Tags.tags_code == tags.tags_code if tags.tags_code else True,
                        Tags.tags_sort == tags.tags_sort if tags.tags_sort else True,
                    )
                )
            )
            .scalars()
            .first()
        )

        return tags_info

    @classmethod
    async def get_tags_list(cls, db: AsyncSession, query_object: TagsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取标签列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 标签列表信息对象
        """
        query = (
            select(Tags)
            .where(
                Tags.tags_code.like(f'%{query_object.tags_code}%') if query_object.tags_code else True,
                Tags.tags_name.like(f'%{query_object.tags_name}%') if query_object.tags_name else True,
                Tags.status == query_object.status if query_object.status else True,
            )
            .order_by(Tags.tags_sort)
            .distinct()
        )
        tags_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return tags_list

    @classmethod
    async def add_tags_dao(cls, db: AsyncSession, tags: TagsModel):
        """
        新增标签数据库操作

        :param db: orm对象
        :param tags: 标签对象
        :return:
        """
        db_tags = Tags(**tags.model_dump())
        db.add(db_tags)
        await db.flush()

        return db_tags

    @classmethod
    async def edit_tags_dao(cls, db: AsyncSession, tags: dict):
        """
        编辑标签数据库操作

        :param db: orm对象
        :param tags: 需要更新的标签字典
        :return:
        """
        await db.execute(update(Tags), [tags])

    @classmethod
    async def delete_tags_dao(cls, db: AsyncSession, tags: TagsModel):
        """
        删除标签数据库操作

        :param db: orm对象
        :param tags: 标签对象
        :return:
        """
        await db.execute(delete(Tags).where(Tags.tags_id.in_([tags.tags_id])))

    @classmethod
    async def count_scales_post_dao(cls, db: AsyncSession, tags_id: int):
        """
        根据标签id查询标签关联的量表数量

        :param db: orm对象
        :param tags_id: 标签id
        :return: 关联的量表数量
        """
        scales_tags_count = (
            await db.execute(select(func.count('*')).select_from(ScalesTags).where(ScalesTags.tags_id == tags_id))
        ).scalar()

        return scales_tags_count
