# Simulación y análisis de señales con Fourier

Proyecto para la Actividad formativa 2. La simulación compara un pulso rectangular, un escalón unitario y una senoide de 50 Hz en los dominios del tiempo y frecuencia. Verifica linealidad, desplazamiento temporal circular y escalamiento temporal.

## Requisitos
- Python 3.9 o posterior
- NumPy
- Matplotlib

Instalación: `python -m pip install numpy matplotlib`

## Ejecución
`python simulacion_fourier.py`

El script genera `senales_tiempo_espectro.png`, `fase_espectral.png` y `escalamiento_frecuencia.png` en el directorio actual.

## Parámetros
Frecuencia de muestreo: 1 kHz; muestras: 2,000; duración: 2 s; resolución espectral: 0.5 Hz. La FFT calcula la DFT de la señal muestreada; el escalón y pulso se observan dentro de una ventana finita.

## Archivos
- `simulacion_fourier.py`: código comentado de la simulación.
- `resultados.csv`: errores de verificación y lectura.
- `Informe_Fourier.docx`: desarrollo, gráficas, análisis, conclusión y referencias.
- `Presentacion_Fourier.pptx`: apoyo para la exposición.

Para publicarlo, crea un repositorio vacío en GitHub, agrega estos archivos con `git add`, confirma con `git commit` y enlaza el repositorio remoto antes de `git push`.
