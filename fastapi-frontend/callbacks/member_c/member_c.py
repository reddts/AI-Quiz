import base64
import time
import uuid
from io import BytesIO
from dash import ctx, dcc, no_update
from dash.dependencies import ALL, Input, Output, State
from dash.exceptions import PreventUpdate
from typing import Dict
from api.member.member import MemberApi
from config.constant import SysNormalDisableConstant
from server import app
from utils.common_util import ValidateUtil
from utils.feedback_util import MessageManager
from utils.permission_util import PermissionManager
from utils.time_format_util import TimeFormatUtil
from views.member import mavatar

def generate_member_table(query_params: Dict):
    """
    根据查询参数获取会员表格数据及分页信息

    :param query_params: 查询参数
    :return: 会员表格数据及分页信息
    """
    table_info = MemberApi.list_member(query_params)
    table_data = table_info['rows']
    table_pagination = dict(
        pageSize=table_info['page_size'],
        current=table_info['page_num'],
        showSizeChanger=True,
        pageSizeOptions=[10, 30, 50, 100],
        showQuickJumper=True,
        total=table_info['total'],
    )
    gender_map = {0: "男性", 1: "女性", 2: "未知", None: "未知"}
    for item in table_data:
        item['gender'] = gender_map.get(int(item.get('gender')), "未知")
        if item['status'] == SysNormalDisableConstant.NORMAL:
            item['status'] = dict(checked=True, disabled=False)
        else:
            item['status'] = dict(checked=False, disabled=False)
        item['create_at'] = TimeFormatUtil.format_time(
            item.get('create_at')
        )
        item['key'] = str(item['member_id'])
        
        item['operation'] = [
            {'title': '修改', 'icon': 'antd-edit'}
            if PermissionManager.check_perms('member:edit')
            else None,
            {'title': '删除', 'icon': 'antd-delete'}
            if PermissionManager.check_perms('member:remove')
            else None,
            {'title': '重置密码', 'icon': 'antd-key'}
            if PermissionManager.check_perms('member:resetPwd')
            else None,
        ]

    return [table_data, table_pagination]

@app.callback(
    output=dict(
        member_table_data=Output('member-list-table', 'data', allow_duplicate=True),
        member_table_pagination=Output(
            'member-list-table', 'pagination', allow_duplicate=True
        ),
        member_table_key=Output('member-list-table', 'key'),
        member_table_selectedrowkeys=Output('member-list-table', 'selectedRowKeys'),
    ),
    inputs=dict(
        search_click=Input('member-search', 'nClicks'),
        refresh_click=Input('member-refresh', 'nClicks'),
        pagination=Input('member-list-table', 'pagination'),
        operations=Input('member-operations-store', 'data'),
    ),
    state=dict(
        member_name=State('member-member_name-input', 'value'),
        phone_number=State('member-phone_number-input', 'value'),
        status_select=State('member-status-select', 'value'),
        create_time_range=State('member-create_time-range', 'value'),
    ),
    prevent_initial_call=True,
)
def get_member_table_data(
    search_click,
    refresh_click,
    pagination,
    operations,
    member_name,
    phone_number,
    status_select,
    create_time_range,
):
    """
    获取会员表格数据回调（进行表格相关增删查改操作后均会触发此回调）
    """
    begin_time = None
    end_time = None
    if create_time_range:
        begin_time = create_time_range[0]
        end_time = create_time_range[1]
    query_params = dict(
        member_name=member_name,
        phonenumber=phone_number,
        status=status_select,
        begin_time=begin_time,
        end_time=end_time,
        page_num=1,
        page_size=10,
    )
    triggered_id = ctx.triggered_id
    if triggered_id == 'member-list-table':
        query_params.update(
            {
                'page_num': pagination['current'],
                'page_size': pagination['pageSize'],
            }
        )
    if search_click or refresh_click or pagination or operations:
        table_data, table_pagination = generate_member_table(query_params)

        return dict(
            member_table_data=table_data,
            member_table_pagination=table_pagination,
            member_table_key=str(uuid.uuid4()),
            member_table_selectedrowkeys=None,
        )

    raise PreventUpdate


