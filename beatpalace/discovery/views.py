from django.db.models import Q
from django.shortcuts import render

from artists.models import ArtistProfile
from producers.models import ProducerProfile


def discover_home(request):

    artists = (
        ArtistProfile.objects
        .select_related("user")
        .filter(user__role="artist")
        .order_by("-created_at")[:6]
    )

    producers = (
        ProducerProfile.objects
        .select_related("user")
        .filter(
            user__role="producer",
            is_published=True
        )
        .order_by("-created_at")[:6]
    )

    context = {
        "artists": artists,
        "producers": producers,
    }

    return render(
        request,
        "discovery/home.html",
        context
    )


def discover_home(request):

    artists = (
        ArtistProfile.objects
        .select_related("user")
        .filter(user__role="artist")
        .order_by("-created_at")[:6]
    )

    producers = (
        ProducerProfile.objects
        .select_related("user")
        .filter(
            user__role="producer",
            is_published=True
        )
        .order_by("-created_at")[:6]
    )

    context = {
        "artists": artists,
        "producers": producers,
    }

    return render(
        request,
        "discovery/home.html",
        context
    )


def discover_artists(request):

    query = request.GET.get("q", "").strip()
    genre = request.GET.get("genre", "").strip()
    location = request.GET.get("location", "").strip()

    artists = (
        ArtistProfile.objects
        .select_related("user")
        .filter(user__role="artist")
    )

    if query:

        artists = artists.filter(
            Q(artist_name__icontains=query) |
            Q(bio__icontains=query) |
            Q(genre__icontains=query) |
            Q(location__icontains=query) |
            Q(user__username__icontains=query)
        )

    if genre:

        artists = artists.filter(
            genre__icontains=genre
        )

    if location:

        artists = artists.filter(
            location__icontains=location
        )

    artists = artists.order_by("-created_at")

    context = {
        "artists": artists,
        "query": query,
        "genre": genre,
        "location": location,
    }

    return render(
        request,
        "discovery/artists.html",
        context
    )

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import render

from engagement.models import Follow


User = get_user_model()


@login_required
def discover_artists(request):

    query = request.GET.get("q", "").strip()
    role = request.GET.get("role", "").strip()
    genre = request.GET.get("genre", "").strip()

    # --------------------------------------------------
    # BASE USERS
    # --------------------------------------------------

    users = (
        User.objects
        .exclude(id=request.user.id)
        .filter(
            role__in=["artist"]
        )
        .select_related(
            "artist_profile",
        )
    )

    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------

    if query:

        users = users.filter(

            Q(username__icontains=query)

            |

            Q(
                artist_profile__artist_name__icontains=query
            )

            |

            Q(
                artist_profile__bio__icontains=query
            )

            |

            Q(
                artist_profile__genre__icontains=query
            )

            |

            Q(
                artist_profile__location__icontains=query
            )

            |

            Q(
                producer_profile__full_name__icontains=query
            )

            |

            Q(
                producer_profile__professional_title__icontains=query
            )

            |

            Q(
                producer_profile__bio__icontains=query
            )

            |

            Q(
                producer_profile__skill_description__icontains=query
            )

            |

            Q(
                producer_profile__software__icontains=query
            )

        )

    # --------------------------------------------------
    # ROLE FILTER
    # --------------------------------------------------

    if role in ["artist"]:

        users = users.filter(
            role=role
        )

    # --------------------------------------------------
    # GENRE FILTER
    # --------------------------------------------------

    if genre:

        users = users.filter(
            artist_profile__genre__icontains=genre
        )

    # --------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------

    users = users.distinct()

    # --------------------------------------------------
    # FOLLOWING
    # --------------------------------------------------

    following_ids = set(
        Follow.objects
        .filter(
            follower=request.user
        )
        .values_list(
            "following_id",
            flat=True
        )
    )

    # --------------------------------------------------
    # CONTEXT
    # --------------------------------------------------

    context = {
        "users": users,
        "query": query,
        "role": role,
        "genre": genre,
        "following_ids": following_ids,
    }

    return render(
        request,
        "discovery/artists.html",
        context
    )


def discover_producers(request):

    query = request.GET.get("q", "").strip()
    role = request.GET.get("role", "").strip()
    genre = request.GET.get("genre", "").strip()

    # --------------------------------------------------
    # BASE USERS
    # --------------------------------------------------

    users = (
        User.objects
        .exclude(id=request.user.id)
        .filter(
            role__in=["producer"]
        )
        .select_related(
            "artist_profile",
        )
    )

    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------

    if query:

        users = users.filter(

            Q(username__icontains=query)

            |

            Q(
                artist_profile__artist_name__icontains=query
            )

            |

            Q(
                artist_profile__bio__icontains=query
            )

            |

            Q(
                artist_profile__genre__icontains=query
            )

            |

            Q(
                artist_profile__location__icontains=query
            )

            |

            Q(
                producer_profile__full_name__icontains=query
            )

            |

            Q(
                producer_profile__professional_title__icontains=query
            )

            |

            Q(
                producer_profile__bio__icontains=query
            )

            |

            Q(
                producer_profile__skill_description__icontains=query
            )

            |

            Q(
                producer_profile__software__icontains=query
            )

        )

    # --------------------------------------------------
    # ROLE FILTER
    # --------------------------------------------------

    if role in ["producer"]:

        users = users.filter(
            role=role
        )

    # --------------------------------------------------
    # GENRE FILTER
    # --------------------------------------------------

    if genre:

        users = users.filter(
            artist_profile__genre__icontains=genre
        )

    # --------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------

    users = users.distinct()

    # --------------------------------------------------
    # FOLLOWING
    # --------------------------------------------------

    following_ids = set(
        Follow.objects
        .filter(
            follower=request.user
        )
        .values_list(
            "following_id",
            flat=True
        )
    )

    # --------------------------------------------------
    # CONTEXT
    # --------------------------------------------------

    context = {
        "users": users,
        "query": query,
        "role": role,
        "genre": genre,
        "following_ids": following_ids,
    }

    return render(
        request,
        "discovery/producers.html",
        context
    )
