from .road import Road
from copy import deepcopy
from .vehicle_generator import VehicleGenerator
from .traffic_signal import TrafficSignal
import csv

class Simulation:
    vehiclesPassed = 0;
    vehiclesPresent = 0;
    vehicleRate = 0;
    isPaused = False;

    def __init__(self, config={}):
        # Establecer configuración predeterminada
        self.set_default_config()

        # Actualizar configuración
        for attr, val in config.items():
            setattr(self, attr, val)

    def set_default_config(self):
        self.t = 0.0            # Control del tiempo
        self.frame_count = 0    # Control del conteo de fotogramas
        self.dt = 1/60          # Paso de tiempo de la simulación
        self.roads = []         # Arreglo para almacenar carreteras
        self.generators = []    # Generadores de vehículos
        self.traffic_signals = [] # Semáforos
        self.iteration = 0      # n-ésima iteración (para muestreo, si está habilitado)

    def create_road(self, start, end):
        road = Road(start, end)
        self.roads.append(road)
        return road

    def create_roads(self, road_list):
        # Crear múltiples carreteras
        for road in road_list:
            self.create_road(*road)

    def create_gen(self, config={}):
        # Crear un generador de vehículos
        gen = VehicleGenerator(self, config)
        self.generators.append(gen)
        Simulation.vehicleRate = gen.vehicle_rate
        return gen

    def create_signal(self, roads, config={}):
        # Crear un semáforo
        roads = [[self.roads[i] for i in road_group] for road_group in roads]
        sig = TrafficSignal(roads, config)
        self.traffic_signals.append(sig)
        return sig

    def update(self):
        # Actualizar cada carretera
        for road in self.roads:
            road.update(self.dt)

        # Agregar vehículos
        for gen in self.generators:
            gen.update()

        # Actualizar semáforos
        for signal in self.traffic_signals:
            signal.update(self)

        # Verificar carreteras para vehículos fuera de límites
        for road in self.roads:
            # Si la carretera no tiene vehículos, continuar
            if len(road.vehicles) == 0: continue
            # Si no
            vehicle = road.vehicles[0]
            # Si el primer vehículo está fuera de los límites de la carretera
            if vehicle.x >= road.length:
                # Si el vehículo tiene una carretera siguiente
                if vehicle.current_road_index + 1 < len(vehicle.path):
                    # Actualizar la carretera actual a la siguiente
                    vehicle.current_road_index += 1
                    # Crear una copia y reiniciar algunas propiedades del vehículo
                    new_vehicle = deepcopy(vehicle)
                    new_vehicle.x = 0
                    # Agregarlo a la siguiente carretera
                    next_road_index = vehicle.path[vehicle.current_road_index]
                    self.roads[next_road_index].vehicles.append(new_vehicle)
                else:
                    Simulation.vehiclesPassed += 1
                # En todos los casos, eliminarlo de su carretera
                road.vehicles.popleft()

        # Verificar el número de vehículos presentes
        Simulation.vehiclesPresent = 0
        for road in self.roads:
            Simulation.vehiclesPresent += len(road.vehicles)

        # Incrementar el tiempo
        self.t += self.dt
        self.frame_count += 1

        # Detener en cierto tiempo en segundos (para propósitos de muestreo. Comentar si no es necesario)
        self.time_limit = 100
        if self.t >= self.time_limit:
            print("Duración del ciclo del semáforo: " + str(self.traffic_signals[0].cycle_length))
            print("Tiempo: " + str(self.t))
            print("Vehículos que pasaron: " + str(Simulation.vehiclesPassed))
            print("Vehículos presentes: " + str(Simulation.vehiclesPresent))
            print("Tasa de vehículos: " + str(Simulation.vehicleRate))
            print("Densidad de tráfico: " + str(Simulation.vehiclesPresent / (len(self.roads) * self.roads[0].length)))
            print("Iteración: " + str(self.iteration))

            # Agregar al CSV el tiempo y los vehículos que pasaron
            with open('data.csv', mode='a') as data_file:
                data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data_writer.writerow([self.traffic_signals[0].cycle_length, Simulation.vehiclesPassed])

            # Reiniciar tiempo y vehículos que pasaron
            self.t = 0.001
            gen.delete_all_vehicles()
            Simulation.vehiclesPassed = 0
            Simulation.vehiclesPresent = 0
            self.iteration += 1
            if self.iteration % 5 == 0:
                # Incrementar en 1 la duración del ciclo de todos los semáforos
                for signal in self.traffic_signals:
                    signal.cycle_length += 1

    def run(self, steps):
        # Ejecutar la simulación por un número de pasos
        for _ in range(steps):
            self.update()

    def pause(self):
        # Pausar la simulación
        self.isPaused = True

    def resume(self):
        # Reanudar la simulación
        self.isPaused = False