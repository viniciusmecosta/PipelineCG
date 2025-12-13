import numpy as np


def obter_matriz_translacao(tx, ty, tz):
    matriz = np.identity(4)
    matriz[0, 3] = tx
    matriz[1, 3] = ty
    matriz[2, 3] = tz

    return matriz


def obter_matriz_escala(sx, sy, sz):
    matriz = np.identity(4)
    matriz[0, 0] = sx
    matriz[1, 1] = sy
    matriz[2, 2] = sz

    return matriz


def obter_matriz_rotacao_x(angulo):
    c = np.cos(angulo)
    s = np.sin(angulo)
    matriz = np.identity(4)
    matriz[1, 1] = c
    matriz[1, 2] = -s
    matriz[2, 1] = s
    matriz[2, 2] = c

    return matriz


def obter_matriz_rotacao_y(angulo):
    c = np.cos(angulo)
    s = np.sin(angulo)
    matriz = np.identity(4)
    matriz[0, 0] = c
    matriz[0, 2] = s
    matriz[2, 0] = -s
    matriz[2, 2] = c

    return matriz


def obter_matriz_rotacao_z(angulo):
    c = np.cos(angulo)
    s = np.sin(angulo)
    matriz = np.identity(4)
    matriz[0, 0] = c
    matriz[0, 1] = -s
    matriz[1, 0] = s
    matriz[1, 1] = c

    return matriz


def obter_matriz_projecao(fov_graus, aspect_ratio, near, far):
    fov_rad = np.radians(fov_graus)
    f = 1.0 / np.tan(fov_rad / 2.0)

    matriz = np.zeros((4, 4))
    matriz[0, 0] = f / aspect_ratio
    matriz[1, 1] = f
    matriz[2, 2] = (far + near) / (near - far)
    matriz[2, 3] = (2 * far * near) / (near - far)
    matriz[3, 2] = -1.0
    matriz[3, 3] = 0.0

    return matriz
