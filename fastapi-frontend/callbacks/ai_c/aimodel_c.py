import time
import uuid
from dash import ctx, dcc, no_update
from dash.dependencies import ALL, Input, Output, State
from dash.exceptions import PreventUpdate
from typing import Dict
from api.ai.aimodel import AiModelApi
from api.ai.modeltype import ModeltypeApi
from config.constant import SysNormalDisableConstant,SysYesNoConstant
from server import app
from utils.common_util import ValidateUtil
from utils.dict_util import DictManager
from utils.feedback_util import MessageManager
from utils.permission_util import PermissionManager
from utils.time_format_util import TimeFormatUtil


def generate_aimodel_table(query_params: Dict):
    """
    根据查询参数获取ai模型表格数据及分页信息

    :param query_params: 查询参数
    :return: ai模型表格数据及分页信息
    """
    table_info = AiModelApi.list_aimodel(query_params)
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
        item['nowused'] = DictManager.get_dict_tag(
            dict_type='sys_yes_no', dict_value=item.get('nowused')
        )
        item['create_time'] = TimeFormatUtil.format_time(
            item.get('create_time')
        )
        item['update_time'] = TimeFormatUtil.format_time(
            item.get('update_time')
        )
        item['key'] = str(item['aimodel_id'])
        item['operation'] = [
            {'content': '修改', 'type': 'link', 'icon': 'antd-edit'}
            if PermissionManager.check_perms('ai:aimodel:edit')
            else {},
            {'content': '删除', 'type': 'link', 'icon': 'antd-delete'}
            if PermissionManager.check_perms('ai:aimodel:remove')
            else {},
        ]

    return [table_data, table_pagination]


@app.callback(
    output=dict(
        aimodel_table_data=Output('aimodel-list-table', 'data', allow_duplicate=True),
        aimodel_table_pagination=Output(
            'aimodel-list-table', 'pagination', allow_duplicate=True
        ),
        aimodel_table_key=Output('aimodel-list-table', 'key'),
        aimodel_table_selectedrowkeys=Output('aimodel-list-table', 'selectedRowKeys'),
    ),
    inputs=dict(
        search_click=Input('aimodel-search', 'nClicks'),
        refresh_click=Input('aimodel-refresh', 'nClicks'),
        pagination=Input('aimodel-list-table', 'pagination'),
        operations=Input('aimodel-operations-store', 'data'),
    ),
    state=dict(
        aimodel_alias=State('aimodel-aimodel_alias-input', 'value'),
        aimodel_name=State('aimodel-aimodel_name-input', 'value'),
        status_select=State('aimodel-status-select', 'value'),
    ),
    prevent_initial_call=True,
)
def get_aimodel_table_data(
    search_click,
    refresh_click,
    pagination,
    operations,
    aimodel_alias,
    aimodel_name,
    status_select,
):
    """
    获取ai模型表格数据回调（进行表格相关增删查改操作后均会触发此回调）
    """

    query_params = dict(
        aimodel_alias=aimodel_alias,
        aimodel_name=aimodel_name,
        status=status_select,
        page_num=1,
        page_size=10,
    )
    triggered_id = ctx.triggered_id
    if triggered_id == 'aimodel-list-table':
        query_params.update(
            {
                'page_num': pagination['current'],
                'page_size': pagination['pageSize'],
            }
        )
    if search_click or refresh_click or pagination or operations:
        table_data, table_pagination = generate_aimodel_table(query_params)
        return dict(
            aimodel_table_data=table_data,
            aimodel_table_pagination=table_pagination,
            aimodel_table_key=str(uuid.uuid4()),
            aimodel_table_selectedrowkeys=None,
        )

    raise PreventUpdate


# 重置ai模型搜索表单数据回调
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
        Output('aimodel-aimodel_alias-input', 'value'),
        Output('aimodel-aimodel_name-input', 'value'),
        Output('aimodel-status-select', 'value'),
        Output('aimodel-operations-store', 'data'),
    ],
    Input('aimodel-reset', 'nClicks'),
    prevent_initial_call=True,
)


# 隐藏/显示ai模型搜索表单回调
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
        Output('aimodel-search-form-container', 'hidden'),
        Output('aimodel-hidden-tooltip', 'title'),
    ],
    Input('aimodel-hidden', 'nClicks'),
    State('aimodel-search-form-container', 'hidden'),
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
    Output({'type': 'aimodel-operation-button', 'index': 'edit'}, 'disabled'),
    Input('aimodel-list-table', 'selectedRowKeys'),
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
    Output({'type': 'aimodel-operation-button', 'index': 'delete'}, 'disabled'),
    Input('aimodel-list-table', 'selectedRowKeys'),
    prevent_initial_call=True,
)


