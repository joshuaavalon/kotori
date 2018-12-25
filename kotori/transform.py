from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Type

from PIL.Image import Image, NEAREST

from kotori.config import TransformConfig


class Transformation(ABC):
    transformations: Dict[str, Type["Transformation"]] = {}

    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        name = cls.name()
        if name not in cls.transformations:
            cls.transformations[name] = cls

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        raise NotImplementedError()

    @abstractmethod
    def transform(self, image: Image, *args) -> Image:
        raise NotImplementedError()

    @classmethod
    def run(cls, image: Image, configs: List[TransformConfig]) -> Image:
        for config in configs:
            if config.type not in cls.transformations:
                raise ValueError(f"Unknown transformation ({config.type})")
            transformation: Transformation = cls.transformations[config.type]()
            image = transformation.transform(image, *config.options)
        return image


class ThumbnailTransformation(Transformation):
    @classmethod
    def name(cls) -> str:
        return "t"

    def transform(self, image: Image, *args) -> Image:
        try:
            width = int(args[0])
            height = int(args[1])
            resample = int(args[2]) if len(args) >= 3 else NEAREST
            image.thumbnail((width, height), resample)
            return image
        except IndexError:
            raise ValueError("Not enough arguments")


class ResizeTransformation(Transformation):
    @classmethod
    def name(cls) -> str:
        return "r"

    def transform(self, image: Image, *args) -> Image:
        try:
            width = int(args[0])
            height = int(args[1])
            if len(args) == 2:
                return self.resize_crop(image, width, height)
            resample = int(args[2])
            if len(args) == 3:
                return self.resize_crop(image, width, height, resample)
            crop = args[3]
            return self.resize_crop(image, width, height, resample, crop)
        except IndexError:
            raise ValueError("Not enough arguments")

    @staticmethod
    def resize(image: Image,
               width: int,
               height: int,
               resample: int = NEAREST) -> Image:
        if resample is None:
            return image.resize((width, height))
        return image.resize((width, height), resample)

    def resize_crop(self, image: Image,
                    width: int,
                    height: int,
                    resample: int = NEAREST,
                    crop: Optional[str] = None) -> Image:
        if crop is None:
            return self.resize(image, width, height, resample)
        image_ratio = image.size[0] / image.size[1]
        ratio = width / height
        if ratio > image_ratio:
            new_height = int(width * image.size[1] / image.size[0])
            image = self.resize(image, width, new_height, resample)
            if crop == "t":
                box = (0, 0, image.size[0], height)
            elif crop == "b":
                box = (0, image.size[1] - height, image.size[0], image.size[1])
            elif crop == "c":
                box = (0, (image.size[1] - height) / 2, image.size[0],
                       (image.size[1] + height) / 2)
            else:
                raise ValueError(f"Unknown crop method: {crop}")
            image = image.crop(box)
            return image
        elif ratio < image_ratio:
            new_width = int(height * image.size[0] / image.size[1])
            image = self.resize(image, new_width, height, resample)
            if crop == "t":
                box = (0, 0, width, image.size[1])
            elif crop == "b":
                box = (image.size[0] - width, 0, image.size[0], image.size[1])
            elif crop == "c":
                box = (
                    (image.size[0] - width) / 2, 0,
                    (image.size[0] + width) / 2,
                    image.size[1])
            else:
                raise ValueError(f"Unknown crop method: {crop}")
            image = image.crop(box)
            return image
        else:
            return self.resize(image, width, height, resample)


class OriginTransformation(Transformation):
    @classmethod
    def name(cls) -> str:
        return "origin"

    def transform(self, image: Image, *args) -> Image:
        return image
