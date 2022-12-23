from django.db import models
from common.models import CommonModel


class Booking(CommonModel):

    """Booking Model Definition"""

    class BookingKindChoices(models.TextChoices):

        ROOM = "room", "Room"
        EXPERIENCE = "experience", "Experience"

    kind = models.CharField(
        max_length=15,
        choices=BookingKindChoices.choices,
    )

    # booking은 오직 한 명의 유저밖에 가질 수 없음
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    # 예약은 한 개의 방만 / 한 개의 방은 많은 예약을 가질 수 있음
    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    experience = models.ForeignKey(
        "experiences.Experiences",
        null=True,
        blank=True,
        # experience가 삭제되어도 유저는 자신이 만들었던
        # booking을 확인 할 수 있어야 함.
        on_delete=models.SET_NULL,
        related_name="bookings",
    )

    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)

    experience_time = models.DateTimeField(null=True, blank=True)
    guests = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.kind.title()} / {self.user}"
