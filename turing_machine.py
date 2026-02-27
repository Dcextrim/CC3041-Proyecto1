class TuringMachine:
    def __init__(self, states, input_alphabet, tape_alphabet,
                 blank_symbol, transitions, initial_state, final_states):
        self.states = states
        self.input_alphabet = input_alphabet
        self.tape_alphabet = tape_alphabet
        self.blank = blank_symbol
        self.transitions = transitions
        self.initial_state = initial_state

        self.current_state = initial_state
        self.final_states = final_states
        self.mem_cache_value = blank_symbol  # Valor en caché (inicialmente blank)
        self.tape = []
        self.head = 0

    def load_tape(self, input_string):
        self.tape = list(input_string) if input_string else []
        self.head = 0
        self.current_state = self.initial_state
        self.mem_cache_value = self.blank  # Inicializar caché como blank

    def step(self):
        # Leer símbolo actual de la cinta
        tape_symbol = self.tape[self.head] if self.head < len(self.tape) else self.blank
        
        # La clave ahora incluye: (estado_actual, valor_en_caché, símbolo_en_cinta)
        key = (self.current_state, self.mem_cache_value, tape_symbol)
        
        if key not in self.transitions:
            return False  # No hay transición → detiene
        
        # Desempacar la transición: (nuevo_estado, nuevo_caché, símbolo_a_escribir, dirección)
        new_state, new_cache, new_symbol, direction = self.transitions[key]
        
        # Escribir en la cinta
        if self.head < len(self.tape):
            self.tape[self.head] = new_symbol
        else:
            self.tape.append(new_symbol)
        
        # Actualizar estado y caché
        self.current_state = new_state
        self.mem_cache_value = new_cache
        
        # Mover el cabezal: R (derecha), L (izquierda), S (stay/quedarse)
        if direction == 'R':
            self.head += 1
        elif direction == 'L':
            self.head -= 1
        # Si es 'S', no hacemos nada (se queda en la misma posición)
        
        # Ajustar la cinta si el cabezal se sale de los límites
        if self.head < 0:
            self.tape.insert(0, self.blank)
            self.head = 0
        elif self.head >= len(self.tape):
            self.tape.append(self.blank)
        
        return True

    def run(self, max_steps=1000):
        steps = 0
        while steps < max_steps:
            print(self.get_configuration())
            if not self.step():
                break
            steps += 1
        return self.current_state in self.final_states

    def get_configuration(self):
        # Mostrar configuración con estado, caché, posición del cabezal y cinta
        cache_display = repr(self.mem_cache_value) if self.mem_cache_value != self.blank else 'B'
        state_display = f"[{self.current_state}, {cache_display}]"
        tape_str = f"{self.tape[:self.head]}{state_display}{self.tape[self.head:]}"
        return f"Cabeza: {self.head:3d} | Estado: {self.current_state} | Cache: {cache_display} | Cinta: {tape_str}"
