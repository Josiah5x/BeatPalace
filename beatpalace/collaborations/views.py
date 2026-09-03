from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import User
from .forms import CollaborationRequestForm
from .models import Collaboration
from messaging.models import Conversation
from django.db.models import Q




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
def respond_collaboration(request, collaboration_id, action):

    collaboration = get_object_or_404(
        Collaboration,
        id=collaboration_id
    )

    # Only the producer who received
    # the request can respond
    if collaboration.producer != request.user:

        messages.error(
            request,
            "You are not allowed to manage this request."
        )

        return redirect(
            "collaborations:requests"
        )

    if request.method != "POST":

        return redirect(
            "collaborations:requests"
        )

    if collaboration.status != "pending":

        messages.warning(
            request,
            "This request has already been processed."
        )

        return redirect(
            "collaborations:requests"
        )

    if action == "accept":

        collaboration.status = "accepted"

        collaboration.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        messages.success(
            request,
            "Collaboration request accepted."
        )

    elif action == "reject":

        collaboration.status = "rejected"

        collaboration.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        messages.success(
            request,
            "Collaboration request rejected."
        )

    else:

        messages.error(
            request,
            "Invalid action."
        )

    return redirect(
        "collaborations:requests"
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


#################################################


@login_required
def collaboration_workspace(request, collaboration_id):

    collaboration = get_object_or_404(
        Collaboration.objects.select_related(
            "artist",
            "producer",
        ),
        id=collaboration_id,
    )

    # Only the artist or producer involved can access it
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
        },
    )

@login_required
def update_collaboration_status(
    request,
    collaboration_id,
    status,
):

    collaboration = get_object_or_404(
        Collaboration.objects.select_related(
            "artist",
            "producer",
        ),
        id=collaboration_id,
    )

    # Only the producer can respond
    if request.user != collaboration.producer:
        messages.error(
            request,
            "Only the producer can respond to this request."
        )
        return redirect("dashboard")

    if request.method != "POST":
        return redirect(
            "collaborations:workspace",
            collaboration_id=collaboration.id,
        )

    if collaboration.status != "pending":
        messages.warning(
            request,
            "This collaboration request has already been processed."
        )
        return redirect(
            "collaborations:workspace",
            collaboration_id=collaboration.id,
        )

    if status not in ["accepted", "rejected"]:
        messages.error(
            request,
            "Invalid collaboration status."
        )
        return redirect(
            "collaborations:workspace",
            collaboration_id=collaboration.id,
        )

    collaboration.status = status
    collaboration.save(update_fields=["status"])

    if status == "accepted":
        messages.success(
            request,
            "Collaboration request accepted."
        )
    else:
        messages.info(
            request,
            "Collaboration request rejected."
        )

    return redirect(
        "collaborations:workspace",
        collaboration_id=collaboration.id,
    )