import cv2
import numpy as np

def obtener_tres_rangos_verdes(imagen_path):
    # Cargar la imagen
    img = cv2.imread(imagen_path)

    # Convertir la imagen de BGR a RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Convertir la imagen a una lista plana de píxeles
    pixels = img_rgb.reshape((-1, 3))

    # Calcular el histograma de los píxeles en el espacio RGB
    histograma = np.histogramdd(pixels, bins=(256, 256, 256), range=((0, 256), (0, 256), (0, 256)))[0]

    # Encontrar los índices de los tres colores verdes más grandes en el histograma
    indices_verdes = np.unravel_index(np.argsort(histograma[:, :, 1], axis=None)[-3:], histograma[:, :, 1].shape)

    # Obtener los tres rangos de colores verdes en términos de RGB
    rangos_verdes = []
    for i in range(3):
        rango_desde = (
            indices_verdes[0][i],
            indices_verdes[1][i],
            0  # Fijar el componente azul a 0 para indicar "desde"
        )

        rango_hasta = (
            indices_verdes[0][i] + 1,
            indices_verdes[1][i] + 1,
            256  # Fijar el componente azul a 256 para indicar "hasta"
        )

        rangos_verdes.append((rango_desde, rango_hasta))

    return rangos_verdes

if __name__ == "__main__":
    imagen_path = "Fotos/8.jpg"

    rangos_verdes = obtener_tres_rangos_verdes(imagen_path)

    for i, rango in enumerate(rangos_verdes):
        print(f"Rango de colores verdes {i + 1} (RGB):")
        print(f"Desde R:{rango[0][0]}, G:{rango[0][1]}, B:{rango[0][2]}")
        print(f"Hasta R:{rango[1][0]}, G:{rango[1][1]}, B:{rango[1][2]}")
        print()
