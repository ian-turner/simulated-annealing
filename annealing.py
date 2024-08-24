from argparse import ArgumentParser
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def get_energy(vertices, path):
    d = 0
    for i in range(len(path)-1):
        d += np.sqrt((vertices[0][path[i]]-vertices[0][path[i+1]])**2
            +(vertices[1][path[i]]-vertices[1][path[i+1]])**2)
    d += np.sqrt((vertices[0][path[0]]-vertices[0][path[len(path)-1]])**2
        +(vertices[1][path[0]]-vertices[1][path[len(path)-1]])**2)
    return d


class Sim:
    def __init__(self, num_points: int, Kmax: int):
        self.Kmax = Kmax
        vertices = np.random.rand(2, num_points)
        self.path = np.arange(num_points)

        # plot setup
        self.fig, self.axs = plt.subplots(1, 2)
        ax = self.axs[1]
        self.energy_plot, = ax.plot([], [], color='green')
        ax.set_title('Energy')
        ax.set_xlabel('Steps')
        ax.set_ylabel('Distance')

        ax = self.axs[0]
        ax.scatter(*vertices, color='black', s=10)
        ax.set_title('T=1.00')

        # plotting the path
        self.lines = []
        for i in range(num_points-1):
            line, = ax.plot(vertices[0, i:i+2], vertices[1, i:i+2], color='black', linewidth=1)
            self.lines.append(line)
        line, = ax.plot([vertices[0][0], vertices[0][num_points-1]],
            [vertices[1][0], vertices[1][num_points-1]], color='black', linewidth=1)
        self.lines.append(line)

        self.vertices = vertices
        self.num_points = num_points
        self.ax = ax

    # creating the animation
    def update(self, k: int):
        # deciding which edges to swap
        T = 1 - (k+1) / self.Kmax
        if T <= 0.:
            return []

        num_points = self.num_points
        path = self.path
        vertices = self.vertices

        i = np.random.randint(low=0, high=num_points)
        j = np.random.randint(low=0, high=num_points)

        # getting energy (total distance) of path and random new path
        new_path = path.copy()
        x = new_path[i]
        new_path[i] = new_path[j]
        new_path[j] = x
        
        energy = get_energy(vertices, self.path)
        new_energy = get_energy(vertices, new_path)

        # deciding whether or not to update
        if new_energy < energy or np.random.rand() <= np.exp(-(new_energy-energy)/T):
            self.path = new_path

        # re-drawing the path
        for i in range(num_points - 1):
            self.lines[i].set_xdata([vertices[0][path[i]], vertices[0][path[i+1]]])
            self.lines[i].set_ydata([vertices[1][path[i]], vertices[1][path[i+1]]])
        self.lines[num_points-1].set_xdata([vertices[0][path[0]], vertices[0][path[num_points-1]]])
        self.lines[num_points-1].set_ydata([vertices[1][path[0]], vertices[1][path[num_points-1]]])
        self.ax.set_title('Travelling Salesman (T=%.2f)' % T)

        energy_y = self.energy_plot.get_ydata()
        energy_y = np.array([*energy_y, get_energy(vertices, self.path)])
        self.energy_plot.set_ydata(energy_y)
        self.energy_plot.set_xdata(np.arange(k+2))
        self.axs[1].set_xlim(0, k+1)
        self.axs[1].set_ylim(min(energy_y) - 1, max(energy_y) + 1)
            
        return [*self.lines, self.energy_plot]


def main():
    parser = ArgumentParser()
    parser.add_argument('num_points', type=int, default=15)
    parser.add_argument('Kmax', type=int, default=2000)

    args = parser.parse_args()

    sim = Sim(args.num_points, args.Kmax)
    anim = FuncAnimation(fig=sim.fig, func=sim.update, interval=10, frames=sim.Kmax, repeat=False)
    plt.show()


if __name__ == '__main__':
    main()
