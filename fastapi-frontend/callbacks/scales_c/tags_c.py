import time
import uuid
from dash import ctx, dcc, no_update
from dash.dependencies import ALL, Input, Output, State
from dash.exceptions import PreventUpdate
from typing import Dict
from api.scales.tags import TagsApi
from config.constant import SysNormalDisableConstant
from server import app
from utils.common_util import ValidateUtil
from utils.dict_util import DictManager
from utils.feedback_util import MessageManager
from utils.permission_util import PermissionManager
from utils.time_format_util import TimeFormatUtil
from views.scales.tags import avatar


def generate_tags_table(query_params: Dict):
    """
    根据查询参数获取标签表格数据及分页信息

    :param query_params: 查询参数
    :return: 标签表格数据及分页信息
    """
    table_info = TagsApi.list_tags(query_params)
    table_data = table_info['rows']
    table_pagination = dict(
        pageSize=table_info['page_size'],
        current=table_info['page_num'],
        showSizeChanger=True,
        pageSizeOptions=[10, 30, 50, 100],
        showQuickJumper=True,
        total=table_info['total'],
    )
    for item in table_data:
        item['status'] = DictManager.get_dict_tag(
            dict_type='sys_normal_disable', dict_value=item.get('status')
        )
        item['position'] = DictManager.get_dict_label(
            dict_type='sys_position', dict_value=item.get('position')
        )
        item['create_time'] = TimeFormatUtil.format_time(
            item.get('create_time')
        )
        item['update_time'] = TimeFormatUtil.format_time(
            item.get('update_time')
        )
        item['key'] = str(item['tags_id'])
        item['operation'] = [
            {'content': '修改', 'type': 'link', 'icon': 'antd-edit'}
            if PermissionManager.check_perms('scales:tags:edit')
            else {},
            {'content': '删除', 'type': 'link', 'icon': 'antd-delete'}
            if PermissionManager.check_perms('scales:tags:remove')
            else {},
        ]

    return [table_data, table_pagination]


@app.callback(
    output=dict(
        tags_table_data=Output('tags-list-table', 'data', allow_duplicate=True),
        tags_table_pagination=Output(
            'tags-list-table', 'pagination', allow_duplicate=True
        ),
        tags_table_key=Output('tags-list-table', 'key'),
        tags_table_selectedrowkeys=Output('tags-list-table', 'selectedRowKeys'),
    ),
    inputs=dict(
        search_click=Input('tags-search', 'nClicks'),
        refresh_click=Input('tags-refresh', 'nClicks'),
        pagination=Input('tags-list-table', 'pagination'),
        operations=Input('tags-operations-store', 'data'),
    ),
    state=dict(
        tags_code=State('tags-tags_code-input', 'value'),
        tags_name=State('tags-tags_name-input', 'value'),
        status_select=State('tags-status-select', 'value'),
    ),
    prevent_initial_call=True,
)
def get_tags_table_data(
    search_click,
    refresh_click,
    pagination,
    operations,
    tags_code,
    tags_name,
    status_select,
):
    """
    获取标签表格数据回调（进行表格相关增删查改操作后均会触发此回调）
    """

    query_params = dict(
        tags_code=tags_code,
        tags_name=tags_name,
        status=status_select,
        page_num=1,
        page_size=10,
    )
    triggered_id = ctx.triggered_id
    if triggered_id == 'tags-list-table':
        query_params.update(
            {
                'page_num': pagination['current'],
                'page_size': pagination['pageSize'],
            }
        )
    if search_click or refresh_click or pagination or operations:
        table_data, table_pagination = generate_tags_table(query_params)
        return dict(
            tags_table_data=table_data,
            tags_table_pagination=table_pagination,
            tags_table_key=str(uuid.uuid4()),
            tags_table_selectedrowkeys=None,
        )

    raise PreventUpdate


