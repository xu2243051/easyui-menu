#coding:utf-8
'''
这个通用的自定义功能页面
'''
from django.conf.urls import patterns, url
def model_serialize(queryset, extra_fields=[], remove_fields = [], fields = []):
    """
    @param queryset  queryset
    @return a list of dict [{}, {}]
    自定义的json转换函数，跟extramixin中的get_fields密切相关
    """

    return_list = []
    for object in queryset:
        value_dict = dict(object.get_fields(field_verbose=False, value_verbose=True, 
            fields=fields, remove_fields=remove_fields, extra_fields=extra_fields))
        return_list.append(value_dict)

    return return_list

def register_views(app_name, view_filename, urlpatterns=None):
    """
    app_name       APP名
    view_filename  views 所在的文件
    urlpatterns    url中已经存在的urlpatterns

    return urlpatterns
    
    只导入View结尾的，是类的视图
    """
    app_module = __import__(app_name)
    view_module = getattr(app_module, view_filename)
    views = dir(view_module)
    for view_name in views:
        if view_name.endswith('View'):
            view = getattr(view_module, view_name)
            if isinstance(view, object):
                if urlpatterns:
                    urlpatterns  += patterns('',
                            url(r'^(?i)%s/$' % view_name, view.as_view(),  name=view_name),
                            )
                else:
                    urlpatterns = patterns('',
                            url(r'^(?i)%s/$' % view_name, view.as_view(),  name=view_name),
                            )
            else:
                pass
    return urlpatterns
