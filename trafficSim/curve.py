def curve_points(start, end, control, resolution=5):
	# Si la curva es una línea recta
	if (start[0] - end[0])*(start[1] - end[1]) == 0:
		return [start, end]

	# Si no, devuelve una curva
	path = []

	for i in range(resolution+1):
		t = i/resolution
		x = (1-t)**2 * start[0] + 2*(1-t)*t * control[0] + t**2 *end[0]
		y = (1-t)**2 * start[1] + 2*(1-t)*t * control[1] + t**2 *end[1]
		path.append((x, y))

	return path

def curve_road(start, end, control, resolution=15):
	points = curve_points(start, end, control, resolution=resolution)
	return [(points[i-1], points[i]) for i in range(1, len(points))]

TURN_LEFT = 0
TURN_RIGHT = 1
def turn_road(start, end, turn_direction, resolution=15):
	# Obtener el punto de control
	x = min(start[0], end[0])
	y = min(start[1], end[1])

	if turn_direction == TURN_LEFT:
		control = (
			x - y + start[1],
			y - x + end[0]
		)
	else:
		control = (
			x - y + end[1],
			y - x + start[0]
		)
	
	return curve_road(start, end, control, resolution=resolution)

