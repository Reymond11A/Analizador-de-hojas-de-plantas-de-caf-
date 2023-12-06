from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt

def recortar_hoja(imagen):
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    _, umbral = cv2.threshold(gris, 128, 255, cv2.THRESH_BINARY)
    contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Encontrar el contorno más grande (suponiendo que sea la hoja)
    contorno_hoja = max(contornos, key=cv2.contourArea)

    # Crear una máscara de la hoja
    mascara_hoja = np.zeros_like(gris)
    cv2.drawContours(mascara_hoja, [contorno_hoja], -1, 255, thickness=cv2.FILLED)

    # Aplicar la máscara para recortar la imagen
    imagen_recortada = cv2.bitwise_and(imagen, imagen, mask=mascara_hoja)

    return imagen_recortada

def detectar_rango_colores(image_path, rangos_colores, umbral_porcentaje):
    # Abrir la imagen
    imagen = Image.open(image_path)
    
    # Convertir la imagen a un arreglo de NumPy
    imagen_np = np.array(imagen)

    # Detección de contornos y segmentación
    imagen_recortada = recortar_hoja(imagen_np)

    # Mostrar la imagen recortada en la consola
    plt.imshow(cv2.cvtColor(imagen_recortada, cv2.COLOR_BGR2RGB))
    plt.title("Imagen Recortada")
    plt.show()

    # Obtener dimensiones de la imagen recortada
    alto, ancho, _ = imagen_recortada.shape

    # Contador para el número de píxeles dentro del rango de colores
    contador_colores = 0

    # Iterar sobre cada píxel de la imagen recortada
    for i in range(alto):
        for j in range(ancho):
            # Obtener el color del píxel en formato RGB
            color_pixel = imagen_recortada[i, j, :3]

            # Verificar si el color del píxel está dentro de al menos un rango permitido
            if any(all(min_c <= c <= max_c for c, min_c, max_c in zip(color_pixel, *rango)) for rango in rangos_colores):
                contador_colores += 1

    # Calcular el porcentaje de píxeles dentro del rango de colores
    porcentaje_colores = (contador_colores / (alto * ancho)) * 100

    # Determinar si el porcentaje supera el umbral
    if porcentaje_colores > umbral_porcentaje:
        resultado = "Hoja enferma"
    else:
        resultado = "Hoja saludable"

    print("Resultado:", resultado)

# Ejemplo de uso con tres rangos de colores
ruta_imagen = "Fotos/9.jpg"
rangos_colores_objetivo = [
    ((100, 50, 0), (200, 150, 50)),  # Rango de colores marrones
    ((0, 100, 0), (100, 200, 100)),  # Rango de colores verdes oscuros
    ((150, 50, 0), (255, 200, 100)),  # Rango de colores naranjas-rojizo
]
umbral = 8  # Umbral del 8%

# Llamada a la función
resultado = detectar_rango_colores(ruta_imagen, rangos_colores_objetivo, umbral)
print(resultado)