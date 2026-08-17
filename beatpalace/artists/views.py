from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import User
from .forms import ArtistProfileForm


@login_required
def artist_profile(request, username):

    user = get_object_or_404(
        User,
        username=username,
        role="artist"
    )

    profile = user.artist_profile

    is_following = user.followers.filter(
        follower=request.user
    ).exists()

    return render(
        request,
        "artists/profile.html",
        {
            "profile_user": user,
            "profile": profile,
            "is_following": is_following,
        }
    )


@login_required
def edit_profile(request):

    profile = request.user.artist_profile

    if request.method == "POST":

        form = ArtistProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            return redirect(
                "artist_profile",
                username=request.user.username
            )

    else:

        form = ArtistProfileForm(
            instance=profile
        )

    return render(
        request,
        "artists/edit_profile.html",
        {
            "form": form
        }
    )