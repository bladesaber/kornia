from enum import Enum, EnumMeta
from typing import TypeVar, Union, cast

import torch
from torch import Tensor

__all__ = ['pi', 'DType', 'Resample', 'BorderType', 'SamplePadding']

pi = torch.tensor(3.14159265358979323846)
T = TypeVar('T', bound='ConstantBase')


class ConstantBase:
    @classmethod
    def get(cls, value: Union[str, int, T]) -> T:  # type: ignore
        if type(value) is str:
            return cls[value.upper()]  # type: ignore
        if type(value) is int:
            return cls(value)  # type: ignore
        if type(value) is cls:
            return value  # type: ignore
        raise TypeError()


class EnumMetaFlags(EnumMeta):
    def __contains__(self, other: Union[str, int, T]) -> bool:  # type: ignore
        if type(other) is str:
            other = cast(str, other)
            return any(val.name == other.upper() for val in self)  # type: ignore
        if type(other) is int:
            return any(val.value == other for val in self)  # type: ignore
        return any(val == other for val in self)  # type: ignore

    def __repr__(self):
        return ' | '.join(f"{self.__name__}.{val.name}" for val in self)


class Resample(ConstantBase, Enum, metaclass=EnumMetaFlags):
    NEAREST = 0
    BILINEAR = 1
    BICUBIC = 2


class BorderType(ConstantBase, Enum, metaclass=EnumMetaFlags):
    CONSTANT = 0
    REFLECT = 1
    REPLICATE = 2
    CIRCULAR = 3


class SamplePadding(ConstantBase, Enum, metaclass=EnumMetaFlags):
    ZEROS = 0
    BORDER = 1
    REFLECTION = 2


class DType(ConstantBase, Enum, metaclass=EnumMetaFlags):
    INT64 = 0
    FLOAT16 = 1
    FLOAT32 = 2
    FLOAT64 = 3

    @classmethod
    def get(cls, value: Union[str, int, torch.dtype, Tensor, T]) -> T:  # type: ignore
        if type(value) is torch.dtype:
            value = str(value).upper()  # Convert to str
        if type(value) is Tensor:
            value = value.item()  # Convert to int
        if type(value) is str:
            if value.upper().startswith("TORCH."):
                return cls[value.upper()[6:]]  # type: ignore
            return cls[value.upper()]  # type: ignore
        if type(value) is int:
            return cls(value)  # type: ignore
        if type(value) is cls:
            return value  # type: ignore
        raise TypeError(f"Invalid identifier {value}.")

    @classmethod
    def to_torch(cls, value: Union[str, int, T]) -> T:  # type: ignore
        data = cls.get(value=value)
        if data == DType.INT64:
            return torch.long
        if data == DType.FLOAT16:
            return torch.float16
        if data == DType.FLOAT32:
            return torch.float32
        if data == DType.FLOAT64:
            return torch.float64
        raise ValueError()


# TODO: (low-priority) add INPUT3D, MASK3D, BBOX3D, LAFs etc.
class DataKey(ConstantBase, Enum, metaclass=EnumMetaFlags):
    INPUT = 0
    MASK = 1
    BBOX = 2
    BBOX_XYXY = 3
    BBOX_XYWH = 4
    KEYPOINTS = 5
    CLASS = 6
