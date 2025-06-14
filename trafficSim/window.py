import pygame
from pygame import gfxdraw
import numpy as np

class Window:
    def __init__(self, sim, config={}):
        # Simulación a dibujar
        self.sim = sim

        # Establecer configuraciones predeterminadas
        self.set_default_config()

        # Actualizar configuraciones
        for attr, val in config.items():
            setattr(self, attr, val)
        
    def set_default_config(self):
        """Establecer configuración predeterminada"""
        self.width = 1400
        self.height = 900
        self.bg_color = (250, 250, 250)

        self.fps = 60
        self.zoom = 5
        self.offset = (0, 0)

        self.mouse_last = (0, 0)
        self.mouse_down = False

        # Invertir eje x
        self.flip_x = True

    def loop(self, loop=None):
        """Muestra una ventana visualizando la simulación y ejecuta la función loop."""
        # Crear una ventana de pygame
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.flip()

        # FPS fijo
        clock = pygame.time.Clock()

        # Para dibujar texto
        pygame.font.init()
        self.text_font = pygame.font.SysFont('Lucida Console', 16)

        # Bucle de dibujo
        running = True
        while running:
            # Actualizar simulación
            if loop: loop(self.sim)

            # Dibujar simulación
            self.draw()

            # Actualizar ventana
            pygame.display.update()
            clock.tick(self.fps)

            # Manejar todos los eventos
            for event in pygame.event.get():
                # Salir del programa si se cierra la ventana
                if event.type == pygame.QUIT:
                    running = False
                # Manejar eventos del ratón
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Si se presiona un botón del ratón
                    if event.button == 1:
                        # Clic izquierdo
                        x, y = pygame.mouse.get_pos()
                        x0, y0 = self.offset
                        self.mouse_last = (x-x0*self.zoom, y-y0*self.zoom)
                        self.mouse_down = True
                    if event.button == 4:
                        # Rueda del ratón hacia arriba
                        self.zoom *=  (self.zoom**2+self.zoom/4+1) / (self.zoom**2+1)
                    if event.button == 5:
                        # Rueda del ratón hacia abajo
                        self.zoom *= (self.zoom**2+1) / (self.zoom**2+self.zoom/4+1)
                elif event.type == pygame.MOUSEMOTION:
                    # Arrastrar contenido
                    if self.mouse_down:
                        x1, y1 = self.mouse_last
                        x2, y2 = pygame.mouse.get_pos()
                        self.offset = ((x2-x1)/self.zoom, (y2-y1)/self.zoom)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_down = False           

    def run(self, steps_per_update=1, max_frames=None):
        """Ejecuta la simulación actualizando en cada iteración del bucle."""
        def loop(sim):
            sim.run(steps_per_update)
        # Modificación: pasar max_frames al bucle
        self.loop_with_stop(loop, max_frames)

    def loop_with_stop(self, loop=None, max_frames=None):
        """Muestra una ventana visualizando la simulación y ejecuta la función loop, deteniéndose en max_frames."""
        # Crear una ventana de pygame
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.flip()

        # FPS fijo
        clock = pygame.time.Clock()

        # Para dibujar texto
        pygame.font.init()
        self.text_font = pygame.font.SysFont('Lucida Console', 16)

        # Bucle de dibujo
        running = True
        while running:
            # Actualizar simulación
            if loop: loop(self.sim)

            # Dibujar simulación
            self.draw()

            # Actualizar ventana
            pygame.display.update()
            clock.tick(self.fps)

            # Manejar todos los eventos
            for event in pygame.event.get():
                # Salir del programa si se cierra la ventana
                if event.type == pygame.QUIT:
                    running = False
                # Manejar eventos del ratón
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Si se presiona un botón del ratón
                    if event.button == 1:
                        # Clic izquierdo
                        x, y = pygame.mouse.get_pos()
                        x0, y0 = self.offset
                        self.mouse_last = (x-x0*self.zoom, y-y0*self.zoom)
                        self.mouse_down = True
                    if event.button == 4:
                        # Rueda del ratón hacia arriba
                        self.zoom *=  (self.zoom**2+self.zoom/4+1) / (self.zoom**2+1)
                    if event.button == 5:
                        # Rueda del ratón hacia abajo
                        self.zoom *= (self.zoom**2+1) / (self.zoom**2+self.zoom/4+1)
                elif event.type == pygame.MOUSEMOTION:
                    # Arrastrar contenido
                    if self.mouse_down:
                        x1, y1 = self.mouse_last
                        x2, y2 = pygame.mouse.get_pos()
                        self.offset = ((x2-x1)/self.zoom, (y2-y1)/self.zoom)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_down = False
            # Detener automáticamente al llegar a max_frames
            if max_frames is not None and self.sim.frame_count >= max_frames:
                running = False

    def convert(self, x, y=None):
        """Convierte coordenadas de la simulación a coordenadas de la pantalla"""
        if isinstance(x, list):
            return [self.convert(e[0], e[1]) for e in x]
        if isinstance(x, tuple):
            return self.convert(*x)
        return (
            int(self.width/2 + (x + self.offset[0])*self.zoom),
            int(self.height/2 + (y + self.offset[1])*self.zoom)
        )

    def inverse_convert(self, x, y=None):
        """Convierte coordenadas de la pantalla a coordenadas de la simulación"""
        if isinstance(x, list):
            return [self.convert(e[0], e[1]) for e in x]
        if isinstance(x, tuple):
            return self.convert(*x)
        return (
            int(-self.offset[0] + (x - self.width/2)/self.zoom),
            int(-self.offset[1] + (y - self.height/2)/self.zoom)
        )

    def background(self, r, g, b):
        """Rellena la pantalla con un color."""
        self.screen.fill((r, g, b))

    def line(self, start_pos, end_pos, color):
        """Dibuja una línea."""
        gfxdraw.line(
            self.screen,
            *start_pos,
            *end_pos,
            color
        )

    def rect(self, pos, size, color):
        """Dibuja un rectángulo."""
        gfxdraw.rectangle(self.screen, (*pos, *size), color)

    def box(self, pos, size, color):
        """Dibuja un rectángulo relleno."""
        gfxdraw.box(self.screen, (*pos, *size), color)

    def circle(self, pos, radius, color, filled=True):
        """Dibuja un círculo."""
        gfxdraw.aacircle(self.screen, *pos, radius, color)
        if filled:
            gfxdraw.filled_circle(self.screen, *pos, radius, color)

    def polygon(self, vertices, color, filled=True):
        """Dibuja un polígono."""
        gfxdraw.aapolygon(self.screen, vertices, color)
        if filled:
            gfxdraw.filled_polygon(self.screen, vertices, color)

    def rotated_box(self, pos, size, angle=None, cos=None, sin=None, centered=True, color=(0, 0, 255), filled=True):
        """Dibuja un rectángulo centrado en *pos* con tamaño *size* rotado en sentido antihorario por *angle*."""
        x, y = pos
        l, h = size

        if angle:
            cos, sin = np.cos(angle), np.sin(angle)
        
        vertex = lambda e1, e2: (
            x + (e1*l*cos + e2*h*sin)/2,
            y + (e1*l*sin - e2*h*cos)/2
        )

        if centered:
            vertices = self.convert(
                [vertex(*e) for e in [(-1,-1), (-1, 1), (1,1), (1,-1)]]
            )
        else:
            vertices = self.convert(
                [vertex(*e) for e in [(0,-1), (0, 1), (2,1), (2,-1)]]
            )

        self.polygon(vertices, color, filled=filled)

    def rotated_rect(self, pos, size, angle=None, cos=None, sin=None, centered=True, color=(0, 0, 255)):
        """Dibuja un rectángulo rotado sin relleno."""
        self.rotated_box(pos, size, angle=angle, cos=cos, sin=sin, centered=centered, color=color, filled=False)

    def arrow(self, pos, size, angle=None, cos=None, sin=None, color=(150, 150, 190)):
        """Dibuja una flecha."""
        if angle:
            cos, sin = np.cos(angle), np.sin(angle)
        
        self.rotated_box(
            pos,
            size,
            cos=(cos - sin) / np.sqrt(2),
            sin=(cos + sin) / np.sqrt(2),
            color=color,
            centered=False
        )

        self.rotated_box(
            pos,
            size,
            cos=(cos + sin) / np.sqrt(2),
            sin=(sin - cos) / np.sqrt(2),
            color=color,
            centered=False
        )

    def draw_axes(self, color=(100, 100, 100)):
        """Dibuja los ejes x e y."""
        x_start, y_start = self.inverse_convert(0, 0)
        x_end, y_end = self.inverse_convert(self.width, self.height)
        self.line(
            self.convert((0, y_start)),
            self.convert((0, y_end)),
            color
        )
        self.line(
            self.convert((x_start, 0)),
            self.convert((x_end, 0)),
            color
        )

    def draw_grid(self, unit=50, color=(150,150,150)):
        """Dibuja una cuadrícula."""
        x_start, y_start = self.inverse_convert(0, 0)
        x_end, y_end = self.inverse_convert(self.width, self.height)

        n_x = int(x_start / unit)
        n_y = int(y_start / unit)
        m_x = int(x_end / unit)+1
        m_y = int(y_end / unit)+1

        for i in range(n_x, m_x):
            self.line(
                self.convert((unit*i, y_start)),
                self.convert((unit*i, y_end)),
                color
            )
        for i in range(n_y, m_y):
            self.line(
                self.convert((x_start, unit*i)),
                self.convert((x_end, unit*i)),
                color
            )

    def draw_roads(self):
        """Dibuja las carreteras."""
        for road in self.sim.roads:
            # Dibujar fondo de la carretera
            self.rotated_box(
                road.start,
                (road.length, 3.7),
                cos=road.angle_cos,
                sin=road.angle_sin,
                color=(180, 180, 220),
                centered=False
            )
            # Dibujar líneas de la carretera
            # self.rotated_box(
            #     road.start,
            #     (road.length, 0.25),
            #     cos=road.angle_cos,
            #     sin=road.angle_sin,
            #     color=(0, 0, 0),
            #     centered=False
            # )

            # Dibujar flecha de la carretera
            if road.length > 5: 
                for i in np.arange(-0.5*road.length, 0.5*road.length, 10):
                    pos = (
                        road.start[0] + (road.length/2 + i + 3) * road.angle_cos,
                        road.start[1] + (road.length/2 + i + 3) * road.angle_sin
                    )

                    self.arrow(
                        pos,
                        (-1.25, 0.2),
                        cos=road.angle_cos,
                        sin=road.angle_sin
                    )   

    def draw_vehicle(self, vehicle, road):
        """Dibuja un vehículo en una carretera."""
        l, h = vehicle.l,  vehicle.h
        sin, cos = road.angle_sin, road.angle_cos

        x = road.start[0] + cos * vehicle.x 
        y = road.start[1] + sin * vehicle.x 

        self.rotated_box((x, y), (l, h), cos=cos, sin=sin, color=vehicle.color, centered=True)

    def draw_vehicles(self):
        """Dibuja todos los vehículos en las carreteras."""
        for road in self.sim.roads:
            # Dibujar vehículos
            for vehicle in road.vehicles:
                self.draw_vehicle(vehicle, road)

    def draw_signals(self):
        """Dibuja los semáforos."""
        for signal in self.sim.traffic_signals:
            for i in range(len(signal.roads)):
                color = (0, 255, 0) if signal.current_cycle[i] else (255, 0, 0)
                for road in signal.roads[i]:
                    a = 0
                    position = (
                        (1-a)*road.end[0] + a*road.start[0],        
                        (1-a)*road.end[1] + a*road.start[1]
                    )
                    self.rotated_box(
                        position,
                        (1, 3),
                        cos=road.angle_cos, sin=road.angle_sin,
                        color=color)
                    

    def draw_status(self):
        """Dibuja información de estado en la pantalla."""
        text_fps = self.text_font.render(f'Tiempo={self.sim.t:.5}', False, (0, 0, 0))
        text_frc = self.text_font.render(f'Frames={self.sim.frame_count}', False, (0, 0, 0))
        vehicles_passed = int(self.sim.vehiclesPassed)
        text_vehicles_passed = self.text_font.render(f'Vehículos Pasados={vehicles_passed}', False, (0, 0, 0))
        text_vehicles_present = self.text_font.render(f'Vehículos Presentes={self.sim.vehiclesPresent}', False, (0, 0, 0))
        text_average_vehicles_per_minute = self.text_font.render(f'AVG Vehículos Por Minuto={int(vehicles_passed/self.sim.t*60)}', False, (0, 0, 0))
        text_total_vehicles = self.text_font.render(f'Total Vehículos={vehicles_passed + self.sim.vehiclesPresent}', False, (0, 0, 0))
        text_vehicle_rate = self.text_font.render(f'Tasa de Vehículos={self.sim.vehicleRate}', False, (0, 0, 0))

        # Añadir rectángulo blanco
        self.screen.fill((255, 255, 255), (0, 0, 1400, 40))
        self.screen.blit(text_fps, (0, 0))
        self.screen.blit(text_frc, (100, 0))
        self.screen.blit(text_vehicles_passed, (200, 0))
        self.screen.blit(text_vehicles_present, (400, 0))
        self.screen.blit(text_average_vehicles_per_minute, (630, 0))
        self.screen.blit(text_total_vehicles, (0, 20))
        self.screen.blit(text_vehicle_rate, (200, 20))

        if self.sim.isPaused:
            text_pause = self.text_font.render(f'Reanudar', False, (0, 0, 0))
        else:
            text_pause = self.text_font.render(f'Pausar', False, (0, 0, 0))
        self.screen.blit(text_pause, (1000, 0))

    def draw(self):
        """Dibuja todos los elementos de la simulación."""
        # Rellenar fondo
        self.background(*self.bg_color)

        # Cuadrícula mayor y menor y ejes
        self.draw_grid(10, (220,220,220))
        self.draw_grid(100, (200,200,200))
        self.draw_axes()

        self.draw_roads()
        self.draw_vehicles()
        self.draw_signals()

        # Dibujar información de estado
        self.draw_status()
