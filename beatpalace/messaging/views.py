from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from collaborations.models import Collaboration

from .models import Conversation, Message


@login_required
def chat(request, collaboration_id):

    # 1. Get the collaboration first
    collaboration = get_object_or_404(
        Collaboration.objects.select_related(
            "artist",
            "producer",
        ),
        id=collaboration_id,
    )

    # 2. Check that the logged-in user belongs to this collaboration
    if request.user not in [
        collaboration.artist,
        collaboration.producer,
    ]:
        messages.error(
            request,
            "You do not have access to this conversation.",
        )

        return redirect("dashboard")

    # 3. Chat is only available after acceptance
    if collaboration.status != "accepted":

        messages.warning(
            request,
            "This collaboration has not been accepted yet.",
        )

        return redirect(
            "collaborations:workspace",
            collaboration_id=collaboration.id,
        )

    # 4. Get or create conversation
    conversation, created = Conversation.objects.get_or_create(
        collaboration=collaboration
    )

    # 5. Send a new message
    if request.method == "POST":

        text = request.POST.get(
            "message",
            ""
        ).strip()

        audio = request.FILES.get(
            "audio"
        )

        # Make sure something was sent
        if text or audio:

            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                message=text,
                audio=audio,
            )

            conversation.save(
                update_fields=["updated_at"]
            )

        return redirect(
            "messaging:chat",
            collaboration_id=collaboration.id,
        )

    # 6. Mark messages from the other user as read
    conversation.messages.filter(
        is_read=False
    ).exclude(
        sender=request.user
    ).update(
        is_read=True
    )

    # 7. Get all messages
    messages_list = conversation.messages.select_related(
        "sender"
    ).all()

    # 8. Render chat
    return render(
        request,
        "messaging/chat.html",
        {
            "conversation": conversation,
            "collaboration": collaboration,
            "messages": messages_list,
        },
    )