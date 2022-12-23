from django.contrib import admin
from .models import Review


class RatingFilter(admin.SimpleListFilter):

    title = "Filter by Good or Bad"

    parameter_name = "GoodOrBad"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("bad", "Bad"),
        ]

    def querySet(self, request, reviews):
        choice = self.value()
        if choice == "good":
            return reviews.filter(rating__gt=2)
        elif choice == "bad":
            return reviews.filter(rating__lt=3)


# 나만의 필터 만들기
class WordFilter(admin.SimpleListFilter):

    title = "Fllter by words!"

    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),  # 실제, 관리자페이지에 보일 이름
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]

    def queryset(self, request, reviews):
        # url query단어를 줌 (word=*good*)
        word = self.value()
        if word:
            return reviews.filter(payload__contains=word)
        else:
            reviews


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "__str__",
        "payload",
    )
    list_filter = (
        WordFilter,
        "rating",
        "user__is_host",
        "room__category",
    )  # FK 속성 기반 필터링 가능
