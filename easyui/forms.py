#!/usr/bin/python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django import forms

from .models import Menu, UserMenu, GroupMenu
class UserLoginForm(forms.Form):
    required_css_class = 'required'
    error_css_class = 'error'
    user = forms.CharField(label='用户')
    passwd = forms.CharField(label='密码', widget = forms.TextInput(attrs={'type':'password'})
)

class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu

        widgets = {
            'text':forms.TextInput(attrs={'class':'easyui-validatebox','data-options':'required:true'}),
            'is_root':forms.CheckboxInput(attrs={'disabled':'disabled'}),
            'namespace':forms.TextInput(attrs={'class':'easyui-validatebox','data-options':'required:false'}),
            'viewname':forms.TextInput(attrs={'class':'easyui-validatebox','data-options':'required:false'}),
            'kwargs':forms.TextInput(attrs={'class':'easyui-validatebox', 'data-options':'required:false'}),
            'parent_id':forms.Select(attrs={'class':'easyui-combobox','data-options':'required:true', "style":"width:150px;height:auto"}),
            }

class SubMenuForm(MenuForm):
    """
    is_root is a hidden field ,and set value to False
    """
    is_root = forms.BooleanField(label='是否顶级节点', widget=forms.CheckboxInput(attrs={'disabled':'disabled'}), required=False, initial=False)

class RootMenuForm(MenuForm):
    is_root = forms.BooleanField(label='是否顶级节点', widget=forms.CheckboxInput(attrs={'onclick':"return false"}), required=False, initial=True)

class UserMenuForm(forms.ModelForm):

    class Meta:
        model = UserMenu
        widgets = {
                'user':forms.Select(attrs={'class':'easyui-combobox','data-options':'required:true'}),
                'menus_show':forms.HiddenInput(),
                'menus_checked':forms.HiddenInput(),
                }

class GroupMenuForm(forms.ModelForm):

    class Meta:
        model = GroupMenu
        widgets = {
                'group':forms.Select(attrs={'class':'easyui-combobox','data-options':'required:true'}),
                'menus_show':forms.HiddenInput(),
                'menus_checked':forms.HiddenInput(),
                }
