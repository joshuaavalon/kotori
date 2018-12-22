from abc import ABC, abstractmethod
from io import IOBase
from os import PathLike
from pathlib import Path
from typing import Dict, Optional, Type

import boto3
from PIL import Image
from botocore.exceptions import ClientError

image_extensions = Image.registered_extensions().keys()

__all__ = ["StorageAdapter", "FileStorageAdapter", "S3StorageAdapter"]


class StorageAdapter(ABC):
    adapters: Dict[str, Type["StorageAdapter"]] = {}

    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        name = cls.name()
        if name not in cls.adapters:
            cls.adapters[name] = cls

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        raise NotImplementedError()

    @abstractmethod
    def read(self, key: str) -> Optional[IOBase]:
        raise NotImplementedError()

    @classmethod
    def create(cls, name: str, **kwargs) -> "StorageAdapter":
        try:
            return cls.adapters[name](**kwargs)
        except IndexError:
            raise ValueError(f"Unknown storage ({name})")


class FileStorageAdapter(StorageAdapter):
    def __init__(self, **kwargs):
        self.root = Path(kwargs.get("root", "/"))
        self.suffixes = kwargs.get("suffixes", image_extensions)

    @classmethod
    def name(cls) -> str:
        return "file"

    def find_file(self, path: str) -> Optional[Path]:
        if not self.is_relative(path):
            return None
        path = self.root.joinpath(path)
        folder = path.parent
        name = path.stem
        for file in folder.glob(f"{name}.*"):
            if file.suffix in image_extensions:
                return file
        return None

    def is_relative(self, path: str) -> bool:
        try:
            self.root.joinpath(path).relative_to(self.root)
            return True
        except ValueError:
            return False

    def read(self, key: str) -> Optional[IOBase]:
        file = self.find_file(key)
        if file is None:
            return None
        try:
            # noinspection PyTypeChecker
            return open(file, "rb")
        except IOError:
            return None


class S3StorageAdapter(StorageAdapter):
    def __init__(self, **kwargs):
        s3 = boto3.resource(
            "s3",
            region_name=kwargs.get("region_name"),
            endpoint_url=kwargs.get("endpoint_url"),
            aws_access_key_id=kwargs.get("aws_access_key_id"),
            aws_secret_access_key=kwargs.get("aws_secret_access_key")
        )
        self.bucket = s3.Bucket(kwargs.get("bucket"))
        self.root = kwargs.get("root", "")

    @classmethod
    def name(cls) -> str:
        return "s3"

    def read(self, key: str) -> Optional[IOBase]:
        try:
            # filter file
            prefix = self.root + key + "."
            for obj in self.bucket.objects.filter(Prefix=prefix):
                file = Path(obj.key)
                if file.suffix in image_extensions:
                    return obj.get()["Body"]
            return None
        except ClientError:
            return None
