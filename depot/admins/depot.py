from depot.models import Item
from django.contrib import admin
from django.db.models import Q


# show items in depot
class ItemsInline(admin.TabularInline):
    model = Item
    extra = 0
    can_delete = False


class DepotAdmin(admin.ModelAdmin):
    """
    Admin interface for depots

    As additional actions, one can archive or restore depots.
    The list of accessible depots is limited to the ones
    managed by the current user. Depots cannot be deleted.

    :author: Leo Tappe
    """

    inlines = [ItemsInline]
    list_display = ['name', 'active']
    ordering = ['name']
    filter_horizontal = ['manager_users', 'manager_groups']

    # Custom admin actions
    actions = ['make_archived', 'make_restored']

    def format_message(self, num_changed, change):
        if num_changed == 1:
            message = '1 depot was'
        else:
            message = '%s depots were' % num_changed
        return '%s successfully %s' % (message, change)

    def make_archived(self, request, queryset):
        depots_archived = queryset.update(active=False)
        self.message_user(request, self.format_message(depots_archived, 'archived'))

    make_archived.short_description = 'Archive selected depots'

    def make_restored(self, request, queryset):
        depots_restored = queryset.update(active=True)
        self.message_user(request, self.format_message(depots_restored, 'restored'))

    make_restored.short_description = 'Restore selected depots'

    # Limit the accessible depots to the one managed by the current user

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        return qs.filter(Q(organization__managers__id=request.user.id) |
                         Q(manager_users__id=request.user.id) |
                         Q(manager_groups__id__in=request.user.groups.all())).distinct()

    def has_add_permission(self, request):
        # Only via the organization's inline admin interface
        return request.user.organization_set.exists()

    def has_change_permission(self, request, obj=None):
        if not obj:
            return self.get_queryset(request).exists()

        return obj.managed_by(request.user)

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        # Remove delete action from dropdown
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']

        return actions

    def get_readonly_fields(self, request, obj=None):
        # Depots cannot be moved to another organization
        if obj:
            return ['organization']

        return []

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj=obj, **kwargs)

        # Limit organization selection to the ones the current user is managing
        if 'organization' in form.base_fields:
            form.base_fields['organization'].queryset = request.user.organization_set

        return form
