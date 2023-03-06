from django.db import models


class Category(models.Model):
    class CategoryKindChoices(models.TextChoices):
        BROADCAST = "broadcast", "BROADCASTS"  # 방송
        EVENT = "event", "EVENTS"  # 행사
        RELEASE = "release", "RELEASES"  # 발매
        CONGRAT = "congrats", "CONGRATS"  # 축하
        SNS = "sns", "SNS"  # sns
        ETC = "etc", "ETC"  # 기타

    type = models.CharField(
        max_length=15,
        choices=CategoryKindChoices.choices,
        default="",
        blank=True,
    )

    # title = models.CharField(
    #     max_length=150,
    #     default="",
    #     blank=False,
    # )

    content = models.TextField(max_length=500, default="")  # 카테고리에 대한 내용

    def __str__(self):
        return self.type

    # type=models.CharField(#idol일정 종류
    #     max_length=15,
    #     choices=CategoryKindChoices.choices,
    # )

    class Meta:
        verbose_name_plural = "Categories"