# 重置会员搜索表单数据回调
app.clientside_callback(
    """
    (reset_click) => {
        if (reset_click) {
            return [null, null, null, null, {'type': 'reset'}]
        }
        return window.dash_clientside.no_update;
    }
    """,
    [
        Output('member-member_name-input', 'value'),
        Output('member-phone_number-input', 'value'),
        Output('member-status-select', 'value'),
        Output('member-create_time-range', 'value'),
        Output('member-operations-store', 'data'),
    ],
    Input('member-reset', 'nClicks'),
    prevent_initial_call=True,
)


# 隐藏/显示会员搜索表单回调
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
        Output('member-search-form-container', 'hidden'),
        Output('member-hidden-tooltip', 'title'),
    ],
    Input('member-hidden', 'nClicks'),
    State('member-search-form-container', 'hidden'),
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
    Output({'type': 'member-operation-button', 'index': 'edit'}, 'disabled'),
    Input('member-list-table', 'selectedRowKeys'),
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
    Output({'type': 'member-operation-button', 'index': 'delete'}, 'disabled'),
    Input('member-list-table', 'selectedRowKeys'),
    prevent_initial_call=True,
)


# 会员表单数据双向绑定回调
app.clientside_callback(
    """
    (row_data, form_value) => {
        trigger_id = window.dash_clientside.callback_context.triggered_id;
        if (trigger_id === 'member-form-store') {
            return [window.dash_clientside.no_update, row_data];
        }
        if (trigger_id === 'member-form') {
            Object.assign(row_data, form_value);
            return [row_data, window.dash_clientside.no_update];
        }
        throw window.dash_clientside.PreventUpdate;
    }
    """,
    [
        Output('member-form-store', 'data', allow_duplicate=True),
        Output('member-form', 'values'),
    ],
    [
        Input('member-form-store', 'data'),
        Input('member-form', 'values'),
    ],
    prevent_initial_call=True,
)
@app.callback(
    output=dict(
        modal_visible=Output('member-modal', 'visible', allow_duplicate=True),
        modal_title=Output('member-modal', 'title'),
        member_name_disabled=Output('member-form-member_name', 'disabled'),
        password_disabled=Output('member-form-password', 'disabled'),
        member_name_password_container=Output(
            'member-member_name-password-container', 'hidden'
        ),
        form_value=Output('member-form-store', 'data', allow_duplicate=True),
        form_label_validate_status=Output(
            'member-form', 'validateStatuses', allow_duplicate=True
        ),
        form_label_validate_info=Output(
            'member-form', 'helps', allow_duplicate=True
        ),
        modal_type=Output('member-modal_type-store', 'data'),
        m_avatar_container=Output('member-avatar-container', 'children'),
    ),
    inputs=dict(
        operation_click=Input(
            {'type': 'member-operation-button', 'index': ALL}, 'nClicks'
        ),
        dropdown_click=Input('member-list-table', 'nClicksDropdownItem'),
    ),
    state=dict(
        selected_row_keys=State('member-list-table', 'selectedRowKeys'),
        recently_clicked_dropdown_item_title=State(
            'member-list-table', 'recentlyClickedDropdownItemTitle'
        ),
        recently_dropdown_item_clicked_row=State(
            'member-list-table', 'recentlyDropdownItemClickedRow'
        ),
    ),
    prevent_initial_call=True,
)
def add_edit_member_modal(
    operation_click,
    dropdown_click,
    selected_row_keys,
    recently_clicked_dropdown_item_title,
    recently_dropdown_item_clicked_row,
):
    """
    显示新增或编辑会员弹窗回调
    """
    trigger_id = ctx.triggered_id
    if (
        trigger_id == {'index': 'add', 'type': 'member-operation-button'}
        or trigger_id == {'index': 'edit', 'type': 'member-operation-button'}
        or (
            trigger_id == 'member-list-table'
            and recently_clicked_dropdown_item_title == '修改'
        )
    ):
        if trigger_id == {'index': 'add', 'type': 'member-operation-button'}:
            member_info = dict(
                nick_name=None,
                phonenumber=None,
                email=None,
                member_name=None,
                password=None,
                member_ids=None,
                gender=None,
                status=SysNormalDisableConstant.NORMAL,
                remark=None,
            )
            return dict(
                modal_visible=True,
                modal_title='新增会员',                
                member_name_disabled=False,
                password_disabled=False,
                member_name_password_container=False,
                form_value=member_info,
                form_label_validate_status=None,
                form_label_validate_info=None,
                modal_type={'type': 'add'},
                m_avatar_container = mavatar.render('',''),
            )
        elif trigger_id == {
            'index': 'edit',
            'type': 'member-operation-button',
        } or (
            trigger_id == 'member-list-table'
            and recently_clicked_dropdown_item_title == '修改'
        ):
            if trigger_id == {'index': 'edit', 'type': 'member-operation-button'}:
                member_id = int(','.join(selected_row_keys))
            else:
                member_id = int(recently_dropdown_item_clicked_row['key'])
            member_info_res = MemberApi.get_member(member_id=member_id)
            member_info = member_info_res['data']
            return dict(
                modal_visible=True,
                modal_title='编辑会员',                
                member_name_disabled=True,
                password_disabled=True,
                member_name_password_container=True,
                form_value=member_info,
                form_label_validate_status=None,
                form_label_validate_info=None,
                modal_type={'type': 'edit'},
                m_avatar_container = mavatar.render(member_id, member_info['avatar']),
            )

    raise PreventUpdate

