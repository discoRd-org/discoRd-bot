import typing

from os import environ

# Object-oriented filesystem paths
# https://docs.python.org/3/library/pathlib.html?highlight=pathlib#module-pathlib
from pathlib import Path

# Reads the key-value pair from .env file and adds them to environment variable.
# https://pypi.org/project/python-dotenv/
import dotenv


dotenv.load_dotenv()


class ConfigMeta(type):
    def resolve_value(cls, value: str):
        _map: typing.Dict[str, typing.Callable] = {
            "bool": bool,
            "int": int,
            "float": float,
            "file": lambda x: Path(x).read_text(),
            "str": str,
            "set": lambda x: set([cls.resolve_value(e.strip()) for e in x.split(",")]),
        }

        return _map[(v := value.split(":", maxsplit=1))[0]](v[1])

    def resolve_key(cls, key: str):
        try:
            return cls.resolve_key(environ[key])
        except:
            return cls.resolve_value(key)

    def __getattr__(cls, name):
        try:
            return cls.resolve_key(name)
        except KeyError:
            raise AttributeError(f"{name} is not a key in config") from None

    def __getitem__(cls, name):
        return cls.__getattr__(name)


class Config(metaclass=ConfigMeta):
    pass

