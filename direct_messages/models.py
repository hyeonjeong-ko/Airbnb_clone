from django.db import models
from common.models import CommonModel


class ChattingRoom(CommonModel):

    """Room Model Definition"""

    users = models.ManyToManyField(
        "users.User",
    )

    def __str__(self):
        return "Chatting Room."


class Message(CommonModel):

    """Message Model Definition"""

    text = models.TextField()

    # 메세지는 한명의 유저에 의해 만들어짐
    user = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    room = models.ForeignKey(
        "direct_messages.ChattingRoom",
        on_delete=models.CASCADE,  # Room이 삭제되면 msg도 삭제됨
    )

    def __str__(self):
        return f"{self.user} says: {self.text}"
