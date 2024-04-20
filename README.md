# PyAssistant

`PyAssistant` is a package designed for building virtual assistants and chatbots in Python. The intents and their available functionalities are defined in a YAML file. Due to its modular structure the mode of input/output can be easily configured/replaced (e.g. CLI-based or using voice recognition). It also allows creating custom input/output methods, e.g. over network. Modification of internal processes such as the intent classification can also be done easily if necessary.

# Requirements

This package requires atleast Python 3.10.

## Usage

```cli
python -m pyassistant --config config.yaml
```

## Configuration

Configuration happens using a YAML-file. As an example, refer to the `examples/` directory. As some parameters are identical for most common projects such as phrases for aborting a request `src/default.yaml` contains values for these cases. All values in there can be overwritten in your `config.yaml`.

### Dynamic Parameter Values

### Supported Services

## Text2Speech
- google-...

### Speech2Text
- google-...

## Architecture

### Request Processing
Every Request basically consists of the following three steps:
1. Input
1. Processing
1. Output

#### Processing
During Processing, four steps are performed:
- determine intent
- extract arguments
- run actions
- build response text

As can be seen, most of the heavy lifting is done in the processing step.

### Context
