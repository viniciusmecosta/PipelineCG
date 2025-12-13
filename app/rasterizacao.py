import numpy as np

from app.projecao import projetar
from app.scc import obter_matriz_visualizacao
from app.scm import compor_cena, aplicar_matriz
from app.trans import obter_matriz_projecao, obter_matriz_escala, obter_matriz_translacao
from app.visualizacao import plotar_rasterizacao


def transformacao_viewport(vertices_ndc, width, height):
    sx = width / 2.0
    sy = height / 2.0
    sz = 1.0

    tx = width / 2.0
    ty = height / 2.0
    tz = 0.0

    m_escala = obter_matriz_escala(sx, sy, sz)
    m_translacao = obter_matriz_translacao(tx, ty, tz)

    m_viewport = m_translacao @ m_escala

    vertices_transformados = aplicar_matriz(vertices_ndc, m_viewport)

    vertices_tela = np.zeros_like(vertices_transformados)
    vertices_tela[:, 0] = np.floor(vertices_transformados[:, 0])
    vertices_tela[:, 1] = np.floor(vertices_transformados[:, 1])
    vertices_tela[:, 2] = vertices_transformados[:, 2]

    return vertices_tela


def produzir_fragmento(x, y, tabela_scanline):
    ym = int(y)
    xm = int(x)

    if ym not in tabela_scanline:
        tabela_scanline[ym] = []

    tabela_scanline[ym].append(xm)


def rasterizar_linha(x1, y1, x2, y2, tabela_scanline):
    x1, y1 = int(x1), int(y1)
    x2, y2 = int(x2), int(y2)

    delta_x = x2 - x1
    delta_y = y2 - y1

    if abs(delta_x) >= abs(delta_y):
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            delta_x = x2 - x1
            delta_y = y2 - y1

        if delta_x == 0:
            m = 0
        else:
            m = delta_y / delta_x

        b = y1 - m * x1

        x = x1
        y = y1

        produzir_fragmento(x, y, tabela_scanline)

        while x < x2:
            x = x + 1
            y = m * x + b
            produzir_fragmento(x, y, tabela_scanline)

    else:
        if y1 > y2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            delta_x = x2 - x1
            delta_y = y2 - y1

        if delta_y == 0:
            m_inv = 0
        else:
            m_inv = delta_x / delta_y

        b_inv = x1 - m_inv * y1

        y = y1
        x = x1

        produzir_fragmento(x, y, tabela_scanline)

        while y < y2:
            y = y + 1
            x = m_inv * y + b_inv
            produzir_fragmento(x, y, tabela_scanline)


def rasterizar_triangulo(v1, v2, v3, grid, cor_rgb, width, height):
    tabela_scanline = {}

    rasterizar_linha(v1[0], v1[1], v2[0], v2[1], tabela_scanline)
    rasterizar_linha(v2[0], v2[1], v3[0], v3[1], tabela_scanline)
    rasterizar_linha(v3[0], v3[1], v1[0], v1[1], tabela_scanline)

    for y, lista_x in tabela_scanline.items():
        if y < 0 or y >= height:
            continue

        lista_x.sort()

        if len(lista_x) >= 2:
            x_inicio = lista_x[0]
            x_fim = lista_x[-1]

            x_inicio = max(0, min(x_inicio, width - 1))
            x_fim = max(0, min(x_fim, width - 1))

            for x in range(x_inicio, x_fim + 1):
                grid[y, x] = cor_rgb


def obter_cor_rgb(nome_cor):
    mapa = {
        'tomato': [1.0, 0.39, 0.28],
        'gold': [1.0, 0.84, 0.0],
        'deepskyblue': [0.0, 0.75, 1.0]
    }
    return mapa.get(nome_cor, [0.5, 0.5, 0.5])


def executar_rasterizacao():
    vertices_mundo, faces, cores, centro_cena = compor_cena()

    eye = np.array([12.0, 0.0, 12.0])
    target = centro_cena
    up = np.array([0.0, 1.0, 0.0])

    m_view = obter_matriz_visualizacao(eye, target, up)

    fov = 60.0
    aspect = 1.0
    near = 0.1
    far = 100.0
    m_proj = obter_matriz_projecao(fov, aspect, near, far)

    vertices_ndc = projetar(vertices_mundo, m_view, m_proj)

    resolucoes = [(100, 100), (300, 300), (800, 800)]
    grids = []

    for res in resolucoes:
        w, h = res
        grid = np.ones((h, w, 3))

        vertices_tela = transformacao_viewport(vertices_ndc, w, h)

        dados_faces = []
        for i, face in enumerate(faces):
            verts = vertices_tela[face]
            if np.any(np.isnan(verts)):
                continue
            z_medio = np.mean(verts[:, 2])
            dados_faces.append({
                'verts': verts,
                'z': z_medio,
                'cor': cores[i]
            })

        dados_faces.sort(key=lambda f: f['z'], reverse=True)

        for dado in dados_faces:
            v = dado['verts']
            cor_rgb = obter_cor_rgb(dado['cor'])
            rasterizar_triangulo(v[0], v[1], v[2], grid, cor_rgb, w, h)

        grids.append(grid)

    return grids, resolucoes


if __name__ == '__main__':
    grids, resolucoes = executar_rasterizacao()
    plotar_rasterizacao(grids, resolucoes)
