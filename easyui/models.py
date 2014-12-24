#coding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy

from .mixins.model_mixins import ModelMixin
# Create your models here.
class Menu(ModelMixin, models.Model):
    """
    menu model
    reverse: args and kwargs cannot be passed to reverse() at the same time.
    这里只是用了kwargs
    """
    text = models.CharField('菜单名', max_length=100, help_text='最多100个英文字母长')
    is_root = models.BooleanField('是否为根节点', help_text='这个不添的，form中缺省处理', default=False)
    parent_id = models.IntegerField('父ID')
    namespace = models.CharField('APP名', max_length=100)
    viewname = models.CharField('view名', max_length=100)
    kwargs = models.CharField('附加参数', max_length=100, blank=True)
    is_system = models.BooleanField('是否为系统菜单', default=False, blank=True, help_text='系统菜单只对超级用户和后台用户显示')

    def get_absolute_url(self):
        return reverse_lazy('menu:MenuListView')

    def __unicode__(self):
        return self.text

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = verbose_name



