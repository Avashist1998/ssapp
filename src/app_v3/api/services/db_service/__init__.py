"""db package init"""
from .utils import (
    FailedToCreateException,
    FailedToGetException,
    FailedToDeleteException,
    FailedToUpdateException,
)

__all__ = [
    "FailedToCreateException",
    "FailedToGetException",
    "FailedToDeleteException",
    "FailedToUpdateException",
]
