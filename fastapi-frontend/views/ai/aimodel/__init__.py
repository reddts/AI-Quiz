import feffery_antd_components as fac
from dash import dcc, html
from callbacks.ai_c import aimodel_c
from components.ApiRadioGroup import ApiRadioGroup
from components.ApiSelect import ApiSelect
from utils.permission_util import PermissionManager


def render(*args, **kwargs):
    query_params = dict(page_num=1, page_size=10)
    table_data, table_pagination = aimodel_c.generate_aimodel_table(query_params)

    return [
        # 用于导出成功后重置dcc.Download的状态，防止多次下载文件
        dcc.Store(id='aimodel-export-complete-judge-container'),
        # 绑定的导出组件
        dcc.Download(id='aimodel-export-container'),
        # 标签管理模块操作类型存储容器
        dcc.Store(id='aimodel-operations-store'),
        # 标签管理模块弹窗类型存储容器
        dcc.Store(id='aimodel-modal_type-store'),
        # 标签管理模块表单数据存储容器
        dcc.Store(id='aimodel-form-store'),
        # 标签管理模块删除操作行key存储容器
        dcc.Store(id='aimodel-delete-ids-store'),
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
                                                                    id='aimodel-aimodel_alias-input',
                                                                    placeholder='请输入模型显示名',
                                                                    autoComplete='off',
                                                                    allowClear=True,
                                                                    style={
                                                                        'width': 210
                                                                    },
                                                                ),
                                                                label='模型显示名',
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdInput(
                                                                    id='aimodel-aimodel_name-input',
                                                                    placeholder='请输入模型调用名',
                                                                    autoComplete='off',
                                                                    allowClear=True,
                                                                    style={
                                                                        'width': 210
                                                                    },
                                                                ),
                                                                label='模型调用名',
                                                            ),
                                                            fac.AntdFormItem(
                                                                ApiSelect(
                                                                    dict_type='sys_normal_disable',
                                                                    id='aimodel-status-select',
                                                                    placeholder='模型状态',
                                                                    style={
                                                                        'width': 200
                                                                    },
                                                                ),
                                                                label='模型状态',
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdButton(
                                                                    '搜索',
                                                                    id='aimodel-search',
                                                                    type='primary',
                                                                    icon=fac.AntdIcon(
                                                                        icon='antd-search'
                                                                    ),
                                                                )
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdButton(
                                                                    '重置',
                                                                    id='aimodel-reset',
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
                                        id='aimodel-search-form-container',
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
                                                    'type': 'aimodel-operation-button',
                                                    'index': 'add',
                                                },
                                                style={
                                                    'color': '#1890ff',
                                                    'background': '#e8f4ff',
                                                    'borderColor': '#a3d3ff',
                                                },
                                            )
                                            if PermissionManager.check_perms(
                                                'ai:aimodel:add'
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
                                                    'type': 'aimodel-operation-button',
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
                                                'ai:aimodel:edit'
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
                                                    'type': 'aimodel-operation-button',
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
                                                'ai:aimodel:remove'
                                            )
                                            else [],
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-arrow-down'
                                                    ),
                                                    '导出',
                                                ],
                                                id='aimodel-export',
                                                style={
                                                    'color': '#ffba00',
                                                    'background': '#fff8e6',
                                                    'borderColor': '#ffe399',
                                                },
                                            )
                                            if PermissionManager.check_perms(
                                                'ai:aimodel:export'
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
                                                        id='aimodel-hidden',
                                                        shape='circle',
                                                    ),
                                                    id='aimodel-hidden-tooltip',
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
                                                        id='aimodel-refresh',
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
                                            id='aimodel-list-table',
                                            data=table_data,
                                            columns=[
                                                {
                                                    'dataIndex': 'aimodel_id',
                                                    'title': '模型编号',
                                                    'width': '8%',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'aimodel_name',
                                                    'title': '调用名称',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'aimodel_alias',
                                                    'title': '显示名称',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'nowused',
                                                    'title': '当前模型',
                                                    'renderOptions': {
                                                        'renderType': 'tags'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'context_num',
                                                    'title': '上下文对话数',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'maxtoken',
                                                    'title': '最大输入token',
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
                                                    'width': 160,
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
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    [                 
                                        fac.AntdFormItem(
                                            fac.AntdInput(
                                                name='aimodel_name',
                                                placeholder='请输入模型调用名称',
                                                allowClear=True,
                                                style={'width': 350},
                                            ),
                                            label='模型调用名称',
                                            required=True,
                                            id={
                                                'type': 'aimodel-form-label',
                                                'index': 'aimodel_name',
                                                'required': True,
                                            },
                                            hasFeedback=True,
                                        ),
                                        fac.AntdFormItem(
                                            fac.AntdInput(
                                                name='aimodel_alias',
                                                placeholder='请输入模型显示名称',
                                                allowClear=True,
                                                style={'width': 350},
                                            ),
                                            label='模型显示名称',
                                            required=True,
                                            id={
                                                'type': 'aimodel-form-label',
                                                'index': 'aimodel_alias',
                                                'required': True,
                                            },
                                            hasFeedback=True,
                                        ),
                                    ],
                                    span=24,
                                ),
                            ],
                            gutter=5,
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    [                
                                        fac.AntdFormItem(
                                            ApiRadioGroup(
                                                dict_type='sys_yes_no',
                                                name='nowused',
                                                defaultValue='0',
                                                style={'width': 350},
                                            ),
                                            label='当前模型',
                                            id={
                                                'type': 'aimodel-form-label',
                                                'index': 'nowused',
                                                'required': True,
                                            },
                                            hasFeedback=True,
                                        ),
                                    ],
                                    span=24,
                                ),
                            ],
                            gutter=5,
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    [
                                        fac.AntdFormItem(
                                            ApiRadioGroup(
                                                dict_type='sys_normal_disable',
                                                name='status',
                                                defaultValue='0',
                                                style={'width': 350},
                                            ),
                                            label='模型状态',
                                            id={
                                                'type': 'aimodel-form-label',
                                                'index': 'status',
                                                'required': False,
                                            },
                                            hasFeedback=True,
                                        ),
                                    ],
                                    span=24,
                                ),
                            ],
                            gutter=5,
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    [
                                        fac.AntdFormItem(
                                            fac.AntdSelect(
                                                id='model-type-select',
                                                name='type_id',
                                                placeholder='请选择模型分类',
                                                allowClear=True,
                                                style={'width': 350},
                                                optionFilterProp='label',
                                                options=[],
                                            ),
                                            label='模型分类',
                                            id={
                                                'type': 'aimodel-form-label',
                                                'index': 'type_id',
                                                'required': True,
                                            },
                                        ),
                                    ],
                                    span=24,
                                ),
                            ],
                            gutter=5,
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    [
                                        fac.AntdFormItem(
                                            fac.AntdInput(
                                                name='context_num',
                                                placeholder='请输入上下文对话数',
                                                allowClear=True,
                                                style={'width': '90%'},
                                            ),
                                            label='上下文对话数',
                                            id={
                                                'type': 'aimodel-form-label',
                                                'index': 'context_num',
                                                'required': True,
                                            },
                                            hasFeedback=True,
                                        ),
                                    ],
                                    span=12,
                                ),
                                 fac.AntdCol(
                                    [
                                        fac.AntdFormItem(
                                            fac.AntdInput(
                                                name='maxtoken',
                                                placeholder='请输入最大输入token',
                                                allowClear=True,
                                                style={'width': '90%'},
                                            ),
                                            label='最大输入token',
                                            id={
                                                'type': 'aimodel-form-label',
                                                'index': 'maxtoken',
                                                'required': True,
                                            },
                                            hasFeedback=True,
                                        ),
                                    ],
                                    span=12,
                                ),
                            ],
                            gutter=5,
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    [
                                        fac.AntdFormItem(
                                            fac.AntdSlider(
                                                id='temperature',
                                                min=0,              # 设置最小值
                                                max=2,            # 设置最大值
                                                step=0.01,             # 设置步长
                                                defaultValue=1,    # 设置默认值
                                            ),
                                            label='随机性',
                                            id={
                                                'type': 'aimodel-form-label',
                                                'index': 'temperature',
                                                'required': True,
                                            },
                                            hasFeedback=True,
                                        ),
                                    ],
                                    span=12,
                                ),
                                fac.AntdCol(
                                    [
                                        fac.AntdFormItem(
                                            fac.AntdSlider(
                                                id='top_p',
                                                min=0,              # 设置最小值
                                                max=1,            # 设置最大值
                                                step=0.01,             # 设置步长
                                                defaultValue=1,    # 设置默认值
                                            ),
                                            label='TopP',
                                            id={
                                                'type': 'aimodel-form-label',
                                                'index': 'top_p',
                                                'required': True,
                                            },
                                            hasFeedback=True,
                                        ),
                                    ],
                                    span=12,
                                ),                                
                            ], 
                            gutter=5,
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    [
                                        fac.AntdFormItem(
                                            fac.AntdSlider(
                                                id='frequency',
                                                min=0,              # 设置最小值
                                                max=2,            # 设置最大值
                                                step=0.01,             # 设置步长
                                                defaultValue=0,    # 设置默认值
                                            ),
                                            label='重复性',
                                            id={
                                                'type': 'aimodel-form-label',
                                                'index': 'frequency',
                                                'required': True,
                                            },
                                            hasFeedback=True,
                                        ),
                                    ],
                                    span=12,
                                ),
                                fac.AntdCol(
                                    [
                                        fac.AntdFormItem(
                                            fac.AntdSlider(
                                                id='presence',
                                                min=0,              # 设置最小值
                                                max=2,            # 设置最大值
                                                step=0.01,             # 设置步长
                                                defaultValue=0,    # 设置默认值
                                            ),
                                            label='创新性',
                                            id={
                                                'type': 'aimodel-form-label',
                                                'index': 'presence',
                                                'required': True,
                                            },
                                            hasFeedback=True,
                                        ),
                                    ],
                                    span=12,
                                ),
                            ],
                            gutter=5,
                        ),                        
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    [
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
                                                'type': 'aimodel-form-label',
                                                'index': 'remark',
                                                'required': False,
                                            },
                                            hasFeedback=True,
                                        ),
                                    ],
                                    span=24,
                                ),
                            ],
                            gutter=5,
                        ),
                    ],                                       
                    id='aimodel-form',
                    enableBatchControl=True,
                    labelCol={'span': 8},
                    wrapperCol={'span': 16},
                    #style={'marginRight': '15px'},
                )
            ],
            id='aimodel-modal',
            mask=False,
            width=680,
            renderFooter=True,
            okClickClose=False,
        ),
        # 删除标签二次确认modal
        fac.AntdModal(
            fac.AntdText('是否确认删除？', id='aimodel-delete-text'),
            id='aimodel-delete-confirm-modal',
            visible=False,
            title='提示',
            renderFooter=True,
            centered=True,
        ),
    ]
