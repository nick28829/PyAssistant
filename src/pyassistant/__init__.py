from typing import Callable, Tuple

import click

from config import Config, load_config
from context import Context


def get_input_handler(config: Config) -> Callable:
    match config['services']['input']:
        case 'default':
            from .modules.input.default import handler as get_input_handler__handler
            return get_input_handler__handler
        case 'cli':
            return input
        case other:
            return # TODO: try loading function from file


def get_output_handler(config: Config) -> Callable:
    match config['services']['output']:
        case 'default':
            from modules.output.default import make_handler
            return make_handler(config)
        case 'cli':
            return print


def get_intent_detection_handler(config: Config) -> Callable:
    match config['services']['output']:
        case 'default':
            from modules.output.default import make_handler
            return make_handler(config)


def get_argument_extraction_handler(config: Config) -> Callable:
    match config['services']['processing']['argument_extraction']:
        case 'default':
            from modules.processing.argument_extraction.default import make_handler
            return make_handler(config)


def get_intent_detection_handler(config: Config) -> Callable:
    match config['services']['processing']['intent_detection']:
        case 'default':
            from modules.processing.intent_detection.default import make_handler
            return make_handler(config)


def get_action_running_handler(config: Config) -> Callable:
    match config['services']['processing']['action_runner']:
        case 'default':
            from modules.processing.action_runner.default import make_handler
            return make_handler(config)


def get_response_building_handler(config: Config) -> Callable:
    match config['services']['processing']['response_builder']:
        case 'default':
            from modules.processing.response_builder.default import make_handler
            return make_handler(config)


def get_processing_handler(config: Config):
    intent_detection_handler = get_intent_detection_handler(config)
    argument_extraction_handler = get_argument_extraction_handler(config)
    action_running_handler = get_action_running_handler(config)
    response_building_handler = get_response_building_handler(config)

    def handler(context: Context, input: str) -> Tuple[Context, str]:
        updated_context = intent_detection_handler(context, input)
        updated_context = argument_extraction_handler(updated_context, input)
        updated_context = action_running_handler(updated_context, input)
        output = response_building_handler(updated_context)
        return updated_context, output
    
    return handler


@click.command()
@click.option(
    '-c', '--config', help='The path to your config file', default='./config.yaml'
)
@click.option(
    '-o', '--overwrite',
    help='Overwrite individual settings without changing the config, e.g. for debugging with the keyboard set services.input=cli',
    multiple=True
)
def main(config: str, overwrite):
    loaded_config = load_config(config, overwrite)
    input_handler = get_input_handler(loaded_config)
    processing_handler = get_processing_handler(loaded_config)
    output_handler = get_output_handler(loaded_config)
    context = {}
    while True:
        user_input = input_handler()
        if user_input:
            output, new_context = processing_handler(context, user_input)
            context = new_context
            output_handler(output)


if __name__=='__main__':
    main()
