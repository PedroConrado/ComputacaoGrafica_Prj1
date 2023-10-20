import polyscope as ps
import numpy as np
from scipy.spatial.transform import Rotation as R
from stl import mesh
import numpy as np

# Using an existing stl file:
stl_mesh = mesh.Mesh.from_file('poo.stl')

# Inicialize listas para os vértices e faces
vertices_poo = []
faces_poo = []

# Percorra as faces da malha
for i, face in enumerate(stl_mesh.points):
    # Crie uma lista de vértices para esta face
    face_vertices = []
    for j in range(3):  # Existem três vértices em cada face
        vertex = stl_mesh.vectors[i][j]
        vertex_coords = [float(coord) for coord in vertex]
        face_vertices.append(vertex_coords)
    vertices_poo.extend(face_vertices)  # Adicione os vértices à lista de vértices

    # Crie uma lista de índices de vértices para esta face
    num_vertices = len(face_vertices)
    face_indices = list(range(len(vertices_poo) - num_vertices, len(vertices_poo)))
    faces_poo.append(face_indices)  # Adicione os índices à lista de faces

faces_poo = np.array(faces_poo)
vertices_poo = np.array(vertices_poo)
vertices_poo = vertices_poo/15


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
configuracoes_piramide = [
    (1.0, [0, 0, 0], R.identity()),            # Configuração padrão
    (1.5, [2, 0, 0], R.from_euler('z', 45)),   
    (0.8, [-3, 0, 0], R.from_euler('y', 90)),
    (1.0, [0, -3, 0], R.from_euler('x', 90)),  
    (0.7, [0, 3, -2], R.from_euler('y', -45)),
    (1.2, [2, 2, 2], R.from_euler('z', 30)),
]

for i, (escala, translacao, rotacao) in enumerate(configuracoes_piramide):
    vertices_piramide_transformados = aplicar_transformacao(escala, translacao, rotacao)
    ps_mesh = ps.register_surface_mesh(f"Piramide {'original' if i == 0 else 'transformação: ' + str(i)}", vertices_piramide_transformados, faces)

ps_mesh = ps.register_surface_mesh(f"Poo", vertices_poo, faces_poo)


# Visualiza as pirâmides nas configurações especificadas
ps.show()
