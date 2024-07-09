from import_export.admin import ImportExportModelAdmin
from advanced_filters.admin import AdminAdvancedFiltersMixin

from django.contrib import admin

from .models import *
from .resource import ContactResource

@admin.action(description='Mark as recently contacted')
def mark_as_recently_contacted(modeladmin, request, queryset):
    queryset.update(recently_contacted=True)

@admin.action(description='Mark as recently bounced')
def mark_as_recently_bounced(modeladmin, request, queryset):
    queryset.update(recently_bounced=True)

class ContactAdmin(AdminAdvancedFiltersMixin, ImportExportModelAdmin):
    resource_class = ContactResource
    list_display = ('id', 'email', 'name', 'phone', 'source', 'recently_contacted', 'recently_bounced', 'get_tags')
    list_per_page = 20
    
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

    actions = [mark_as_recently_contacted, mark_as_recently_bounced]


    def get_tags(self, obj):
        return ", ".join([t.tag_name for t in obj.tags.all()])
    
    get_tags.short_description = 'Tags'

admin.site.register(Contact, ContactAdmin)
admin.site.register(Tag)
admin.site.register(Import)