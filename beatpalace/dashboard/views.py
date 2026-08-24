from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db.models import Q

from accounts.models import User
from engagement.models import Follow


@login_required
def dashboard(request):

    if request.user.role == "producer":

        return redirect(
            "producer_dashboard"
        )

    if request.user.role == "artist":

        return redirect(
            "artist_dashboard"
        )

    return render(
        request,
        "dashboard/dashboard.html"
    )


@login_required
def producer_dashboard(request):

    return render(
        request,
        "dashboard/producer.html"
    )


@login_required
def artist_dashboard(request):

    return render(
        request,
        "dashboard/artist.html"
    )






@login_required
def discover(request):

    query = request.GET.get("q", "").strip()
    role = request.GET.get("role", "").strip()
    genre = request.GET.get("genre", "").strip()

    users = User.objects.exclude(
        id=request.user.id
    ).filter(
        role__in=["artist", "producer"]
    )

    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------

    if query:

        users = users.filter(
            Q(username__icontains=query)
            |
            Q(artist_profile__artist_name__icontains=query)
            |
            Q(artist_profile__bio__icontains=query)
            |
            Q(artist_profile__genre__icontains=query)
            |
            Q(producer_profile__full_name__icontains=query)
            |
            Q(producer_profile__professional_title__icontains=query)
            |
            Q(producer_profile__bio__icontains=query)
        )

    # --------------------------------------------------
    # ROLE FILTER
    # --------------------------------------------------

    if role in ["artist", "producer"]:
        users = users.filter(role=role)

    # --------------------------------------------------
    # GENRE
    # --------------------------------------------------

    if genre:

        users = users.filter(
            Q(artist_profile__genre__icontains=genre)
        )

    users = users.select_related(
        "artist_profile",
        "producer_profile",
    ).distinct()

    #------------------------------------
    Follow
    #------------------------------------

    following_ids = set(
    Follow.objects.filter(
        follower=request.user
    ).values_list(
        "following_id",
        flat=True
    )
    )
    return render(
        request,
        "dashboard/discover.html",
        {
            "users": users,
            "query": query,
            "role": role,
            "genre": genre,
            "following_ids": following_ids,
        }
    )