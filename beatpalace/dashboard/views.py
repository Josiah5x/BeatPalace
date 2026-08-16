from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
def dashboard(request):

    if request.user.role == "producer":

        return redirect(
            "producer_dashboard"
        )

    if request.user.role == "artist":

        return redirect(
            "artist_dashboard"
        )

    return render(
        request,
        "dashboard/dashboard.html"
    )


@login_required
def producer_dashboard(request):

    return render(
        request,
        "dashboard/producer.html"
    )


@login_required
def artist_dashboard(request):

    return render(
        request,
        "dashboard/artist.html"
    )