from django.urls import path

# from .views import (
#     producer_profile,
#     edit_profile,
# )


# urlpatterns = [


#     path(
#         "profile/edit/",
#         edit_profile,
#         name="producer_edit_profile"
#     ),

#     path(
#         "<str:username>/",
#         producer_profile,
#         name="producer_profile"
#     ),


    

# ]


from django.urls import path

from .views import (
    producer_profile,
    producer_edit_profile,
    producer_add_project,
    producer_delete_project,
    producer_add_skill,
    producer_delete_skill,
)


urlpatterns = [

    path(
        "profile/",
        producer_profile,
        name="producer_profile"
    ),

    path(
        "profile/edit/",
        producer_edit_profile,
        name="producer_edit_profile"
    ),

    path(
        "profile/project/add/",
        producer_add_project,
        name="producer_add_project"
    ),

    path(
        "profile/project/<int:project_id>/delete/",
        producer_delete_project,
        name="producer_delete_project"
    ),

    path(
        "profile/skill/add/",
        producer_add_skill,
        name="producer_add_skill"
    ),

    path(
        "profile/skill/<int:skill_id>/delete/",
        producer_delete_skill,
        name="producer_delete_skill"
    ),
]