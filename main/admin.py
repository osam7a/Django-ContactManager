from import_export.admin import ImportExportModelAdmin
from advanced_filters.admin import AdminAdvancedFiltersMixin

from django.contrib import admin
from django.contrib import messages
from django.utils.translation import gettext as _

from .models import *
from .resource import ContactResource

# @admin.action(description='Mark as recently contacted')
# def mark_as_recently_contacted(modeladmin, request, queryset):
#     queryset.update(recently_contacted=True)

# @admin.action(description='Mark as recently bounced')
# def mark_as_recently_bounced(modeladmin, request, queryset):
#     queryset.update(recently_bounced=True)

# @admin.action(description='Bulk edit contacts')
# def bulk_edit_contacts(modeladmin, request, queryset):
#     # open popup with form
    

class ContactAdmin(AdminAdvancedFiltersMixin, ImportExportModelAdmin):
    resource_class = ContactResource
    list_display = ('id', 'email', 'name', 'phone', 'source', 'recently_contacted', 'recently_bounced', 'get_tags')
    list_per_page = 150
    
    advanced_filter_fields = (
        'name',
        'email',
        'company',
        'address',
        'phone',
        'source',
        'tags__tag_name',
        'recently_contacted',
        'recently_bounced'
    )
    list_filter = ('source', 'import__import_title', 'tags__tag_name', 'recently_contacted', 'recently_bounced')
    search_fields = ('name', 'email', 'company', 'address', 'phone', 'source', 'tags__tag_name')

    actions = ['mark_as_recently_contacted', 'mark_as_recently_bounced', 'clear_tags']

    def get_tags(self, obj):
        return ", ".join([t.tag_name for t in obj.tags.all()])
    
    get_tags.short_description = 'Tags'

    def get_actions(self, request):
        actions = super().get_actions(request)
        for tag in Tag.objects.all():
            action_name = f'add_tag_{tag.id}'
            actions[action_name] = (self.add_tag, action_name, f'Add tag: {tag.tag_name}')
        return actions

    def add_tag(self, modeladmin, request, queryset):
        tag_id = int(request.POST['action'].split('_')[-1])
        tag = Tag.objects.get(id=tag_id)
        for contact in queryset:
            contact.tags.add(tag)
        self.message_user(
            request,
            _(f'{queryset.count()} contacts were tagged with {tag.tag_name}.'),
            messages.SUCCESS
        )

    @admin.action(description='Clear tags')
    def clear_tags(self, request, queryset):
        for contact in queryset:
            contact.tags.clear()
        self.message_user(
            request,
            _(f'{queryset.count()} contacts were untagged.'),
            messages.SUCCESS
        )

    @admin.action(description='Mark as recently contacted')
    def mark_as_recently_contacted(self, request, queryset):
        queryset.update(recently_contacted=True)
        self.message_user(
            request,
            _(f'{queryset.count()} contacts were marked as recently contacted.'),
            messages.SUCCESS
        )

    @admin.action(description='Mark as recently bounced')
    def mark_as_recently_bounced(self, request, queryset):
        queryset.update(recently_bounced=True)
        self.message_user(
            request,
            _(f'{queryset.count()} contacts were marked as recently bounced.'),
            messages.SUCCESS
        )

admin.site.register(Contact, ContactAdmin)
admin.site.register(Tag)
admin.site.register(Import)