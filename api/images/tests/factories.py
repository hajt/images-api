import factory
import factory.fuzzy

from api.users.tests.factories import UserFactory
from ..models import Image


class ImageFactory(factory.django.DjangoModelFactory):
    """
    Factory for Image object.
    """

    title = factory.fuzzy.FuzzyText(length=12)
    width = factory.fuzzy.FuzzyInteger(low=1, high=4096)
    height = factory.fuzzy.FuzzyInteger(low=1, high=4096)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Image
