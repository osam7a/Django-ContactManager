from django.db import models
from django.utils.translation import gettext_lazy as _

class Tag(models.Model): # Approx. 0.02 GB per 1 million records
    tag_name = models.CharField(max_length=100, unique=True, help_text=_("The name of the tag."))

    def __str__(self):
        return self.tag_name

class Import(models.Model): # Approx. 0.02 GB per 1 million records
    created_at = models.DateTimeField(auto_now_add=True)
    import_title = models.CharField(max_length=100, blank=True, help_text=_("The title of the import."))
    contacts = models.ManyToManyField('Contact', blank=True, help_text=_("The contacts of the import."))

    def __str__(self):
        return self.import_title

class Contact(models.Model): # Approx. 8.02 GB per 1 million records
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, help_text=_("The name of the contact."))
    email = models.EmailField(unique=True, help_text=_("The email address of the contact."))
    company = models.CharField(max_length=100, blank=True, help_text=_("The company of the contact."))
    address = models.CharField(max_length=255, blank=True, help_text=_("The address of the contact."))
    title = models.CharField(max_length=5, blank=True, help_text=_("The title of the contact."))
    phone = models.CharField(max_length=20, blank=True, help_text=_("The phone number of the contact."))
    birthday = models.DateField(blank=True, null=True, help_text=_("The birthday of the contact."))
    website = models.URLField(blank=True, help_text=_("The website of the contact."))

    recently_contacted = models.BooleanField(default=False, help_text=_("Whether the contact was recently contacted in a campaign or not."))
    recently_bounced = models.BooleanField(default=False, help_text=_("Whether the contact recently bounced in one of the campiagns or not."))
    subscribed = models.BooleanField(default=True, help_text=_("Whether the contact is subscribed or not."))
    source = models.CharField(blank=True, max_length=255, help_text=_("The source of the contact."))
    tags = models.ManyToManyField(Tag, blank=True, null=True, help_text=_("The tags of the contact."))
    
    auto_unmark = models.IntegerField(default=0, help_text=_("The number of days to wait before unmarking the contact as `recently_contacted`, put \"0\" to manually unmark."))

    def __str__(self):
        return self.email