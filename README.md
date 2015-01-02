### Django Tastypie Html (v 0.1) ###
----------------

This app implements a HTML/JSON serializer to be used with [django-tastypie](https://github.com/toastdriven/django-tastypie) resources. Using the `HtmlJsonSerializer` class, a single resource class
would serve both `HTML` and `JSON` response based on requested format.

----------------

### Installation ###

Currently DTH does not have a pip package. So to install the app you'd need to clone the repo and add it to your python path

```
git clone https://github.com/amyth/django-tastypie-html.git
export PYTHONPATH=$PYTHONPATH:/path/to/repo
```
----------------

### Usage ###

Once installed you can use the app as follows:

1). Add the `tastypie_html` to your django project's `INSTALLED_APPS`.

2). Add the `HtmlJsonSerializer` to the resource you would like to use it with. Make sure you pass the template_name as the first argument while initializing the serializer class.

```
    #api.py
    
    from tastypie.resource import resources
    from tastypie_html.serializers import HtmlJsonSerializer
    
    
    class TestResource(resources.ModelResource):
        class Meta:
            serializer = HtmlJsonSerialier('example.html') # pass the template
```

3). Also make sure that you use the `TastyHtmlMixin` with the resource for `HTML` rendering to properly work.

```
    #api.py
    
    from tastypie.resource import resources
    from tastypie_html.mixins import TastyHtmlMixin
    from tastypie_html.serializers import HtmlJsonSerializer
    
    
    class TestResource(resources.ModelResource, TastyHtmlMixin):
        class Meta(TastyHtmlMixin.Meta):
            serializer = HtmlJsonSerialier('example.html')
```
----------------

### Settings ###


#####`TASTYPIE_HTML_DEFAULT_FORMAT` ####

options are `json` and `html`. Default is `html`

----------------

### contributors ###

[Amyth Arora](https://plus.google.com/+AmythArora)
