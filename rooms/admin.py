from django.contrib import admin
from .models import Room, Amenity


# action은 세개의 매개변수를 가짐
# 호출한 클래스 / 호출한 유저정보 / 쿼리셋
@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, rooms):
    for room in rooms.all():
        room.price = 0
        room.save()


@admin.register(Room)  # 해당 class가 Room을 control
class RoomAdmin(admin.ModelAdmin):

    actions = (reset_prices,)

    list_display = (
        "name",
        "price",
        "kind",
        "total_amenities",
        "rating",
        "owner",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "country",
        "city",
        "price",
        "rooms",
        "toilets",
        "pet_friendly",
        "kind",
        "amenities",
    )

    search_fields = (
        "^name",  # ^ ; name시작부분, = ; 100%동일
        "price",
        "^owner__username",  # owner의 username으로 검색
    )

    # def total_amenities(self, room):
    #     return room.amenities.count()


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
