from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from collaborations.models import Collaboration

from .models import Conversation, Message


@login_required
def chat(request, collaboration_id):

    # 1. Get the collaboration
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

    # ==========================================================
    # 5. SEND MESSAGE
    # ==========================================================

    if request.method == "POST":

        text = request.POST.get(
            "message",
            ""
        ).strip()

        # New uploaded audio file
        audio = request.FILES.get(
            "audio"
        )

        # Existing audio message selected from dropdown
        audio_message_id = request.POST.get(
            "audio_message_id"
        )

        # Trimmer values
        audio_start_raw = request.POST.get(
            "audio_start"
        )

        audio_end_raw = request.POST.get(
            "audio_end"
        )

        # ------------------------------------------------------
        # Convert trim values
        # ------------------------------------------------------

        audio_start = 0
        audio_end = None

        try:

            if audio_start_raw:
                audio_start = float(
                    audio_start_raw
                )

            if audio_end_raw:
                audio_end = float(
                    audio_end_raw
                )

        except (
            TypeError,
            ValueError,
        ):

            audio_start = 0
            audio_end = None

        # ------------------------------------------------------
        # Determine which audio should be saved
        # ------------------------------------------------------

        audio_to_save = None

        # ======================================================
        # OPTION 1
        # Existing audio selected from chat
        # ======================================================

        if audio_message_id:

            source_audio_message = get_object_or_404(
                Message,
                id=audio_message_id,
                conversation=conversation,
            )

            if source_audio_message.audio:

                # Reuse the existing FileField file.
                #
                # IMPORTANT:
                # We save the existing storage NAME,
                # not the URL.
                #
                # This means Django continues to support:
                #
                # {{ message.audio.url }}
                #
                audio_to_save = (
                    source_audio_message.audio.name
                )

        # ======================================================
        # OPTION 2
        # New audio uploaded from computer
        # ======================================================

        elif audio:

            audio_to_save = audio

        # ======================================================
        # 6. Create message
        # ======================================================

        if text or audio_to_save:

            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                message=text,
                audio=audio_to_save,
                audio_start=audio_start,
                audio_end=audio_end,
            )

            conversation.save(
                update_fields=[
                    "updated_at"
                ]
            )

        return redirect(
            "messaging:chat",
            collaboration_id=collaboration.id,
        )

    # ==========================================================
    # 7. Mark messages from the other user as read
    # ==========================================================

    conversation.messages.filter(
        is_read=False
    ).exclude(
        sender=request.user
    ).update(
        is_read=True
    )

    # ==========================================================
    # 8. Get all messages
    # ==========================================================

    messages_list = (
        conversation.messages
        .select_related("sender")
        .all()
    )

    # ==========================================================
    # 9. Get uploaded audio messages
    #
    # These are used by the audio dropdown/trimmer.
    # ==========================================================

    audio_messages = (
        conversation.messages
        .filter(
            audio__isnull=False
        )
        .exclude(
            audio=""
        )
        .select_related("sender")
    )

    # ==========================================================
    # 10. Render chat
    # ==========================================================

    return render(
        request,
        "messaging/chat.html",
        {
            "conversation": conversation,
            "collaboration": collaboration,
            "messages": messages_list,
            "audio_messages": audio_messages,
        },
    )