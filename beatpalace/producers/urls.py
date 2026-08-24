from django.urls import path

from .views import (
    producer_profile,
    public_producer_profile,
    producer_edit_profile,
    producer_add_project,
    producer_delete_project,
    producer_add_skill,
    producer_delete_skill,
)


app_name = "producers"


urlpatterns = [

    path(
        "profile/",
        producer_profile,
        name="producer_profile",
    ),

    path(
        "profile/edit/",
        producer_edit_profile,
        name="producer_edit_profile",
    ),

  

    path(
        "u/<str:username>/",
        public_producer_profile,
        name="public_producer_profile",
    ),

    path(
        "projects/add/",
        producer_add_project,
        name="producer_add_project"
    ),
    path(
        "projects/add/",
        producer_add_skill,
        name="producer_add_skill"
    ),
    path(
        "projects/<int:project_id>/delete/",
        producer_delete_project,
        name="producer_delete_project"
    ),
    path(
        "projects/<int:skill_id>/delete/",
        producer_delete_skill,
        name="producer_delete_skill"
    ),

]