import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import html, dcc
from callbacks.scales_c import avatar_c  # noqa: F401
from config.env import ApiConfig


def render(tags_id, avatar_path):
    return [
        html.Div(
            [
                fac.AntdImage(
                    id='tags-avatar-image-info',
                    src=f'{ApiConfig.BaseUrl}{avatar_path}'
                    if avatar_path
                    else '/assets/imgs/tags.png',
                    preview=False,
                    height='120px',
                    width='120px',
                    style={'borderRadius': '50%'},
                )
            ],
            id='tags-avatar-edit-click',
            className='tags-info-head',
        ),
        fuc.FefferyStyle(
            rawStyle="""
            .tags-info-head {
              position: relative;
              display: inline-block;
              height: 120px;
            }

            .tags-info-head:hover:after {
              content: '+';
              position: absolute;
              left: 0;
              right: 0;
              top: 0;
              bottom: 0;
              color: #eee;
              background: rgba(0, 0, 0, 0.5);
              font-size: 24px;
              font-style: normal;
              -webkit-font-smoothing: antialiased;
              -moz-osx-font-smoothing: grayscale;
              cursor: pointer;
              line-height: 110px;
              border-radius: 50%;
            }
            """
        ),
        fac.AntdModal(
            [
                fac.AntdRow(
                    [
                        fac.AntdCol(
                            [
                                html.Div(
                                    [
                                        fuc.FefferyImageCropper(
                                            id='tags-avatar-cropper',
                                            alt='avatar',
                                            aspectRatio=1,
                                            dragMode='move',
                                            cropBoxMovable=False,
                                            cropBoxResizable=False,
                                            wheelZoomRatio=0.01,
                                            preview='#tags-avatar-image-preview',
                                            style={
                                                'width': '100%',
                                                'height': '100%',
                                            },
                                        )
                                    ],
                                    id='tags-avatar-cropper-container',
                                    style={'height': '350px', 'width': '100%'},
                                ),
                            ],
                            span=12,
                        ),
                        fac.AntdCol(
                            [
                                html.Div(
                                    id='tags-avatar-image-preview',
                                    className='avatar-upload-preview',
                                ),
                                fuc.FefferyStyle(
                                    rawStyle="""
                                    .avatar-upload-preview {
                                        margin: 18% auto;
                                        width: 220px;
                                        height: 220px;
                                        border-radius: 50%;
                                        box-shadow: 0 0 4px #ccc;
                                        overflow: hidden;
                                    }
                                    """
                                ),
                            ],
                            span=12,
                        ),
                    ]
                ),
                html.Br(),
                fac.AntdRow(
                    [
                        fac.AntdCol(
                            dcc.Upload(
                                fac.AntdButton(
                                    '选择',
                                    icon=fac.AntdIcon(icon='antd-cloud-upload'),
                                ),
                                id='tags-avatar-upload-choose',
                                accept='.jpeg,.jpg,.png',
                                max_size=10 * 1024 * 1024,
                            ),
                            span=4,
                        ),
                        fac.AntdCol(
                            fac.AntdButton(
                                id='zoom-out',
                                icon=fac.AntdIcon(icon='antd-plus'),
                            ),
                            span=2,
                        ),
                        fac.AntdCol(
                            fac.AntdButton(
                                id='zoom-in',
                                icon=fac.AntdIcon(icon='antd-minus'),
                            ),
                            span=2,
                        ),
                        fac.AntdCol(
                            fac.AntdButton(
                                icon=fac.AntdIcon(
                                    id='rotate-left', icon='antd-undo'
                                )
                            ),
                            span=2,
                        ),
                        fac.AntdCol(
                            fac.AntdButton(
                                icon=fac.AntdIcon(
                                    id='rotate-right', icon='antd-redo'
                                )
                            ),
                            span=7,
                        ),
                        fac.AntdCol(
                            fac.AntdButton(
                                '提交',
                                id='tags-change-avatar-submit',
                                type='primary',
                            ),
                            span=7,
                        ),
                    ],
                    gutter=10,
                ),
                dcc.Input(
                    id='tags-id-hidden',
                    type='hidden',
                    value=tags_id,
                ),
            ],
            id='tags-avatar-cropper-modal',
            title='修改图标',
            width=850,
            mask=False,
        ),
    ]
