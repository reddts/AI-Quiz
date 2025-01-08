import time
import uuid
from dash import ctx, dcc, no_update
from dash.dependencies import ALL, Input, Output, State
from dash.exceptions import PreventUpdate
from typing import Dict
from api.ai.keypool import KeypoolApi
from api.ai.modeltype import ModeltypeApi
from config.constant import SysNormalDisableConstant
from server import app
from utils.common_util import ValidateUtil
from utils.dict_util import DictManager
from utils.feedback_util import MessageManager
from utils.permission_util import PermissionManager
from utils.time_format_util import TimeFormatUtil


def generate_keypool_table(query_params: Dict):
    """
    根据查询参数获取key池表格数据及分页信息

    :param query_params: 查询参数
    :return: key池表格数据及分页信息
    """
    table_info = KeypoolApi.list_keypool(query_params)
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
        item['key_type_label'] = ModeltypeApi.get_modeltype_label(item.get('key_typeid'))['data']
        item['create_time'] = TimeFormatUtil.format_time(
            item.get('create_time')
        )
        item['update_time'] = TimeFormatUtil.format_time(
            item.get('update_time')
        )
        item['key'] = str(item['key_id'])
        item['operation'] = [
            {'content': '修改', 'type': 'link', 'icon': 'antd-edit'}
            if PermissionManager.check_perms('scales:keypool:edit')
            else {},
            {'content': '删除', 'type': 'link', 'icon': 'antd-delete'}
            if PermissionManager.check_perms('scales:keypool:remove')
            else {},
        ]

    return [table_data, table_pagination]


@app.callback(
    output=dict(
        keypool_table_data=Output('keypool-list-table', 'data', allow_duplicate=True),
        keypool_table_pagination=Output(
            'keypool-list-table', 'pagination', allow_duplicate=True
        ),
        keypool_table_key=Output('keypool-list-table', 'key'),
        keypool_table_selectedrowkeys=Output('keypool-list-table', 'selectedRowKeys'),
        modetype_option=Output('keypool-key_typeid-select', 'options'),
    ),
    inputs=dict(
        search_click=Input('keypool-search', 'nClicks'),
        refresh_click=Input('keypool-refresh', 'nClicks'),
        pagination=Input('keypool-list-table', 'pagination'),
        operations=Input('keypool-operations-store', 'data'),
    ),
    state=dict(
        key_typeid=State('keypool-key_typeid-select', 'value'),
        key_name=State('keypool-key_name-input', 'value'),
        status_select=State('keypool-status-select', 'value'),
    ),
    prevent_initial_call=True,
)
def get_keypool_table_data(
    search_click,
    refresh_click,
    pagination,
    operations,
    key_typeid,
    key_name,
    status_select,
):
    """
    获取key池表格数据回调（进行表格相关增删查改操作后均会触发此回调）
    """

    query_params = dict(
        key_typeid=key_typeid,
        key_name=key_name,
        status=status_select,
        page_num=1,
        page_size=10,
    )
    triggered_id = ctx.triggered_id
    modeltype_info = ModeltypeApi.get_modeltype_select()
    if triggered_id == 'keypool-list-table':
        query_params.update(
            {
                'page_num': pagination['current'],
                'page_size': pagination['pageSize'],
            }
        )
    if search_click or refresh_click or pagination or operations:
        table_data, table_pagination = generate_keypool_table(query_params)
        return dict(
            keypool_table_data=table_data,
            modetype_option=[
                    dict(label=item['type_name'], value=item['type_id'])
                    for item in modeltype_info['data']
                    if item
                ]
                or [],
            keypool_table_pagination=table_pagination,
            keypool_table_key=str(uuid.uuid4()),
            keypool_table_selectedrowkeys=None,
        )

    raise PreventUpdate


# 重置key池搜索表单数据回调
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
        Output('keypool-key_typeid-select', 'value'),
        Output('keypool-key_name-input', 'value'),
        Output('keypool-status-select', 'value'),
        Output('keypool-operations-store', 'data'),
    ],
    Input('keypool-reset', 'nClicks'),
    prevent_initial_call=True,
)


# 隐藏/显示key池搜索表单回调
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
        Output('keypool-search-form-container', 'hidden'),
        Output('keypool-hidden-tooltip', 'title'),
    ],
    Input('keypool-hidden', 'nClicks'),
    State('keypool-search-form-container', 'hidden'),
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
    Output({'type': 'keypool-operation-button', 'index': 'edit'}, 'disabled'),
    Input('keypool-list-table', 'selectedRowKeys'),
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
    Output({'type': 'keypool-operation-button', 'index': 'delete'}, 'disabled'),
    Input('keypool-list-table', 'selectedRowKeys'),
    prevent_initial_call=True,
)