# ai模型表单数据双向绑定回调
app.clientside_callback(
    """
    (row_data, form_value) => {
        trigger_id = window.dash_clientside.callback_context.triggered_id;
        if (trigger_id === 'aimodel-form-store') {
            return [window.dash_clientside.no_update, row_data];
        }
        if (trigger_id === 'aimodel-form') {
            Object.assign(row_data, form_value);
            return [row_data, window.dash_clientside.no_update];
        }
        throw window.dash_clientside.PreventUpdate;
    }
    """,
    [
        Output('aimodel-form-store', 'data', allow_duplicate=True),
        Output('aimodel-form', 'values'),
    ],
    [
        Input('aimodel-form-store', 'data'),
        Input('aimodel-form', 'values'),
    ],
    prevent_initial_call=True,
)


@app.callback(
    output=dict(
        modal_visible=Output('aimodel-modal', 'visible', allow_duplicate=True),
        modal_title=Output('aimodel-modal', 'title'),
        modetype_option=Output('model-type-select', 'options'),
        form_value=Output('aimodel-form-store', 'data', allow_duplicate=True),
        form_label_validate_status=Output(
            'aimodel-form', 'validateStatuses', allow_duplicate=True
        ),
        form_label_validate_info=Output(
            'aimodel-form', 'helps', allow_duplicate=True
        ),
        modal_type=Output('aimodel-modal_type-store', 'data'),
    ),
    inputs=dict(
        operation_click=Input(
            {'type': 'aimodel-operation-button', 'index': ALL}, 'nClicks'
        ),
        button_click=Input('aimodel-list-table', 'nClicksButton'),
    ),
    state=dict(
        selected_row_keys=State('aimodel-list-table', 'selectedRowKeys'),
        clicked_content=State('aimodel-list-table', 'clickedContent'),
        recently_button_clicked_row=State(
            'aimodel-list-table', 'recentlyButtonClickedRow'
        ),
    ),
    prevent_initial_call=True,
)
def add_edit_aimodel_modal(
    operation_click,
    button_click,
    selected_row_keys,
    clicked_content,
    recently_button_clicked_row,
):
    """
    显示新增或编辑ai模型弹窗回调
    """
    trigger_id = ctx.triggered_id
    if (
        trigger_id == {'index': 'add', 'type': 'aimodel-operation-button'}
        or trigger_id == {'index': 'edit', 'type': 'aimodel-operation-button'}
        or (trigger_id == 'aimodel-list-table' and clicked_content == '修改')
    ):
        modeltype_info = ModeltypeApi.get_modeltype_select()
        if trigger_id == {'index': 'add', 'type': 'aimodel-operation-button'}:
            aimodel_info = dict(
                aimodel_name=None,
                aimodel_alias=None,
                type_id=None,
                nowused=SysYesNoConstant.NO,
                context_num=6,
                maxtoken=128000,
                temperature=1,
                top_p=1,
                frequency=0,
                presence=0,                
                status=SysNormalDisableConstant.NORMAL,
                remark=None,
            )
            return dict(
                modal_visible=True,
                modal_title='新增AI模型',
                modetype_option=[
                    dict(label=item['type_name'], value=item['type_id'])
                    for item in modeltype_info['data']
                    if item
                ]
                or [],
                form_value=aimodel_info,
                form_label_validate_status=None,
                form_label_validate_info=None,
                modal_type={'type': 'add'},                
            )
        elif trigger_id == {
            'index': 'edit',
            'type': 'aimodel-operation-button',
        } or (trigger_id == 'aimodel-list-table' and clicked_content == '修改'):
            if trigger_id == {'index': 'edit', 'type': 'aimodel-operation-button'}:
                aimodel_id = int(','.join(selected_row_keys))
            else:
                aimodel_id = int(recently_button_clicked_row['key'])
            aimodel_info_res = AiModelApi.get_aimodel(aimodel_id=aimodel_id)
            aimodel_info = aimodel_info_res['data']
            modetype_option = modeltype_info['data']
            return dict(
                modal_visible=True,
                modal_title='编辑AI模型',
                modetype_option=[
                    dict(label=item['type_name'], value=item['type_id'])
                    for item in modetype_option
                    if item
                ]
                or [],
                form_value=aimodel_info,
                form_label_validate_status=None,
                form_label_validate_info=None,
                modal_type={'type': 'edit'},
            )

    raise PreventUpdate


