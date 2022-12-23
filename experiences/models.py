from django.db import models
from common.models import CommonModel


class Experiences(CommonModel):
    """Experience Model Definition"""

    country = models.CharField(
        max_length=50,
        default="한국",
    )
    city = models.CharField(
        max_length=80,
        default="서울",
    )
    name = models.CharField(
        max_length=250,
    )
    host = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=250)
    # datefield: 일/월/연도 저장 . datetimefield: 일/월/년도/시간/분/초 저장. timefield: 시간/분/초 저장
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField()
    perks = models.ManyToManyField(
        "experiences.Perk",
    )
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,  # Cate삭제된다면, Experiences의 Cate를 null로 만듦.
    )

    def __str__(self) -> str:
        return self.name


class Perk(CommonModel):
    """What is included on an Experience"""

    name = models.CharField(
        max_length=100,
        blank=True,
        default="",
    )
    detail = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    explanation = models.TextField()

    def __str__(self) -> str:
        return self.name