# 重置标签搜索表单数据回调
app.clientside_callback(
    """
    (reset_click) => {
        if (reset_click) {
            return [null, null, null, {'type': 'reset'}]
        }
        return window.dash_clientside.no_update;
    }
    """,
    [
        Output('tags-tags_code-input', 'value'),
        Output('tags-tags_name-input', 'value'),
        Output('tags-status-select', 'value'),
        Output('tags-operations-store', 'data'),
    ],
    Input('tags-reset', 'nClicks'),
    prevent_initial_call=True,
)


# 隐藏/显示标签搜索表单回调
app.clientside_callback(
    """
    (hidden_click, hidden_status) => {
        if (hidden_click) {
            return [
                !hidden_status,
                hidden_status ? '隐藏搜索' : '显示搜索'
            ]
        }
        return window.dash_clientside.no_update;
    }
    """,
    [
        Output('tags-search-form-container', 'hidden'),
        Output('tags-hidden-tooltip', 'title'),
    ],
    Input('tags-hidden', 'nClicks'),
    State('tags-search-form-container', 'hidden'),
    prevent_initial_call=True,
)

# 根据选择的表格数据行数控制修改按钮状态回调
app.clientside_callback(
    """
    (table_rows_selected) => {
        outputs_list = window.dash_clientside.callback_context.outputs_list;
        if (outputs_list) {
            if (table_rows_selected?.length === 1) {
                return false;
            }
            return true;
        }
        throw window.dash_clientside.PreventUpdate;
    }
    """,
    Output({'type': 'tags-operation-button', 'index': 'edit'}, 'disabled'),
    Input('tags-list-table', 'selectedRowKeys'),
    prevent_initial_call=True,
)


# 根据选择的表格数据行数控制删除按钮状态回调
app.clientside_callback(
    """
    (table_rows_selected) => {
        outputs_list = window.dash_clientside.callback_context.outputs_list;
        if (outputs_list) {
            if (table_rows_selected?.length > 0) {
                return false;
            }
            return true;
        }
        throw window.dash_clientside.PreventUpdate;
    }
    """,
    Output({'type': 'tags-operation-button', 'index': 'delete'}, 'disabled'),
    Input('tags-list-table', 'selectedRowKeys'),
    prevent_initial_call=True,
)


# 标签表单数据双向绑定回调
app.clientside_callback(
    """
    (row_data, form_value) => {
        trigger_id = window.dash_clientside.callback_context.triggered_id;
        if (trigger_id === 'tags-form-store') {
            return [window.dash_clientside.no_update, row_data];
        }
        if (trigger_id === 'tags-form') {
            Object.assign(row_data, form_value);
            return [row_data, window.dash_clientside.no_update];
        }
        throw window.dash_clientside.PreventUpdate;
    }
    """,
    [
        Output('tags-form-store', 'data', allow_duplicate=True),
        Output('tags-form', 'values'),
    ],
    [
        Input('tags-form-store', 'data'),
        Input('tags-form', 'values'),
    ],
    prevent_initial_call=True,
)


