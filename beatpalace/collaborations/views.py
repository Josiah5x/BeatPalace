from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import User
from .forms import CollaborationRequestForm
from .models import Collaboration
from messaging.models import Conversation




@login_required
def collaboration_dashboard(request):

    received_requests = Collaboration.objects.filter(
        receiver=request.user
    ).select_related(
        "sender",
        "receiver",
    )

    sent_requests = Collaboration.objects.filter(
        sender=request.user
    ).select_related(
        "sender",
        "receiver",
    )

    active_collaborations = Collaboration.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user),
        status__in=[
            "accepted",
            "in_progress",
        ]
    ).select_related(
        "sender",
        "receiver",
    )

    completed_collaborations = Collaboration.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user),
        status="completed",
    ).select_related(
        "sender",
        "receiver",
    )

    context = {
        "received_requests": received_requests,
        "sent_requests": sent_requests,
        "active_collaborations": active_collaborations,
        "completed_collaborations": completed_collaborations,
    }

    return render(
        request,
        "collaborations/dashboard.html",
        context
    )


@login_required
def send_collaboration(request, username):

    recipient = get_object_or_404(
        User,
        username=username
    )

    # -----------------------------------------
    # CANNOT COLLABORATE WITH YOURSELF
    # -----------------------------------------

    if recipient == request.user:

        messages.error(
            request,
            "You cannot send a collaboration request to yourself."
        )

        return redirect("dashboard")


    # -----------------------------------------
    # ONLY ARTIST CAN SEND FOR NOW
    # -----------------------------------------

    if request.user.role != "artist":

        messages.error(
            request,
            "Only artists can send collaboration requests."
        )

        return redirect("dashboard")


    # -----------------------------------------
    # RECIPIENT MUST BE PRODUCER
    # -----------------------------------------

    if recipient.role != "producer":

        messages.error(
            request,
            "Collaboration requests can only be sent to producers."
        )

        return redirect(
            "dashboard:discover"
        )


    # -----------------------------------------
    # CHECK EXISTING PENDING REQUEST
    # -----------------------------------------

    existing = Collaboration.objects.filter(
        artist=request.user,
        producer=recipient,
        status="pending"
    ).first()


    if existing:

        messages.warning(
            request,
            "You already have a pending collaboration request."
        )

        return redirect(
            "producers:public_producer_profile",
            username=recipient.username
        )


    # -----------------------------------------
    # FORM
    # -----------------------------------------

    if request.method == "POST":

        form = CollaborationRequestForm(
            request.POST
        )

        if form.is_valid():

            collaboration = form.save(
                commit=False
            )

            collaboration.artist = request.user

            collaboration.producer = recipient

            collaboration.status = "pending"

            collaboration.save()


            messages.success(
                request,
                "Collaboration request sent successfully."
            )


            return redirect(
                "producers:public_producer_profile",
                username=recipient.username
            )

    else:

        form = CollaborationRequestForm()


    return render(
        request,
        "collaborations/send_request.html",
        {
            "form": form,
            "producer": recipient,
        }
    )


@login_required
def collaboration_requests(request):

    # Producer receives requests
    if request.user.role == "producer":

        requests = Collaboration.objects.filter(
            producer=request.user
        ).select_related(
            "artist",
            "producer",
        )

    # Artist sees requests they sent
    elif request.user.role == "artist":

        requests = Collaboration.objects.filter(
            artist=request.user
        ).select_related(
            "artist",
            "producer",
        )

    else:

        requests = Collaboration.objects.none()
    

    return render(
        request,
        "collaborations/requests.html",
        {
            "requests": requests,
        }
    )


@login_required
def accept_collaboration(request, pk):

    collaboration = get_object_or_404(
        Collaboration,
        pk=pk,
        producer=request.user,
        status="pending",
    )

    if request.method == "POST":

        # collaboration.status = "accepted"
        # collaboration.save(
        #     update_fields=[
        #         "status",
        #         "updated_at",
        #     ]
        # )

        if action == "accept":

            collaboration.status = "accepted"
            collaboration.save()

            Conversation.objects.get_or_create(
                collaboration=collaboration
            )

  
        messages.success(
            request,
            "Collaboration request accepted."
        )

    return redirect(
        "collaborations:requests"
    )


@login_required
def reject_collaboration(request, pk):

    collaboration = get_object_or_404(
        Collaboration,
        pk=pk,
        producer=request.user,
        status="pending",
    )

    if request.method == "POST":

        collaboration.status = "rejected"
        collaboration.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        messages.info(
            request,
            "Collaboration request rejected."
        )

    return redirect(
        "collaborations:requests"
    )


@login_required
def cancel_collaboration(request, pk):

    collaboration = get_object_or_404(
        Collaboration,
        pk=pk,
        artist=request.user,
        status="pending",
    )

    if request.method == "POST":

        collaboration.status = "cancelled"
        collaboration.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        messages.info(
            request,
            "Collaboration request cancelled."
        )

    return redirect(
        "collaborations:requests"
    )


@login_required
def collaboration_workspace(request, collaboration_id):

    collaboration = get_object_or_404(
        Collaboration.objects.select_related(
            "artist",
            "producer",
            "artist__artist_profile",
            "producer__producer_profile",
        ),
        id=collaboration_id,
    )

    # Only the two participants can access
    # the workspace.
    if request.user not in [
        collaboration.artist,
        collaboration.producer,
    ]:

        messages.error(
            request,
            "You do not have access to this collaboration."
        )

        return redirect("dashboard")

    return render(
        request,
        "collaborations/workspace.html",
        {
            "collaboration": collaboration,
        }
    )