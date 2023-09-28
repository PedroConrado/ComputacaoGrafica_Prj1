import polyscope as ps
import numpy as np
from scipy.spatial.transform import Rotation as R

# Define os vértices da pirâmide
vertices = np.array([
    [0, 0, 1],    # Ponto no topo da pirâmide
    [-1, -1, -1],  # Vértice da base
    [1, -1, -1],   # Vértice da base
    [1, 1, -1],    # Vértice da base
    [-1, 1, -1]    # Vértice da base
])

# Define as faces que conectam os vértices para formar a pirâmide
faces = np.array([
    [0, 1, 2],
    [0, 2, 3],
    [0, 3, 4],
    [0, 4, 1],
    [1, 2, 3],
    [1, 3, 4]
])

# Inicializa a visualização
ps.init()

# Crie uma função para aplicar transformações geométricas aos vértices
def aplicar_transformacao(escala, translacao, rotacao):
    transformacao = np.eye(4)
    transformacao[:3, :3] = rotacao.as_matrix()
    transformacao[:3, 3] = translacao
    transformacao = np.dot(np.diag([escala, escala, escala, 1]), transformacao)
    return np.dot(vertices, transformacao[:3, :3].T) + transformacao[:3, 3]

# Aplicar transformações geométricas em diferentes configurações
configuracoes = [
    (1.0, [0, 0, 0], R.identity()),            # Configuração padrão
    (1.5, [2, 0, 0], R.from_euler('z', 45)),   # Escala, Translação e Rotação personalizadas
    (0.8, [-2, 0, 0], R.from_euler('y', 90)),
    (1.0, [0, -2, 0], R.from_euler('x', 90)),  # Translação e Rotação adicionais
    (0.7, [0, 0, -2], R.from_euler('y', -45)),
    (1.2, [2, 2, 2], R.from_euler('z', 30)),
]

for i, (escala, translacao, rotacao) in enumerate(configuracoes):
    vertices_transformados = aplicar_transformacao(escala, translacao, rotacao)
    ps_mesh = ps.register_surface_mesh(f"Piramide {i+1}", vertices_transformados, faces)

# Visualiza as pirâmides nas configurações especificadas
ps.show()
