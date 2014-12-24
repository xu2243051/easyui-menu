#coding:utf-8
import json

from django.core.exceptions import  ObjectDoesNotExist
from django.core.urlresolvers import  reverse_lazy
from django.http import HttpResponse, Http404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import   View

from easyui.utils import model_serialize
from easyui.models import Menu

# path_info path的resolve是否有区别，当在nginx中部署的时候
#
class EasyUIGetVarMixin(object):
    """
    设置了get页面的默认参数，get_context_data增加了prefix, view_url
    """

    def get_prefix(self):
        resolver_match = self.request.resolver_match
        namespace = resolver_match.namespace
        url_name = resolver_match.url_name
        prefix = '%s_%s' %(namespace, url_name) #menu_menucreateview
        return prefix.lower()

    def get_url(self):
        return self.request.get_full_path()

    def get_context_data(self, *args, **kwargs):
        context = super(EasyUIGetVarMixin, self).get_context_data(*args, **kwargs)
        context.update(prefix=self.get_prefix())
        context.update(view_url=self.get_url())

        verbose_name = self.model._meta.verbose_name
        context.update(verbose_name=verbose_name)

        model_name = self.model.__name__               # get the name of model
        app_label = self.model._meta.app_label         # get app_label of model
        context.update(model_name=model_name)
        context.update(app_label=app_label)
        return context


class EasyUIListMixin(EasyUIGetVarMixin, View):
    """
    EasyUi datagrid treegrid 专用
    method = None
    easyui_keywords = ['rows', 'page', 'order', 'sort'] #
    """
    options = None
    method = None
    easyui_keywords = ['rows', 'page', 'order', 'sort'] #
    easyui_prefix = 'easyui_'
    single_select = True
    # 一般是方法,是数据库中不存在字典
    extra_fields = []
    # 不显示的字段
    remove_fields = []

    def get_context_data(self, *args, **kwargs):
        context = super(EasyUIListMixin, self).get_context_data(*args, **kwargs)
        model_name = self.model.__name__               # get the name of model
        app_label = self.model._meta.app_label         # get app_label of model
        # datagrid  需要用到4个地址，并且这4个地址是有规律的
        list_url = reverse_lazy('%s:%sListView' %(app_label, model_name))
        create_url = reverse_lazy('%s:%sCreateView' %(app_label, model_name))
        update_url = reverse_lazy('%s:%sUpdateView' %(app_label, model_name))
        delete_url = reverse_lazy('%s:%sDeleteView' %(app_label, model_name))
        context.update(list_url=list_url)
        context.update(create_url=create_url)
        context.update(update_url=update_url)
        context.update(delete_url=delete_url)

        #options datagrid的options
        if self.options:
            # 如果有必要,定义一个get_options函数
            # datagrid定义用到的
            context.update(options=self.options)
        
        return context

    def get_querydict(self):
        """
        这个函数跟 self.method有关
        self.method 暂时没用, querydict都是POST的 
        """
        if self.method:
            querydict =  getattr(self.request, self.method.upper())
        else:
            querydict =  getattr(self.request, 'POST'.upper())
        # copy make querydict mutable

        query_dict =  dict(querydict.items())
        return query_dict



    def get_filter_dict(self):
        '''
        处理过滤字段 
        rows   一页显示多少行
        page   第几页, 1开始
        order  desc, asc      
        sort   指定排序的字段 order_by(sort)
        querydict 中的字段名和格式需要可以直接查询
        '''
        querydict = self.get_querydict()

        # post ,在cookie中设置了csrfmiddlewaretoken
        if querydict.has_key('csrfmiddlewaretoken'):
            querydict.pop('csrfmiddlewaretoken')

        try:
            page =  int(querydict.pop('page'))
            rows = int(querydict.pop('rows'))   
            setattr(self, 'easyui_page', page)
            setattr(self, 'easyui_rows', rows)
        except KeyError:
            setattr(self, 'easyui_page', None)
            setattr(self, 'easyui_rows', None)

        try:
            # order-> string  The default sort order, can only be 'asc' or 'desc' 
            # sort-> filed name
            # order_by('id')   order_by('-id')
            order = querydict.pop('order')
            sort = querydict.pop('sort')
            # order = 1
            # sort = 1
            if order == 'asc':
                setattr(self, 'easyui_order', sort)
            else:
                setattr(self, 'easyui_order', '-%s'% sort)

        except KeyError:
            setattr(self, 'easyui_order', None)

        # 过滤掉那些没有填写数据的input字段
        remove_key = []
        for key in querydict:
            if querydict[key] == '':
                remove_key.append(key)
        for key in remove_key:
            querydict.pop(key)

        return querydict

    def get_slice_start(self):
        """
        返回queryset切片的头
        """
        value = None
        if self.easyui_page:
            value = (self.easyui_page -1) * self.easyui_rows
        return  value

    def get_slice_end(self):
        """
        返回queryset切片的尾巴
        """
        value = None
        if self.easyui_page:
            value = self.easyui_page  * self.easyui_rows
        return value

    def get_queryset(self):
        """
        queryset 
        """
        filter_dict = self.get_filter_dict()
        queryset = super(EasyUIListMixin, self).get_queryset()
        queryset =  queryset.filter(**filter_dict)
        if self.easyui_order:
            # 如果指定了排序字段，返回排序的queryset
            queryset = queryset.order_by(self.easyui_order)

        return queryset


    def get_limit_queryset(self):
        """
        返回分页之后的queryset
        """
        queryset = self.get_queryset()
        limit_queryset = queryset.all()[self.get_slice_start() :self.get_slice_end()] #等增加排序
        return  limit_queryset

    def get_easyui_context(self, **kwargs):
        """
        初始化一个空的context
        """
        context = {}
        queryset = self.get_queryset()
        limit_queryset =  self.get_limit_queryset()
        data = model_serialize(limit_queryset, self.extra_fields, self.remove_fields)
        count = queryset.count()
        # datagrid 返回的数据中，total是总的行数，rows是查询到的结果集
        context.update(rows=data)
        context.update(total=count)
        return context

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)


    def post(self, request, *args, **kwargs):
        data = self.get_easyui_context()
        return self.render_to_json_response(data)

