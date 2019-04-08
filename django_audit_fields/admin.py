from edc_utils import get_utcnow

audit_fields = [
    "user_created",
    "user_modified",
    "created",
    "modified",
    "hostname_created",
    "hostname_modified",
]

audit_fieldset_tuple = (
    "Audit", {"classes": ("collapse",), "fields": audit_fields})


class ModelAdminAuditFieldsMixin:
    def save_model(self, request, obj, form, change):
        if not change:
            obj.user_created = request.user.username
            obj.created = get_utcnow()
        else:
            obj.user_modified = request.user.username
            obj.modified = get_utcnow()
        super().save_model(request, obj, form, change)

    def get_list_filter(self, request):
        fields = [
            "created",
            "modified",
            "user_created",
            "user_modified",
            "hostname_created",
            "hostname_modified",
        ]
        self.list_filter = list(self.list_filter) + [
            f for f in fields if f not in self.list_filter
        ]
        return self.list_filter

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        return list(readonly_fields) + [
            f for f in audit_fields if f not in readonly_fields
        ]
