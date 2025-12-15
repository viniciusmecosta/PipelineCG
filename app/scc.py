import numpy as np

from app.scm import compor_cena, aplicar_matriz
from app.visualizacao import plotar_comparacao_camera


def calcular_base_camera(eye, target, up):
    n = eye - target
    norma_n = np.linalg.norm(n)
    if norma_n > 0:
        n = n / norma_n
    u = np.cross(up, n)
    norma_u = np.linalg.norm(u)
    if norma_u > 0:
        u = u / norma_u
    v = np.cross(n, u)
    return u, v, n


def obter_matriz_visualizacao(eye, target, up):
    u, v, n = calcular_base_camera(eye, target, up)
    matriz_r = np.identity(4)
    matriz_r[0, 0] = u[0]
    matriz_r[0, 1] = u[1]
    matriz_r[0, 2] = u[2]
    matriz_r[1, 0] = v[0]
    matriz_r[1, 1] = v[1]
    matriz_r[1, 2] = v[2]
    matriz_r[2, 0] = n[0]
    matriz_r[2, 1] = n[1]
    matriz_r[2, 2] = n[2]

    matriz_t = np.identity(4)
    matriz_t[0, 3] = -eye[0]
    matriz_t[1, 3] = -eye[1]
    matriz_t[2, 3] = -eye[2]

    return matriz_r @ matriz_t


if __name__ == '__main__':
    vertices_mundo, faces, cores, centro_cena = compor_cena()

    eye = np.array([6.0, 0.0, 6.0])
    target = centro_cena
    up = np.array([0.0, 1.0, 0.0])

    m_view = obter_matriz_visualizacao(eye, target, up)
    vertices_camera = aplicar_matriz(vertices_mundo, m_view)

    ponto_origem_mundo = np.array([0.0, 0.0, 0.0, 1.0])
    ponto_origem_camera = m_view @ ponto_origem_mundo
    origem_camera_coord = ponto_origem_camera[:3]

    ponto_alvo_mundo = np.append(target, 1.0)
    ponto_alvo_camera = m_view @ ponto_alvo_mundo
    alvo_camera_coord = ponto_alvo_camera[:3]

    plotar_comparacao_camera(vertices_mundo, vertices_camera, faces, cores, eye, target, origem_camera_coord,
                             alvo_camera_coord)
