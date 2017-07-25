# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

class ProfilesIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(ProfilesIndexPage, self).get_context(request)
        profilepages = self.get_children().live().order_by('-first_published_at')
        context['profilepages'] = profilepages
        return context

# Keep the definition of ProfilePage, and add:
class ProfilePage(Page):
    name = models.CharField(max_length=250)
    bio = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('name'),
        index.SearchField('bio'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('bio', classname="full"),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

class ProfilePageGalleryImage(Orderable):
    page = ParentalKey(ProfilePage, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]
