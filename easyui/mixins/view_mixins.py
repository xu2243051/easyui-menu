#!/usr/bin/python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .easyui_mixins import MenuPositionMixin, EasyUIListMixin, EasyUIGetVarMixin
from .easyui_mixins import  EasyUIFormMixin
# CsrfExemptMixin 第一次提交失败，第二次提交，csrf总失败
from .easyui_mixins import SingleObjectMixin, CsrfExemptMixin

#LogViewMixin
class EasyUIDatagridView(MenuPositionMixin, EasyUIListMixin, ListView):
    """
    包含datagrid的默认参数处理，菜单的位置等
    """

    def get_template_names(self):
        """
        datagrid的默认模板
        """
        names = super(EasyUIDatagridView, self).get_template_names()
        names.append('easyui/datagrid.html')
        return names

class EasyUICreateView(EasyUIFormMixin, CsrfExemptMixin, SingleObjectMixin, EasyUIGetVarMixin, CreateView):
    """
    EasyUI的CreateView
    """

    success_url = reverse_lazy('easyui:success')
    def get_template_names(self):
        """
        datagrid的默认模板
        """
        names = super(EasyUICreateView, self).get_template_names()
        names.append('easyui/form.html')
        return names


class EasyUIUpdateView(EasyUIFormMixin, CsrfExemptMixin, SingleObjectMixin, EasyUIGetVarMixin, UpdateView):
    """
    EasyUI的UpdateView
    """
    success_url = reverse_lazy('easyui:success')

    def get_template_names(self):
        """
        datagrid的默认模板
        """
        names = super(EasyUIUpdateView, self).get_template_names()
        names.append('easyui/form.html')
        return names

class EasyUIDeleteView( SingleObjectMixin, EasyUIGetVarMixin, DeleteView):
    """
    EasyUI的DeleteView
    """
    # 这个url不存在的
    success_url = reverse_lazy('easyui:success')

    def get_template_names(self):
        """
        datagrid的默认模板
        """
        names = super(EasyUIDeleteView, self).get_template_names()
        names.append('easyui/confirm_delete.html')
        return names
