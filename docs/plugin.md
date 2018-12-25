# Plugin

You can create custom plugins to create your own transformation.

You need to set environment variable `KOTORI_PLUGINS` to set the plugin folder.

## Configuration

You can load you custom configuration by extending `ConfigLoader`.

## Transformation

You can create custom plugins to create your own transformation.

You need to extend `Transformation`. Here is an example.

**invert_transform.py**

```python
from PIL import ImageOps
from PIL.Image import Image

from kotori.transform import Transformation


class InvertTransformation(Transformation):
    @classmethod
    def name(cls) -> str:
        return "invert"

    def transform(self, image: Image, *args) -> Image:
        return ImageOps.invert(image)
```

Then, you put the `invert_transform.py` in your plugin folder.
Now you can use `invert` query.