import feffery_antd_components as fac
from dash import dcc, html
from api.member.member import MemberApi
from callbacks.member_c import member_c
from components import ManuallyUpload
from components.ApiRadioGroup import ApiRadioGroup
from components.ApiSelect import ApiSelect
from utils.permission_util import PermissionManager


def render(*args, **kwargs):
    query_params = dict(page_num=1, page_size=10)
    table_data, table_pagination = member_c.generate_member_table(query_params)

    return [
        # 用于导出成功后重置dcc.Download的状态，防止多次下载文件
        dcc.Store(id='member-export-complete-judge-container'),
        # 绑定的导出组件
        dcc.Download(id='member-export-container'),
        # 用户管理模块操作类型存储容器
        dcc.Store(id='member-operations-store'),
        # 用户管理模块弹窗类型存储容器
        dcc.Store(id='member-modal_type-store'),
        # 用户管理模块表单数据存储容器
        dcc.Store(id='member-form-store'),
        # 用户管理模块删除操作行key存储容器
        dcc.Store(id='member-delete-ids-store'),
        fac.AntdRow(
            [                
                fac.AntdCol(
                    [
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    html.Div(
                                        [
                                            fac.AntdForm(
                                                [
                                                    fac.AntdSpace(
                                                        [
                                                            fac.AntdFormItem(
                                                                fac.AntdInput(
                                                                    id='member-member_name-input',
                                                                    placeholder='请输入用户名称',
                                                                    autoComplete='off',
                                                                    allowClear=True,
                                                                    style={
                                                                        'width': 240
                                                                    },
                                                                ),
                                                                label='会员名称',
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdInput(
                                                                    id='member-phone_number-input',
                                                                    placeholder='请输入手机号码',
                                                                    autoComplete='off',
                                                                    allowClear=True,
                                                                    style={
                                                                        'width': 240
                                                                    },
                                                                ),
                                                                label='手机号码',
                                                            ),
                                                            fac.AntdFormItem(
                                                                ApiSelect(
                                                                    dict_type='sys_normal_disable',
                                                                    id='member-status-select',
                                                                    placeholder='会员状态',
                                                                    style={
                                                                        'width': 240
                                                                    },
                                                                ),
                                                                label='会员状态',
                                                            ),
                                                        ],
                                                        style={
                                                            'paddingBottom': '10px'
                                                        },
                                                    ),
                                                    fac.AntdSpace(
                                                        [
                                                            fac.AntdFormItem(
                                                                fac.AntdDateRangePicker(
                                                                    id='member-create_time-range',
                                                                    style={
                                                                        'width': 240
                                                                    },
                                                                ),
                                                                label='创建时间',
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdButton(
                                                                    '搜索',
                                                                    id='member-search',
                                                                    type='primary',
                                                                    icon=fac.AntdIcon(
                                                                        icon='antd-search'
                                                                    ),
                                                                )
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdButton(
                                                                    '重置',
                                                                    id='member-reset',
                                                                    icon=fac.AntdIcon(
                                                                        icon='antd-sync'
                                                                    ),
                                                                )
                                                            ),
                                                        ],
                                                        style={
                                                            'paddingBottom': '10px'
                                                        },
                                                    ),
                                                ],
                                                layout='inline',
                                            )
                                        ],
                                        id='member-search-form-container',
                                        hidden=False,
                                    ),
                                )
                            ]
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdSpace(
                                        [
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-plus'
                                                    ),
                                                    '新增',
                                                ],
                                                id={
                                                    'type': 'member-operation-button',
                                                    'index': 'add',
                                                },
                                                style={
                                                    'color': '#1890ff',
                                                    'background': '#e8f4ff',
                                                    'border-color': '#a3d3ff',
                                                },
                                            )
                                            if PermissionManager.check_perms(
                                                'member:add'
                                            )
                                            else [],
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-edit'
                                                    ),
                                                    '修改',
                                                ],
                                                id={
                                                    'type': 'member-operation-button',
                                                    'index': 'edit',
                                                },
                                                disabled=True,
                                                style={
                                                    'color': '#71e2a3',
                                                    'background': '#e7faf0',
                                                    'border-color': '#d0f5e0',
                                                },
                                            )
                                            if PermissionManager.check_perms(
                                                'member:edit'
                                            )
                                            else [],
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-minus'
                                                    ),
                                                    '删除',
                                                ],
                                                id={
                                                    'type': 'member-operation-button',
                                                    'index': 'delete',
                                                },
                                                disabled=True,
                                                style={
                                                    'color': '#ff9292',
                                                    'background': '#ffeded',
                                                    'border-color': '#ffdbdb',
                                                },
                                            )
                                            if PermissionManager.check_perms(
                                                'member:remove'
                                            )
                                            else [],
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-arrow-up'
                                                    ),
                                                    '导入',
                                                ],
                                                id='member-import',
                                                style={
                                                    'color': '#909399',
                                                    'background': '#f4f4f5',
                                                    'border-color': '#d3d4d6',
                                                },
                                            )
                                            if PermissionManager.check_perms(
                                                'member:import'
                                            )
                                            else [],
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-arrow-down'
                                                    ),
                                                    '导出',
                                                ],
                                                id='member-export',
                                                style={
                                                    'color': '#ffba00',
                                                    'background': '#fff8e6',
                                                    'border-color': '#ffe399',
                                                },
                                            )
                                            if PermissionManager.check_perms(
                                                'member:export'
                                            )
                                            else [],
                                        ],
                                        style={'paddingBottom': '10px'},
                                    ),
                                    span=16,
                                ),
                                fac.AntdCol(
                                    fac.AntdSpace(
                                        [
                                            html.Div(
                                                fac.AntdTooltip(
                                                    fac.AntdButton(
                                                        [
                                                            fac.AntdIcon(
                                                                icon='antd-search'
                                                            ),
                                                        ],
                                                        id='member-hidden',
                                                        shape='circle',
                                                    ),
                                                    id='member-hidden-tooltip',
                                                    title='隐藏搜索',
                                                )
                                            ),
                                            html.Div(
                                                fac.AntdTooltip(
                                                    fac.AntdButton(
                                                        [
                                                            fac.AntdIcon(
                                                                icon='antd-sync'
                                                            ),
                                                        ],
                                                        id='member-refresh',
                                                        shape='circle',
                                                    ),
                                                    title='刷新',
                                                )
                                            ),
                                        ],
                                        style={
                                            'float': 'right',
                                            'paddingBottom': '10px',
                                        },
                                    ),
                                    span=8,
                                    style={'paddingRight': '10px'},
                                ),
                            ],
                            gutter=5,
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdSpin(
                                        fac.AntdTable(
                                            id='member-list-table',
                                            data=table_data,
                                            columns=[
                                                {
                                                    'dataIndex': 'member_id',
                                                    'title': '会员编号',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'member_name',
                                                    'title': '会员名称',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'nick_name',
                                                    'title': '会员昵称',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },  
                                                {
                                                    'dataIndex': 'gender',
                                                    'title': '会员性别',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },                                              
                                                {
                                                    'dataIndex': 'phonenumber',
                                                    'title': '手机号码',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'email',
                                                    'title': '电子邮箱',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'login_date',
                                                    'title': '最后登陆时间',
                                                    'width': 120,
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'status',
                                                    'title': '状态',
                                                    'width': 100,
                                                    'renderOptions': {
                                                        'renderType': 'switch'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'create_at',
                                                    'title': '创建时间',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'title': '操作',
                                                    'dataIndex': 'operation',
                                                    'width': 120,
                                                    'renderOptions': {
                                                        'renderType': 'dropdown',
                                                        'dropdownProps': {
                                                            'title': '更多'
                                                        },
                                                    },
                                                },
                                            ],
                                            rowSelectionType='checkbox',
                                            rowSelectionWidth=50,
                                            bordered=True,
                                            pagination=table_pagination,
                                            mode='server-side',
                                            style={
                                                'width': '100%',
                                                'paddingRight': '10px',
                                            },
                                        ),
                                        text='数据加载中',
                                    ),
                                )
                            ]
                        ),
                    ],
                    span=24,
                ),
            ],
            gutter=5,
        ),
        # 新增和编辑用户表单modal
        fac.AntdModal(
            [
                fac.AntdForm(
                    [
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            name='member_name',
                                            placeholder='请输入会员名称',
                                            allowClear=True,
                                            style={'width': '100%'},
                                        ),
                                        label='会员名称',
                                        required=True,
                                        id={
                                            'type': 'member-form-label',
                                            'index': 'member_name',
                                            'required': True,
                                        },
                                    ),
                                    span=12,
                                ),                                
                            ],
                            gutter=10,
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            name='nick_name',
                                            placeholder='请输入会员昵称',
                                            allowClear=True,
                                            style={'width': '100%'},
                                        ),
                                        label='会员昵称',
                                        required=True,
                                        id={
                                            'type': 'member-form-label',
                                            'index': 'nick_name',
                                            'required': True,
                                        },
                                    ),
                                    span=12,
                                ),                                
                            ],
                            gutter=10,
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            name='phonenumber',
                                            placeholder='请输入手机号码',
                                            allowClear=True,
                                            style={'width': '100%'},
                                        ),
                                        label='手机号码',
                                        id={
                                            'type': 'member-form-label',
                                            'index': 'phonenumber',
                                            'required': False,
                                        },
                                    ),
                                    span=12,
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            name='email',
                                            placeholder='请输入邮箱',
                                            allowClear=True,
                                            style={'width': '100%'},
                                        ),
                                        label='邮箱',
                                        id={
                                            'type': 'member-form-label',
                                            'index': 'email',
                                            'required': False,
                                        },
                                    ),
                                    span=12,
                                ),
                            ],
                            gutter=10,
                        ),
                        html.Div(
                            fac.AntdRow(
                                [
                                    fac.AntdCol(
                                        fac.AntdFormItem(
                                            fac.AntdInput(
                                                id='member-form-member_name',
                                                name='member_name',
                                                placeholder='请输入会员名称',
                                                allowClear=True,
                                                style={'width': '100%'},
                                            ),
                                            label='会员名称',
                                            required=True,
                                            id={
                                                'type': 'member-form-label',
                                                'index': 'member_name',
                                                'required': True,
                                            },
                                        ),
                                        span=12,
                                    ),
                                    fac.AntdCol(
                                        fac.AntdFormItem(
                                            fac.AntdInput(
                                                id='member-form-password',
                                                name='password',
                                                placeholder='请输入密码',
                                                mode='password',
                                                passwordUseMd5=True,
                                                style={'width': '100%'},
                                            ),
                                            label='会员密码',
                                            required=True,
                                            id={
                                                'type': 'member-form-label',
                                                'index': 'password',
                                                'required': True,
                                            },
                                        ),
                                        span=12,
                                    ),
                                ],
                                gutter=10,
                            ),
                            id='member-member_name-password-container',
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        ApiSelect(
                                            dict_type='member_gender',
                                            name='gender',
                                            placeholder='请选择性别',
                                            style={'width': '100%'},
                                        ),
                                        label='会员性别',
                                        id={
                                            'type': 'member-form-label',
                                            'index': 'gender',
                                            'required': False,
                                        },
                                    ),
                                    span=12,
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        ApiRadioGroup(
                                            dict_type='sys_normal_disable',
                                            name='status',
                                            defaultValue='0',
                                            style={'width': '100%'},
                                        ),
                                        label='会员状态',
                                        id={
                                            'type': 'member-form-label',
                                            'index': 'status',
                                            'required': False,
                                        },
                                    ),
                                    span=12,
                                ),
                            ],
                            gutter=10,
                        ),                        
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            name='remark',
                                            placeholder='请输入内容',
                                            allowClear=True,
                                            mode='text-area',
                                            style={'width': '100%'},
                                        ),
                                        label='备注',
                                        id={
                                            'type': 'member-form-label',
                                            'index': 'remark',
                                            'required': False,
                                        },
                                        labelCol={'span': 4},
                                        wrapperCol={'span': 20},
                                    ),
                                    span=24,
                                ),
                            ],
                            gutter=10,
                        ),
                    ],
                    id='member-form',
                    enableBatchControl=True,
                    labelCol={'span': 8},
                    wrapperCol={'span': 16},
                    style={'marginRight': '15px'},
                )
            ],
            id='member-modal',
            mask=False,
            width=650,
            renderFooter=True,
            okClickClose=False,
        ),
        # 删除用户二次确认modal
        fac.AntdModal(
            fac.AntdText('是否确认删除？', id='member-delete-text'),
            id='member-delete-confirm-modal',
            visible=False,
            title='提示',
            renderFooter=True,
            centered=True,
        ),
        # 用户导入modal
        fac.AntdModal(
            [
                html.Div(
                    [
                        ManuallyUpload(
                            id='member-upload-choose', accept='.xls,.xlsx'
                        ),
                    ],
                    style={'marginTop': '10px'},
                ),
                html.Div(
                    [
                        fac.AntdCheckbox(
                            id='member-import-update-check', checked=False
                        ),
                        fac.AntdText(
                            '是否更新已经存在的会员数据',
                            style={'marginLeft': '5px'},
                        ),
                    ],
                    style={'textAlign': 'center', 'marginTop': '10px'},
                ),
                html.Div(
                    [
                        fac.AntdText('仅允许导入xls、xlsx格式文件。'),
                        fac.AntdButton(
                            '下载模板',
                            id='download-member-import-template',
                            type='link',
                        ),
                    ],
                    style={'textAlign': 'center', 'marginTop': '10px'},
                ),
            ],
            id='member-import-confirm-modal',
            visible=False,
            title='会员导入',
            width=600,
            renderFooter=True,
            centered=True,
            okText='导入',
            okClickClose=False,
        ),
        fac.AntdModal(
            fac.AntdText(
                id='member-batch-result-content',
                className={'whiteSpace': 'break-spaces'},
            ),
            id='member-batch-result-modal',
            visible=False,
            title='会员导入结果',
            renderFooter=False,
            centered=True,
        ),
        # 重置密码modal
        fac.AntdModal(
            [
                fac.AntdForm(
                    [
                        fac.AntdFormItem(
                            fac.AntdInput(
                                id='member-reset-password-input', mode='password'
                            ),
                            label='请输入新密码',
                        ),
                    ],
                    layout='vertical',
                ),
                dcc.Store(id='member-reset-password-row-key-store'),
            ],
            id='member-reset-password-confirm-modal',
            visible=False,
            title='重置密码',
            renderFooter=True,
            centered=True,
            okClickClose=False,
        ),        
    ]
