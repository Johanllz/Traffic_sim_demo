import subprocess
import re

def run_and_capture(script):
    result = subprocess.run(['python', script], capture_output=True, text=True)
    return result.stdout

def extract_time(output, label):
    match = re.search(rf"{label}:\s*([\d\.]+)", output)
    return float(match.group(1)) if match else None

def extract_metric(output, label):
    match = re.search(rf"{label}:\s*([^\n]+)", output)
    return match.group(1).strip() if match else "N/A"

# Etiquetas y nombres legibles
metric_labels = [
    ("Tiempo simulado", "Tiempo simulado (s)"),
    ("Frames simulados", "Frames simulados"),
    ("Vehículos que pasaron", "Vehículos que pasaron"),
    ("Vehículos presentes", "Vehículos presentes"),
    ("Tasa de vehículos", "Tasa de vehículos"),
    ("Densidad de tráfico", "Densidad de tráfico"),
    ("Duración del ciclo del semáforo", "Duración del ciclo del semáforo"),
    ("Número de carreteras", "Número de carreteras"),
    ("Número de semáforos", "Número de semáforos"),
]

# Ejecutar secuencial
print("Ejecutando versión secuencial...")
out_seq = run_and_capture('main.py')
print("Ejecutando versión paralela...")
out_par = run_and_capture('main_parallel.py')

# Extraer métricas
seq_time = extract_time(out_seq, "Tiempo de ejecución secuencial")
par_time = extract_time(out_par, "Tiempo de ejecución paralelo")

# Mostrar métricas principales con etiquetas
print("\n--- Métricas versión secuencial ---")
for label, pretty in metric_labels:
    print(f"{pretty}: {extract_metric(out_seq, label)}")

print("\n--- Métricas versión paralela ---")
for label, pretty in metric_labels:
    print(f"{pretty}: {extract_metric(out_par, label)}")

# Calcular speedup y eficiencia
if seq_time and par_time:
    speedup = seq_time / par_time
    num_processors = 6 # Ajusta según tu CPU
    efficiency = speedup / num_processors
    print("\n--- Comparación automática ---")
    print(f"Tiempo secuencial: {seq_time:.2f} s")
    print(f"Tiempo paralelo: {par_time:.2f} s")
    print(f"Speedup: {speedup:.2f}")
    print(f"Eficiencia: {efficiency:.2f}")
else:
    print("No se pudieron extraer los tiempos correctamente.")
