import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, Circle

# Параметры системы
g = 9.81
m = 1.0
r = 0.05       # Радиус шарика
M = 1e6        # Большая масса стержня
L = 0.1        # Длина стержня
a = 1       # Толщина стержня
A = 1.0        # Амплитуда колебаний
omega = 2*np.pi  # Частота колебаний
phi0 = 0.0     # Начальная фаза
alpha = 0.5   # Коэффициент потерь

# Начальные условия
y0_ball = 2.0  # Начальная высота центра шарика
v0_ball = 0.0   # Начальная скорость

# Время моделирования
t_max = 10.0

# Функции движения стержня
def y_rod(t):
    return A*np.sin(omega*t + phi0)

def v_rod(t):
    return A*omega*np.cos(omega*t + phi0)

# Уравнения движения шарика
def ballistic(t, state):
    y, v = state
    return [v, -g]

# Событие столкновения
def collision_event(t, state):
    y, v = state
    return (y - r) - (y_rod(t) + a/2)  # Учет размеров

collision_event.terminal = True
collision_event.direction = -1

# Моделирование
times = []
y_ball = []
y_rod_t = []
state = [y0_ball, v0_ball]
t_prev = 0.0

while t_prev < t_max:
    sol = solve_ivp(ballistic, [t_prev, t_max], state, 
                   events=collision_event, max_step=0.01)
    
    # Сохранение данных
    times.extend(sol.t)
    y_ball.extend(sol.y[0])
    y_rod_t.extend(y_rod(sol.t))
    
    if not sol.t_events[0].size > 0:
        break
    
    # Обработка столкновения
    t_coll = sol.t_events[0][0]
    v_ball_before = sol.y_events[0][0][1]
    v_rod_before = v_rod(t_coll)
    
    # Расчет новой скорости
    rel_vel = v_ball_before - v_rod_before
    new_rel_vel = -np.sqrt(1 - alpha)*rel_vel if alpha else -rel_vel
    v_ball_after = v_rod_before + new_rel_vel
    
    # Корректировка позиции
    state = [y_rod(t_coll) + a/2 + r, v_ball_after]
    t_prev = t_coll

# Настройка анимации
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(-10*L, 10*L)
ax.set_ylim(-A*1.5, y0_ball*5)
ax.set_aspect('equal')
ax.grid(True)

# Создание графических объектов
rod = Rectangle((-L/2, y_rod(0)-a/2), L, a, fc='gray', zorder=1)
ball = Circle((0, y0_ball), r, fc='red', zorder=2)
ax.add_patch(rod)
ax.add_patch(ball)

def init():
    rod.set_y(y_rod(0)-a/2)
    ball.set_center((0, y0_ball))
    return rod, ball

def animate(i):
    rod.set_y(y_rod_t[i]-a/2)
    ball.set_center((0, y_ball[i]))
    return rod, ball

ani = animation.FuncAnimation(fig, animate, init_func=init,
                            frames=len(times), interval=20, blit=True)

plt.show()