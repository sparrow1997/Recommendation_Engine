from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .models import Review, Cafe, Cluster
from .forms import ReviewForm
from .suggestions import update_clusters

import datetime

from django.contrib.auth.decorators import login_required

def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list':latest_review_list}
    return render(request, 'reviews/review_list.html', context)


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/review_detail.html', {'review': review})


def cafe_list(request):
    cafe_list = Cafe.objects.order_by('-name')
    context = {'cafe_list':cafe_list}
    return render(request, 'reviews/cafe_list.html', context)


def cafe_detail(request, cafe_id):
    cafe = get_object_or_404(Cafe, pk=cafe_id)
    form = ReviewForm()
    return render(request, 'reviews/cafe_detail.html', {'cafe': cafe, 'form': form})

@login_required
def add_review(request, cafe_id):
    cafe = get_object_or_404(Cafe, pk=cafe_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = request.user.username
        review = Review()
        review.cafe = cafe
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        update_clusters()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('reviews:cafe_detail', args=(cafe.id,)))
    
    return render(request, 'reviews/cafe_detail.html', {'cafe': cafe, 'form': form})
    

def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user_name=username).order_by('-pub_date')
    context = {'latest_review_list':latest_review_list, 'username':username}
    return render(request, 'reviews/user_review_list.html', context)


@login_required
def user_recommendation_list(request):
    
    # get request user reviewed cafes
    user_reviews = Review.objects.filter(user_name=request.user.username).prefetch_related('cafe')
    user_reviews_cafe_ids = set(map(lambda x: x.cafe.id, user_reviews))

    # get request user cluster name (just the first one righ now)
    try:
        user_cluster_name =   User.objects.get(username=request.user.username).cluster_set.first().name
    except: # if no cluster assigned for a user, update clusters
        update_clusters()
        user_cluster_name =  User.objects.get(username=request.user.username).cluster_set.first().name
    
    # get usernames for other memebers of the cluster
    user_cluster_other_members = \
        Cluster.objects.get(name=user_cluster_name).users \
            .exclude(username=request.user.username).all()
    other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

    # get reviews by those users, excluding cafes reviewed by the request user
    other_users_reviews = \
        Review.objects.filter(user_name__in=other_members_usernames) \
            .exclude(cafe__id__in=user_reviews_cafe_ids)
    other_users_reviews_cafe_ids = set(map(lambda x: x.cafe.id, other_users_reviews))
    
    # then get a cafe list including the previous IDs, order by rating
    cafe_list = sorted(
        list(Cafe.objects.filter(id__in=other_users_reviews_cafe_ids)), 
        key=lambda x: x.average_rating, 
        reverse=True
    )

    return render(
        request, 
        'reviews/user_recommendation_list.html', 
        {'username': request.user.username,'cafe_list': cafe_list}
    )

