from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from .models import Collaboration


User = get_user_model()


@login_required
def send_collaboration(request, username):

    # Person receiving the collaboration request
    receiver = get_object_or_404(
        User,
        username=username,
    )

    # Prevent sending to yourself
    if receiver == request.user:

        messages.error(
            request,
            "You cannot send a collaboration request to yourself."
        )

        return redirect(
            request.META.get("HTTP_REFERER", "/")
        )

    if request.method == "POST":

        message = request.POST.get(
            "message",
            ""
        ).strip()

        # Determine artist/producer
        sender = request.user

        if sender.role == "artist" and receiver.role == "producer":

            artist = sender
            producer = receiver

        elif sender.role == "producer" and receiver.role == "artist":

            artist = receiver
            producer = sender

        else:

            messages.error(
                request,
                "Collaboration is only available between artists and producers."
            )

            return redirect(
                request.META.get("HTTP_REFERER", "/")
            )

        # Prevent duplicate pending requests
        existing = Collaboration.objects.filter(
            artist=artist,
            producer=producer,
            status="pending",
        ).first()

        if existing:

            messages.warning(
                request,
                "You already have a pending collaboration request."
            )

            return redirect(
                request.META.get("HTTP_REFERER", "/")
            )

        Collaboration.objects.create(
            artist=artist,
            producer=producer,
            message=message,
            status="pending",
        )

        messages.success(
            request,
            f"Collaboration request sent to {receiver.username}."
        )

        return redirect(
            request.META.get("HTTP_REFERER", "/")
        )

    return redirect(
        request.META.get("HTTP_REFERER", "/")
    )