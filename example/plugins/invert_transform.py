from PIL import ImageOps
from PIL.Image import Image

from kotori.transform import Transformation


class InvertTransformation(Transformation):
    @classmethod
    def name(cls) -> str:
        return "invert"

    def transform(self, image: Image, *args) -> Image:
        return ImageOps.invert(image)
