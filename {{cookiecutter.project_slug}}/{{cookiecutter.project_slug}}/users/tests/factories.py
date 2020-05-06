# -*- coding: utf-8 -*-

"""User factory."""

from typing import Any
from typing import Sequence

from factory import DjangoModelFactory
from factory import Faker
from factory import post_generation

from ..models import User


class UserFactory(DjangoModelFactory):
    """Factory for users."""

    username = Faker('user_name')
    email = Faker('email')
    name = Faker('name')

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        """Fake password generator."""
        password = (
            extracted
            if extracted
            else Faker(
                'password',
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).generate(extra_kwargs={})
        )
        self.set_password(password)

    class Meta:
        """Metadata for the factory."""

        model = User
        django_get_or_create = ['username']
