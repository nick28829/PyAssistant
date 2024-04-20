from config import Config
from context import Context


def make_handler(config: Config):
    # vectorize example phrases from all intents for quick comparison

    def handler(context: Context, input: str):
        # vectorize input

        # compare input vector against possible intent vectors
        pass
    return handler
