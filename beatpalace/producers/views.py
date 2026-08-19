from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import User
from .forms import ProducerProfileForm


@login_required
def producer_profile(request, username):

    user = get_object_or_404(
        User,
        username=username,
        role="producer"
    )

    profile = user.producer_profile

    is_following = user.followers.filter(
        follower=request.user
    ).exists()

    return render(
        request,
        "producers/profile.html",
        {
            "profile_user": user,
            "profile": profile,
            "is_following": is_following,
        }
    )


@login_required
def edit_profile(request):

    profile = request.user.producer_profile

    if request.method == "POST":

        form = ProducerProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            return redirect(
                "producer_profile",
                username=request.user.username
            )

    else:

        form = ProducerProfileForm(
            instance=profile
        )

    return render(
        request,
        "producers/edit_profile.html",
        {
            "form": form
        }
    )

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import (
    ProducerProfile,
    ProducerProject,
    ProducerSkill,
)

from .forms import (
    ProducerProfileForm,
    ProducerProjectForm,
    ProducerSkillForm,
)


# ==========================================================
# PRODUCER PROFILE / CV
# ==========================================================

@login_required
def producer_profile(request):

    profile, created = ProducerProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "full_name": request.user.get_full_name()
            or request.user.username
        }
    )

    projects = profile.projects.filter(
        is_visible=True
    )

    skills = profile.skills.all()

    return render(
        request,
        "producers/profile.html",
        {
            "profile": profile,
            "projects": projects,
            "skills": skills,
        }
    )


# ==========================================================
# EDIT PRODUCER PROFILE
# ==========================================================

@login_required
def producer_edit_profile(request):

    profile, created = ProducerProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "full_name": request.user.get_full_name()
            or request.user.username
        }
    )

    if request.method == "POST":

        form = ProducerProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            profile = form.save(commit=False)

            profile.user = request.user

            profile.save()

            messages.success(
                request,
                "Your producer profile has been updated successfully."
            )

            return redirect("producer_profile")

    else:

        form = ProducerProfileForm(
            instance=profile
        )

    return render(
        request,
        "producers/edit_profile.html",
        {
            "form": form,
            "profile": profile,
        }
    )


# ==========================================================
# ADD PROJECT
# ==========================================================

@login_required
def producer_add_project(request):

    profile = get_object_or_404(
        ProducerProfile,
        user=request.user
    )

    if request.method == "POST":

        form = ProducerProjectForm(
            request.POST
        )

        if form.is_valid():

            project = form.save(
                commit=False
            )

            project.producer = profile

            project.save()

            messages.success(
                request,
                "Project added successfully."
            )

            return redirect(
                "producer_edit_profile"
            )

    else:

        form = ProducerProjectForm()

    return render(
        request,
        "producers/add_project.html",
        {
            "form": form,
            "profile": profile,
        }
    )


# ==========================================================
# DELETE PROJECT
# ==========================================================

@login_required
def producer_delete_project(
    request,
    project_id
):

    profile = get_object_or_404(
        ProducerProfile,
        user=request.user
    )

    project = get_object_or_404(
        ProducerProject,
        id=project_id,
        producer=profile
    )

    if request.method == "POST":

        project.delete()

        messages.success(
            request,
            "Project deleted successfully."
        )

    return redirect(
        "producer_edit_profile"
    )


# ==========================================================
# ADD SKILL
# ==========================================================

@login_required
def producer_add_skill(request):

    profile = get_object_or_404(
        ProducerProfile,
        user=request.user
    )

    if request.method == "POST":

        form = ProducerSkillForm(
            request.POST
        )

        if form.is_valid():

            skill = form.save(
                commit=False
            )

            skill.producer = profile

            skill.save()

            messages.success(
                request,
                "Skill added successfully."
            )

            return redirect(
                "producer_edit_profile"
            )

    else:

        form = ProducerSkillForm()

    return render(
        request,
        "producers/add_skill.html",
        {
            "form": form,
            "profile": profile,
        }
    )


# ==========================================================
# DELETE SKILL
# ==========================================================

@login_required
def producer_delete_skill(
    request,
    skill_id
):

    profile = get_object_or_404(
        ProducerProfile,
        user=request.user
    )

    skill = get_object_or_404(
        ProducerSkill,
        id=skill_id,
        producer=profile
    )

    if request.method == "POST":

        skill.delete()

        messages.success(
            request,
            "Skill deleted successfully."
        )

    return redirect(
        "producer_edit_profile"
    )