#新增，修改弹窗确认回调
@app.callback(
    output=dict(
        form_label_validate_status=Output(
            'member-form', 'validateStatuses', allow_duplicate=True
        ),
        form_label_validate_info=Output(
            'member-form', 'helps', allow_duplicate=True
        ),
        modal_visible=Output('member-modal', 'visible'),
        operations=Output(
            'member-operations-store', 'data', allow_duplicate=True
        ),
    ),
    inputs=dict(confirm_trigger=Input('member-modal', 'okCounts')),
    state=dict(
        modal_type=State('member-modal_type-store', 'data'),
        form_value=State('member-form-store', 'data'),
        form_label=State(
            {'type': 'member-form-label', 'index': ALL, 'required': True}, 'label'
        ),
    ),
    running=[[Output('member-modal', 'confirmLoading'), True, False]],
    prevent_initial_call=True,
)
def member_confirm(confirm_trigger, modal_type, form_value, form_label):
    """
    新增或编辑会员弹窗确认回调，实现新增或编辑操作
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
                MemberApi.add_member(params_add)
            if modal_type == 'edit':
                MemberApi.update_member(params_edit)
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
    Output('member-operations-store', 'data', allow_duplicate=True),
    [
        Input('member-list-table', 'recentlySwitchDataIndex'),
        Input('member-list-table', 'recentlySwitchStatus'),
        Input('member-list-table', 'recentlySwitchRow'),
    ],
    prevent_initial_call=True,
)
def table_switch_member_status(
    recently_switch_data_index, recently_switch_status, recently_switch_row
):
    """
    表格内切换会员状态回调
    """
    if recently_switch_data_index:
        MemberApi.change_member_status(
            member_id=int(recently_switch_row['key']),
            status='0' if recently_switch_status else '1',
        )
        MessageManager.success(content='修改成功')

        return {'type': 'switch-status'}

    raise PreventUpdate


@app.callback(
    [
        Output('member-delete-text', 'children'),
        Output('member-delete-confirm-modal', 'visible'),
        Output('member-delete-ids-store', 'data'),
    ],
    [
        Input({'type': 'member-operation-button', 'index': ALL}, 'nClicks'),
        Input('member-list-table', 'nClicksDropdownItem'),
    ],
    [
        State('member-list-table', 'selectedRowKeys'),
        State('member-list-table', 'recentlyClickedDropdownItemTitle'),
        State('member-list-table', 'recentlyDropdownItemClickedRow'),
    ],
    prevent_initial_call=True,
)
def member_delete_modal(
    operation_click,
    dropdown_click,
    selected_row_keys,
    recently_clicked_dropdown_item_title,
    recently_dropdown_item_clicked_row,
):
    """
    显示删除会员二次确认弹窗回调
    """
    trigger_id = ctx.triggered_id
    if trigger_id == {'index': 'delete', 'type': 'member-operation-button'} or (
        trigger_id == 'member-list-table'
        and recently_clicked_dropdown_item_title == '删除'
    ):
        if trigger_id == {'index': 'delete', 'type': 'member-operation-button'}:
            member_ids = ','.join(selected_row_keys)
        else:
            if recently_clicked_dropdown_item_title == '删除':
                member_ids = recently_dropdown_item_clicked_row['key']
            else:
                raise PreventUpdate

        return [
            f'是否确认删除会员编号为{member_ids}的会员？',
            True,
            member_ids,
        ]

    raise PreventUpdate


@app.callback(
    Output('member-operations-store', 'data', allow_duplicate=True),
    Input('member-delete-confirm-modal', 'okCounts'),
    State('member-delete-ids-store', 'data'),
    prevent_initial_call=True,
)
def member_delete_confirm(delete_confirm, member_ids_data):
    """
    删除会员弹窗确认回调，实现删除操作
    """
    if delete_confirm:
        params = member_ids_data
        MemberApi.del_member(params)
        MessageManager.success(content='删除成功')

        return {'type': 'delete'}

    raise PreventUpdate


@app.callback(
    [
        Output(
            'member-reset-password-confirm-modal', 'visible', allow_duplicate=True
        ),
        Output('member-reset-password-row-key-store', 'data'),
        Output('member-reset-password-input', 'value'),
    ],
    Input('member-list-table', 'nClicksDropdownItem'),
    [
        State('member-list-table', 'recentlyClickedDropdownItemTitle'),
        State('member-list-table', 'recentlyDropdownItemClickedRow'),
    ],
    prevent_initial_call=True,
)
def member_reset_password_modal(
    dropdown_click,
    recently_clicked_dropdown_item_title,
    recently_dropdown_item_clicked_row,
):
    """
    显示重置会员密码弹窗回调
    """
    if dropdown_click:
        if recently_clicked_dropdown_item_title == '重置密码':
            member_id = recently_dropdown_item_clicked_row['key']
        else:
            raise PreventUpdate

        return [True, member_id, None]

    raise PreventUpdate


@app.callback(
    [
        Output('member-operations-store', 'data', allow_duplicate=True),
        Output(
            'member-reset-password-confirm-modal', 'visible', allow_duplicate=True
        ),
    ],
    Input('member-reset-password-confirm-modal', 'okCounts'),
    [
        State('member-reset-password-row-key-store', 'data'),
        State('member-reset-password-input', 'value'),
    ],
    running=[
        [
            Output('member-reset-password-confirm-modal', 'confirmLoading'),
            True,
            False,
        ]
    ],
    prevent_initial_call=True,
)
def member_reset_password_confirm(reset_confirm, member_id_data, reset_password):
    """
    重置会员密码弹窗确认回调，实现重置密码操作
    """
    if reset_confirm:
        MemberApi.reset_member_pwd(
            member_id=int(member_id_data), password=reset_password
        )
        MessageManager.success(content='重置成功')

        return [{'type': 'reset-password'}, False]

    raise PreventUpdate



# 显示会员导入弹窗及重置上传弹窗组件状态回调
app.clientside_callback(
    """
    (nClicks) => {
        if (nClicks) {
            return [
                true, 
                null, 
                false
            ];
        }
        return [
            false,
            window.dash_clientside.no_update,
            window.dash_clientside.no_update
        ];
    }
    """,
    [
        Output('member-import-confirm-modal', 'visible', allow_duplicate=True),
        Output('member-upload-choose', 'contents'),
        Output('member-import-update-check', 'checked'),
    ],
    Input('member-import', 'nClicks'),
    prevent_initial_call=True,
)


@app.callback(
    output=dict(
        result_modal_visible=Output('member-batch-result-modal', 'visible'),
        import_modal_visible=Output(
            'member-import-confirm-modal', 'visible', allow_duplicate=True
        ),
        batch_result=Output('member-batch-result-content', 'children'),
        operations=Output(
            'member-operations-store', 'data', allow_duplicate=True
        ),
    ),
    inputs=dict(import_confirm=Input('member-import-confirm-modal', 'okCounts')),
    state=dict(
        contents=State('member-upload-choose', 'contents'),
        is_update=State('member-import-update-check', 'checked'),
    ),
    running=[
        [Output('member-import-confirm-modal', 'confirmLoading'), True, False],
        [Output('member-import-confirm-modal', 'okText'), '导入中', '导入'],
    ],
    prevent_initial_call=True,
)
def member_import_confirm(import_confirm, contents, is_update):
    """
    会员导入弹窗确认回调，实现批量导入会员操作
    """
    if import_confirm:
        if contents:
            # url = list_upload_task_record[-1].get('url')
            # batch_param = dict(url=url, is_update=is_update)
            batch_import_result = MemberApi.import_member(
                file=BytesIO(base64.b64decode(contents.split(',', 1)[1])),
                update_support=is_update,
            )
            MessageManager.success(content='导入成功')

            return dict(
                result_modal_visible=True
                if batch_import_result.get('msg')
                else False,
                import_modal_visible=True
                if batch_import_result.get('msg')
                else False,
                batch_result=batch_import_result.get('msg'),
                operations={'type': 'batch-import'},
            )
        else:
            MessageManager.warning(content='请上传需要导入的文件')

            return dict(
                result_modal_visible=no_update,
                import_modal_visible=True,
                batch_result=no_update,
                operations=no_update,
            )

    raise PreventUpdate


@app.callback(
    [
        Output('member-export-container', 'data', allow_duplicate=True),
        Output(
            'member-export-complete-judge-container', 'data', allow_duplicate=True
        ),
    ],
    Input('download-member-import-template', 'nClicks'),
    prevent_initial_call=True,
)
def download_member_template(download_click):
    """
    下载导入会员模板回调
    """
    if download_click:
        download_template_res = MemberApi.download_template()
        download_template = download_template_res.content
        MessageManager.success(content='下载成功')

        return [
            dcc.send_bytes(
                download_template,
                f'会员导入模板_{time.strftime("%Y%m%d%H%M%S", time.localtime())}.xlsx',
            ),
            {'timestamp': time.time()},
        ]

    raise PreventUpdate

@app.callback(
        [
            Output('member-export-container', 'data', allow_duplicate=True),
            Output(
                'member-export-complete-judge-container', 'data', allow_duplicate=True
            ),
        ],
        Input('member-export', 'nClicks'),
        [
            State('member-member_name-input', 'value'),
            State('member-phone_number-input', 'value'),
            State('member-status-select', 'value'),
            State('member-create_time-range', 'value'),
        ],
        running=[[Output('member-export', 'loading'), True, False]],
        prevent_initial_call=True,
    )
def export_member_list(
        export_click,
        member_name,
        phone_number,
        status_select,
        create_time_range,
):
        """
        导出会员信息回调
        """
        if export_click:
            begin_time = None
            end_time = None
            if create_time_range:
                begin_time = create_time_range[0]
                end_time = create_time_range[1]
            export_params = dict(
                member_name=member_name,
                phonenumber=phone_number,
                status=status_select,
                begin_time=begin_time,
                end_time=end_time,
            )
            export_member_res = MemberApi.export_member(export_params)
            MessageManager.success(content='导出成功')

            export_member = export_member_res.content

            return [
                dcc.send_bytes(
                    export_member,
                    f'会员信息_{time.strftime("%Y%m%d%H%M%S", time.localtime())}.xlsx',
                ),
                {'timestamp': time.time()},
            ]

        raise PreventUpdate


@app.callback(
        Output('member-export-container', 'data', allow_duplicate=True),
        Input('member-export-complete-judge-container', 'data'),
        prevent_initial_call=True,
    )
def reset_member_export_status(data):
        """
        导出完成后重置下载组件数据回调，防止重复下载文件
        """
        time.sleep(0.5)
        if data:
            return None

        raise PreventUpdate
