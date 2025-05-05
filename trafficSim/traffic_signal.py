import random

class TrafficSignal:
    def __init__(self, roads, config={}):
        # Inicializar carreteras
        self.roads = roads
        # Establecer configuración predeterminada
        self.set_default_config()

        # Actualizar configuración
        for attr, val in config.items():
            setattr(self, attr, val)
        # Calcular propiedades
        self.init_properties()

    def set_default_config(self):
        self.cycle = [(False, False, False, True), (False, False, True, False), (False, True, False, False), (True, False, False, False)]
        self.slow_distance = 50  # Distancia para reducir la velocidad
        self.slow_factor = 0.4   # Factor de reducción de velocidad
        self.stop_distance = 12  # Distancia para detenerse
        self.cycle_length = 1    # Duración del ciclo del semáforo

        self.current_cycle_index = 0  # Índice del ciclo actual

        self.last_t = 0  # Último tiempo registrado

    def init_properties(self):
        # Configurar semáforo para cada carretera
        for i in range(len(self.roads)):
            for road in self.roads[i]:
                road.set_traffic_signal(self, i)

    @property
    def current_cycle(self):
        # Obtener el ciclo actual del semáforo
        return self.cycle[self.current_cycle_index]
    
    def update(self, sim):
        cycle_length = self.cycle_length
        # Aleatorizar la duración del ciclo después de cada ciclo
        if(sim.t % cycle_length == 0):
            cycle_length = random.randint(20, 40)
        k = (sim.t // cycle_length) % 4
        self.current_cycle_index = int(k)
        if(len(self.roads) < 4):
            self.current_cycle_index = 3
