import numpy as np
from skimage import measure

from app.util import visualizar_malha


def calcular_sdf_cubo(tamanho, resolucao):
    limite = tamanho / 2.0 + 1.0
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
                d = max(abs(x_vals[i, j, k]), abs(y_vals[i, j, k]), abs(z_vals[i, j, k]))
                volume[i, j, k] = d - (tamanho / 2.0)
    return volume, limite


def gerar_cubo(tamanho, resolucao=10):
    volume, limite = calcular_sdf_cubo(tamanho, resolucao)
    vertices, faces, normais, valores = measure.marching_cubes(volume, level=0)
    passo = (2 * limite) / (resolucao - 1)
    vertices = vertices * passo - limite
    return vertices, faces


if __name__ == '__main__':
    tamanho = 1
    resolucao = 10
    v, f = gerar_cubo(tamanho)
    visualizar_malha(v, f, '1-a) Cubo', 'tomato')
