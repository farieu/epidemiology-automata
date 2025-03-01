import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns

# Definição dos estados
SUSCEPTIBLE = 0
EXPOSED = 1
INFECTED = 2
RECOVERED = 3

# Parâmetros do modelo
grid_size = 50  # Tamanho da grade
infection_prob = 0.55  # Probabilidade de infecção
min_incubation = 7  # Tempo mínimo de incubação
max_incubation = 18  # Tempo máximo de incubação
recovery_time = 10  # Tempo de recuperação
initial_infected = 6  # Número inicial de infectados

grid = np.zeros((grid_size, grid_size), dtype=int)
incubation_timers = np.zeros((grid_size, grid_size), dtype=int)
infection_timers = np.zeros((grid_size, grid_size), dtype=int)

for _ in range(initial_infected):
    x, y = np.random.randint(0, grid_size, size=2)
    grid[x, y] = INFECTED
    infection_timers[x, y] = recovery_time

# Função para atualizar a grade
def update(frame):
    global grid, incubation_timers, infection_timers
    
    new_grid = grid.copy()
    
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i, j] == SUSCEPTIBLE:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < grid_size and 0 <= nj < grid_size:
                            if grid[ni, nj] == INFECTED and np.random.rand() < infection_prob:
                                new_grid[i, j] = EXPOSED
                                incubation_timers[i, j] = np.random.randint(min_incubation, max_incubation + 1)
                                break
            elif grid[i, j] == EXPOSED:
                incubation_timers[i, j] -= 1
                if incubation_timers[i, j] <= 0:
                    new_grid[i, j] = INFECTED
                    infection_timers[i, j] = recovery_time
            elif grid[i, j] == INFECTED:
                infection_timers[i, j] -= 1
                if infection_timers[i, j] <= 0:
                    new_grid[i, j] = RECOVERED
    
    grid = new_grid.copy()
    return grid

# Configuração para visualizar múltiplos estágios [gerações]
fig, axes = plt.subplots(2, 3, figsize=(12, 6), constrained_layout=True)
frames_to_plot = [10, 20, 40, 60, 80, 120]
snapshots = []

def capture_snapshots():
    global grid
    for i in range(max(frames_to_plot)):
        grid = update(i)
        if i + 1 in frames_to_plot:
            snapshots.append(grid.copy())

capture_snapshots()

for ax, snapshot, frame in zip(axes.ravel(), snapshots, frames_to_plot):
    sns.heatmap(snapshot, ax=ax, cmap="plasma", cbar=False, square=True, linewidths=0.1, linecolor='black')
    ax.set_title(f"Geração {frame}", fontsize=10, fontweight='ultralight')
    ax.set_xticks([])
    ax.set_yticks([])

plt.suptitle("Evolução da Infecção ao Longo das Gerações", fontsize=14, fontweight='bold')
plt.show()

