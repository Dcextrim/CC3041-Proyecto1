import sys
import time  # para medir tiempos de ejecución
from parser_yaml import load_turing_machine
from turing_machine import TuringMachine
import os

MAX_STEPS = 10000  # Límite de pasos para evitar bucles infinitos


def simulate_string(tm, input_str, f, csv_f):
    """Simula una cadena, imprime en pantalla y escribe en los archivos de salida."""
    print(f"Simulando cadena: {repr(input_str)}")
    f.write(f"Simulando cadena: {input_str}\n")
    f.write("-" * 70 + "\n")

    tm.load_tape(input_str)
    step_counter = 0

    start_time = time.perf_counter_ns()
    while step_counter < MAX_STEPS:
        config_line = f"Paso {step_counter:03d}: {tm.get_configuration()}"
        print(config_line)
        f.write(config_line + "\n")
        if not tm.step():
            break
        step_counter += 1
    end_time = time.perf_counter_ns()
    execution_time = end_time - start_time

    if step_counter >= MAX_STEPS:
        msg = "\nSimulación detenida: límite de pasos alcanzado (posible bucle infinito)"
        result = "INDETERMINADA"
        print(msg)
        f.write(msg + "\n")
    else:
        accepted = tm.current_state in tm.final_states
        result = "ACEPTADA" if accepted else "RECHAZADA"

    tape_str = ''.join(str(s) if s is not None else '_' for s in tm.tape)
    summary = (
        f"\nResultado final: {result}\n"
        f"Pasos totales: {step_counter}\n"
        f"Tiempo de ejecución: {execution_time} ns\n"
        f"Cinta final: {tape_str}"
    )
    print(summary)
    f.write(summary + "\n")
    f.write("=" * 70 + "\n\n")

    csv_f.write(f"{input_str},{len(input_str)},{step_counter},{execution_time}\n")


def run_turing_machine(yaml_file):
    # Carga configuración desde YAML
    config, transitions = load_turing_machine(yaml_file)
    tm = TuringMachine(
        config['states'],
        config['input_alphabet'],
        config['tape_alphabet'],
        config['blank'],
        transitions,
        config['initial_state'],
        config['final_states']
    )

    # Crea carpeta de resultados
    output_dir = "resultados"
    os.makedirs(output_dir, exist_ok=True)

    yaml_name   = os.path.splitext(os.path.basename(yaml_file))[0]
    output_file = os.path.join(output_dir, f"{yaml_name}_salida.txt")
    csv_file    = os.path.join(output_dir, f"{yaml_name}_datos_analisis.csv")

    with open(output_file, "w", encoding="utf-8") as f, \
         open(csv_file,    "w", encoding="utf-8") as csv_f:

        f.write(f"Simulación de Máquina de Turing: {yaml_file}\n")
        f.write("=" * 70 + "\n\n")
        csv_f.write("entrada_n,longitud_entrada,pasos,tiempo_ns\n")

        # ── 1. Cadenas predefinidas del YAML ─────────────────────────────
        if config['simulation_strings']:
            print("\n" + "=" * 70)
            print("CADENAS PREDEFINIDAS (simulation_strings del YAML)")
            print("=" * 70)
            f.write("CADENAS PREDEFINIDAS\n")
            f.write("=" * 70 + "\n\n")
            for input_str in config['simulation_strings']:
                simulate_string(tm, input_str, f, csv_f)

        # ── 2. Modo interactivo ───────────────────────────────────────────
        print("\n" + "=" * 70)
        print("MODO INTERACTIVO")
        print(f"Alfabeto de entrada permitido: {config['input_alphabet']}")
        print("Escribe una cadena y presiona Enter para simularla.")
        print("Escribe 'salir' o presiona Enter vacío para terminar.")
        print("=" * 70)

        f.write("CADENAS INTERACTIVAS\n")
        f.write("=" * 70 + "\n\n")

        while True:
            try:
                user_input = input("\nCadena de entrada: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nSaliendo del modo interactivo.")
                break

            if user_input.lower() in ("salir", "exit", ""):
                print("Saliendo del modo interactivo.")
                break

            # Validar símbolos
            invalid = [c for c in user_input if c not in config['input_alphabet']]
            if invalid:
                print(f"  Símbolos no válidos: {invalid}. Usa solo: {config['input_alphabet']}")
                continue

            simulate_string(tm, user_input, f, csv_f)

    print(f"\nSimulación completada.")
    print(f"Detalles guardados en: {output_file}")
    print(f"Datos para regresión:  {csv_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <archivo_yaml>")
        sys.exit(1)

    yaml_file = sys.argv[1]
    run_turing_machine(yaml_file)