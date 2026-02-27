import yaml
from turing_machine import TuringMachine


def load_turing_machine(yaml_file):
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)

    # Fix: use correct keys matching the YAML structure
    q_states        = data['states']
    input_alphabet  = data['input_alphabet']
    tape_alphabet   = data['tape_alphabet']
    blank_symbol    = data['blank']
    initial_state   = data['initial_state']
    final_states    = data['final_states']

    transitions = {}
    for rule in data['delta']:
        p = rule['params']
        o = rule['output']
        key = (
            p['initial_state'],
            p['mem_cache_value'],
            p['tape_input']
        )
        transitions[key] = (
            o['final_state'],
            o['mem_cache_value'],
            o['tape_output'],
            o['tape_displacement']
        )


    config = {
        'states':             q_states,
        'input_alphabet':     input_alphabet,
        'tape_alphabet':      tape_alphabet,
        'blank':              blank_symbol,
        'initial_state':      initial_state,
        'final_states':       final_states,
        'simulation_strings': data.get('simulation_strings', []),  # Add this line
    }

    tm = TuringMachine(
        states         = q_states,
        input_alphabet = input_alphabet,
        tape_alphabet  = tape_alphabet,
        blank_symbol   = blank_symbol,
        transitions    = transitions,
        initial_state  = initial_state,
        final_states   = final_states
    )

    return config, transitions