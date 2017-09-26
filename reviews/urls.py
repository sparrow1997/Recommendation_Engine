from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /
    url(r'^$', views.review_list, name='review_list'),
    # ex: /review/5/
    url(r'^review/(?P<review_id>[0-9]+)/$', views.review_detail, name='review_detail'),
    # ex: /cafe/
    url(r'^cafe$', views.cafe_list, name='cafe_list'),
    # ex: /cafe/5/
    url(r'^cafe/(?P<cafe_id>[0-9]+)/$', views.cafe_detail, name='cafe_detail'),
    url(r'^cafe/(?P<cafe_id>[0-9]+)/add_review/$', views.add_review, name='add_review'),
    # ex: /review/user - get reviews for the logged user
    url(r'^review/user/(?P<username>\w+)/$', views.user_review_list, name='user_review_list'),
    # ex: /review/user - get reviews for the user passed in the url
    url(r'^review/user/$', views.user_review_list, name='user_review_list'),
    # ex: /recommendation - get cafe recommendations for the logged user
    url(r'^recommendation/$', views.user_recommendation_list, name='user_recommendation_list'),
]