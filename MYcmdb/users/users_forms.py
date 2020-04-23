import re
from django import forms
from users.models import UsersProfile
# gender_choice = ( ('1', "男"),('2',"女"))

class UserRegisterModelForm(forms.ModelForm):
    class Meta:
        model = UsersProfile
        fields=[
            "username","password","email",
            "mobile","age","gender","avatar",]
        widgets = {
            #字段名称: 小插件
            'gender': forms.RadioSelect()
        }
    def clean_mobile(self):
            """
            验证手机号是否合法
            :return: 合法的数据或者错误信息
            """
            mobile = self.cleaned_data['mobile']
            PRGEX_MOBILE = r'^1[358]\d{9}|^147\d{8}|^176\d{8}$'
            regex = re.compile(PRGEX_MOBILE)
            if regex.match(mobile):
                return mobile
            else:
                raise forms.ValidationError(
                    '无效手机号',
                    code='mobile_invalid'
                )

