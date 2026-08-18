from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import User
from .forms import ProducerProfileForm


@login_required
def producer_dashboard(request):

    return render(
        request,
        "producers/dashboard.html"
    )

@login_required
def producer_profile(request, username):

    user = get_object_or_404(
        User,
        username=username,
        role="producer"
    )

    profile = user.producer_profile

    is_following = user.followers.filter(
        follower=request.user
    ).exists()

    return render(
        request,
        "producers/profile.html",
        {
            "profile_user": user,
            "profile": profile,
            "is_following": is_following,
        }
    )


@login_required
def edit_profile(request):

    profile = request.user.producer_profile

    if request.method == "POST":

        form = ProducerProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            return redirect(
                "producer_profile",
                username=request.user.username
            )

    else:

        form = ProducerProfileForm(
            instance=profile
        )

    return render(
        request,
        "producers/edit_profile.html",
        {
            "form": form
        }
    )