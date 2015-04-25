from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'recipes.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
     url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/saloni/recipes/allrecipes/images/media/files', 'show_indexes': False}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^recipes/',include('allrecipes.urls')),
   
)
