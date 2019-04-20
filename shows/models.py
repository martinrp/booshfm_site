# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from modelcluster.fields import ParentalKey

# Create your models here.
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index



class ShowIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(ShowIndexPage, self).get_context(request)
        showpages = self.get_children().live().order_by('-first_published_at')
        context['showpages'] = showpages
        return context

# Keep the definition of BlogIndexPage, and add:


class ShowPage(Page):
    showname = models.CharField(max_length=250)
    showdescription = RichTextField(blank=True)
    automationID = RichTextField(blank=True)
    profileID = RichTextField(blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('showname'),
        index.SearchField('showdescription'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('showname'),
        FieldPanel('showdescription'),
        FieldPanel('automationID'),
        FieldPanel('profileID', classname="full"),
        InlinePanel('gallery_images', label="Gallery images"),

    ]


class ShowPageGalleryImage(Orderable):
    page = ParentalKey(ShowPage, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]
