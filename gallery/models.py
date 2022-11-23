from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


# При необходимости могу так же сделать кастомную модель пользователя
# и разбить приложение gallery на разные приложения

class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name=_('user'), related_name='photo')
    title = models.CharField(max_length=255, verbose_name=_('title'))
    description = models.TextField(verbose_name=_('description'))
    file = models.ImageField(upload_to=f'gallery', verbose_name=_('ímage'))

    class Meta:
        verbose_name_plural = _('images')
        verbose_name = _('image')

    def __str__(self):
        return self.title
