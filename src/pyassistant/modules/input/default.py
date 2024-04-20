from config import Config
from context import Context


def make_handler(config: Config):
    def handler(context: Context, input: str):
        pass
    return handler
