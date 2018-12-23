from io import BytesIO, IOBase
from typing import Optional

import PIL
from PIL.Image import Image
from flask import Response, abort, send_file

from kotori.config import Config, ItemKey
from kotori.error import ConfigError
from kotori.storage import StorageAdapter
from kotori.transform import Transformation


class Kotori:
    def __init__(self, config: Config):
        self.config = config
        self.validate_config()

    def validate_config(self):
        for key in Transformation.transformations:
            if key in self.config.transform:
                raise ConfigError(f"{key} cannot be used as a transform name.")

    def get(self, path: str) -> Response:
        key = ItemKey(path)
        if not self.config.allow_transform(key):
            abort(404)
        route = self.config.route_of(key)
        transforms = self.config.transforms_of(key)
        image = self.get_image(key)
        if image is None:
            abort(404)
        image = Transformation.run(image, transforms)
        result: IOBase = BytesIO()
        if key.format in route.save:
            image.save(result, format=key.format, **route.save[key.format])
        else:
            image.save(result, format=key.format)
        result.seek(0)
        return send_file(result,
                         mimetype=PIL.Image.MIME[key.format],
                         cache_timeout=route.expire)

    def get_image(self, key: ItemKey) -> Optional[Image]:
        config = self.config.storage_of(key)
        storage = StorageAdapter.create(config.type, **config.options)
        stream = storage.read(key.key)
        if stream is None:
            return None
        return PIL.Image.open(stream)
