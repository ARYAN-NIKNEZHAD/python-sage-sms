import pkgutil
import inspect
from importlib import import_module
from typing import ClassVar, Dict

from .utils import load_settings
from .backend.base import ConsoleSMSBackend
from .design.interfaces.provider import ISmsProvider


class BackendModuleLoader:
    _cached_backends: ClassVar[Dict[str, type]] = {}
    _provider_classname_map: ClassVar[Dict[str, type]] = {}

    @classmethod
    def discover_backends(cls, base_package: str):
        backend_package = import_module(base_package)
        for _, module_name, _ in pkgutil.iter_modules(backend_package.__path__):
            module = import_module(f"{base_package}.{module_name}")
            for name, obj in inspect.getmembers(module, inspect.isclass):
                # Check if the class implements ISmsProvider and is not ISmsProvider itself
                if issubclass(obj, ISmsProvider) and obj is not ISmsProvider:
                    cls._provider_classname_map[module_name] = obj.__name__
                    break

    @staticmethod
    def _get_class_name(module_name: str) -> str:
        # Convert the module name to CamelCase
        return ''.join(word.capitalize() for word in module_name.split('_'))

    @staticmethod
    def load_backend_module(provider: dict):
        provider_name = provider.get("NAME")

        if not provider_name:
            raise ValueError("Provider name is missing in settings.")

        if provider_name not in BackendModuleLoader._provider_classname_map:
            raise ValueError(f"Unsupported provider: {provider_name}")

        if provider_name in BackendModuleLoader._cached_backends:
            return BackendModuleLoader._cached_backends[provider_name]

        provider_class = BackendModuleLoader._provider_classname_map[provider_name]
        BackendModuleLoader._cached_backends[provider_name] = provider_class
        return provider_class


class SMSBackendFactory:
    @staticmethod
    def get_backend(settings: dict, *args, **kwargs):
        if settings.get("debug", False):
            return ConsoleSMSBackend

        backend_class = BackendModuleLoader.load_backend_module(settings.get("provider"))
        return backend_class
