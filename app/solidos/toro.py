import numpy as np
from skimage import measure
from app.util import visualizar_malha

def calcular_sdf_toro(raio_maior, raio_menor, resolucao):
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
                d_xy = np.sqrt(x_vals[i, j, k]**2 + y_vals[i, j, k]**2) - raio_maior
                volume[i, j, k] = np.sqrt(d_xy**2 + z_vals[i, j, k]**2) - raio_menor

    return volume, limite

def gerar_toro(raio_maior, raio_menor, resolucao):
    volume, limite = calcular_sdf_toro(raio_maior, raio_menor, resolucao)
    vertices, faces, normais, valores = measure.marching_cubes(volume, 0)
    passo = (2 * limite) / (resolucao - 1)
    vertices = vertices * passo - limite
    return vertices, faces

if __name__ == '__main__':
    raio_maior = 5.0
    raio_menor = 2.0
    resolucao = 30
    v, f = gerar_toro(raio_maior, raio_menor, resolucao)
    visualizar_malha(v, f, '1- c) Toro', 'gold')
