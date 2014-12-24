#!/usr/bin/python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.http import  HttpResponseRedirect

class LoginRequiredMixin(object):
    """
    需要有self.model
    permission_required: add, delete, change
    add: can add, upload , update
    delete: can delete
    permission_required = None, 只要登录就可以操作
    permission_required = add 需要有add权限, ......
    **权限不足会跳到login页面**

    """
    permission_required = None
    @method_decorator(login_required(login_url=reverse_lazy('easyui:login')))
    def dispatch(self, request, *args, **kwargs):
        """
        增加了权限控制，当self存在model和permission_required时，才会检查权限
        """
        if getattr(self, 'model', None) and self.permission_required:
            app_label = self.model._meta.app_label
            model_name = self.model.__name__.lower()
            permission_required = self.permission_required.lower()
            permission = '%(app_label)s.%(permission_required)s_%(model_name)s' % {
                'app_label':app_label,
                'permission_required':permission_required,
                'model_name': model_name
            }
            if not self.request.user.has_perm(permission):
                return HttpResponseRedirect(reverse_lazy('easyui:login'))

        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
