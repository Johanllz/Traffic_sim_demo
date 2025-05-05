from .vehicle import Vehicle
from numpy.random import randint

class VehicleGenerator:
    def __init__(self, sim, config={}):
        self.sim = sim

        # Establecer configuraciones predeterminadas
        self.set_default_config()

        # Actualizar configuraciones
        for attr, val in config.items():
            setattr(self, attr, val)

        # Calcular propiedades
        self.init_properties()

    def set_default_config(self):
        """Establecer configuración predeterminada"""
        self.vehicle_rate = 20
        self.vehicles = [
            (1, {})
        ]
        self.last_added_time = 0

    def init_properties(self):
        self.upcoming_vehicle = self.generate_vehicle()

    def generate_vehicle(self):
        """Devuelve un vehículo aleatorio de self.vehicles con proporciones aleatorias"""
        total = sum(pair[0] for pair in self.vehicles)
        r = randint(1, total+1)
        for (weight, config) in self.vehicles:
            r -= weight
            if r <= 0:
                return Vehicle(config)

    def update(self):
        """Agregar vehículos"""
        if self.sim.t - self.last_added_time >= 60 / self.vehicle_rate:
            # Si el tiempo transcurrido desde el último vehículo agregado
            # es mayor que el período de generación de vehículos, generar un vehículo
            road = self.sim.roads[self.upcoming_vehicle.path[0]]      
            if len(road.vehicles) == 0\
               or road.vehicles[-1].x > self.upcoming_vehicle.s0 + self.upcoming_vehicle.l:
                # Si hay espacio para el vehículo generado, agregarlo
                self.upcoming_vehicle.time_added = self.sim.t
                road.vehicles.append(self.upcoming_vehicle)
                # Reiniciar last_added_time y upcoming_vehicle
                self.last_added_time = self.sim.t
            self.upcoming_vehicle = self.generate_vehicle()

    def delete_all_vehicles(self):
        # Eliminar todos los vehículos de las carreteras
        for road in self.sim.roads:
            road.vehicles.clear()
        self.last_added_time = 0
