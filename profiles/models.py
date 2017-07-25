# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsearch import index



class ProfilesIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

# Keep the definition of BlogIndexPage, and add:


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
    ]
