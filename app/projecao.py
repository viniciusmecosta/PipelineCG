import numpy as np

from app.scc import obter_matriz_visualizacao
from app.scm import compor_cena
from app.trans import obter_matriz_projecao
from app.visualizacao import plotar_projecao_2d


def projetar(vertices_mundo, matriz_view, matriz_projecao):
    if vertices_mundo.shape[1] == 3:
        uns = np.ones((vertices_mundo.shape[0], 1))
        vertices_homogeneos = np.hstack([vertices_mundo, uns])
    else:
        vertices_homogeneos = vertices_mundo

    matriz_total = matriz_projecao @ matriz_view
    vertices_clip = vertices_homogeneos @ matriz_total.T

    xc = vertices_clip[:, 0]
    yc = vertices_clip[:, 1]
    zc = vertices_clip[:, 2]
    wc = vertices_clip[:, 3]

    vertices_ndc = np.full((vertices_clip.shape[0], 3), np.nan)
    mask = wc > 0.001

    vertices_ndc[mask, 0] = xc[mask] / wc[mask]
    vertices_ndc[mask, 1] = yc[mask] / wc[mask]
    vertices_ndc[mask, 2] = zc[mask] / wc[mask]

    return vertices_ndc


if __name__ == '__main__':
    vertices_mundo, faces, cores, centro_cena = compor_cena()

    eye = np.array([-1.0, 1.0, 6.5])
    target = centro_cena
    up = np.array([0.0, 1.0, 0.0])

    m_view = obter_matriz_visualizacao(eye, target, up)

    fov = 60.0
    aspect = 1.0
    near = 0.1
    far = 100.0

    m_proj = obter_matriz_projecao(fov, aspect, near, far)

    vertices_ndc = projetar(vertices_mundo, m_view, m_proj)

    plotar_projecao_2d(vertices_ndc, faces, cores)
