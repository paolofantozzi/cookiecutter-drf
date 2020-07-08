# -*- coding: utf-8 -*-

"""Settings for custom module.

Originally developed in https://github.com/encode/django-rest-framework/blob/master/rest_framework/settings.py
"""

from functools import partial

from django.conf import settings
from django.test.signals import setting_changed

from {{ cookiecutter.project_slug }}.utils.module_import import import_modules


class APISettings:
    """A settings object.

    The class acts as interface between the module and the settings, letting also the possibility to use user-custom
    settings together with default settings. The instance auto connects to the signal for settings changed and it
    performs some operations (like cache clearing) when the settings change.

    Attributes:
        settings_key: the key to be used in settings to be mapped to module settings
        defaults: values that should be used as defaults if the user does not customize the module. Keyword only arg.
        settings_to_import: list of setting keys that should be managed as module attributes. Keyword only arg.
        raise_if_not_exist: when True it raises an exception if the key does not exist neither in user_settings and
            in defaults. It returns None otherwise. Keyword only arg.

    An example of using in a module settings.py is:
    >>> from vasplat.utils.api_settings import APISettings
    >>> defaults = {'KEY_1': 'value1', 'KEY_TO_IMPORT': 'module.class_attribute', 'KEY_2': 'module.class_attribute'}
    >>> settings_to_import = ['KEY_TO_IMPORT']
    >>> api_settings = APISettings('KEY_IN_SETTINGS', defaults=defaults, settings_to_import=settings_to_import)
    >>> api_settings.KEY_1
    'value1'
    >>> api_settings.KEY_TO_IMPORT
    <class 'module.class_attribute'>
    >>> api_settings.KEY_2
    'module.class_attribute'
    """

    def __init__(self, settings_key, *, defaults=None, settings_to_import=None, raise_if_not_exist=True):
        """Set defaults settings and empty cache."""
        self.settings_key = settings_key
        self.defaults = defaults or {}
        self.settings_to_import = set(settings_to_import or [])
        self.raise_if_not_exist = raise_if_not_exist
        self._cached_attrs = set()
        self._user_settings = None

        # register the reloading method of this class to the signal
        reload_this_api_settings = partial(APISettings.reload, self)
        setting_changed.connect(reload_this_api_settings)

    @property
    def user_settings(self):
        """Return settings defined by user if any, empty dictionary otherwise."""
        if self._user_settings is None:
            self._user_settings = getattr(settings, self.settings_key, {})
        return self._user_settings

    def reload(self, *args, **kwargs):
        """Empty object cache if the settings changed."""
        if kwargs.get('setting', None) == self.settings_key:
            self._do_reload()

    def __getattr__(self, attr):
        """Search the setting and then cache it."""
        setting_value = self._get_setting(attr)
        if attr in self.settings_to_import:
            setting_value = import_modules(setting_value)
        self._cached_attrs.add(attr)
        setattr(self, attr, setting_value)
        return setting_value

    def _do_reload(self):
        """Empty class-level cache."""
        for attr in self._cached_attrs:
            delattr(self, attr)  # noqa: WPS421
        self._cached_attrs.clear()
        self._user_settings = None

    def _get_setting(self, key):
        try:
            return self.user_settings[key]
        except KeyError:
            pass  # noqa: WPS420

        try:
            return self.defaults[key]
        except KeyError:
            if self.raise_if_not_exist:
                raise AttributeError(f"Invalid API setting: '{key}'")
            return None
