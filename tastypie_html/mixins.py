#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#
#    Django Tastypie Html v 0.1
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

from django.conf import settings
from django.http import HttpResponse

from tastypie import resources
from tastypie.utils.mime import build_content_type


class TastyHtmlMixin(resources.Resource):
    """
    A mixin that overrides default tastypie resource class methods
    to implement methods that help in serialization/deserialization
    of HTML data
    """

    class Meta:
        default_format = getattr(settings, 'TASTYPIE_HTML_DEFAULT_FORMAT', 'html')
        response_options = {}

    def determine_format(self, request, *args, **kwargs):
        """
        Overrides the determine format method to make sure the
        the default format for a request is set either to JSON
        or HTML
        """

        default_format = getattr(self.Meta, 'default_format', 'html')
        content_types = {
            'json': 'application/json',
            'html': 'text/html',
        }

        _format = request.GET.get('format', default_format)
        if _format not in ['json', 'html']:
            _format = default_format

        return content_types.get(_format)

    def serialize(self, request, data, format, options=None):
        """
        Overrides the serialize method to pass in the request
        object to the serializer class' serialize() method as
        it is required for rendering templates.
        """

        options = options or {}

        if 'text/javascript' in format:
            # get JSONP callback name. default to "callback"
            callback = request.GET.get('callback', 'callback')

            if not is_valid_jsonp_callback_value(callback):
                raise BadRequest('JSONP callback name is invalid.')

            options['callback'] = callback

        return self._meta.serializer.serialize(request, data, format, options)

    def create_response(self, request, data, response_class=HttpResponse,
            **response_kwargs):
        """
        Overrides the create_response method to pass in the request
        object to the resource class' serialize() method so it could
        be passed to the serializer class.
        """

        desired_format = self.determine_format(request)
        serialized = self.serialize(request, data,
                desired_format, self.Meta.response_options)
        return response_class(content=serialized,
                content_type=build_content_type(
                    desired_format), **response_kwargs)
