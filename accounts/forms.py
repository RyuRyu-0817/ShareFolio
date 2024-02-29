# カスタム認証フォーム
from allauth.account.forms import (
    SignupForm,
    LoginForm,
    ResetPasswordForm,
    ResetPasswordKeyForm,
    ChangePasswordForm,
    AddEmailForm,
    SetPasswordForm, 
)

from django import forms

from allauth.socialaccount.forms import SignupForm as socialSignupForm


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #labelが不要なら
        self.fields['login'].label = ""
        self.fields['login'].widget.attrs['placeholder'] = "ユーザ名 または メールアドレス"

        self.fields['password'].label = ""
        self.fields['password'].widget.attrs['placeholder'] = "パスワード"

        self.fields['remember'].label = "ログインしたままに"

class CustomSignupForm(SignupForm):

    
    # username = forms.CharField(
    #     label=_("Username"),
    #     min_length=app_settings.USERNAME_MIN_LENGTH,
    #     widget=forms.TextInput(
    #         attrs={"placeholder": _("Username"), "autocomplete": "username"}
    #     ),
    # )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["terms"] = forms.BooleanField(
            widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            label='利用規約に同意する',
            error_messages={
                'required': '利用規約に同意してください'
        })

        #labelが不要なら
        self.fields['email'].label = ""
        self.fields['email'].widget.attrs['placeholder'] = "メールアドレス"

        self.fields['username'].label = ""
        self.fields['username'].widget.attrs['placeholder'] = "ユーザ名"

        self.fields['password1'].label = ""
        self.fields['password1'].widget.attrs['placeholder'] = "パスワード"

        self.fields['password2'].label = ""
        self.fields['password2'].widget.attrs['placeholder'] = "パスワード(again)"

class CustomResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #labelが不要なら
        self.fields['email'].label = ""
        self.fields['email'].widget.attrs['placeholder'] = "メールアドレス"

class CustomSocialSignupForm(socialSignupForm):
    pass