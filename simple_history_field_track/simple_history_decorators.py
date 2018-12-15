from simple_history_field_track.models import ModelsTrackingFields
from simple_history.manager import HistoryManager


def should_record_history(wrapped_func):
    def wrapper(*args, **kwargs):
        if len(args) > 0:
            self = args[0]

            if not self.id:
                self.skip_history_when_saving = True

            else:
                query_set = HistoryManager(self._meta.model).get_queryset()
                previous_state = query_set.get(id=self.id)

                campaign_model_fields = [f.name for f in self._meta.get_fields()]
                try:
                    changed_fields = list(filter(lambda field: field.split('|')[1] in ModelsTrackingFields.objects.get(
                        model_name=self._meta.model.__name__).tracking_fields and getattr(self, field, None) != getattr(
                        previous_state, field, None), campaign_model_fields))
                    if len(changed_fields) == 0:
                        self.skip_history_when_saving = True
                except ModelsTrackingFields.DoesNotExist:
                    self.skip_history_when_saving = True

            new_args = list(args)

            new_args[0] = self
        else:
            new_args = args

        wrapped_func(*new_args, **kwargs)

    return wrapper
