"""Simulación de señales y transformada discreta de Fourier.
Requisitos: Python 3, NumPy y Matplotlib.
Ejecutar: python simulacion_fourier.py
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Muestreo uniforme de dos segundos a 1 kHz.
fs = 1000.0
N = 2000
dt = 1 / fs
t = np.arange(N) / fs - 1.0

# Señales elementales. El escalón se observa en una ventana finita.
pulso = (np.abs(t) < 0.1).astype(float)
escalon = (t >= 0).astype(float)
senoide = np.sin(2 * np.pi * 50 * t)
senales = [("Pulso rectangular", pulso), ("Escalón unitario", escalon),
           ("Senoide de 50 Hz", senoide)]
frecuencia = np.fft.rfftfreq(N, d=dt)

def espectro_amplitud(x):
    """Espectro unilateral con amplitud normalizada para señales reales."""
    magnitud = np.abs(np.fft.rfft(x)) / N
    magnitud[1:-1] *= 2  # No duplicar DC ni Nyquist.
    return magnitud

fig, axes = plt.subplots(3, 2, figsize=(12, 9), constrained_layout=True)
for i, (nombre, x) in enumerate(senales):
    X = np.fft.rfft(x)
    magnitud = espectro_amplitud(x)
    fase = np.angle(X)
    axes[i, 0].plot(t, x, color="#12847e")
    axes[i, 0].set_xlim(-0.5, 0.5)
    axes[i, 0].set_title(f"{nombre}: dominio del tiempo")
    axes[i, 0].set_xlabel("Tiempo (s)"); axes[i, 0].set_ylabel("Amplitud")
    axes[i, 0].grid(True, alpha=.25)
    axes[i, 1].plot(frecuencia, magnitud, color="#2e75b6", label="Magnitud")
    axes[i, 1].set_xlim(0, 120)
    axes[i, 1].set_title(f"{nombre}: magnitud del espectro")
    axes[i, 1].set_xlabel("Frecuencia (Hz)"); axes[i, 1].set_ylabel("Amplitud")
    axes[i, 1].grid(True, alpha=.25)
    # La fase se guarda en gráfico adicional para mantener legible la comparación.
fig.suptitle("Señales elementales y transformada discreta de Fourier")
fig.savefig("senales_tiempo_espectro.png", dpi=180)
plt.close(fig)

# Fase espectral de cada señal (se interpreta con cautela donde la magnitud es casi cero).
fig, axes = plt.subplots(3, 1, figsize=(10, 8), constrained_layout=True)
for ax, (nombre, x) in zip(axes, senales):
    X = np.fft.rfft(x)
    fase = np.angle(X)
    fase[np.abs(X) < 1e-8] = np.nan
    ax.plot(frecuencia, fase, color="#ad5c2a")
    ax.set_xlim(0, 120); ax.set_ylim(-np.pi, np.pi)
    ax.set_title(nombre); ax.set_ylabel("Fase (rad)"); ax.grid(True, alpha=.25)
axes[-1].set_xlabel("Frecuencia (Hz)")
fig.suptitle("Fase del espectro (saltos de fase en bins de baja magnitud)")
fig.savefig("fase_espectral.png", dpi=180)
plt.close(fig)

# Propiedad de linealidad: se compara la FFT de una combinación con la combinación de FFT.
a, b = 1.7, -0.4
error_linealidad = np.max(np.abs(np.fft.fft(a*pulso + b*senoide) -
                                  (a*np.fft.fft(pulso) + b*np.fft.fft(senoide))))
# Desplazamiento circular de 125 muestras: la magnitud se mantiene y cambia la fase.
retardo = 125
X = np.fft.fft(pulso)
X_retardada = np.fft.fft(np.roll(pulso, retardo))
f_norm = np.fft.fftfreq(N)
factor_fase = np.exp(-2j*np.pi*f_norm*retardo)
error_desplazamiento = np.max(np.abs(X_retardada - X*factor_fase))

# Escalamiento en tiempo: reducir el ancho del pulso a la mitad ensancha el espectro.
pulso_comprimido = (np.abs(t) < 0.05).astype(float)
fig, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)
for x, etiqueta in [(pulso, "ancho 0.20 s"), (pulso_comprimido, "ancho 0.10 s")]:
    ax.plot(frecuencia, espectro_amplitud(x), label=etiqueta)
ax.set_xlim(0, 40); ax.set_xlabel("Frecuencia (Hz)"); ax.set_ylabel("Amplitud")
ax.set_title("Compresión temporal y expansión del espectro"); ax.grid(True, alpha=.25); ax.legend()
fig.savefig("escalamiento_frecuencia.png", dpi=180)
plt.close(fig)
print(f"Error de linealidad: {error_linealidad:.3e}")
print(f"Error de desplazamiento: {error_desplazamiento:.3e}")
print("Las gráficas PNG se guardaron en el directorio actual.")
