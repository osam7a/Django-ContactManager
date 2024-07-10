from import_export import resources
from import_export import widgets

from django.db.utils import IntegrityError

from datetime import datetime
from .models import *

class ContactResource(resources.ModelResource):
    tags = widgets.ManyToManyWidget(Tag, field='tag_name')

    class Meta:
        model = Contact
        skip_unchanged = True
        report_skipped = True

    def before_import_row(self, row, **kwargs):
        tags = row.get('tags').replace("\"", "").split(',')
        row['tags'] = ""
        for i, tag in enumerate(tags):
            tag = tag.strip()
            tag, created = Tag.objects.get_or_create(tag_name=tag)
            row['tags'] += str(tag.pk) + ("," if i < len(tags) - 1 else "")
        

    def after_import(self, dataset, result, *args, **kwargs):
        title = "Import at " + datetime.now().strftime("%Y-%m-%d %H:%M")
        import_instance = Import(import_title=title)
        import_instance.save()
        for row in result.rows:
            if not row.instance:
                continue
            instance = row.instance
            import_instance.contacts.add(instance)
            import_instance.save()

    def before_export(self, queryset, *args, **kwargs):
        self.fields['tags'].widget = widgets.ManyToManyWidget(Tag, field='tag_name')
        
    # FIX UNIQUE CONSTRAINT VIOLATION
    def skip_row(self, instance, original, *args):
        try:
            instance.save()
        except IntegrityError:
            return True
        return False