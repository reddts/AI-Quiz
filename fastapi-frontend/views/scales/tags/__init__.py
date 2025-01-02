import feffery_antd_components as fac
from dash import dcc, html
from callbacks.scales_c import tags_c
from components.ApiRadioGroup import ApiRadioGroup
from components.ApiSelect import ApiSelect
from utils.permission_util import PermissionManager


def render(*args, **kwargs):
    query_params = dict(page_num=1, page_size=10)
    table_data, table_pagination = tags_c.generate_tags_table(query_params)

    return [
        # 用于导出成功后重置dcc.Download的状态，防止多次下载文件
        dcc.Store(id='tags-export-complete-judge-container'),
        # 绑定的导出组件
        dcc.Download(id='tags-export-container'),
        # 标签管理模块操作类型存储容器
        dcc.Store(id='tags-operations-store'),
        # 标签管理模块弹窗类型存储容器
        dcc.Store(id='tags-modal_type-store'),
        # 标签管理模块表单数据存储容器
        dcc.Store(id='tags-form-store'),
        # 标签管理模块删除操作行key存储容器
        dcc.Store(id='tags-delete-ids-store'),
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
                                                                    id='tags-tags_code-input',
                                                                    placeholder='请输入标签编码',
                                                                    autoComplete='off',
                                                                    allowClear=True,
                                                                    style={
                                                                        'width': 210
                                                                    },
                                                                ),
                                                                label='标签编码',
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdInput(
                                                                    id='tags-tags_name-input',
                                                                    placeholder='请输入标签名称',
                                                                    autoComplete='off',
                                                                    allowClear=True,
                                                                    style={
                                                                        'width': 210
                                                                    },
                                                                ),
                                                                label='标签名称',
                                                            ),
                                                            fac.AntdFormItem(
                                                                ApiSelect(
                                                                    dict_type='sys_normal_disable',
                                                                    id='tags-status-select',
                                                                    placeholder='标签状态',
                                                                    style={
                                                                        'width': 200
                                                                    },
                                                                ),
                                                                label='标签状态',
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdButton(
                                                                    '搜索',
                                                                    id='tags-search',
                                                                    type='primary',
                                                                    icon=fac.AntdIcon(
                                                                        icon='antd-search'
                                                                    ),
                                                                )
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdButton(
                                                                    '重置',
                                                                    id='tags-reset',
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
                                        id='tags-search-form-container',
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
                                                    'type': 'tags-operation-button',
                                                    'index': 'add',
                                                },
                                                style={
                                                    'color': '#1890ff',
                                                    'background': '#e8f4ff',
                                                    'borderColor': '#a3d3ff',
                                                },
                                            )
                                            if PermissionManager.check_perms(
                                                'scales:tags:add'
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
                                                    'type': 'tags-operation-button',
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
                                                'scales:tags:edit'
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
                                                    'type': 'tags-operation-button',
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
                                                'scales:tags:remove'
                                            )
                                            else [],
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-arrow-down'
                                                    ),
                                                    '导出',
                                                ],
                                                id='tags-export',
                                                style={
                                                    'color': '#ffba00',
                                                    'background': '#fff8e6',
                                                    'borderColor': '#ffe399',
                                                },
                                            )
                                            if PermissionManager.check_perms(
                                                'scales:tags:export'
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
                                                        id='tags-hidden',
                                                        shape='circle',
                                                    ),
                                                    id='tags-hidden-tooltip',
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
                                                        id='tags-refresh',
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
                                            id='tags-list-table',
                                            data=table_data,
                                            columns=[
                                                {
                                                    'dataIndex': 'tags_id',
                                                    'title': '标签编号',
                                                    'width': '8%',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'tags_code',
                                                    'title': '标签编码',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'tags_name',
                                                    'title': '标签名称',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'position',
                                                    'title': '展示位置',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'tags_sort',
                                                    'title': '标签排序',
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
        # 新增和编辑标签表单modal
        fac.AntdModal(
            [
                fac.AntdForm(
                    [
                        html.Div(
                            id='tags-avatar-container',
                            style={
                                'textAlign': 'center',
                                'marginBottom': '10px',
                            },
                        ),
                        #html.Div(
                        #    '如需图标请点击进入后单独修改',
                        #    style={
                        #    'textAlign': 'center',
                        #    'color': 'blue',
                        #    'marginTop': '10px',
                        #    },
                        #),
                        html.Br(),
                        fac.AntdFormItem(
                            fac.AntdInput(
                                name='tags_name',
                                placeholder='请输入标签名称',
                                allowClear=True,
                                style={'width': 350},
                            ),
                            label='标签名称',
                            required=True,
                            id={
                                'type': 'tags-form-label',
                                'index': 'tags_name',
                                'required': True,
                            },
                            hasFeedback=True,
                        ),
                        fac.AntdFormItem(
                            fac.AntdInput(
                                name='tags_code',
                                placeholder='请输入标签编码',
                                allowClear=True,
                                style={'width': 350},
                            ),
                            label='标签编码',
                            required=True,
                            id={
                                'type': 'tags-form-label',
                                'index': 'tags_code',
                                'required': True,
                            },
                            hasFeedback=True,
                        ),
                        fac.AntdFormItem(
                            fac.AntdInputNumber(
                                name='tags_sort',
                                defaultValue=0,
                                min=0,
                                style={'width': 350},
                            ),
                            label='标签顺序',
                            required=True,
                            id={
                                'type': 'tags-form-label',
                                'index': 'tags_sort',
                                'required': True,
                            },
                            hasFeedback=True,
                        ),
                        fac.AntdFormItem(
                            ApiSelect(
                                dict_type='sys_position',
                                name='position',
                                placeholder='请选择展示位置',
                                style={'width': 350},
                            ),
                            label='展示位置',
                            id={
                                'type': 'tags-form-label',
                                'index': 'position',
                                'required': False,
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
                            label='标签状态',
                            id={
                                'type': 'tags-form-label',
                                'index': 'status',
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
                                'type': 'tags-form-label',
                                'index': 'remark',
                                'required': False,
                            },
                            hasFeedback=True,
                        ),
                    ],
                    id='tags-form',
                    enableBatchControl=True,
                    labelCol={'span': 6},
                    wrapperCol={'span': 18},
                )
            ],
            id='tags-modal',
            mask=False,
            width=580,
            renderFooter=True,
            okClickClose=False,
        ),
        # 删除标签二次确认modal
        fac.AntdModal(
            fac.AntdText('是否确认删除？', id='tags-delete-text'),
            id='tags-delete-confirm-modal',
            visible=False,
            title='提示',
            renderFooter=True,
            centered=True,
        ),
    ]
