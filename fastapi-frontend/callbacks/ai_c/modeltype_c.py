import time
import uuid
from dash import ctx, dcc, no_update
from dash.dependencies import ALL, Input, Output, State
from dash.exceptions import PreventUpdate
from typing import Dict
from api.ai.modeltype import ModeltypeApi
from config.constant import SysNormalDisableConstant
from server import app
from utils.common_util import ValidateUtil
from utils.dict_util import DictManager
from utils.feedback_util import MessageManager
from utils.permission_util import PermissionManager
from utils.time_format_util import TimeFormatUtil


def generate_modeltype_table(query_params: Dict):
    """
    根据查询参数获取模型分类表格数据及分页信息

    :param query_params: 查询参数
    :return: 模型分类表格数据及分页信息
    """
    table_info = ModeltypeApi.list_modeltype(query_params)
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
        item['create_time'] = TimeFormatUtil.format_time(
            item.get('create_time')
        )
        item['update_time'] = TimeFormatUtil.format_time(
            item.get('update_time')
        )
        item['key'] = str(item['type_id'])
        item['operation'] = [
            {'content': '修改', 'type': 'link', 'icon': 'antd-edit'}
            if PermissionManager.check_perms('ai:modeltype:edit')
            else {},
            {'content': '删除', 'type': 'link', 'icon': 'antd-delete'}
            if PermissionManager.check_perms('ai:modeltype:remove')
            else {},
        ]

    return [table_data, table_pagination]


@app.callback(
    output=dict(
        modeltype_table_data=Output('modeltype-list-table', 'data', allow_duplicate=True),
        modeltype_table_pagination=Output(
            'modeltype-list-table', 'pagination', allow_duplicate=True
        ),
        modeltype_table_key=Output('modeltype-list-table', 'key'),
        modeltype_table_selectedrowkeys=Output('modeltype-list-table', 'selectedRowKeys'),
    ),
    inputs=dict(
        search_click=Input('modeltype-search', 'nClicks'),
        refresh_click=Input('modeltype-refresh', 'nClicks'),
        pagination=Input('modeltype-list-table', 'pagination'),
        operations=Input('modeltype-operations-store', 'data'),
    ),
    state=dict(
        type_name=State('modeltype-type_name-input', 'value'),
        status_select=State('modeltype-status-select', 'value'),
    ),
    prevent_initial_call=True,
)
def get_modeltype_table_data(
    search_click,
    refresh_click,
    pagination,
    operations,
    type_name,
    status_select,
):
    """
    获取模型分类表格数据回调（进行表格相关增删查改操作后均会触发此回调）
    """

    query_params = dict(
        type_name=type_name,
        status=status_select,
        page_num=1,
        page_size=10,
    )
    triggered_id = ctx.triggered_id
    if triggered_id == 'modeltype-list-table':
        query_params.update(
            {
                'page_num': pagination['current'],
                'page_size': pagination['pageSize'],
            }
        )
    if search_click or refresh_click or pagination or operations:
        table_data, table_pagination = generate_modeltype_table(query_params)
        return dict(
            modeltype_table_data=table_data,
            modeltype_table_pagination=table_pagination,
            modeltype_table_key=str(uuid.uuid4()),
            modeltype_table_selectedrowkeys=None,
        )

    raise PreventUpdate


# 重置模型分类搜索表单数据回调
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
        Output('modeltype-type_name-input', 'value'),
        Output('modeltype-status-select', 'value'),
        Output('modeltype-operations-store', 'data'),
    ],
    Input('modeltype-reset', 'nClicks'),
    prevent_initial_call=True,
)


# 隐藏/显示模型分类搜索表单回调
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
        Output('modeltype-search-form-container', 'hidden'),
        Output('modeltype-hidden-tooltip', 'title'),
    ],
    Input('modeltype-hidden', 'nClicks'),
    State('modeltype-search-form-container', 'hidden'),
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
    Output({'type': 'modeltype-operation-button', 'index': 'edit'}, 'disabled'),
    Input('modeltype-list-table', 'selectedRowKeys'),
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
    Output({'type': 'modeltype-operation-button', 'index': 'delete'}, 'disabled'),
    Input('modeltype-list-table', 'selectedRowKeys'),
    prevent_initial_call=True,
)


# 模型分类表单数据双向绑定回调
app.clientside_callback(
    """
    (row_data, form_value) => {
        trigger_id = window.dash_clientside.callback_context.triggered_id;
        if (trigger_id === 'modeltype-form-store') {
            return [window.dash_clientside.no_update, row_data];
        }
        if (trigger_id === 'modeltype-form') {
            Object.assign(row_data, form_value);
            return [row_data, window.dash_clientside.no_update];
        }
        throw window.dash_clientside.PreventUpdate;
    }
    """,
    [
        Output('modeltype-form-store', 'data', allow_duplicate=True),
        Output('modeltype-form', 'values'),
    ],
    [
        Input('modeltype-form-store', 'data'),
        Input('modeltype-form', 'values'),
    ],
    prevent_initial_call=True,
)


