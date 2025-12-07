import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
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
    mesh.set_linewidth(0)
    mesh.set_alpha(0.9)
    ax.add_collection3d(mesh)
    ax.set_xlabel('Eixo X')
    ax.set_ylabel('Eixo Y')
    ax.set_zlabel('Eixo Z')
    ax.set_title('Questao 2')
    ax.set_xlim(-8, 8)
    ax.set_ylim(-8, 8)
    ax.set_zlim(-8, 8)
    plt.show()
