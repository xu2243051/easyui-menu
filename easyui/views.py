#!coding:utf-8
from django.shortcuts import render
from django.http import  HttpResponseRedirect, HttpResponse

from easyui.models import Menu
# Create your views here.
from easyui.mixins import view_mixins 
from easyui.mixins.easyui_mixins import CsrfExemptMixin


from easyui.mixins.permission_mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormMixin

def success(request):
    """
    增删改操作成功之后返回这个页面
    """
    return HttpResponse('success')

def get_url(request):
    """
    通过menu_id，获取对应的URL
    eg. /easyui/MenuListView/
    """

    menu_id = request.GET.get('menu_id')
    m_object = Menu.objects.get(pk=menu_id)
    namespace = m_object.namespace
    viewname = m_object.viewname
    url_string = '%s:%s' %(namespace, viewname)
    url = reverse(url_string)

    return HttpResponse(url)

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'base/home.html'

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['user'] = self.request.user
            return kwargs

from django.contrib.auth import authenticate, logout, login
from django.core.urlresolvers import reverse
from easyui.forms import UserLoginForm
class LoginView(FormMixin, TemplateView):
    form_class = UserLoginForm
    template_name = 'login.html'


    def form_valid(self, form):
        user = form.cleaned_data['user']
        passwd = form.cleaned_data['passwd']
        user = authenticate(username=user, password=passwd)
        print user

        if user is not None:
            # the password verified for the user 
             if user.is_active:
                 login(self.request, user)
                 redirect_url = self.request.GET.get('next', None)
                 if not redirect_url:
                     redirect_url = reverse('easyui:home')

                 return HttpResponseRedirect(redirect_url)

        #如果账号无效，或者账号不存在，密码错误，都提示一样的错误
        form.errors.update({'user':[u'账号或者密码不正确']})
        return self.form_invalid(form=form)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('easyui:home'))

import json
from django.db.models import get_model
class MenuListView(CsrfExemptMixin, view_mixins.EasyUIDatagridView):
    """
    MenuListView 根据权限返回menu的数据
    用户菜单权限，只有超级用户和staff用户可以操作
    """
    model = Menu

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)


    def get_menu_checked(self, request):
        """
        获取用户或者用户组checked的菜单列表
        myusermenu_form.html 中定义
        myusermenu  这两个model的定义类似，比如menus_checked和menus_show
        mygroupmenu
        @return  eg. ['1', '8', '9', '10' ]
        获取用户或者用户组的check_ids,会给出app_label, model_name, pk eg. /easyui/menulistview/?app_label=easyui&model_name=UserMenu&pk=1
        """
        checked_id = []
        qd = request.GET
        query_dict = dict(qd.items())
        checked_id = []
        if query_dict:
            #object = get_object(**query_dict)
            app_label = query_dict['app_label']
            model_name = query_dict['model_name']
            pk = query_dict['pk']
            model = get_model(app_label, model_name)
            object =  model.objects.get(pk=pk)
            checked_id = object.menus_checked.split(',')

        return checked_id

    def post(self, request, *args, **kwargs):
        # 这个是tree的view，只需要直接返回rows中的内容
        data = self.get_easyui_context()['rows']

        # 把
        checked_id = self.get_menu_checked(request)
        for row in data:
            if row['id'] in checked_id:
                # 把对应用户已经checked的菜单设置为checked
                row['checked'] = True

        if request.user.is_superuser:
            pass
        elif request.user.is_staff:
            # is_staff 为true,可以登录后台,一般为公司内部员工
            pass
        else:
            menu_id_list = []
            myusermenu_set = request.user.myusermenu_set.all()
            if(myusermenu_set):
                # 判断一个用户是否有菜单的记录
                # 用户的显示菜单列表
                menu_list = myusermenu_set[0].menus_show.split(',')
                menu_id_list.extend(menu_list)

            # 处理组的权限
            groups = request.user.groups.all()
            for group in groups:
                mygroupmenu_set= group.mygroupmenu_set.all()
                # 判断一个用户组是否有菜单的记录
                if(mygroupmenu_set):
                    menu_list = mygroupmenu_set[0].menus_show.split(',')
                    menu_id_list.extend(menu_list)
            menu_id_set = set(menu_id_list)

            if(menu_id_set):
                # 把id的列表处理为字典，方便等会的比较
                id_dict = dict(zip(menu_id_set, menu_id_set))
                new_data = []
                for row in data:
                    if id_dict.has_key(row['id']):
                        new_data.append(row)

                data = new_data

            else:
                data = []

            # 普通用户的菜单在这里进行处理
        # print data
        return self.render_to_json_response(data)

from .forms import RootMenuForm, SubMenuForm, MenuForm
class MenuCreateView(view_mixins.EasyUICreateView):
    model = Menu
    form_class = MenuForm
    sub_form_class = SubMenuForm
    root_form_class = RootMenuForm

    def get_form_class(self):
        type = self.request.GET.get('type', None)
        if type == 'sub_menu':
            return self.sub_form_class
        elif type == 'root_menu':
            return self.root_form_class
        else:
            raise Exception('创建菜单出错,请传type参数')

class MenuUpdateView(view_mixins.EasyUIUpdateView):
    model = Menu
    form_class = MenuForm

class MenuDeleteView(view_mixins.EasyUIDeleteView):
    model = Menu
