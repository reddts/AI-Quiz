from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from api.member import MemberApi
from server import app
from utils.feedback_util import MessageManager


@app.callback(
    [
        Output('reset-member-nick_name-form-item', 'validateStatus'),
        Output('reset-member-phonenumber-form-item', 'validateStatus'),
        Output('reset-member-email-form-item', 'validateStatus'),
        Output('reset-member-nick_name-form-item', 'help'),
        Output('reset-member-phonenumber-form-item', 'help'),
        Output('reset-member-email-form-item', 'help'),
    ],
    Input('reset-submit', 'nClicks'),
    [
        State('reset-member-nick_name', 'value'),
        State('reset-member-phonenumber', 'value'),
        State('reset-member-email', 'value'),
        State('reset-member-sex', 'value'),
    ],
    running=[[Output('reset-submit', 'loading'), True, False]],
    prevent_initial_call=True,
)
def reset_submit_member_info(reset_click, nick_name, phonenumber, email, sex):
    """
    修改当前会员信息回调
    """
    if reset_click:
        if all([nick_name, phonenumber, email]):
            params = dict(
                nick_name=nick_name,
                phonenumber=phonenumber,
                email=email,
                sex=sex,
            )
            MemberApi.update_member_profile(params)
            MessageManager.success(content='修改成功')

            return [None] * 6

        return [
            None if nick_name else 'error',
            None if phonenumber else 'error',
            None if email else 'error',
            None if nick_name else '请输入会员昵称！',
            None if phonenumber else '请输入手机号码！',
            None if email else '请输入邮箱！',
        ]

    raise PreventUpdate


@app.callback(
    [
        Output('tabs-container', 'latestDeletePane', allow_duplicate=True),
        Output('tabs-container', 'tabCloseCounts', allow_duplicate=True),
    ],
    Input('reset-close', 'nClicks'),
    State('tabs-container', 'tabCloseCounts'),
    prevent_initial_call=True,
)
def close_personal_info_modal(close_click, tab_close_counts):
    """
    关闭当前个人资料标签页回调
    """
    if close_click:
        return ['Profile/member/profile', tab_close_counts + 1 if tab_close_counts else 1]
    raise PreventUpdate
