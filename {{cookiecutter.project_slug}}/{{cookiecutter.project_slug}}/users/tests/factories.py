# -*- coding: utf-8 -*-

"""User factory."""

import factory
from factory import Faker
from factory.django import DjangoModelFactory

from ..models import User


class UserFactory(DjangoModelFactory):
    """Factory for users in django."""

    username = Faker('user_name')
    email = Faker('email')
    name = Faker('name', locale='it_IT')
    cf = Faker('ssn', locale='it_IT')
    password = Faker(
        'password',
        length=42,
        special_chars=True,
        digits=True,
        upper_case=True,
        lower_case=True,
    )

    @classmethod
    def as_dict(cls):
        """Generate new random data as dict."""
        return factory.build(dict, FACTORY_CLASS=cls)

    @classmethod
    def get_random_password(cls):
        """Return a new random password."""
        return cls.password.generate({'locale': 'it_IT'})

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create_user(*args, **kwargs)

    class Meta:
        """Metadata for the factory."""

        model = User
        django_get_or_create = ['username']
