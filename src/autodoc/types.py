from typing import Union, List

from pydantic import BaseModel
from pydantic.typing import NoneType


class CommandResult(BaseModel):
    command: List[str]
    description: Union[NoneType, str]


class AutoDocResult(BaseModel):
    commands: List[CommandResult]