# key池表单数据双向绑定回调
app.clientside_callback(
    """
    (row_data, form_value) => {
        trigger_id = window.dash_clientside.callback_context.triggered_id;
        if (trigger_id === 'keypool-form-store') {
            return [window.dash_clientside.no_update, row_data];
        }
        if (trigger_id === 'keypool-form') {
            Object.assign(row_data, form_value);
            return [row_data, window.dash_clientside.no_update];
        }
        throw window.dash_clientside.PreventUpdate;
    }
    """,
    [
        Output('keypool-form-store', 'data', allow_duplicate=True),
        Output('keypool-form', 'values'),
    ],
    [
        Input('keypool-form-store', 'data'),
        Input('keypool-form', 'values'),
    ],
    prevent_initial_call=True,
)


@app.callback(
    output=dict(
        modal_visible=Output('keypool-modal', 'visible', allow_duplicate=True),
        modal_title=Output('keypool-modal', 'title'),
        form_value=Output('keypool-form-store', 'data', allow_duplicate=True),
        modetype_option=Output('keypool-type-select', 'options'),
        form_label_validate_status=Output(
            'keypool-form', 'validateStatuses', allow_duplicate=True
        ),
        form_label_validate_info=Output(
            'keypool-form', 'helps', allow_duplicate=True
        ),
        modal_type=Output('keypool-modal_type-store', 'data'),
    ),
    inputs=dict(
        operation_click=Input(
            {'type': 'keypool-operation-button', 'index': ALL}, 'nClicks'
        ),
        button_click=Input('keypool-list-table', 'nClicksButton'),
    ),
    state=dict(
        selected_row_keys=State('keypool-list-table', 'selectedRowKeys'),
        clicked_content=State('keypool-list-table', 'clickedContent'),
        recently_button_clicked_row=State(
            'keypool-list-table', 'recentlyButtonClickedRow'
        ),
    ),
    prevent_initial_call=True,
)
def add_edit_keypool_modal(
    operation_click,
    button_click,
    selected_row_keys,
    clicked_content,
    recently_button_clicked_row,
):
    """
    显示新增或编辑key池弹窗回调
    """
    trigger_id = ctx.triggered_id
    if (
        trigger_id == {'index': 'add', 'type': 'keypool-operation-button'}
        or trigger_id == {'index': 'edit', 'type': 'keypool-operation-button'}
        or (trigger_id == 'keypool-list-table' and clicked_content == '修改')
    ):
        modeltype_info = ModeltypeApi.get_modeltype_select()
        if trigger_id == {'index': 'add', 'type': 'keypool-operation-button'}:
            keypool_info = dict(
                key_name=None,
                key_typeid=None,
                type_token=None,
                status=SysNormalDisableConstant.NORMAL,
                remark=None,
            )
            return dict(
                modal_visible=True,
                modal_title='新增Key',
                modetype_option=[
                    dict(label=item['type_name'], value=item['type_id'])
                    for item in modeltype_info['data']
                    if item
                ]
                or [],
                form_value=keypool_info,
                form_label_validate_status=None,
                form_label_validate_info=None,
                modal_type={'type': 'add'},                
            )
        elif trigger_id == {
            'index': 'edit',
            'type': 'keypool-operation-button',
        } or (trigger_id == 'keypool-list-table' and clicked_content == '修改'):
            if trigger_id == {'index': 'edit', 'type': 'keypool-operation-button'}:
                key_id = int(','.join(selected_row_keys))
            else:
                key_id = int(recently_button_clicked_row['key'])
            keypool_info_res = KeypoolApi.get_keypool(key_id=key_id)
            keypool_info = keypool_info_res['data']
            modetype_option = modeltype_info['data']
            return dict(
                modal_visible=True,
                modal_title='编辑Key',
                modetype_option=[
                    dict(label=item['type_name'], value=item['type_id'])
                    for item in modetype_option
                    if item
                ]
                or [],
                form_value=keypool_info,
                form_label_validate_status=None,
                form_label_validate_info=None,
                modal_type={'type': 'edit'},
            )

    raise PreventUpdate