@app.callback(
    output=dict(
        modal_visible=Output('tags-modal', 'visible', allow_duplicate=True),
        modal_title=Output('tags-modal', 'title'),
        form_value=Output('tags-form-store', 'data', allow_duplicate=True),
        form_label_validate_status=Output(
            'tags-form', 'validateStatuses', allow_duplicate=True
        ),
        form_label_validate_info=Output(
            'tags-form', 'helps', allow_duplicate=True
        ),
        modal_type=Output('tags-modal_type-store', 'data'),
        tags_avatar_container=Output('tags-avatar-container', 'children'),
    ),
    inputs=dict(
        operation_click=Input(
            {'type': 'tags-operation-button', 'index': ALL}, 'nClicks'
        ),
        button_click=Input('tags-list-table', 'nClicksButton'),
    ),
    state=dict(
        selected_row_keys=State('tags-list-table', 'selectedRowKeys'),
        clicked_content=State('tags-list-table', 'clickedContent'),
        recently_button_clicked_row=State(
            'tags-list-table', 'recentlyButtonClickedRow'
        ),
    ),
    prevent_initial_call=True,
)
def add_edit_tags_modal(
    operation_click,
    button_click,
    selected_row_keys,
    clicked_content,
    recently_button_clicked_row,
):
    """
    显示新增或编辑标签弹窗回调
    """
    trigger_id = ctx.triggered_id
    if (
        trigger_id == {'index': 'add', 'type': 'tags-operation-button'}
        or trigger_id == {'index': 'edit', 'type': 'tags-operation-button'}
        or (trigger_id == 'tags-list-table' and clicked_content == '修改')
    ):
        if trigger_id == {'index': 'add', 'type': 'tags-operation-button'}:
            tags_info = dict(
                tags_name=None,
                tags_code=None,
                tags_sort=0,
                status=SysNormalDisableConstant.NORMAL,
                remark=None,
            )
            return dict(
                modal_visible=True,
                modal_title='新增标签',
                form_value=tags_info,
                form_label_validate_status=None,
                form_label_validate_info=None,
                tags_avatar_container=avatar.render('',''),
                modal_type={'type': 'add'},                
            )
        elif trigger_id == {
            'index': 'edit',
            'type': 'tags-operation-button',
        } or (trigger_id == 'tags-list-table' and clicked_content == '修改'):
            if trigger_id == {'index': 'edit', 'type': 'tags-operation-button'}:
                tags_id = int(','.join(selected_row_keys))
            else:
                tags_id = int(recently_button_clicked_row['key'])
            tags_info_res = TagsApi.get_tags(tags_id=tags_id)
            tags_info = tags_info_res['data']
            return dict(
                modal_visible=True,
                modal_title='编辑标签',
                form_value=tags_info,
                form_label_validate_status=None,
                form_label_validate_info=None,
                tags_avatar_container=avatar.render(tags_id,tags_info['avatar']),
                modal_type={'type': 'edit'},
            )

    raise PreventUpdate


@app.callback(
    output=dict(
        form_label_validate_status=Output(
            'tags-form', 'validateStatuses', allow_duplicate=True
        ),
        form_label_validate_info=Output(
            'tags-form', 'helps', allow_duplicate=True
        ),
        modal_visible=Output('tags-modal', 'visible'),
        operations=Output(
            'tags-operations-store', 'data', allow_duplicate=True
        ),
    ),
    inputs=dict(confirm_trigger=Input('tags-modal', 'okCounts')),
    state=dict(
        modal_type=State('tags-modal_type-store', 'data'),
        form_value=State('tags-form-store', 'data'),
        form_label=State(
            {'type': 'tags-form-label', 'index': ALL, 'required': True}, 'label'
        ),
    ),
    running=[[Output('tags-modal', 'confirmLoading'), True, False]],
    prevent_initial_call=True,
)
def tags_confirm(confirm_trigger, modal_type, form_value, form_label):
    """
    新增或编辑标签弹窗确认回调，实现新增或编辑操作
    """
    if confirm_trigger:
        # 获取所有必填表单项对应label的index
        form_label_list = [x['id']['index'] for x in ctx.states_list[-1]]
        # 获取所有输入必填表单项对应的label
        form_label_state = {
            x['id']['index']: x.get('value') for x in ctx.states_list[-1]
        }
        if all(
            ValidateUtil.not_empty(item)
            for item in [form_value.get(k) for k in form_label_list]
        ):
            params_add = form_value
            params_edit = params_add.copy()
            modal_type = modal_type.get('type')
            if modal_type == 'add':
                TagsApi.add_tags(params_add)
            if modal_type == 'edit':
                TagsApi.update_tags(params_edit)
            if modal_type == 'add':
                MessageManager.success(content='新增成功')

                return dict(
                    form_label_validate_status=None,
                    form_label_validate_info=None,
                    modal_visible=False,
                    operations={'type': 'add'},
                )
            if modal_type == 'edit':
                MessageManager.success(content='编辑成功')

                return dict(
                    form_label_validate_status=None,
                    form_label_validate_info=None,
                    modal_visible=False,
                    operations={'type': 'edit'},
                )

            return dict(
                form_label_validate_status=None,
                form_label_validate_info=None,
                modal_visible=no_update,
                operations=no_update,
            )

        return dict(
            form_label_validate_status={
                form_label_state.get(k): None
                if ValidateUtil.not_empty(form_value.get(k))
                else 'error'
                for k in form_label_list
            },
            form_label_validate_info={
                form_label_state.get(k): None
                if ValidateUtil.not_empty(form_value.get(k))
                else f'{form_label_state.get(k)}不能为空!'
                for k in form_label_list
            },
            modal_visible=no_update,
            operations=no_update,
        )

    raise PreventUpdate


