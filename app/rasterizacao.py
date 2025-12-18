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


def produz_fragmento(x, y, tabela_scanline):
    xm = int(x)
    ym = int(y)
    if ym not in tabela_scanline:
        tabela_scanline[ym] = []
    tabela_scanline[ym].append(xm)


def rasterizar_linha(x1, y1, x2, y2, tabela_scanline):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) >= abs(dy):
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            dx = x2 - x1
            dy = y2 - y1
        if dx == 0:
            m = 0
        else:
            m = dy / dx
        b = y1 - m * x1
        x = x1
        x_end = x2
        while x <= x_end:
            y = m * x + b
            produz_fragmento(x, y, tabela_scanline)
            x += 1
    else:
        if y1 > y2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            dx = x2 - x1
            dy = y2 - y1
        if dy == 0:
            m_inv = 0
        else:
            m_inv = dx / dy
        b_inv = x1 - m_inv * y1
        y = y1
        y_end = y2
        while y <= y_end:
            x = m_inv * y + b_inv
            produz_fragmento(x, y, tabela_scanline)
            y += 1


def impar_par(tabela_scanline, grid, cor_rgb, width, height):
    for y, lista_x in tabela_scanline.items():
        if y < 0 or y >= height:
            continue
        lista_x.sort()
        qtd = len(lista_x)
        for i in range(0, qtd - 1, 2):
            x_inicio = lista_x[i]
            x_fim = lista_x[i + 1]
            x_inicio = max(0, min(x_inicio, width - 1))
            x_fim = max(0, min(x_fim, width - 1))
            for x in range(x_inicio, x_fim + 1):
                grid[y, x] = cor_rgb


def rasterizar_poligono(vertices, grid, cor_rgb, width, height):
    tabela_scanline = {}
    num_vertices = len(vertices)
    for i in range(num_vertices):
        v1 = vertices[i]
        v2 = vertices[(i + 1) % num_vertices]
        x1, y1 = v1[0], v1[1]
        x2, y2 = v2[0], v2[1]
        if int(y1) == int(y2):
            continue
        if y1 > y2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        dx = x2 - x1
        dy = y2 - y1
        m_inv = dx / dy if dy != 0 else 0
        y_start = int(np.ceil(y1))
        y_end = int(y2)
        for y in range(y_start, y_end):
            x_intersecao = int(x1 + (y - y1) * m_inv)
            if y not in tabela_scanline:
                tabela_scanline[y] = []
            tabela_scanline[y].append(x_intersecao)
    impar_par(tabela_scanline, grid, cor_rgb, width, height)


def obter_cor_rgb(nome_cor):
    mapa = {
        'tomato': [1.0, 0.39, 0.28],
        'gold': [1.0, 0.84, 0.0],
        'deepskyblue': [0.0, 0.75, 1.0]
    }
    return mapa.get(nome_cor, [0.5, 0.5, 0.5])


def rasterizar():
    vertices_mundo, faces, cores, centro_cena = compor_cena()

    eye = np.array([6.0, 0.0, 6.0])
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
            rasterizar_poligono(v, grid, cor_rgb, w, h)
        grids.append(grid)

    return grids, resolucoes


if __name__ == '__main__':
    grids, resolucoes = rasterizar()
    plotar_rasterizacao(grids, resolucoes)
