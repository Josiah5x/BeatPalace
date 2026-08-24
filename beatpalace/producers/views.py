

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import User
from engagement.models import Follow

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
# PUBLIC PRODUCER PROFILE
# ==========================================================

@login_required
def public_producer_profile(request, username):

    # Find the producer from the URL
    user = get_object_or_404(
        User,
        username=username,
        role="producer",
    )

    # Find that producer's profile
    profile = get_object_or_404(
        ProducerProfile,
        user=user,
    )

    # Visible projects
    projects = profile.projects.filter(
        is_visible=True
    )

    # Producer skills
    skills = profile.skills.all()

    # Is the current user following this producer?
    is_following = Follow.objects.filter(
        follower=request.user,
        following=user,
    ).exists()

    return render(
        request,
        "producers/public_producer_profile.html",
        {
            "profile": profile,
            "projects": projects,
            "skills": skills,
            "is_following": is_following,
            "is_owner": request.user == user,
        },
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

            return redirect("producers:producer_profile")

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



