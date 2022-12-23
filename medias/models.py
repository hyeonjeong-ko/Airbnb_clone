from django.db import models
from common.models import CommonModel


class Photo(CommonModel):

    file = models.ImageField()
    description = models.CharField(max_length=140)

    # 한개의 방이 많은 photo를 가질 수 있음 (N:1)
    # 방이 삭제되면 사진도 삭제됨

    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    experience = models.ForeignKey(
        "experiences.Experiences",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return "Photo File"


class Video(CommonModel):
    file = models.FileField()
    experience = models.OneToOneField(
        "experiences.Experiences",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "Video File"