@app.callback(
    output=dict(
        modal_visible=Output('modeltype-modal', 'visible', allow_duplicate=True),
        modal_title=Output('modeltype-modal', 'title'),
        form_value=Output('modeltype-form-store', 'data', allow_duplicate=True),
        form_label_validate_status=Output(
            'modeltype-form', 'validateStatuses', allow_duplicate=True
        ),
        form_label_validate_info=Output(
            'modeltype-form', 'helps', allow_duplicate=True
        ),
        modal_type=Output('modeltype-modal_type-store', 'data'),
    ),
    inputs=dict(
        operation_click=Input(
            {'type': 'modeltype-operation-button', 'index': ALL}, 'nClicks'
        ),
        button_click=Input('modeltype-list-table', 'nClicksButton'),
    ),
    state=dict(
        selected_row_keys=State('modeltype-list-table', 'selectedRowKeys'),
        clicked_content=State('modeltype-list-table', 'clickedContent'),
        recently_button_clicked_row=State(
            'modeltype-list-table', 'recentlyButtonClickedRow'
        ),
    ),
    prevent_initial_call=True,
)
def add_edit_modeltype_modal(
    operation_click,
    button_click,
    selected_row_keys,
    clicked_content,
    recently_button_clicked_row,
):
    """
    显示新增或编辑模型分类弹窗回调
    """
    trigger_id = ctx.triggered_id
    if (
        trigger_id == {'index': 'add', 'type': 'modeltype-operation-button'}
        or trigger_id == {'index': 'edit', 'type': 'modeltype-operation-button'}
        or (trigger_id == 'modeltype-list-table' and clicked_content == '修改')
    ):
        if trigger_id == {'index': 'add', 'type': 'modeltype-operation-button'}:
            modeltype_info = dict(
                type_name=None,
                api_url=None,
                status=SysNormalDisableConstant.NORMAL,
                remark=None,
            )
            return dict(
                modal_visible=True,
                modal_title='新增模型分类',
                form_value=modeltype_info,
                form_label_validate_status=None,
                form_label_validate_info=None,
                modal_type={'type': 'add'},                
            )
        elif trigger_id == {
            'index': 'edit',
            'type': 'modeltype-operation-button',
        } or (trigger_id == 'modeltype-list-table' and clicked_content == '修改'):
            if trigger_id == {'index': 'edit', 'type': 'modeltype-operation-button'}:
                type_id = int(','.join(selected_row_keys))
            else:
                type_id = int(recently_button_clicked_row['key'])
            modeltype_info_res = ModeltypeApi.get_modeltype(type_id=type_id)
            modeltype_info = modeltype_info_res['data']
            return dict(
                modal_visible=True,
                modal_title='编辑模型分类',
                form_value=modeltype_info,
                form_label_validate_status=None,
                form_label_validate_info=None,
                modal_type={'type': 'edit'},
            )

    raise PreventUpdate


@app.callback(
    output=dict(
        form_label_validate_status=Output(
            'modeltype-form', 'validateStatuses', allow_duplicate=True
        ),
        form_label_validate_info=Output(
            'modeltype-form', 'helps', allow_duplicate=True
        ),
        modal_visible=Output('modeltype-modal', 'visible'),
        operations=Output(
            'modeltype-operations-store', 'data', allow_duplicate=True
        ),
    ),
    inputs=dict(confirm_trigger=Input('modeltype-modal', 'okCounts')),
    state=dict(
        modal_type=State('modeltype-modal_type-store', 'data'),
        form_value=State('modeltype-form-store', 'data'),
        form_label=State(
            {'type': 'modeltype-form-label', 'index': ALL, 'required': True}, 'label'
        ),
    ),
    running=[[Output('modeltype-modal', 'confirmLoading'), True, False]],
    prevent_initial_call=True,
)
def modeltype_confirm(confirm_trigger, modal_type, form_value, form_label):
    """
    新增或编辑模型分类弹窗确认回调，实现新增或编辑操作
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
                ModeltypeApi.add_modeltype(params_add)
            if modal_type == 'edit':
                ModeltypeApi.update_modeltype(params_edit)
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
        Output('modeltype-delete-text', 'children'),
        Output('modeltype-delete-confirm-modal', 'visible'),
        Output('modeltype-delete-ids-store', 'data'),
    ],
    [
        Input({'type': 'modeltype-operation-button', 'index': ALL}, 'nClicks'),
        Input('modeltype-list-table', 'nClicksButton'),
    ],
    [
        State('modeltype-list-table', 'selectedRowKeys'),
        State('modeltype-list-table', 'clickedContent'),
        State('modeltype-list-table', 'recentlyButtonClickedRow'),
    ],
    prevent_initial_call=True,
)
def modeltype_delete_modal(
    operation_click,
    button_click,
    selected_row_keys,
    clicked_content,
    recently_button_clicked_row,
):
    """
    显示删除模型分类二次确认弹窗回调
    """
    trigger_id = ctx.triggered_id
    if trigger_id == {'index': 'delete', 'type': 'modeltype-operation-button'} or (
        trigger_id == 'modeltype-list-table' and clicked_content == '删除'
    ):
        if trigger_id == {'index': 'delete', 'type': 'modeltype-operation-button'}:
            type_ids = ','.join(selected_row_keys)
        else:
            if clicked_content == '删除':
                type_ids = recently_button_clicked_row['key']
            else:
                raise PreventUpdate

        return [f'是否确认删除模型分类编号为{type_ids}的模型分类？', True, type_ids]

    raise PreventUpdate


@app.callback(
    Output('modeltype-operations-store', 'data', allow_duplicate=True),
    Input('modeltype-delete-confirm-modal', 'okCounts'),
    State('modeltype-delete-ids-store', 'data'),
    prevent_initial_call=True,
)
def modeltype_delete_confirm(delete_confirm, modeltype_ids_data):
    """
    删除模型分类弹窗确认回调，实现删除操作
    """
    if delete_confirm:
        params = modeltype_ids_data
        ModeltypeApi.del_modeltype(params)
        MessageManager.success(content='删除成功')

        return {'type': 'delete'}

    raise PreventUpdate

