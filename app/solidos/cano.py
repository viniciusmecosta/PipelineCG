import numpy as np
from app.util import visualizar_malha

def calcular_hermite(p0, p1, t0, t1, segmentos):
    t = np.linspace(0, 1, segmentos)
    h00 = 2 * t ** 3 - 3 * t ** 2 + 1
    h10 = t ** 3 - 2 * t ** 2 + t
    h01 = -2 * t ** 3 + 3 * t ** 2
    h11 = t ** 3 - t ** 2

    curva = np.outer(h00, p0) + np.outer(h10, t0) + np.outer(h01, p1) + np.outer(h11, t1)
    return curva

def calcular_frame(pontos, indice, up_inicial):
    if indice < len(pontos) - 1:
        t = pontos[indice + 1] - pontos[indice]
    else:
        t = pontos[indice] - pontos[indice - 1]

    t = t / np.linalg.norm(t)

    up = up_inicial.copy()
    if np.allclose(np.abs(np.dot(t, up)), 1.0):
        up = np.array([1.0, 0.0, 0.0])

    normal = up - np.dot(up, t) * t
    normal = normal / np.linalg.norm(normal)
    binormal = np.cross(t, normal)

    return t, normal, binormal

def gerar_anel(centro, normal, binormal, raio_ext, raio_int, fatias):
    angulos = np.linspace(0, 2 * np.pi, fatias, endpoint=False)
    vertices = []

    for a in angulos:
        offset = normal * np.cos(a) + binormal * np.sin(a)
        vertices.append(centro + raio_ext * offset)
        vertices.append(centro + raio_int * offset)

    return vertices

def conectar_aneis(faces, indice_anel, fatias):
    for j in range(fatias):
        k = (j + 1) % fatias

        v1e = (indice_anel * fatias + j) * 2
        v1i = v1e + 1
        v2e = (indice_anel * fatias + k) * 2
        v2i = v2e + 1

        v3e = ((indice_anel + 1) * fatias + k) * 2
        v3i = v3e + 1
        v4e = ((indice_anel + 1) * fatias + j) * 2
        v4i = v4e + 1

        faces.append([v1e, v4e, v3e])
        faces.append([v1e, v3e, v2e])
        faces.append([v1i, v3i, v4i])
        faces.append([v1i, v2i, v3i])

def fechar_tampas(faces, indice_anel, fatias, inicio):
    for j in range(fatias):
        k = (j + 1) % fatias

        v1e = (indice_anel * fatias + j) * 2
        v1i = v1e + 1
        v2e = (indice_anel * fatias + k) * 2
        v2i = v2e + 1

        if inicio:
            faces.append([v1i, v2e, v1e])
            faces.append([v1i, v2i, v2e])
        else:
            faces.append([v1i, v1e, v2e])
            faces.append([v1i, v2e, v2i])

def gerar_cano(raio, espessura, p0, p1, t0, t1, segmentos, fatias):
    if espessura >= raio:
        raise ValueError("A espessura deve ser menor que o raio.")

    curva = calcular_hermite(p0, p1, t0, t1, segmentos)
    raio_int = raio - espessura
    vertices = []
    faces = []
    up = np.array([0.0, 1.0, 0.0])

    for i in range(segmentos):
        normal, binormal = calcular_frame(curva, i, up)[1:]
        anel = gerar_anel(curva[i], normal, binormal, raio, raio_int, fatias)
        vertices.extend(anel)

    vertices = np.array(vertices)

    for i in range(segmentos - 1):
        conectar_aneis(faces, i, fatias)

    fechar_tampas(faces, 0, fatias, True)
    fechar_tampas(faces, segmentos - 1, fatias, False)

    return vertices, np.array(faces)

if __name__ == '__main__':
    p0 = np.array([0.0, 0.0, 0.0])
    p1 = np.array([10.0, 0.0, 10.0])
    t0 = np.array([15.0, 0.0, 0.0])
    t1 = np.array([0.0, 15.0, 0.0])

    raio = 3.0
    espessura = 1.0
    segmentos = 40
    fatias = 12

    v, f = gerar_cano(raio, espessura, p0, p1, t0, t1, segmentos, fatias)
    visualizar_malha(v, f, '1-b) Cano Curvado', 'deepskyblue')