class MenuPositionMixin(object):
    """
    获取菜单的名字，显示菜单的名字，新的MenuPosMixin使用menu id
    """
    def get_context_data(self, *args, **kwargs):
        context = super(MenuPositionMixin, self).get_context_data(*args, **kwargs)

        # 点击菜单打开新的页面的时候，会传一个menu_id
        # get参数中的menu_id
        menu_id = getattr(self.request.GET, 'menu_id', None)
        print "MenuPositionMixin   menu_id: ", menu_id
        if menu_id !=None:
            menu = Menu.objects.get(pk=menu_id)

            menu_name_list = [menu.name]

            parent_menu = Menu.objects.get(pk = menu.parent_id)
            while parent_menu:
                if parent_menu.is_root:
                    break
                menu_name_list.insert(0, parent_menu.text)

                # 用get，如果没有对应的菜单，会出错
                menus = Menu.objects.filter(pk = parent_menu.parent_id)
                if menus:
                    parent_menu = menus[0]
                else:
                    parent_menu =  None

            current_pos = '>>'.join(menu_name_list)
            context.update(current_pos = current_pos)
        return context

class EasyUIFormMixin(object):
    """
    普通用户的form_class和超级用户的form_class不一样，
    如果是普通用户，并且有 self.user_form_class,直接返回这个
    """
    user_form_class = None
    def get_form_class(self):
        if not self.request.user.is_superuser  and not self.request.user.is_staff and self.user_form_class:
            return self.user_form_class
        return super(EasyUIFormMixin, self).get_form_class()



class SingleObjectMixin(object):
    """
    重定义UpdateView, DeleteView的get函数，我使用GET
    """
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        pk = self.request.GET.get(self.pk_url_kwarg, None)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        else:
            raise AttributeError("Generic detail view %s must be called with "
                    " an object pk."
                    % self.__class__.__name__)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                    {'verbose_name': queryset.model._meta.verbose_name})

        return obj

class CsrfExemptMixin(object):
    """
    csrf_exempt decorator applied to dispatch
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CsrfExemptMixin, self).dispatch(*args, **kwargs)
