from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from accounts.models import User
from .models import Follow


@login_required
def toggle_follow(request, user_id):

    if request.method != "POST":
        return redirect("artists:artist_discover")

    target_user = get_object_or_404(
        User,
        id=user_id
    )

    # Cannot follow yourself
    if target_user == request.user:
        return redirect(
            request.META.get(
                "HTTP_REFERER",
                "/"
            )
        )

    follow = Follow.objects.filter(
        follower=request.user,
        following=target_user
    ).first()

    if follow:

        # UNFOLLOW
        follow.delete()

    else:

        # FOLLOW
        Follow.objects.create(
            follower=request.user,
            following=target_user
        )

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "/"
        )
    )