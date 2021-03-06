import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import seaborn as sns

sns.set()


class AnimationMaker():
    def __init__(self, theta1file, theta2file, l1=150, l2=150):
        self._loadData(theta1file, theta2file)

        self.l1 = l1
        self.l2 = l2

        self.trajectory_x = []
        self.trajectory_y = []

        self._init_figure()

    def _loadData(self, theta1file, theta2file):
        theta1 = np.loadtxt(theta1file, delimiter=',', unpack=True)
        theta2 = np.loadtxt(theta2file, delimiter=',', unpack=True)
        self.time = theta1[0]
        self.theta1 = theta1[1]
        self.theta2 = theta2[1]

    def _init_figure(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 6))

        self.line_trajectory, = self.ax.plot(
            [], [], color='tab:blue', label='trajectory')
        self.line_l1, = self.ax.plot(
            [], [], color='tab:gray', label='l1', linewidth=3)
        self.line_l2, = self.ax.plot(
            [], [], color='tab:gray', label='l2', linewidth=3)

        self.endEffector = patches.Circle(xy=(0, 0), radius=6, fc='tab:blue')
        self.ax.add_patch(self.endEffector)

        self.ax.set_xlabel('x [mm]')
        self.ax.set_ylabel('y [mm]')
        maxlen = self.l1 + self.l2 + 10
        self.ax.set_xlim(-maxlen, maxlen)
        self.ax.set_ylim(-maxlen, maxlen)
        self.ax.set_aspect('equal')
        # ax.legend(loc='lower left')
        # plt.subplots_adjust(left=0.1, right=0.97, bottom=0.04, top=0.97)

    def _update(self, i):
        theta1 = math.radians(self.theta1[i])
        theta2 = math.radians(self.theta2[i])

        x1 = self.l1 * math.cos(theta1)
        y1 = self.l1 * math.sin(theta1)
        x2 = x1 + self.l2 * math.cos(theta1 + theta2)
        y2 = y1 + self.l2 * math.sin(theta1 + theta2)

        self.trajectory_x.append(x2)
        self.trajectory_y.append(y2)

        self.line_l1.set_data([0, x1], [0, y1])
        self.line_l2.set_data([x1, x2], [y1, y2])
        self.line_trajectory.set_data(self.trajectory_x, self.trajectory_y)
        self.endEffector.set_center([x2, y2])

        plt.title('t = {:3.2f} [s], (x, y) = ({:4.0f}, {:4.0f})'.format(
            self.time[i], x2, y2))

    def makeAnimation(self):
        return animation.FuncAnimation(self.fig, self._update,
                                       interval=100, frames=len(self.time))


if __name__ == '__main__':
    # animationMaker = AnimationMaker('theta1example.csv', 'theta2example.csv', 150, 150)
    animationMaker = AnimationMaker(
        'data/theta1.csv', 'data/theta2.csv', l1=140, l2=160)
    ani = animationMaker.makeAnimation()
    ani.save('graph/animation.gif', writer='pillow')

    # plt.plot(animationMaker.trajectory_x, animationMaker.trajectory_y)
    plt.savefig('graph/trajectory.png')
