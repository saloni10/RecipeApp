from django.conf.urls import patterns, include, url
from django.conf import settings
from allrecipes import views
import allrecipes
urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/saloni/forum/QAforum/media/', 'show_indexes': False}),
    url(r'^index/', views.index,name='index' ),
    url(r'^about/', views.about,name='about' ),
    url(r'^contact_us/', views.contact,name='contact' ),
    url(r'^tips/', views.tips,name='tips' ),
    url(r'^search/', views.search,name='search_recipe' ),
    url(r'^register/', views.register,name='registration' ),
    url(r'^submission/', views.submit,name='submit-form' ),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^changepwd/$', views.changepwd, name='changepwdform'),
    url(r'^changepassword/$', views.changepassword),
    url(r'^password_reset/$', views.cust_password_reset),
    url(r'^password_reset/done/$', views.cust_password_reset_done),
    url(r'^reset/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$', views.cust_password_reset_confirm),
    url(r'^reset/done/$', views.cust_password_reset_complete),
    url(r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.PasswordResetConfirmView.as_view(),name='reset_password_confirm'), 
    # PS: url above is going to used for next section of implementation.
    url(r'^reset_password/$', allrecipes.views.ResetPasswordRequestView.as_view(),name="reset_password"),  
    
)

