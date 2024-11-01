import numpy as np
import matplotlib.pyplot as plt

# Параметры для генерации данных
num_samples = 100  # Количество точек

# Генерация двух массивов случайных данных
x_data = np.random.rand(num_samples)
y_data = np.random.rand(num_samples)

# Построение диаграммы рассеяния
plt.scatter(x_data, y_data, color='green', alpha=0.5, edgecolor='black')
plt.title('Диаграмма рассеяния для двух наборов случайных данных')
plt.xlabel('X данные')
plt.ylabel('Y данные')
plt.grid(True)
plt.show()
