from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from collaborations.models import Collaboration
from .models import Conversation, Message


@login_required
def chat(request, collaboration_id):

    collaboration = get_object_or_404(
        Collaboration.objects.select_related(
            "artist",
            "producer",
        ),
        id=collaboration_id,
    )

    # Only the artist and producer involved
    # in this collaboration can access the chat.
    if request.user not in [
        collaboration.artist,
        collaboration.producer,
    ]:
        messages.error(
            request,
            "You do not have access to this conversation."
        )

        return redirect("dashboard")

    # Chat is only available after acceptance.
    if collaboration.status != "accepted":
        messages.warning(
            request,
            "This collaboration has not been accepted yet."
        )

        return redirect(
            "collaborations:workspace",
            collaboration_id=collaboration.id,
        )

    conversation, created = Conversation.objects.get_or_create(
        collaboration=collaboration
    )

    if request.method == "POST":

        text = request.POST.get("message", "").strip()

        if text:

            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                message=text,
            )

            conversation.save(
                update_fields=["updated_at"]
            )

        return redirect(
            "messaging:chat",
            collaboration_id=collaboration.id,
        )

    # Mark messages sent by the other person as read.
    conversation.messages.filter(
        is_read=False
    ).exclude(
        sender=request.user
    ).update(
        is_read=True
    )

    return render(
        request,
        "messaging/chat.html",
        {
            "conversation": conversation,
            "collaboration": collaboration,
        },
    )
