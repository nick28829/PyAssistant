import logging
import re
from typing import List, Literal, NamedTuple

class GeneralConfig(NamedTuple):
    activation_response: str
    falback_response: str
    greeting: str

PAServices = Literal['google']

class Parameter(NamedTuple):
    pass

class ProcessingConfig(NamedTuple):
    intent_detection: Literal['default']
    argument_extraction: Literal['default']
    action_runner: Literal['default']
    response_builder: Literal['default']

class ServicesConfig(NamedTuple):
    text2speech: PAServices
    speech2text: PAServices
    input: Literal['default', 'cli']
    output: Literal['default', 'cli']
    processing: ProcessingConfig

class Intent(NamedTuple):
    type: Literal['simple', 'multi_step']
    name: str
    example_phrases: List[str]

class SimpleIntent(Intent):
    type: Literal['simple']
    response: str
    response_parameters: List[Parameter]

class IntentStep(NamedTuple):
    question: str
    answer_type: Literal['free_text', 'choice']
    choices: List[str]

class MultiStepIntent(Intent):
    type: Literal['multi_step']
    steps: IntentStep

class Config(NamedTuple):
    general: GeneralConfig
    services: ServicesConfig
    intents: List[Intent]

def load_config(path: str, overwrites: List[str]) -> Config:
    config = {}
    # load `default.yaml`
    with open('../defaults.yaml', 'r') as default:
        config.update(default)
    # load user-specified config file
    with open(path, 'r') as user_specified:
        config.update(user_specified)
    # add overwrites
    if overwrites:
        for overwrite in overwrites:
            if not re.match('^[a-z\._]+=.+$', overwrite):
                logging.warning(f'Could not apply overwrite {overwrite}, bad format.')
                continue
            parts = overwrite.split('=')
            if not len(parts) == 2:
                logging.warning(f'Could not apply overwrite {overwrite}, bad format.')
            
            # this is one ugly-ass way to set a property but I can't think of another way right now
            name, value = parts
            ref = config
            parts = name.split('.')
            for idx in range(len(parts) - 1):
                ref = ref[parts[idx]]
            ref[parts[-1]] = value
    return config

