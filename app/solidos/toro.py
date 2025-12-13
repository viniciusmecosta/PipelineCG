import numpy as np
from skimage import measure

from app.visualizacao import visualizar_malha


def calcular_toro(raio_maior, raio_menor, resolucao):
    limite = raio_maior + raio_menor + 1.0
    eixos = np.linspace(-limite, limite, resolucao)
    x_vals = np.zeros((resolucao, resolucao, resolucao))
    y_vals = np.zeros((resolucao, resolucao, resolucao))
    z_vals = np.zeros((resolucao, resolucao, resolucao))
    for i in range(resolucao):
        for j in range(resolucao):
            for k in range(resolucao):
                x_vals[i, j, k] = eixos[i]
                y_vals[i, j, k] = eixos[j]
                z_vals[i, j, k] = eixos[k]
    volume = np.zeros((resolucao, resolucao, resolucao))
    for i in range(resolucao):
        for j in range(resolucao):
            for k in range(resolucao):
                x = x_vals[i, j, k]
                y = y_vals[i, j, k]
                z = z_vals[i, j, k]
                len_xy = np.sqrt(x * x + y * y)
                d = np.sqrt((len_xy - raio_maior) ** 2 + z * z) - raio_menor
                volume[i, j, k] = d
    return volume, limite


def gerar_toro(raio_maior, raio_menor, resolucao=15):
    volume, limite = calcular_toro(raio_maior, raio_menor, resolucao)
    vertices, faces, normais, valores = measure.marching_cubes(volume, level=0)
    passo = (2 * limite) / (resolucao - 1)
    vertices = vertices * passo - limite
    return vertices, faces


if __name__ == '__main__':
    raio_maior = 5.0
    raio_menor = 2.0
    resolucao = 20
    v, f = gerar_toro(raio_maior, raio_menor, resolucao)
    visualizar_malha(v, f, '1- c) Toro', 'gold')
