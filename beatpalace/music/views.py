from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import MusicUploadForm, Music


@login_required
def my_music(request):

    music = Music.objects.filter(
        owner=request.user
    )

    return render(
        request,
        "music/my_music.html",
        {
            "music": music
        }
    )

@login_required
def upload_music(request):

    if request.method == "POST":

        form = MusicUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            music = form.save(commit=False)

            music.owner = request.user

            music.save()

            return redirect(
                "my_music"
            )

    else:

        form = MusicUploadForm()

    return render(
        request,
        "music/upload.html",
        {
            "form": form
        }
    )