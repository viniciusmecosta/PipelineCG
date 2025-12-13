import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np


def visualizar_malha(vertices, faces, titulo, cor):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    mesh = Poly3DCollection(vertices[faces])
    mesh.set_facecolor(cor)
    mesh.set_edgecolor('black')
    mesh.set_linewidth(0.3)
    mesh.set_alpha(1.0)
    ax.add_collection3d(mesh)
    ax.set_xlabel('Eixo X')
    ax.set_ylabel('Eixo Y')
    ax.set_zlabel('Eixo Z')
    ax.set_title(titulo)
    min_lim = np.min(vertices)
    max_lim = np.max(vertices)
    ax.set_xlim(min_lim, max_lim)
    ax.set_ylim(min_lim, max_lim)
    ax.set_zlim(min_lim, max_lim)
    plt.show()


def ajustar_limites_com_pontos(ax, vertices, pontos_extras=[]):
    if pontos_extras:
        extras_formatados = [np.array(p).reshape(1, 3) for p in pontos_extras]
        todos_pontos = np.vstack([vertices] + extras_formatados)
    else:
        todos_pontos = vertices
    min_vals = np.min(todos_pontos, axis=0)
    max_vals = np.max(todos_pontos, axis=0)
    max_range = (max_vals - min_vals).max() / 2.0
    mid_vals = (max_vals + min_vals) / 2.0
    max_range *= 1.1
    ax.set_xlim(mid_vals[0] - max_range, mid_vals[0] + max_range)
    ax.set_ylim(mid_vals[1] - max_range, mid_vals[1] + max_range)
    ax.set_zlim(mid_vals[2] - max_range, mid_vals[2] + max_range)


def plotar_cena(vertices, faces, cores):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    poly3d = []
    for face in faces:
        pontos_face = vertices[face]
        poly3d.append(pontos_face)
    mesh = Poly3DCollection(poly3d)
    mesh.set_facecolor(cores)
    mesh.set_edgecolor('black')
    mesh.set_linewidth(0.07)
    mesh.set_alpha(0.9)
    ax.add_collection3d(mesh)
    ax.set_xlabel('Eixo X')
    ax.set_ylabel('Eixo Y')
    ax.set_zlabel('Eixo Z')
    ax.set_title('Questao 2')
    ajustar_limites_com_pontos(ax, vertices)
    plt.show()


def plotar_comparacao_camera(vertices_mundo, vertices_camera, faces, cores, eye, target, origem_mundo_camera,
                             target_camera):
    fig = plt.figure(figsize=(14, 7))

    ax1 = fig.add_subplot(121, projection='3d')
    poly3d_mundo = [vertices_mundo[face] for face in faces]
    mesh_mundo = Poly3DCollection(poly3d_mundo)
    mesh_mundo.set_facecolor(cores)
    mesh_mundo.set_edgecolor('black')
    mesh_mundo.set_linewidth(0.05)
    mesh_mundo.set_alpha(0.9)
    ax1.add_collection3d(mesh_mundo)

    label_eye = f"Camera ({eye[0]:.1f}, {eye[1]:.1f}, {eye[2]:.1f})"
    ax1.scatter(eye[0], eye[1], eye[2], color='red', marker='o', s=100, label=label_eye)

    label_target = f"AT ({target[0]:.1f}, {target[1]:.1f}, {target[2]:.1f})"
    ax1.scatter(target[0], target[1], target[2], color='green', marker='x', s=100, label=label_target)

    origem_mundo = np.array([0.0, 0.0, 0.0])
    label_origem = f"Origem ({origem_mundo[0]:.1f}, {origem_mundo[1]:.1f}, {origem_mundo[2]:.1f})"
    ax1.scatter(origem_mundo[0], origem_mundo[1], origem_mundo[2], color='hotpink', marker='o', s=100,
                label=label_origem)

    ax1.set_title('Mundo')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.legend()
    ajustar_limites_com_pontos(ax1, vertices_mundo, [eye, target, origem_mundo])

    ax2 = fig.add_subplot(122, projection='3d')
    poly3d_camera = [vertices_camera[face] for face in faces]
    mesh_camera = Poly3DCollection(poly3d_camera)
    mesh_camera.set_facecolor(cores)
    mesh_camera.set_edgecolor('black')
    mesh_camera.set_linewidth(0.05)
    mesh_camera.set_alpha(0.9)
    ax2.add_collection3d(mesh_camera)

    posicao_camera_local = np.array([0.0, 0.0, 0.0])
    label_cam_local = f"Camera ({posicao_camera_local[0]:.1f}, {posicao_camera_local[1]:.1f}, {posicao_camera_local[2]:.1f})"
    ax2.scatter(posicao_camera_local[0], posicao_camera_local[1], posicao_camera_local[2], color='red', marker='o',
                s=100, label=label_cam_local)

    label_target_cam = f"AT ({target_camera[0]:.1f}, {target_camera[1]:.1f}, {target_camera[2]:.1f})"
    ax2.scatter(target_camera[0], target_camera[1], target_camera[2], color='green', marker='x', s=100,
                label=label_target_cam)

    label_orig_cam = f"Origem Mundo ({origem_mundo_camera[0]:.1f}, {origem_mundo_camera[1]:.1f}, {origem_mundo_camera[2]:.1f})"
    ax2.scatter(origem_mundo_camera[0], origem_mundo_camera[1], origem_mundo_camera[2], color='hotpink', marker='o',
                s=100, label=label_orig_cam)

    ax2.set_title('Camera')
    ax2.set_xlabel('U')
    ax2.set_ylabel('V')
    ax2.set_zlabel('N')
    ax2.legend()
    ajustar_limites_com_pontos(ax2, vertices_camera, [origem_mundo_camera, posicao_camera_local, target_camera])
    plt.show()


def plotar_projecao_2d(vertices_ndc, faces, cores, titulo="Questao 4 - Projecao em Perspectiva"):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)
    dados_faces = []

    for i, face in enumerate(faces):
        verts_face = vertices_ndc[face]

        if np.any(np.isnan(verts_face)):
            continue

        z_medio = np.mean(verts_face[:, 2])
        dados_faces.append({
            'verts': verts_face[:, :2],
            'z': z_medio,
            'cor': cores[i]
        })

    dados_faces.sort(key=lambda f: f['z'], reverse=True)

    for dado in dados_faces:
        poly = Polygon(dado['verts'], closed=True, facecolor=dado['cor'], edgecolor='black', linewidth=0.5, alpha=0.9)
        ax.add_patch(poly)

    ax.set_title(titulo)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)

    rect = plt.Rectangle((-1, -1), 2, 2, fill=False, color='red', linestyle='--', linewidth=1.5, label='Janela de Projeção')
    ax.add_patch(rect)

    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend()
    plt.show()
