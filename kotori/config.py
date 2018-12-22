import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from os.path import splitext
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, Union

from PIL import Image
from ruamel.yaml import YAML

from kotori.error import ConfigError

__all__ = [
    "ItemKey", "RouteConfig", "TransformConfig", "StorageConfig", "Config",
    "ConfigLoader", "DictConfigLoader", "JsonConfigLoader", "YamlConfigLoader"
]


@dataclass
class ItemKey:
    path: str
    key_path: str = field(init=False)
    key: str = field(init=False)
    transform: str = field(init=False)
    suffix: str = field(init=False)
    folder: str = field(init=False)
    name: str = field(init=False)
    folders: List[str] = field(init=False)
    format: str = field(init=False)

    def __post_init__(self):
        if self.path.endswith("/"):
            raise ValueError("path cannot end with /")
        path, suffix = splitext(self.path)
        parts: List[str] = list(filter(None, path.split("/")))
        self.format = Image.registered_extensions().get(suffix)
        if self.format is None:
            raise ValueError("Unknown format")
        if len(parts) < 2:
            raise ValueError("Too few arguments")
        self.transform = parts[0]
        key_parts = parts[1:]
        self.key = "/".join(key_parts)
        self.key_path = f"/{self.key}"
        self.suffix = suffix
        self.name = key_parts.pop()
        self.folder = f"/{'/'.join(key_parts)}"
        self.folders = [self.key_path]
        for i in range(0, len(key_parts) + 1):
            num = len(key_parts) - i
            self.folders.append("/" + "/".join(key_parts[:num]))


@dataclass
class SaveConfig:
    format: str
    options: Dict[str, Any]


@dataclass
class RouteConfig:
    storage: str
    transform: Union[bool, List[str], str] = False
    expire: Optional[int] = None
    save: Dict[str, Dict[str, Any]] = field(default_factory=dict)


@dataclass
class TransformConfig:
    type: str
    options: List[str]

    @staticmethod
    def from_query(query: str) -> "TransformConfig":
        parts = [t.strip() for t in query.split("_")]
        return TransformConfig(type=parts[0], options=parts[1:])

    @staticmethod
    def from_queries(queries: str) -> List["TransformConfig"]:
        queries = [t.strip() for t in queries.split(",")]
        for query in queries:
            yield TransformConfig.from_query(query)


@dataclass
class StorageConfig:
    type: str
    options: Dict[str, Any]


@dataclass
class Config:
    storage: Dict[str, StorageConfig]
    transform: Dict[str, List[TransformConfig]]
    route: Dict[str, RouteConfig]

    def storage_of(self, key: ItemKey) -> StorageConfig:
        route = self.route_of(key)
        return self.storage[route.storage]

    def route_of(self, key: ItemKey) -> RouteConfig:
        for folder in key.folders:
            config = self.route.get(folder)
            if config is not None:
                return config
        raise ConfigError(f"Cannot find config for {key.path}")

    def transforms_of(self, key: ItemKey) -> List[TransformConfig]:
        if key.transform in self.transform.keys():
            return self.transform[key.transform]
        return TransformConfig.from_queries(key.transform)

    def allow_transform(self, key: ItemKey) -> bool:
        route = self.route_of(key)
        if not route.transform:
            return False
        if isinstance(route.transform, bool):
            return True
        if isinstance(route.transform, str):
            transforms = [route.transform]
        else:
            transforms = route.transform
        if key.transform in self.transform.keys():
            return key.transform in transforms
        configs = TransformConfig.from_queries(key.transform)
        for config in configs:
            if config.type not in transforms:
                return False
        return True


class ConfigLoader(ABC):
    loaders: Dict[str, Type["ConfigLoader"]] = {}

    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        for suffix in cls.support_suffixes():
            if suffix not in cls.loaders:
                cls.loaders[suffix] = cls

    @classmethod
    @abstractmethod
    def support_suffixes(cls) -> List[str]:
        raise NotImplementedError()

    @classmethod
    def load(cls, path: Union[Path, str]) -> Config:
        if isinstance(path, str):
            path = Path(path)
        suffix = path.suffix
        if suffix not in cls.loaders:
            raise ConfigError(f"{suffix} is a unknown format")
        loader = cls.loaders[suffix]()
        config = loader._load(path)
        return config

    @abstractmethod
    def _load(self, path: Path) -> Config:
        raise NotImplementedError()


class DictConfigLoader(ConfigLoader):
    @classmethod
    def support_suffixes(cls) -> List[str]:
        return []

    def _load(self, path: Path) -> Config:
        config = self._load_dict(path)
        storage = {}
        for name, cfg in config.get("storage", {}).items():
            storage[name] = StorageConfig(**cfg)
        transform = {}
        for name, cfg in config.get("transform", {}).items():
            transform[name] = [TransformConfig(**c) for c in cfg]
        route = {}
        for name, cfg in config.get("route", {}).items():
            route[name] = RouteConfig(**cfg)
        return Config(
            storage=storage,
            transform=transform,
            route=route
        )

    @abstractmethod
    def _load_dict(self, path: Path) -> Dict[str, Any]:
        raise NotImplementedError()


class JsonConfigLoader(DictConfigLoader):
    @classmethod
    def support_suffixes(cls) -> List[str]:
        return [".json"]

    def _load_dict(self, path: Path) -> Dict[str, Any]:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)


class YamlConfigLoader(DictConfigLoader):
    @classmethod
    def support_suffixes(cls) -> List[str]:
        return [".yml", ".yaml"]

    def _load_dict(self, path: Path) -> Dict[str, Any]:
        yaml = YAML(typ="safe")
        with open(path, "r", encoding="utf-8") as file:
            return yaml.load(file)
