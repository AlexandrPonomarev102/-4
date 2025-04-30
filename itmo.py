#чтение файла
with open('CdSe_CdZnS Core_Shell.txt', 'r') as file:
    lines = file.readlines()

powers = [] # массив мощностей излучения
for line in lines:
    parts = line.strip().replace(',', '.').split()
    if len(parts) >= 2:
        power = float(parts[1])
        powers.append(power)

# вычисление среднего
n = len(powers)
m = 0.0
for i in powers:
    m += i
m /= n #среднее

# вычисление среднего квадратичного 
sum = 0.0
for j in powers:
    delta = j - m
    sum += delta ** 2
ms = (sum / n) ** 0.5 #среднее квадратичное

print(f"среднее значение: {m:.2f}")
print(f"среднеквадратичное отклонение: {ms:.2f}")
