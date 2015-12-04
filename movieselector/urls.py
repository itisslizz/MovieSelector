from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from movieselector import views

urlpatterns = [
    url(r'^selections/(?P<selection_id>[0-9]+)/movies/$', views.MovieInSelectionList.as_view()),
    url(r'^selections/(?P<selection_id>[0-9]+)/movies/(?P<pk>[0-9]+)/$', views.MovieInSelectionDetail.as_view()),
    url(r'^selections/$', views.SelectionList.as_view()),
    url(r'^selections/(?P<pk>[0-9]+)/$', views.SelectionDetail.as_view()),
    url(r'^selections/(?P<selection_id>[0-9]+)/users/$', views.UserInSelectionList.as_view()),
    url(r'^selections/(?P<selection_id>[0-9]+)/users/(?P<pk>[0-9]+)/$', views.UserInSelectionDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^selections/(?P<selection_id>[0-9]+)/rounds/(?P<voting_round>[0-9]+)/votes/$', views.VoteList.as_view()),
    url(r'^selections/(?P<selection_id>[0-9]+)/rounds/(?P<voting_round>[0-9]+)/votes/(?P<pk>[0-9]+)/$', views.VoteDetail.as_view()),
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                                namespace='rest_framework'))
]

urlpatterns = format_suffix_patterns(urlpatterns)
