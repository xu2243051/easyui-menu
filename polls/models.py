import datetime

from django.db import models
from django.utils import timezone

from easyui.mixins.model_mixins import ModelMixin
# Create your models here.
class Question(ModelMixin, models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(' date published')

    def __unicode__(self):             # __str__ on Python 3
        return self.question_text 

    def was_published_recently(self):
        now  = timezone.now()
        return timezone.now() - datetime.timedelta(days=1) <=self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently'

    def test_command(self, *args, **kwargs):
        return 'xupeiyuan'

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):             # __str__ on Python 3
        return self.choice_text 
