from django.contrib.postgres.fields import ArrayField
from django.db import models


class ModelsTrackingFields(models.Model):
    model_name = models.CharField(
        max_length=128,
        verbose_name='مدل'
    )

    tracking_fields = ArrayField(
        models.CharField(max_length=128),
        default=list,
        verbose_name='فیلد‌های قابل نمایش در تاریخچه'
    )

    class Meta:
        verbose_name = 'مدل و فیلدهای قابل نمایش در تاریخچه'
        verbose_name_plural = 'مدل‌ها و فیلدهای قابل نمایش در تاریخچه'


