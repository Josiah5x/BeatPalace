from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db.models import Q

from accounts.models import User


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
    role = request.GET.get("role", "")
    genre = request.GET.get("genre", "").strip()

    users = User.objects.exclude(
        id=request.user.id
    ).filter(
        is_active=True
    )

    # Search
    if query:

        users = users.filter(
            Q(username__icontains=query)
            | Q(
                artist_profile__artist_name__icontains=query
            )
            | Q(
                producer_profile__stage_name__icontains=query
            )
        )

    # Role filter
    if role in ["artist", "producer"]:

        users = users.filter(
            role=role
        )

    # Genre filter
    if genre:

        users = users.filter(
            Q(
                artist_profile__genre__icontains=genre
            )
            |
            Q(
                producer_profile__genre__icontains=genre
            )
        )

    users = users.distinct()

    artists = users.filter(
        role="artist"
    )

    producers = users.filter(
        role="producer"
    )

    return render(
        request,
        "dashboard/discover.html",
        {
            "users": users,
            "artists": artists,
            "producers": producers,
            "query": query,
            "role": role,
            "genre": genre,
        }
    )