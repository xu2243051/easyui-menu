#!coding:utf-8
import json

from django.db.models import get_model
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, logout, login
from django.http import  HttpResponseRedirect, HttpResponse

from .models import Menu, UserMenu, GroupMenu
from .forms import  UserMenuForm, GroupMenuForm
from .forms import UserLoginForm
from .forms import RootMenuForm, SubMenuForm, MenuForm
from easyui.mixins.view_mixins import EasyUICreateView, EasyUIUpdateView, \
        EasyUIDeleteView, EasyUIDatagridView, CommandDatagridView
from easyui.mixins.easyui_mixins import CsrfExemptMixin
from easyui.mixins.permission_mixins import LoginRequiredMixin

from django.views.generic.base import TemplateView, View
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

class AjaxUpdateView(CsrfExemptMixin, View):
    """
    datagrid中每一行的操作
    curl  -d "pk=1&app_label=easyui&model_name=Menu&method=test&name=xupeiyuan&row_index=1" 10.2.1.242:9000/easyui/AjaxUpdateView/
    """
    
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)
        
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests only
        argument:
            row_index HTML中第几行的标记，原值返回
            app_label
            model_name
            pk   app_label + model_name + pk 可以获取一个object
            method  object + method 得到要调用的方法 
            其它参数，html和method中同时定义, 在上面的方法中使用
        """
        query_dict = dict(self.request.POST.items())
        # row_index原值返回，在datagrid对应行显示结果 
        row_index = query_dict.pop('row_index')
        # 如果命令执行成功，并且没有返回值，则返回 "text+'成功'" 的提示
        text = query_dict.pop('text', None)

        app_label = query_dict.pop('app_label')
        model_name  = query_dict.pop('model_name')
        method  = query_dict.pop('method')
        pk = query_dict.pop('pk')
        model = get_model(app_label, model_name)
        object = model.objects.get(pk=pk)

        try:
            status = 0 # 0 success;  else fail
            func = getattr(object, method)
            # query_dict中的其它参数传递给调用的方法, 所有参数都是字符串
            print query_dict
            return_value = func(**query_dict)
            message = return_value
        except Exception, error_message:
            # ajax 处理失败
            status = 1  # 1 means fail
            message = unicode(error_message)

        # 如果命令执行成功，并且没有返回值，则返回 "text+'成功'" 的提示
        if not message:
            message = text+'成功'

        return self.render_to_json_response({'status':status, 'message':message, 'row_index':row_index})

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'base/home.html'

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['user'] = self.request.user
            return kwargs

class LoginView(FormMixin, TemplateView):
    form_class = UserLoginForm
    template_name = 'login.html'


    def form_valid(self, form):
        user = form.cleaned_data['user']
        passwd = form.cleaned_data['passwd']
        user = authenticate(username=user, password=passwd)

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

class MenuListView(CsrfExemptMixin, EasyUIDatagridView):
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
        usermenu_form.html 中定义
        usermenu  这两个model的定义类似，比如menus_checked和menus_show
        groupmenu
        @return  eg. ['1', '8', '9', '10' ]
        获取用户或者用户组的check_ids,会给出app_label, model_name, pk eg. /easyui/menulistview/?app_label=easyui&model_name=UserMenu&pk=1
        """
        checked_id = []
        qd = request.GET
        query_dict = dict(qd.items())
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

        checked_id = self.get_menu_checked(request)
        for row in data:
            if row['id'] in checked_id:
                # 把对应用户已经checked的菜单设置为checked
                row['checked'] = True

        if request.user.is_superuser:
            pass
        #elif request.user.is_staff:
        #    # is_staff 为true,可以登录后台,一般为公司内部员工
        #    pass
        else:
            # 普通用户的菜单在这里进行处理
            menu_id_list = []
            usermenu_set = request.user.usermenu_set.all()
            if(usermenu_set):
                # 判断一个用户是否有菜单的记录
                # 用户的显示菜单列表
                menu_list = usermenu_set[0].menus_show.split(',')
                menu_id_list.extend(menu_list)

            # 处理组的权限
            groups = request.user.groups.all()
            for group in groups:
                groupmenu_set= group.groupmenu_set.all()
                # 判断一个用户组是否有菜单的记录
                if(groupmenu_set):
                    menu_list = groupmenu_set[0].menus_show.split(',')
                    menu_id_list.extend(menu_list)
            menu_id_set = set(menu_id_list)

            if(menu_id_set):
                # 把id的列表处理为字典，方便等会的比较, 类型统一为int
                menu_id_set = [int(i) for i in menu_id_set]
                id_dict = dict(zip(menu_id_set, menu_id_set))
                new_data = []
                for row in data:
                    if id_dict.has_key(int(row['id'])):
                        new_data.append(row)

                data = new_data

            else:
                data = []

        return self.render_to_json_response(data)

class MenuCreateView(EasyUICreateView):
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

class MenuUpdateView(EasyUIUpdateView):
    model = Menu
    form_class = MenuForm

class MenuDeleteView(EasyUIDeleteView):
    model = Menu

class UserMenuCreateView(EasyUICreateView):
    model = UserMenu
    form_class = UserMenuForm

class UserMenuUpdateView(EasyUIUpdateView):
    model = UserMenu
    form_class = UserMenuForm

class UserMenuDeleteView(EasyUIDeleteView):
    model = UserMenu


class UserMenuListView(EasyUIDatagridView):
    options = """
        columns:[[
            {field:'cb', title:'', checkbox:true},
            {field:'id',title:'id',width:100},
            {field:'user',title:'用户',width:100},
            {field:'menus_show',title:'要显示的菜单ID',width:100},
            {field:'menus_checked',title:'checked菜单',width:100},
        ]]

    """
    model = UserMenu


class GroupMenuCreateView(EasyUICreateView):
    model = GroupMenu
    form_class = GroupMenuForm

class GroupMenuUpdateView(EasyUIUpdateView):
    model = GroupMenu
    form_class = GroupMenuForm

class GroupMenuDeleteView(EasyUIDeleteView):
    model = GroupMenu


class GroupMenuListView(EasyUIDatagridView):
    model = GroupMenu
    options = """
        columns:[[
            {field:'cb', title:'', checkbox:true},
            {field:'id',title:'id',width:100},
            {field:'group',title:'用户组',width:100},
            {field:'menus_show',title:'要显示的菜单ID',width:100},
            {field:'menus_checked',title:'checked菜单',width:100},
        ]]
    """

