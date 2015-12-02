from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from movieselector import views

urlpatterns = [
    url(r'^movies/$', views.MovieList.as_view()),
    url(r'^movies/(?P<pk>[0-9]+)/$', views.MovieDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^selections/$', views.SelectionList.as_view()),
    url(r'^selections/(?P<pk>[0-9]+)/$', views.SelectionDetail.as_view()),
    url(r'^rounds/$', views.RoundList.as_view()),
    url(r'^rounds/(?P<pk>[0-9]+)/$', views.RoundDetail.as_view()),
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                                namespace='rest_framework'))
]

urlpatterns = format_suffix_patterns(urlpatterns)
