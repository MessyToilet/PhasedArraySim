import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import display, clear_output

plt.rcParams["figure.figsize"] = (8, 8)
plt.rcParams["font.size"] = 14

class Emitter():
    def __init__(self, x, y, c, f, phi, rMax=100, color="blue"):
        # y(r) = R(exp(i(kr - wt + phi)))
        # kr - wt - phi = 2pi n, n ele of Z

        self.r = np.array([x, y])
        self.c = c
        self.f = f
        self.rMax  = rMax 
        self.color = color
        self.SetUp()
        self.SetPhase(phi)

    def Increment(self, dt):
        pass
        
    def SetPhase(self, phi):
        self.phi = self.Wrap(phi, 2*np.pi)
        self.t0 = self.T*(1 - self.phi / (2*np.pi))
        self.t = 0

    def SetUp(self):
        self.lambda0 = self.c / self.f 
        self.T = 1./self.f 
        self.N = int(np.ceil(self.rMax / self.lambda0))
        self.circles = [plt.Circle(xy = tuple(self.r), fill=False, lw =1.5, radius=i*self.lambda0, alpha=0.2, color=self.color) 
                        for i in range (self.N)]
        
    def Wrap(self, x, x_max):
        if x >= 0:
            return x - np.floor(x / x_max) * x_max 
        if x < 0:
            return x_max - (-x -np.floor(-x / x_max) * x_max)   

FPS = 30
X, Y = 100, 100
c, f = 3, 0.1


duration = 5  # Duration of the animation in seconds

fig, ax = plt.subplots()
ax.set_xlim([-X/2, Y/2])
ax.set_ylim([-X/2, Y/2])
ax.set_aspect(1)
ax.grid(alpha=0.3)
fig.tight_layout()

e = Emitter(0, 0, c, f, 0)

circles = [plt.Circle(xy=tuple(e.r), fill=False, lw=1.5, radius=(i + 1) * e.lambda0, alpha=0.2, color=e.color)
           for i in range(e.N)]
emitter = plt.Circle(xy=tuple(e.r), fill=True, lw=1.5, radius=2, color=e.color)

ax.add_patch(emitter)

for circle in e.circles:
    ax.add_patch(circle)

def init():
    return circles + [emitter]

def update(frame_number):
    dt = 1 / FPS
    e.Increment(dt)

    for i, circle in enumerate(circles):
        circle.set_center(tuple(e.r))
        circle.set_radius((i + 1) * e.lambda0)

    emitter.set_center(tuple(e.r))

    return circles + [emitter]

ani = FuncAnimation(fig, update, init_func=init, frames=FPS * duration, interval=1000 / FPS, blit=True)

plt.show()
