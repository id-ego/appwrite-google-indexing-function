from pydantic import BaseModel
from typing import Literal


class ResponseType(BaseModel):
    """
    A class to represent a response type.

    Attributes
    ----------
    type : Literal["success", "error"]
        The type of response, which can either be "success" or "error".
    message : str
        The message associated with the response, providing additional information.
    """

    type: Literal["success", "error"]
    message: str