@app.callback(
    [
        Output('tags-delete-text', 'children'),
        Output('tags-delete-confirm-modal', 'visible'),
        Output('tags-delete-ids-store', 'data'),
    ],
    [
        Input({'type': 'tags-operation-button', 'index': ALL}, 'nClicks'),
        Input('tags-list-table', 'nClicksButton'),
    ],
    [
        State('tags-list-table', 'selectedRowKeys'),
        State('tags-list-table', 'clickedContent'),
        State('tags-list-table', 'recentlyButtonClickedRow'),
    ],
    prevent_initial_call=True,
)
def tags_delete_modal(
    operation_click,
    button_click,
    selected_row_keys,
    clicked_content,
    recently_button_clicked_row,
):
    """
    显示删除标签二次确认弹窗回调
    """
    trigger_id = ctx.triggered_id
    if trigger_id == {'index': 'delete', 'type': 'tags-operation-button'} or (
        trigger_id == 'tags-list-table' and clicked_content == '删除'
    ):
        if trigger_id == {'index': 'delete', 'type': 'tags-operation-button'}:
            tags_ids = ','.join(selected_row_keys)
        else:
            if clicked_content == '删除':
                tags_ids = recently_button_clicked_row['key']
            else:
                raise PreventUpdate

        return [f'是否确认删除标签编号为{tags_ids}的标签？', True, tags_ids]

    raise PreventUpdate


@app.callback(
    Output('tags-operations-store', 'data', allow_duplicate=True),
    Input('tags-delete-confirm-modal', 'okCounts'),
    State('tags-delete-ids-store', 'data'),
    prevent_initial_call=True,
)
def tags_delete_confirm(delete_confirm, tags_ids_data):
    """
    删除标签弹窗确认回调，实现删除操作
    """
    if delete_confirm:
        params = tags_ids_data
        TagsApi.del_tags(params)
        MessageManager.success(content='删除成功')

        return {'type': 'delete'}

    raise PreventUpdate


@app.callback(
    [
        Output('tags-export-container', 'data', allow_duplicate=True),
        Output('tags-export-complete-judge-container', 'data'),
    ],
    Input('tags-export', 'nClicks'),
    [
        State('tags-tags_code-input', 'value'),
        State('tags-tags_name-input', 'value'),
        State('tags-status-select', 'value'),
    ],
    running=[[Output('tags-export', 'loading'), True, False]],
    prevent_initial_call=True,
)
def export_tags_list(export_click, tags_code, tags_name, status):
    """
    导出标签信息回调
    """
    if export_click:
        export_params = dict(
            tags_code=tags_code, tags_name=tags_name, status=status
        )
        export_tags_res = TagsApi.export_tags(export_params)
        export_tags = export_tags_res.content
        MessageManager.success(content='导出成功')

        return [
            dcc.send_bytes(
                export_tags,
                f'标签信息_{time.strftime("%Y%m%d%H%M%S", time.localtime())}.xlsx',
            ),
            {'timestamp': time.time()},
        ]

    raise PreventUpdate


@app.callback(
    Output('tags-export-container', 'data', allow_duplicate=True),
    Input('tags-export-complete-judge-container', 'data'),
    prevent_initial_call=True,
)
def reset_tags_export_status(data):
    """
    导出完成后重置下载组件数据回调，防止重复下载文件
    """
    time.sleep(0.5)
    if data:
        return None

    raise PreventUpdate
