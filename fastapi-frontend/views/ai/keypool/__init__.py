import feffery_antd_components as fac
from dash import dcc, html
from callbacks.ai_c import keypool_c
from components.ApiRadioGroup import ApiRadioGroup
from components.ApiSelect import ApiSelect
from utils.permission_util import PermissionManager


def render(*args, **kwargs):
    query_params = dict(page_num=1, page_size=10)
    table_data, table_pagination = keypool_c.generate_keypool_table(query_params)

    return [
        # 用于导出成功后重置dcc.Download的状态，防止多次下载文件
        dcc.Store(id='keypool-export-complete-judge-container'),
        # 绑定的导出组件
        dcc.Download(id='keypool-export-container'),
        # KEY管理模块操作类型存储容器
        dcc.Store(id='keypool-operations-store'),
        # KEY管理模块弹窗类型存储容器
        dcc.Store(id='keypool-modal_type-store'),
        # KEY管理模块表单数据存储容器
        dcc.Store(id='keypool-form-store'),
        # KEY管理模块删除操作行key存储容器
        dcc.Store(id='keypool-delete-ids-store'),
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
                                                                    id='keypool-key_name-input',
                                                                    placeholder='请输入KEY名称',
                                                                    autoComplete='off',
                                                                    allowClear=True,
                                                                    style={
                                                                        'width': 210
                                                                    },
                                                                ),
                                                                label='KEY名称',
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdSelect(
                                                                    id='keypool-key_typeid-select',
                                                                    placeholder='请选择分类',
                                                                    allowClear=True,
                                                                    style={
                                                                        'width': 210
                                                                    },
                                                                    optionFilterProp='label',
                                                                    options=[],
                                                                ),
                                                                label='KEY分类',
                                                            ),
                                                            fac.AntdFormItem(
                                                                ApiSelect(
                                                                    dict_type='sys_normal_disable',
                                                                    id='keypool-status-select',
                                                                    placeholder='KEY状态',
                                                                    style={
                                                                        'width': 200
                                                                    },
                                                                ),
                                                                label='KEY状态',
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdButton(
                                                                    '搜索',
                                                                    id='keypool-search',
                                                                    type='primary',
                                                                    icon=fac.AntdIcon(
                                                                        icon='antd-search'
                                                                    ),
                                                                )
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdButton(
                                                                    '重置',
                                                                    id='keypool-reset',
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
                                        id='keypool-search-form-container',
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
                                                    'type': 'keypool-operation-button',
                                                    'index': 'add',
                                                },
                                                style={
                                                    'color': '#1890ff',
                                                    'background': '#e8f4ff',
                                                    'borderColor': '#a3d3ff',
                                                },
                                            )
                                            if PermissionManager.check_perms(
                                                'scales:keypool:add'
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
                                                    'type': 'keypool-operation-button',
                                                    'index': 'edit',
                                                },
                                                disabled=True,
                                                style={
                                                    'color': '#71e2a3',
                                                    'background': '#e7faf0',
                                                    'borderColor': '#d0f5e0',
                                                },
                                            )
                                            if PermissionManager.check_perms(
                                                'scales:keypool:edit'
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
                                                    'type': 'keypool-operation-button',
                                                    'index': 'delete',
                                                },
                                                disabled=True,
                                                style={
                                                    'color': '#ff9292',
                                                    'background': '#ffeded',
                                                    'borderColor': '#ffdbdb',
                                                },
                                            )
                                            if PermissionManager.check_perms(
                                                'scales:keypool:remove'
                                            )
                                            else [],
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-arrow-down'
                                                    ),
                                                    '导出',
                                                ],
                                                id='keypool-export',
                                                style={
                                                    'color': '#ffba00',
                                                    'background': '#fff8e6',
                                                    'borderColor': '#ffe399',
                                                },
                                            )
                                            if PermissionManager.check_perms(
                                                'scales:keypool:export'
                                            )
                                            else [],
                                        ],
                                        style={
                                            'paddingBottom': '10px',
                                        },
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
                                                        id='keypool-hidden',
                                                        shape='circle',
                                                    ),
                                                    id='keypool-hidden-tooltip',
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
                                                        id='keypool-refresh',
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
                                            id='keypool-list-table',
                                            data=table_data,
                                            columns=[
                                                {
                                                    'dataIndex': 'key_id',
                                                    'title': 'KEY编号',
                                                    'width': '8%',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'key_type_label',
                                                    'title': 'KEY分类',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'key_name',
                                                    'title': 'KEY名称',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'key_token',
                                                    'title': 'TOKEN',
                                                    'width':'35%',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'status',
                                                    'title': '状态',
                                                    'renderOptions': {
                                                        'renderType': 'tags'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'create_time',
                                                    'title': '创建时间',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'update_time',
                                                    'title': '更新时间',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'title': '操作',
                                                    'dataIndex': 'operation',
                                                    'width': 170,
                                                    'renderOptions': {
                                                        'renderType': 'button'
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
                )
            ],
            gutter=5,
        ),
        # 新增和编辑KEY表单modal
        fac.AntdModal(
            [
                fac.AntdForm(
                    [
                        fac.AntdFormItem(
                            fac.AntdInput(
                                name='key_name',
                                placeholder='请输入KEY名称',
                                allowClear=True,
                                style={'width': 350},
                            ),
                            label='KEY名称',
                            required=True,
                            id={
                                'type': 'keypool-form-label',
                                'index': 'key_name',
                                'required': True,
                            },
                            hasFeedback=True,
                        ),
                        fac.AntdFormItem(
                            fac.AntdSelect(
                                id='keypool-type-select',
                                name='key_typeid',
                                placeholder='请选择KEY分类',
                                allowClear=True,
                                style={'width': 350},
                                optionFilterProp='label',
                                options=[],
                            ),
                            label='KEY分类',
                            id={
                                'type': 'aimodel-form-label',
                                'index': 'key_typeid',
                                'required': True,
                            },
                            required=True,
                            hasFeedback=True,
                        ),  
                        fac.AntdFormItem(
                            fac.AntdInput(
                                name='key_token',
                                placeholder='请输入TOKEN',
                                allowClear=True,
                                style={'width': 350},
                            ),
                            label='KEY-TOKEN',
                            required=True,
                            id={
                                'type': 'keypool-form-label',
                                'index': 'key_token',
                                'required': True,
                            },
                            hasFeedback=True,
                        ),                     
                        fac.AntdFormItem(
                            ApiRadioGroup(
                                dict_type='sys_normal_disable',
                                name='status',
                                defaultValue='0',
                                style={'width': 350},
                            ),
                            label='KEY状态',
                            id={
                                'type': 'keypool-form-label',
                                'index': 'status',
                                'required': False,
                            },
                            hasFeedback=True,
                        ),
                        fac.AntdFormItem(
                            fac.AntdInput(
                                name='disablereason',
                                placeholder='停用原因是系统自动识别的，不用修改',
                                allowClear=True,
                                mode='text-area',
                                style={'width': 350},
                                readOnly=True,
                            ),
                            label='停用原因',
                            id={
                                'type': 'keypool-form-label',
                                'index': 'disablereason',
                                'required': False,
                            },
                            hasFeedback=True,
                        ),
                        fac.AntdFormItem(
                            fac.AntdInput(
                                name='remark',
                                placeholder='请输入内容',
                                allowClear=True,
                                mode='text-area',
                                style={'width': 350},
                            ),
                            label='备注',
                            id={
                                'type': 'keypool-form-label',
                                'index': 'remark',
                                'required': False,
                            },
                            hasFeedback=True,
                        ),
                    ],
                    id='keypool-form',
                    enableBatchControl=True,
                    labelCol={'span': 6},
                    wrapperCol={'span': 18},
                )
            ],
            id='keypool-modal',
            mask=False,
            width=580,
            renderFooter=True,
            okClickClose=False,
        ),
        # 删除KEY二次确认modal
        fac.AntdModal(
            fac.AntdText('是否确认删除？', id='keypool-delete-text'),
            id='keypool-delete-confirm-modal',
            visible=False,
            title='提示',
            renderFooter=True,
            centered=True,
        ),
    ]
