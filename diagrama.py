"""
diagrama_fibonacci.py
Genera el diagrama de estados de la MT de Fibonacci desde su YAML,
produce un archivo .dot y lo renderiza a PNG con Graphviz.
"""
import os
import subprocess
from parser_yaml import load_turing_machine

# ── Configuración ────────────────────────────────────────────────────────────
YAML_FILE  = "examples/fibonacci.yaml"
DOT_FILE   = "diagramas/fibonacci.dot"
PNG_FILE   = "diagramas/fibonacci.png"

# Descripción breve de cada estado (para la etiqueta del nodo)
STATE_LABELS = {
    "q_init"   : "q_init\nEstado\nInicial",
    "q_base_1" : "q_base_1\nCaso base\nn=1",
    "q_setup"  : "q_setup\nConvertir '1'\na marcas X",
    "q_loop"   : "q_loop\nBucle\nprincipal",
    "q_copy"   : "q_copy\nCopiar '1'\nal final",
    "q_back"   : "q_back\nRegresar\nal inicio",
    "q_final"  : "q_final\nACEPTA",
}
# ─────────────────────────────────────────────────────────────────────────────


def symbol_str(s):
    """Representa un símbolo de forma legible."""
    return "blank" if s is None else str(s)


def build_dot(config, transitions):
    """Construye el contenido del archivo .dot."""
    initial  = config["initial_state"]
    finals   = set(config["final_states"])
    states   = config["states"]

    # Agrupar transiciones por (origen → destino) para compactar etiquetas
    edges: dict[tuple, list[str]] = {}
    for (q, cache, tape_in), (q2, new_cache, tape_out, direction) in transitions.items():
        key = (q, q2)
        label = (
            f"({symbol_str(cache)}, {symbol_str(tape_in)}) →\n"
            f"({symbol_str(new_cache)}, {symbol_str(tape_out)}, {direction})"
        )
        edges.setdefault(key, []).append(label)

    lines = []
    lines.append("// Máquina de Turing – Fibonacci en Unario")
    lines.append("")
    lines.append("digraph MT_Fibonacci {")
    lines.append('    rankdir=LR;')
    lines.append('    size="16,10";')
    lines.append('    node [shape=circle, style=filled, fillcolor=lightyellow, fontsize=10];')
    lines.append('    edge [fontsize=8];')
    lines.append("")

    # Nodos
    lines.append("    // Estados")
    for s in states:
        lbl = STATE_LABELS.get(s, s)
        if s in finals:
            lines.append(f'    {s} [label="{lbl}", shape=doublecircle, fillcolor=lightgreen];')
        elif s == initial:
            lines.append(f'    {s} [label="{lbl}", fillcolor=lightblue];')
        else:
            lines.append(f'    {s} [label="{lbl}"];')

    lines.append("")
    lines.append("    // Flecha de inicio")
    lines.append("    __start__ [shape=point];")
    lines.append(f"    __start__ -> {initial};")
    lines.append("")

    # Aristas
    lines.append("    // Transiciones")
    for (src, dst), labels in sorted(edges.items()):
        combined = "\\n".join(labels)
        lines.append(f'    {src} -> {dst} [label="{combined}"];')

    lines.append("}")
    return "\n".join(lines)


def render_dot(dot_file, png_file):
    """Intenta renderizar el .dot con Graphviz (dot)."""
    try:
        result = subprocess.run(
            ["dot", "-Tpng", dot_file, "-o", png_file],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"Diagrama PNG generado: {png_file}")
        else:
            print("Graphviz encontró un error:")
            print(result.stderr)
    except FileNotFoundError:
        print("Graphviz (dot) no está instalado o no está en el PATH.")
        print(f"Puedes renderizar manualmente el archivo: {dot_file}")
        print("  → Instala Graphviz desde https://graphviz.org/download/")
        print("  → O usa https://dreampuf.github.io/GraphvizOnline/")


def main():
    os.makedirs("diagramas", exist_ok=True)

    config, transitions = load_turing_machine(YAML_FILE)

    dot_content = build_dot(config, transitions)

    with open(DOT_FILE, "w", encoding="utf-8") as f:
        f.write(dot_content)
    print(f"Archivo DOT generado: {DOT_FILE}")

    render_dot(DOT_FILE, PNG_FILE)

    # Mostrar resumen de la estructura
    print("\n── Estructura de la MT Fibonacci ──────────────────────────")
    print(f"  Estado inicial : {config['initial_state']}")
    print(f"  Estados finales: {config['final_states']}")
    print(f"  Total estados  : {len(config['states'])}")
    print(f"  Alfabeto entrada : {config['input_alphabet']}")
    print(f"  Alfabeto cinta   : {[symbol_str(s) for s in config['tape_alphabet']]}")
    print(f"  Total transiciones: {len(transitions)}")
    sort_key = lambda item: (item[0][0], str(item[0][1]), str(item[0][2]))
    print("\n  Transiciones:")
    for (q, cache, tape_in), (q2, new_cache, tape_out, direction) in sorted(transitions.items(), key=sort_key):
        print(f"    ({q}, {symbol_str(cache)}, {symbol_str(tape_in)}) "
              f"→ ({q2}, {symbol_str(new_cache)}, {symbol_str(tape_out)}, {direction})")


if __name__ == "__main__":
    main()