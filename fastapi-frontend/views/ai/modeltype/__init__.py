import feffery_antd_components as fac
from dash import dcc, html
from callbacks.ai_c import modeltype_c
from components.ApiRadioGroup import ApiRadioGroup
from components.ApiSelect import ApiSelect
from utils.permission_util import PermissionManager


def render(*args, **kwargs):
    query_params = dict(page_num=1, page_size=10)
    table_data, table_pagination = modeltype_c.generate_modeltype_table(query_params)

    return [
        # 用于导出成功后重置dcc.Download的状态，防止多次下载文件
        dcc.Store(id='modeltype-export-complete-judge-container'),
        # 绑定的导出组件
        dcc.Download(id='modeltype-export-container'),
        # 标签管理模块操作类型存储容器
        dcc.Store(id='modeltype-operations-store'),
        # 标签管理模块弹窗类型存储容器
        dcc.Store(id='modeltype-modal_type-store'),
        # 标签管理模块表单数据存储容器
        dcc.Store(id='modeltype-form-store'),
        # 标签管理模块删除操作行key存储容器
        dcc.Store(id='modeltype-delete-ids-store'),
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
                                                                    id='modeltype-type_name-input',
                                                                    placeholder='请输入模型分类名称',
                                                                    autoComplete='off',
                                                                    allowClear=True,
                                                                    style={
                                                                        'width': 210
                                                                    },
                                                                ),
                                                                label='模型分类名称',
                                                            ),
                                                            fac.AntdFormItem(
                                                                ApiSelect(
                                                                    dict_type='sys_normal_disable',
                                                                    id='modeltype-status-select',
                                                                    placeholder='分类状态',
                                                                    style={
                                                                        'width': 200
                                                                    },
                                                                ),
                                                                label='分类状态',
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdButton(
                                                                    '搜索',
                                                                    id='modeltype-search',
                                                                    type='primary',
                                                                    icon=fac.AntdIcon(
                                                                        icon='antd-search'
                                                                    ),
                                                                )
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdButton(
                                                                    '重置',
                                                                    id='modeltype-reset',
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
                                        id='modeltype-search-form-container',
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
                                                    'type': 'modeltype-operation-button',
                                                    'index': 'add',
                                                },
                                                style={
                                                    'color': '#1890ff',
                                                    'background': '#e8f4ff',
                                                    'borderColor': '#a3d3ff',
                                                },
                                            )
                                            if PermissionManager.check_perms(
                                                'ai:modeltype:add'
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
                                                    'type': 'modeltype-operation-button',
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
                                                'ai:modeltype:edit'
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
                                                    'type': 'modeltype-operation-button',
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
                                                'ai:modeltype:remove'
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
                                                        id='modeltype-hidden',
                                                        shape='circle',
                                                    ),
                                                    id='modeltype-hidden-tooltip',
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
                                                        id='modeltype-refresh',
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
                                            id='modeltype-list-table',
                                            data=table_data,
                                            columns=[
                                                {
                                                    'dataIndex': 'type_id',
                                                    'title': '模型分类编号',
                                                    'width': '8%',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },                                                
                                                {
                                                    'dataIndex': 'type_name',
                                                    'title': '模型分类名称',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'api_url',
                                                    'title': 'API接口',
                                                    'width': '25%',
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
        # 新增和编辑模型分类表单modal
        fac.AntdModal(
            [
                fac.AntdForm(
                    [                        
                        fac.AntdFormItem(
                            fac.AntdInput(
                                name='type_name',
                                placeholder='请输入模型分类名称',
                                allowClear=True,
                                style={'width': 350},
                            ),
                            label='模型分类名称',
                            required=True,
                            id={
                                'type': 'modeltype-form-label',
                                'index': 'type_name',
                                'required': True,
                            },
                            hasFeedback=True,
                        ),
                        fac.AntdFormItem(
                            fac.AntdInput(
                                name='api_url',
                                placeholder='请输入模型分类API接口',
                                allowClear=True,
                                style={'width': 350},
                            ),
                            label='API接口',
                            required=True,
                            id={
                                'type': 'modeltype-form-label',
                                'index': 'api_url',
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
                            label='模型分类状态',
                            id={
                                'type': 'modeltype-form-label',
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
                                'type': 'modeltype-form-label',
                                'index': 'remark',
                                'required': False,
                            },
                            hasFeedback=True,
                        ),
                    ],
                    id='modeltype-form',
                    enableBatchControl=True,
                    labelCol={'span': 6},
                    wrapperCol={'span': 18},
                )
            ],
            id='modeltype-modal',
            mask=False,
            width=580,
            renderFooter=True,
            okClickClose=False,
        ),
        # 删除标签二次确认modal
        fac.AntdModal(
            fac.AntdText('是否确认删除？', id='modeltype-delete-text'),
            id='modeltype-delete-confirm-modal',
            visible=False,
            title='提示',
            renderFooter=True,
            centered=True,
        ),
    ]
