from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from simple_history_field_track.models import ModelsTrackingFields


def is_valid_model(content_type):
    return content_type.model_class() is not None and hasattr(content_type.model_class(), 'history')


class FieldSelectForm(forms.ModelForm):
    valid_content_types = list(filter(lambda ct: is_valid_model(ct), ContentType.objects.all()))

    model_name = forms.ChoiceField(
        choices=[(content_type.model.lower(), content_type.model_class()._meta.verbose_name) for content_type in
                 valid_content_types]
    )

    meta_options = [content_type.model_class()._meta for content_type in valid_content_types]

    tracking_fields = forms.MultipleChoiceField(
        choices=[(meta.model_name.lower() + '|' + field.name, meta.verbose_name + ' | ' + str(field.verbose_name)) for meta in meta_options
                 for field in meta.local_fields]
    )

    def clean(self):
        data = self.cleaned_data
        if not all([field.split('|')[0] == data['model_name'] for field in data['tracking_fields']]):
            raise forms.ValidationError('Error')

    class Meta:
        model = ModelsTrackingFields
        fields = '__all__'


@admin.register(ModelsTrackingFields)
class ModelsTrackingFieldsAdmin(admin.ModelAdmin):
    form = FieldSelectForm
