# -*- coding:utf-8 -*-
from django.forms import Form, widgets, fields, ValidationError


class register(Form):
    userName = fields.CharField(max_length=10)
    password = fields.CharField(max_length=10, widget=widgets.PasswordInput)
    repassword = fields.CharField(max_length=10, widget=widgets.PasswordInput)

    def clean(self):
        userName = self.cleaned_data['userName']
        password = self.cleaned_data['password']
        repassword = self.cleaned_data['repassword']
        if not password == repassword:
            myerror = '两次密码不一致,请重新输入'
            raise ValidationError(myerror)

        return self.cleaned_data


class login(Form):
    userName = fields.CharField(max_length=10)
    password = fields.CharField(max_length=10, widget=widgets.PasswordInput)
