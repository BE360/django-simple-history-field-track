from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from simple_history.admin import SimpleHistoryAdmin as DefaultSimpleHistoryAdmin


class SimpleHistoryAdmin(DefaultSimpleHistoryAdmin):
    def history_form_view(self, request, object_id, version_id):
        if request.method == 'POST' and request.POST.get('_save') == 'Revert':
            request.current_app = self.admin_site.name
            original_opts = self.model._meta
            model = getattr(
                self.model,
                self.model._meta.simple_history_manager_attribute).model
            obj = get_object_or_404(model, **{
                original_opts.pk.attname: object_id,
                'history_id': version_id,
            }).instance
            obj._state.adding = False

            if not self.has_delete_permission(request, obj):
                raise PermissionDenied

        return super(SimpleHistoryAdmin, self).history_form_view(request, object_id, version_id)