@app.callback(
    output=dict(
        form_label_validate_status=Output(
            'keypool-form', 'validateStatuses', allow_duplicate=True
        ),
        form_label_validate_info=Output(
            'keypool-form', 'helps', allow_duplicate=True
        ),
        modal_visible=Output('keypool-modal', 'visible'),
        operations=Output(
            'keypool-operations-store', 'data', allow_duplicate=True
        ),
    ),
    inputs=dict(confirm_trigger=Input('keypool-modal', 'okCounts')),
    state=dict(
        modal_type=State('keypool-modal_type-store', 'data'),
        form_value=State('keypool-form-store', 'data'),
        form_label=State(
            {'type': 'keypool-form-label', 'index': ALL, 'required': True}, 'label'
        ),
    ),
    running=[[Output('keypool-modal', 'confirmLoading'), True, False]],
    prevent_initial_call=True,
)
def keypool_confirm(confirm_trigger, modal_type, form_value, form_label):
    """
    新增或编辑key池弹窗确认回调，实现新增或编辑操作
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
                KeypoolApi.add_keypool(params_add)
            if modal_type == 'edit':
                KeypoolApi.update_keypool(params_edit)
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
        Output('keypool-delete-text', 'children'),
        Output('keypool-delete-confirm-modal', 'visible'),
        Output('keypool-delete-ids-store', 'data'),
    ],
    [
        Input({'type': 'keypool-operation-button', 'index': ALL}, 'nClicks'),
        Input('keypool-list-table', 'nClicksButton'),
    ],
    [
        State('keypool-list-table', 'selectedRowKeys'),
        State('keypool-list-table', 'clickedContent'),
        State('keypool-list-table', 'recentlyButtonClickedRow'),
    ],
    prevent_initial_call=True,
)
def keypool_delete_modal(
    operation_click,
    button_click,
    selected_row_keys,
    clicked_content,
    recently_button_clicked_row,
):
    """
    显示删除key池二次确认弹窗回调
    """
    trigger_id = ctx.triggered_id
    if trigger_id == {'index': 'delete', 'type': 'keypool-operation-button'} or (
        trigger_id == 'keypool-list-table' and clicked_content == '删除'
    ):
        if trigger_id == {'index': 'delete', 'type': 'keypool-operation-button'}:
            key_ids = ','.join(selected_row_keys)
        else:
            if clicked_content == '删除':
                key_ids = recently_button_clicked_row['key']
            else:
                raise PreventUpdate

        return [f'是否确认删除编号为{key_ids}的Key？', True, key_ids]

    raise PreventUpdate


@app.callback(
    Output('keypool-operations-store', 'data', allow_duplicate=True),
    Input('keypool-delete-confirm-modal', 'okCounts'),
    State('keypool-delete-ids-store', 'data'),
    prevent_initial_call=True,
)
def keypool_delete_confirm(delete_confirm, keypool_ids_data):
    """
    删除key池弹窗确认回调，实现删除操作
    """
    if delete_confirm:
        params = keypool_ids_data
        KeypoolApi.del_keypool(params)
        MessageManager.success(content='删除成功')

        return {'type': 'delete'}

    raise PreventUpdate


@app.callback(
    [
        Output('keypool-export-container', 'data', allow_duplicate=True),
        Output('keypool-export-complete-judge-container', 'data'),
    ],
    Input('keypool-export', 'nClicks'),
    [
        State('keypool-key_typeid-select', 'value'),
        State('keypool-key_name-input', 'value'),
        State('keypool-status-select', 'value'),
    ],
    running=[[Output('keypool-export', 'loading'), True, False]],
    prevent_initial_call=True,
)
def export_keypool_list(export_click, key_typeid, key_name, status):
    """
    导出key池信息回调
    """
    if export_click:
        export_params = dict(
            key_typeid=key_typeid, key_name=key_name, status=status
        )
        export_keypool_res = KeypoolApi.export_keypool(export_params)
        export_keypool = export_keypool_res.content
        MessageManager.success(content='导出成功')

        return [
            dcc.send_bytes(
                export_keypool,
                f'key池信息_{time.strftime("%Y%m%d%H%M%S", time.localtime())}.xlsx',
            ),
            {'timestamp': time.time()},
        ]

    raise PreventUpdate


@app.callback(
    Output('keypool-export-container', 'data', allow_duplicate=True),
    Input('keypool-export-complete-judge-container', 'data'),
    prevent_initial_call=True,
)
def reset_keypool_export_status(data):
    """
    导出完成后重置下载组件数据回调，防止重复下载文件
    """
    time.sleep(0.5)
    if data:
        return None

    raise PreventUpdate
