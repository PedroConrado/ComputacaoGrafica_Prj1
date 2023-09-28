import polyscope as ps
import numpy as np
from scipy.spatial.transform import Rotation as R
import time

# Define os vértices da pirâmide
vertices_piramide = np.array([
    [0, 0, 1],    # Ponto no topo da pirâmide
    [-1, -1, -1],  # Vértice da base
    [1, -1, -1],   # Vértice da base
    [1, 1, -1],    # Vértice da base
    [-1, 1, -1]    # Vértice da base
], dtype=np.float32)

# Define as faces que conectam os vértices para formar a pirâmide
faces_piramide = np.array([
    [0, 1, 2],
    [0, 2, 3],
    [0, 3, 4],
    [0, 4, 1],
    [1, 2, 3],
    [1, 3, 4]
], dtype=np.int32)

# Inicializa a visualização
ps.init()

# Função para aplicar transformações geométricas aos vértices
def aplicar_transformacao(escala, translacao, rotacao, vertices):
    transformacao = np.eye(4)
    transformacao[:3, :3] = rotacao.as_matrix()
    transformacao[:3, 3] = translacao
    transformacao = np.dot(np.diag([escala, escala, escala, 1]), transformacao)
    return np.dot(vertices, transformacao[:3, :3].T) + transformacao[:3, 3]

# Função para criar uma pirâmide com uma transformação específica
def criar_piramide(escala, translacao, rotacao):
    vertices_transformados = aplicar_transformacao(escala, translacao, rotacao, vertices_piramide)
    return vertices_transformados, faces_piramide

# Parâmetros da animação
num_frames = 100  # Número de quadros na animação
escala_inicial = 1.0
translacao_inicial = [0, 0, 0]
rotacao_inicial = R.identity()
escala_final = 1.0
translacao_final = [2, 0, 0]
rotacao_final = R.from_euler('z', 45, degrees=True)

# Função para criar a cena com base nas transformações
def criar_cena(escala, translacao, rotacao):
    vertices, _ = criar_piramide(escala, translacao, rotacao)
    ps.clear()
    ps.register_surface_mesh("Piramide", vertices, faces_piramide)
    ps.show()

# Executar a animação
for i in range(num_frames):
    progresso = i / (num_frames - 1)
    escala_atual = escala_inicial + progresso * (escala_final - escala_inicial)
    translacao_atual = [translacao_inicial[j] + progresso * (translacao_final[j] - translacao_inicial[j]) for j in range(3)]
    rotacao_atual = rotacao_inicial * (1 - progresso) + rotacao_final * progresso

    criar_cena(escala_atual, translacao_atual, rotacao_atual)
    time.sleep(0.1)  # Pequena pausa para controlar a taxa de quadros

# Mantenha a janela aberta até que a animação seja fechada
while not ps.pressed('q'):
    pass

# Fechar a janela de visualização
ps.shutdown()
