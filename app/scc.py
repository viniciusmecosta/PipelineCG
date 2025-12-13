import numpy as np

from app.scm import compor_cena, aplicar_matriz
from app.util import plotar_comparacao_camera


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
    matriz_rotacao = np.identity(4)
    matriz_rotacao[0, 0] = u[0]
    matriz_rotacao[0, 1] = u[1]
    matriz_rotacao[0, 2] = u[2]
    matriz_rotacao[1, 0] = v[0]
    matriz_rotacao[1, 1] = v[1]
    matriz_rotacao[1, 2] = v[2]
    matriz_rotacao[2, 0] = n[0]
    matriz_rotacao[2, 1] = n[1]
    matriz_rotacao[2, 2] = n[2]

    matriz_translacao = np.identity(4)
    matriz_translacao[0, 3] = -eye[0]
    matriz_translacao[1, 3] = -eye[1]
    matriz_translacao[2, 3] = -eye[2]

    return matriz_rotacao @ matriz_translacao


if __name__ == '__main__':
    vertices_mundo, faces, cores, centro_cena = compor_cena()

    eye = np.array([15.0, 0.0, 15.0])
    target = centro_cena
    up = np.array([0.0, 1.0, 0.0])

    m_view = obter_matriz_visualizacao(eye, target, up)
    vertices_camera = aplicar_matriz(vertices_mundo, m_view)

    ponto_origem = np.array([0.0, 0.0, 0.0, 1.0])
    origem_transf = m_view @ ponto_origem
    origem_camera = origem_transf[:3]

    ponto_target = np.append(target, 1.0)
    target_transf = m_view @ ponto_target
    target_camera = target_transf[:3]

    plotar_comparacao_camera(vertices_mundo, vertices_camera, faces, cores, eye, target, origem_camera, target_camera)
