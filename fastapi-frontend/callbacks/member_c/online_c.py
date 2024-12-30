import uuid
from dash import ctx
from dash.dependencies import ALL, Input, Output, State
from dash.exceptions import PreventUpdate
from typing import Dict
from api.member.online import OnlineApi
from server import app
from utils.feedback_util import MessageManager
from utils.permission_util import PermissionManager


def generate_online_table(query_params: Dict):
    """
    根据查询参数获取在线会员表格数据及分页信息

    :param query_params: 查询参数
    :return: 在线会员表格数据及分页信息
    """
    table_info = OnlineApi.list_online(query_params)
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
        item['key'] = str(item['token_id'])
        item['operation'] = [
            {'content': '强退', 'type': 'link', 'icon': 'antd-delete'}
            if PermissionManager.check_perms('member:online:forceLogout')
            else {},
        ]

    return [table_data, table_pagination]


@app.callback(
    output=dict(
        online_table_data=Output(
            'online-member-list-table', 'data', allow_duplicate=True
        ),
        online_table_pagination=Output(
            'online-member-list-table', 'pagination', allow_duplicate=True
        ),
        online_table_key=Output('online-member-list-table', 'key'),
        online_table_selectedrowkeys=Output(
            'online-member-list-table', 'selectedRowKeys'
        ),
    ),
    inputs=dict(
        search_click=Input('online-member-search', 'nClicks'),
        refresh_click=Input('online-member-refresh', 'nClicks'),
        pagination=Input('online-member-list-table', 'pagination'),
        operations=Input('online-member-operations-store', 'data'),
    ),
    state=dict(
        ipaddr=State('online-member-ipaddr-input', 'value'),
        member_name=State('online-member-member_name-input', 'value'),
    ),
    prevent_initial_call=True,
)
def get_online_table_data(
    search_click,
    refresh_click,
    pagination,
    operations,
    ipaddr,
    member_name,
):
    """
    获取在线会员表格数据回调（进行表格相关增删查改操作后均会触发此回调）
    """
    query_params = dict(
        ipaddr=ipaddr, member_name=member_name, page_num=1, page_size=10
    )
    triggered_id = ctx.triggered_id
    if triggered_id == 'online-member-list-table':
        query_params.update(
            {
                'page_num': pagination['current'],
                'page_size': pagination['pageSize'],
            }
        )
    if search_click or refresh_click or pagination or operations:
        table_data, table_pagination = generate_online_table(query_params)
        return dict(
            online_table_data=table_data,
            online_table_pagination=table_pagination,
            online_table_key=str(uuid.uuid4()),
            online_table_selectedrowkeys=None,
        )

    raise PreventUpdate


# 重置在线会员搜索表单数据回调
app.clientside_callback(
    """
    (reset_click) => {
        if (reset_click) {
            return [null, null, {'type': 'reset'}]
        }
        return window.dash_clientside.no_update;
    }
    """,
    [
        Output('online-member-ipaddr-input', 'value'),
        Output('online-member-member_name-input', 'value'),
        Output('online-member-operations-store', 'data'),
    ],
    Input('online-member-reset', 'nClicks'),
    prevent_initial_call=True,
)


# 隐藏/显示在线会员搜索表单回调
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
        Output('online-member-search-form-container', 'hidden'),
        Output('online-member-hidden-tooltip', 'title'),
    ],
    Input('online-member-hidden', 'nClicks'),
    State('online-member-search-form-container', 'hidden'),
    prevent_initial_call=True,
)


# 根据选择的表格数据行数控制批量强退按钮状态回调
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
    Output({'type': 'online-member-operation-button', 'index': 'delete'}, 'disabled'),
    Input('online-member-list-table', 'selectedRowKeys'),
    prevent_initial_call=True,
)


@app.callback(
    [
        Output('online-member-delete-text', 'children'),
        Output('online-member-delete-confirm-modal', 'visible'),
        Output('online-member-delete-ids-store', 'data'),
    ],
    [
        Input({'type': 'online-member-operation-button', 'index': ALL}, 'nClicks'),
        Input('online-member-list-table', 'nClicksButton'),
    ],
    [
        State('online-member-list-table', 'selectedRowKeys'),
        State('online-member-list-table', 'clickedContent'),
        State('online-member-list-table', 'recentlyButtonClickedRow'),
    ],
    prevent_initial_call=True,
)
def online_delete_modal(
    operation_click,
    button_click,
    selected_row_keys,
    clicked_content,
    recently_button_clicked_row,
):
    """
    显示强退在线会员二次确认弹窗回调
    """
    trigger_id = ctx.triggered_id
    if trigger_id == {'index': 'delete', 'type': 'online-operation-button'} or (
        trigger_id == 'online-member-list-table' and clicked_content == '强退'
    ):
        if trigger_id == {'index': 'delete', 'type': 'online-operation-button'}:
            session_ids = ','.join(selected_row_keys)
        else:
            if clicked_content == '强退':
                session_ids = recently_button_clicked_row['key']
            else:
                raise PreventUpdate

        return [
            f'是否确认强退会话编号为{session_ids}的会话？',
            True,
            session_ids,
        ]

    raise PreventUpdate


@app.callback(
    Output('online-member-operations-store', 'data', allow_duplicate=True),
    Input('online-member-delete-confirm-modal', 'okCounts'),
    State('online-member-delete-ids-store', 'data'),
    prevent_initial_call=True,
)
def online_delete_confirm(delete_confirm, session_ids_data):
    """
    强退在线会员弹窗确认回调，实现强退操作
    """
    if delete_confirm:
        params = session_ids_data
        OnlineApi.force_logout(params)
        MessageManager.success(content='强退成功')

        return {'type': 'force'}

    raise PreventUpdate
