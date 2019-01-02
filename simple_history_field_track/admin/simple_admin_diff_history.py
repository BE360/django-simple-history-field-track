from simple_history.admin import SimpleHistoryAdmin
from simple_history_field_track.models import ModelsTrackingFields
from simple_history_field_track.templatetags.simple_history_admin_list import fa_datetime_filter


class SimpleAdminDiffHistory(SimpleHistoryAdmin):
    object_history_template = "simple_history_field_track/object_history.html"

    def compare(self, obj1, obj2):
        excluded_keys = 'history_user_id', 'changed_fields', 'modified', 'history_change_reason', 'history_type',\
                        'history_id', 'history_date', '_state'
        return self._compare(obj1, obj2, excluded_keys)

    def _compare(self, obj1, obj2, excluded_keys):
        d1, d2 = obj1.__dict__, obj2.__dict__
        try:
            included_fields = list(map(lambda x: x.split('|')[1], ModelsTrackingFields.objects.get(
                model_name=obj1._meta.model.__name__[10:].lower()).tracking_fields))
            old, new = {}, {}
            for k, v in d1.items():
                if k in excluded_keys or k not in included_fields:
                    continue
                try:
                    if v != d2[k]:
                        old.update({k: v})
                        new.update({k: d2[k]})
                except KeyError:
                    old.update({k: v})

            return '، '.join(set(map(lambda x: self.model._meta.get_field(x).verbose_name, old)) | set(
                map(lambda x: self.model._meta.get_field(x).verbose_name, new)))
        except ModelsTrackingFields.DoesNotExist:
            return None

    def history_view(self, request, object_id, extra_context=None):
        model = self.model
        opts = model._meta
        pk_name = opts.pk.attname
        history = getattr(model, model._meta.simple_history_manager_attribute)
        action_list = list(history.filter(**{pk_name: object_id}).order_by('-history_id'))

        for index, action in enumerate(action_list):
            action.history_date = fa_datetime_filter(action.history_date)
            action.changed_fields = ''
            if index < len(action_list) - 1:
                action.changed_fields = self.compare(action, action_list[index + 1])
            else:
                action.changed_fields = '-'
            action_list[index] = action

        action_list = list(filter(lambda x: x.changed_fields or x.history_type == '+', action_list))

        context = {
            **(extra_context or {}),
            'action_list': action_list,
        }
        return super(SimpleAdminDiffHistory, self).history_view(request, object_id, context)
