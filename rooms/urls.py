from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.see_all_rooms),
    path("<int:room_pk>", views.see_one_room),  # address query parameter
    # path("<str:room_name>/<str:room_id>",s)
]
