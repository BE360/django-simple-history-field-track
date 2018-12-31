from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from simple_history_field_track.models import ModelsTrackingFields


def is_valid_model(content_type):
    return content_type.model_class() is not None and hasattr(content_type.model_class(), 'history')


class FieldSelectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FieldSelectForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        if instance:
            if hasattr(instance, 'model_name'):
                meta_options = [content_type.model_class()._meta for content_type in self.valid_content_types if
                                content_type.model_class()._meta.model_name == instance.model_name]
                self.fields['tracking_fields'] = forms.MultipleChoiceField(
                    choices=[(meta.model_name.lower() + '|' + field.name,
                              meta.verbose_name + ' | ' + str(field.verbose_name))
                             for
                             meta in meta_options
                             for field in meta.local_fields],
                    required=False
                )

    valid_content_types = list(filter(lambda ct: is_valid_model(ct), ContentType.objects.all()))

    model_name = forms.ChoiceField(
        choices=[(content_type.model.lower(), content_type.model_class()._meta.verbose_name) for content_type in
                 valid_content_types]
    )

    def clean(self):
        data = self.cleaned_data
        if 'tracking_fields' in data:
            if not all([field.split('|')[0] == data['model_name'] for field in data['tracking_fields']]):
                raise forms.ValidationError('Invalid tracking fields')

    class Meta:
        model = ModelsTrackingFields
        fields = '__all__'


@admin.register(ModelsTrackingFields)
class ModelsTrackingFieldsAdmin(admin.ModelAdmin):
    form = FieldSelectForm

    list_display = ('model_name', 'get_tracking_fields')

    def get_tracking_fields(self, instance):
        return ', '.join(instance.tracking_fields)

    get_tracking_fields.short_description = 'فیلد‌های قابل نمایش در تاریخچه'
