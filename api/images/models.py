from django.core.validators import MinValueValidator
from django.db import models

from api.core.models import CommonModel
from api.users.models import User


class Image(CommonModel):
    title = models.CharField(max_length=120)
    width = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    height = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    file = models.ImageField(upload_to="images/")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self})>"

    def __str__(self) -> str:
        return self.title
