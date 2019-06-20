from simple_history_field_track.models import ModelsTrackingFields
from simple_history.manager import HistoryManager


def should_record_history(wrapped_func):
    def wrapper(*args, **kwargs):
        if len(args) > 0:
            self = args[0]
            if hasattr(self, 'skip_history_when_saving'):
                del self.skip_history_when_saving

            if self.pk:
                query_set = HistoryManager(self._meta.model).get_queryset()
                previous_state = query_set.get(id=self.pk)

                model_fields = [f.name for f in self._meta.get_fields()]
                try:
                    tracking_fields = [field.split('|')[1] for field in ModelsTrackingFields.objects.get(
                        model_name=self._meta.model.__name__.lower()).tracking_fields]

                    changed_fields = list(filter(
                        lambda field: (field in tracking_fields) and getattr(self, field, None) != getattr(
                            previous_state, field, None), model_fields))
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