@app.callback(
    output=dict(
        form_label_validate_status=Output(
            'aimodel-form', 'validateStatuses', allow_duplicate=True
        ),
        form_label_validate_info=Output(
            'aimodel-form', 'helps', allow_duplicate=True
        ),
        modal_visible=Output('aimodel-modal', 'visible'),
        operations=Output(
            'aimodel-operations-store', 'data', allow_duplicate=True
        ),
    ),
    inputs=dict(confirm_trigger=Input('aimodel-modal', 'okCounts')),
    state=dict(
        modal_type=State('aimodel-modal_type-store', 'data'),
        form_value=State('aimodel-form-store', 'data'),
        form_label=State(
            {'type': 'aimodel-form-label', 'index': ALL, 'required': True}, 'label'
        ),
    ),
    running=[[Output('aimodel-modal', 'confirmLoading'), True, False]],
    prevent_initial_call=True,
)
def aimodel_confirm(confirm_trigger, modal_type, form_value, form_label):
    """
    新增或编辑ai模型弹窗确认回调，实现新增或编辑操作
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
                AiModelApi.add_aimodel(params_add)
            if modal_type == 'edit':
                AiModelApi.update_aimodel(params_edit)
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
        Output('aimodel-delete-text', 'children'),
        Output('aimodel-delete-confirm-modal', 'visible'),
        Output('aimodel-delete-ids-store', 'data'),
    ],
    [
        Input({'type': 'aimodel-operation-button', 'index': ALL}, 'nClicks'),
        Input('aimodel-list-table', 'nClicksButton'),
    ],
    [
        State('aimodel-list-table', 'selectedRowKeys'),
        State('aimodel-list-table', 'clickedContent'),
        State('aimodel-list-table', 'recentlyButtonClickedRow'),
    ],
    prevent_initial_call=True,
)
def aimodel_delete_modal(
    operation_click,
    button_click,
    selected_row_keys,
    clicked_content,
    recently_button_clicked_row,
):
    """
    显示删除ai模型二次确认弹窗回调
    """
    trigger_id = ctx.triggered_id
    if trigger_id == {'index': 'delete', 'type': 'aimodel-operation-button'} or (
        trigger_id == 'aimodel-list-table' and clicked_content == '删除'
    ):
        if trigger_id == {'index': 'delete', 'type': 'aimodel-operation-button'}:
            aimodel_ids = ','.join(selected_row_keys)
        else:
            if clicked_content == '删除':
                aimodel_ids = recently_button_clicked_row['key']
            else:
                raise PreventUpdate

        return [f'是否确认删除AI模型编号为{aimodel_ids}的AI模型？', True, aimodel_ids]

    raise PreventUpdate


@app.callback(
    Output('aimodel-operations-store', 'data', allow_duplicate=True),
    Input('aimodel-delete-confirm-modal', 'okCounts'),
    State('aimodel-delete-ids-store', 'data'),
    prevent_initial_call=True,
)
def aimodel_delete_confirm(delete_confirm, aimodel_ids_data):
    """
    删除ai模型弹窗确认回调，实现删除操作
    """
    if delete_confirm:
        params = aimodel_ids_data
        AiModelApi.del_aimodel(params)
        MessageManager.success(content='删除成功')

        return {'type': 'delete'}

    raise PreventUpdate


@app.callback(
    [
        Output('aimodel-export-container', 'data', allow_duplicate=True),
        Output('aimodel-export-complete-judge-container', 'data'),
    ],
    Input('aimodel-export', 'nClicks'),
    [
        State('aimodel-aimodel_name-input', 'value'),
        State('aimodel-aimodel_alias-input', 'value'),
        State('aimodel-status-select', 'value'),
    ],
    running=[[Output('aimodel-export', 'loading'), True, False]],
    prevent_initial_call=True,
)
def export_aimodel_list(export_click, aimodel_alias, aimodel_name, status):
    """
    导出ai模型信息回调
    """
    if export_click:
        export_params = dict(
            aimodel_alias=aimodel_alias, aimodel_name=aimodel_name, status=status
        )
        export_aimodel_res = AiModelApi.export_aimodel(export_params)
        export_aimodel = export_aimodel_res.content
        MessageManager.success(content='导出成功')

        return [
            dcc.send_bytes(
                export_aimodel,
                f'AI模型信息_{time.strftime("%Y%m%d%H%M%S", time.localtime())}.xlsx',
            ),
            {'timestamp': time.time()},
        ]

    raise PreventUpdate


@app.callback(
    Output('aimodel-export-container', 'data', allow_duplicate=True),
    Input('aimodel-export-complete-judge-container', 'data'),
    prevent_initial_call=True,
)
def reset_aimodel_export_status(data):
    """
    导出完成后重置下载组件数据回调，防止重复下载文件
    """
    time.sleep(0.5)
    if data:
        return None

    raise PreventUpdate
