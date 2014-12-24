#!/usr/bin/python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django.db.models import   ForeignKey

class ModelMixin(object):
    """
    add custom method to models
    """

    def get_default_fields(self):
        """
        get all fields of model, execpt id
        """
        field_names = self._meta.get_all_field_names()
        if 'id' in field_names:
            field_names.remove('id')

        return field_names

    def get_field_value(self, field, value_verbose=True):
        """
        返回显示的值，而不是单纯的数据库中的值
        field  是model中的field type
        value_verbose 为True，返回数据的显示数据，会转换为choice的内容，
        如果value_verbose 为False， 返回数据的实际值
        """
        if not value_verbose:
            """
            value_verbose == false, return raw value
            """
            value = field._get_val_from_obj(self)
        else:
            if isinstance(field, ForeignKey):
                # 获取外键的内容
                value = getattr(self, field.name)
            else:
                # 非外键
                try:
                    value =  self._get_FIELD_display(field)
                except :
                    value = field._get_val_from_obj(self)
        if(value == True or value == False or isinstance(value, (int, float))):
            return value
        return unicode(value)

# 模拟admin的field_list，但是效率低，有空看看源代码
    def get_fields(self, field_verbose=True, value_verbose=True, fields=[], extra_fields=[], remove_fields = []):
        '''
        返回字段名及其对应值的列表
        field_verbose 为True，返回定义中的字段的verbose_name， False返回其name
        value_verbose 为True，返回数据的显示数据，会转换为choice的内容，为False， 返回数据的实际值
        fields 指定了要显示的字段
        extra_fields 指定了要特殊处理的非field，比如是函数
        remove_fields 指定了不显示的字段
        '''
        field_list = []
        for field in self.__class__._meta.fields:
            if field.name in remove_fields:
                # 不显示的字段，跳过循环
                continue

            if fields and field.name not in fields:
                # fields 不为空列表，即指定了要显示的字段，并且field.name  不再指定的列表中，跳过循环
                continue

            if field.verbose_name and field_verbose:
                value_tuple = (field.verbose_name, self.get_field_value(field, value_verbose))
            else:
                value_tuple = (field.name, self.get_field_value(field, value_verbose))

            field_list.append(value_tuple)

        for name in extra_fields:
            # 处理函数
            method = getattr(self, name)
            result = method()
            value_tuple = (name, result)
            field_list.append(value_tuple)

        return field_list


