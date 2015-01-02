from tastypie import resources
from tastypie_html.mixins import TastyHtmlMixin


class WrapBaseResource(resources.Resource):
    class Meta:
        pass


class BaseResource(WrapBaseResource, TastyHtmlMixin):
    class Meta(TastyHtmlMixin.Meta):
        pass


class BaseModelResource(resources.ModelResource, TastyHtmlMixin):
    class Meta(TastyHtmlMixin.Meta):
        pass
