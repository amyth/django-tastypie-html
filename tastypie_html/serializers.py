#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#
#    Django Tastypie Html
#
#    Copyright (C) 2014  Amyth Arora
#    @Author - Amyth Arora <mail@amythsingh.com>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; Applies version 2 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import urlparse

from django.template import loader, Context, TemplateDoesNotExist
from django.template.response import TemplateResponse

from tastypie.bundle import Bundle
from tastypie.serializers import Serializer


class HtmlJsonSerializer(Serializer):
    """
    Extends tastypie's base serializer to support
    html serialization/deserialization.
    """

    def __init__(self, template_name, forms=None, *args, **kwargs):
        self.template_name = template_name
        self.forms = forms if forms else {}
        super(HtmlJsonSerializer, self).__init__(*args, **kwargs)

    def to_json(self, request, data, *args, **kwargs):
        return super(HtmlJsonSerializer, self).to_json(data,
                *args, **kwargs)

    def to_html(self, request, data, options=None):
        """
        Given some python data and a django template,
        produces HTML output.
        """

        options = options if options else {}
        template = self.template_name

        objects = data.get('objects', [])
        objects = [obj.obj if isinstance(obj, Bundle) else \
                obj for obj in objects]
        data['objects'] = objects

        # Add forms to the context
        if self.forms:
            for name, form in self.forms.iteritems():
                data[name] = form

        try:
            t = TemplateResponse(request, template, data)
            t.render()
        except (TemplateDoesNotExist, AttributeError) as err:
            raise TemplateDoesNotExist(template)

        return t.content

    def from_html(self, content):
        """
        Handles a HTML form input, and deserializes the
        form data into python data.
        """

        qdict = urlparse.parse_qs(content)
        return qdict


    def serialize(self, request, bundle, format='application/json', options=None):
        """
        Given some data and a format, calls the correct method to serialize
        the data and returns the result.
        """

        desired_format = None
        if options is None:
            options = {}

        for short_format, long_format in self.content_types.items():
            if format == long_format:
                if hasattr(self, "to_%s" % short_format):
                    desired_format = short_format
                    break

        if desired_format is None:
            raise UnsupportedFormat("The format indicated '%s' "\
                    "had no available serialization method. "\
                    "Please check your ``formats`` and "\
                    "``content_types`` on your Serializer." % format)

        serialized = getattr(self, "to_%s" % desired_format)(
                request, bundle, options)
        return serialized

    def deserialize(self, content, format="application/json"):
        if format == 'application/x-www-form-urlencoded':
            format = 'text/html'

        return super(HtmlJsonSerializer, self).deserialize(content,
                format=format)
