import importlib
import pkgutil
import sys
from logging import getLogger
from os import environ
from pathlib import Path

from flask import Flask, abort
from flask_caching import Cache
from werkzeug.exceptions import NotFound

from kotori.config import Config, ConfigLoader
from kotori.core import Kotori

__all__ = ["KotoriServer"]
logger = getLogger(__name__)


class KotoriServer(Flask):
    def __init__(self, import_name: str):
        super().__init__(import_name)
        self.import_plugins()
        config_path = environ.get("KOTORI_CONFIG")
        if config_path is None:
            raise ValueError("Please set KOTORI_CONFIG")
        config_file = Path(config_path)
        config = ConfigLoader.load(config_file)
        if config is None:
            raise ValueError(f"{config_path} cannot be loaded.")
        self.kotori = Kotori(config)
        self._init_cache(config)
        self._init_path()

    def _init_cache(self, config: Config):
        if config.cache.get("CACHE_TYPE", "null") == "null":
            return
        self.cache = Cache(self, config=config.cache)
        with self.app_context():
            self.cache.clear()
        self.get_image = self.cache.memoize()(self.get_image)

    def _init_path(self):
        self.get_image = self.route("/<path:path>",
                                    methods=["GET"])(self.get_image)
        self.errorhandler(ValueError)(self.on_value_error)
        self.errorhandler(404)(self.no_not_found)

    @staticmethod
    def import_plugins():
        path = environ.get("KOTORI_PLUGINS")
        if path is None:
            return
        plugin_dir = Path(path)
        if not plugin_dir.is_dir():
            return

        sys.path.append(str(plugin_dir.absolute()))
        for _, package_name, _ in pkgutil.iter_modules([plugin_dir]):
            if package_name not in sys.modules:
                importlib.import_module(package_name)

    def get_image(self, path: str):  # pylint: disable=method-hidden
        if path == "favicon.ico":
            abort(404)
        response = self.kotori.get(f"/{path}")
        response.headers["server"] = "Kotori"
        return response

    @staticmethod
    def on_value_error(error: ValueError):
        logger.exception(error, exc_info=False)
        return "", 404

    @staticmethod
    def no_not_found(_: NotFound):
        return "", 404
