from scipy.spatial import distance
from collections import deque

class Road:
    def __init__(self, start, end):
        self.start = start
        self.end = end

        self.vehicles = deque()

        self.init_properties()

    def init_properties(self):
        self.length = distance.euclidean(self.start, self.end)
        self.angle_sin = (self.end[1]-self.start[1]) / self.length
        self.angle_cos = (self.end[0]-self.start[0]) / self.length
        # self.angle = np.arctan2(self.end[1]-self.start[1], self.end[0]-self.start[0])
        self.has_traffic_signal = False

    def set_traffic_signal(self, signal, group):
        self.traffic_signal = signal
        self.traffic_signal_group = group
        self.has_traffic_signal = True

    @property
    def traffic_signal_state(self):
        if self.has_traffic_signal:
            i = self.traffic_signal_group
            return self.traffic_signal.current_cycle[i]
        return True

    def update(self, dt):
        n = len(self.vehicles)

        if n > 0:
            # Actualizar el primer vehículo
            self.vehicles[0].update(None, dt)
            # Actualizar los demás vehículos
            for i in range(1, n):
                lead = self.vehicles[i-1]
                self.vehicles[i].update(lead, dt)

             # Verificar el estado del semáforo
            if self.traffic_signal_state:
                # Si el semáforo está en verde o no existe
                # Entonces deja pasar a los vehículos
                self.vehicles[0].unstop()
                for vehicle in self.vehicles:
                    vehicle.unslow()
            else:
                # Si el semáforo está en rojo
                if self.vehicles[0].x >= self.length - self.traffic_signal.slow_distance:
                    # Reducir la velocidad de los vehículos en la zona de desaceleración
                    self.vehicles[0].slow(self.traffic_signal.slow_factor*self.vehicles[0]._v_max)
                if self.vehicles[0].x >= self.length - self.traffic_signal.stop_distance and\
                   self.vehicles[0].x <= self.length - self.traffic_signal.stop_distance / 2:
                    # Detener los vehículos en la zona de parada
                    self.vehicles[0].stop()
