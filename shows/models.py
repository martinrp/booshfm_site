# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
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

    search_fields = Page.search_fields + [
        index.SearchField('showname'),
        index.SearchField('showdescription'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('showname'),
        FieldPanel('showdescription'),
        FieldPanel('automationID'),
        FieldPanel('profileID', classname="full"),
    ]
