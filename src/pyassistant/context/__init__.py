from typing import List, NamedTuple, Any

from config import Intent

class Argument(NamedTuple):
    name: str
    value: Any

class Context(NamedTuple):
    """The `Context` contains information about a user request / conversation such as current
    intent, missing arguments or past requests.
    """
    follow_up: bool
    """Whether currently a follow has to be done / was done for additional information"""
    missing_args: List[Any]
    """Arguments for which a follow_up is necessary"""
    intent_args: List[Argument]
    """Already provided arguments"""
    current_intent: Intent