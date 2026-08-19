from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from accounts.models import User

from .models import Follow


@login_required
def toggle_follow(request, user_id):

    target_user = get_object_or_404(
        User,
        id=user_id
    )

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
        follow.delete()

    else:
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