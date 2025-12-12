import numpy as np

from app.solidos.cano import gerar_cano
from app.solidos.cubo import gerar_cubo
from app.solidos.toro import gerar_toro
from app.trans import (
    obter_matriz_translacao,
    obter_matriz_escala,
    obter_matriz_rotacao_x,
    obter_matriz_rotacao_y,
    obter_matriz_rotacao_z
)
from app.util import plotar_cena


def aplicar_matriz(vertices, matriz):
    novos_vertices = np.zeros_like(vertices)
    for i in range(len(vertices)):
        ponto = np.array([vertices[i, 0], vertices[i, 1], vertices[i, 2], 1.0])
        ponto_transformado = matriz @ ponto
        novos_vertices[i, 0] = ponto_transformado[0]
        novos_vertices[i, 1] = ponto_transformado[1]
        novos_vertices[i, 2] = ponto_transformado[2]
    return novos_vertices


def compor_cena():
    todos_vertices = []
    todas_faces = []
    todas_cores = []

    v_cubo, f_cubo = gerar_cubo(1.0, resolucao=10)
    m_esc_cubo = obter_matriz_escala(3.0, 3.0, 3.0)
    m_rot_cubo = obter_matriz_rotacao_y(45)
    m_trans_cubo = obter_matriz_translacao(-4.0, -4.0, 0.0)
    m_final_cubo = m_trans_cubo @ m_rot_cubo @ m_esc_cubo
    v_cubo = aplicar_matriz(v_cubo, m_final_cubo)
    centro_cubo = np.mean(v_cubo, axis=0)

    offset = len(todos_vertices)
    for v in v_cubo:
        todos_vertices.append(v)
    for f in f_cubo:
        nova_face = []
        for idx in f:
            nova_face.append(idx + offset)
        todas_faces.append(nova_face)
        todas_cores.append('tomato')

    v_toro, f_toro = gerar_toro(2.0, 0.6, resolucao=20)
    m_esc_toro = obter_matriz_escala(1.5, 1.5, 1.5)
    m_rot_toro = obter_matriz_rotacao_x(60)
    m_trans_toro = obter_matriz_translacao(4.0, 4.0, 0.0)

    m_final_toro = m_trans_toro @ m_rot_toro @ m_esc_toro
    v_toro = aplicar_matriz(v_toro, m_final_toro)
    centro_toro = np.mean(v_toro, axis=0)

    offset = len(todos_vertices)
    for v in v_toro:
        todos_vertices.append(v)
    for f in f_toro:
        nova_face = [idx + offset for idx in f]
        todas_faces.append(nova_face)
        todas_cores.append('gold')

    p0 = np.array([0.0, -2.0, 0.0])
    p1 = np.array([0.0, 2.0, 0.0])
    t0 = np.array([8.0, 0.0, 0.0])
    t1 = np.array([-8.0, 0.0, 0.0])
    v_cano, f_cano = gerar_cano(1.0, 0.3, p0, p1, t0, t1, segmentos=15, fatias=10)

    m_esc_cano = obter_matriz_escala(1.2, 1.2, 1.2)
    m_rot_cano = obter_matriz_rotacao_z(90)
    m_trans_cano = obter_matriz_translacao(0.0, 0.0, 4.0)
    m_final_cano = m_trans_cano @ m_rot_cano @ m_esc_cano
    v_cano = aplicar_matriz(v_cano, m_final_cano)
    centro_cano = np.mean(v_cano, axis=0)

    offset = len(todos_vertices)
    for v in v_cano:
        todos_vertices.append(v)
    for f in f_cano:
        nova_face = [idx + offset for idx in f]
        todas_faces.append(nova_face)
        todas_cores.append('deepskyblue')

    vertices_np = np.array(todos_vertices)

    max_val = 0.0
    for i in range(len(vertices_np)):
        for j in range(3):
            if abs(vertices_np[i, j]) > max_val:
                max_val = abs(vertices_np[i, j])

    centro_medio = (centro_cubo + centro_toro + centro_cano) / 3.0

    if max_val > 0:
        fator = 8.0 / max_val
        m_escala_global = obter_matriz_escala(fator, fator, fator)
        vertices_np = aplicar_matriz(vertices_np, m_escala_global)
        centro_cena = aplicar_matriz(np.array([centro_medio]), m_escala_global)[0]
    else:
        centro_cena = centro_medio

    return vertices_np, todas_faces, todas_cores, centro_cena


if __name__ == '__main__':
    vertices_cena, faces_cena, cores_faces, centro = compor_cena()
    plotar_cena(vertices_cena, faces_cena, cores_faces)
