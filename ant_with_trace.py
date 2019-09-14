import random
import numpy as np

trace = False		# трассировка значений включена/выключена

# это была тестовая матрица 5х5
#mPaths = np.array([[0, 2, 30, 9, 1], [4, 0, 47, 7, 7], [31, 33, 0, 33, 36], [20, 13, 16, 0, 28], [9, 36, 22, 22, 0]])
np.random.seed(7)
mPaths = np.random.randint(1, 50, size=(20,20))
if trace:
	print("Матрица длин путей между городами:\r\n", mPaths)

# ГИПЕРПАРАМЕТРЫ
# используется при расчёте приращения феромона. Можно задать вручную. Либо рассчитать исходя из суммы одного ряда
#Q = sum(mPaths[0][i] for i in range(mPaths.shape[0])) / 3
Q = 3
ATTENUATION = 0.99			# коэффициент затухания феромонов
STEPS = 10000				# максимальное количество шагов
FALSE_STEPS = mPaths.shape[0] * 40	# если в течение этого количества шагов более короткий путь не найден, завязываем

min_path = []				# Кратчайший путь
min_path_len = 100000000 		# Минимальная длина пути. Просто красивое число, чтобы не делать лишнее сравнение с нулём в коде

# матрица феромонов муравьёв. По размеру матрицы длин. Инициализируется рандомно, потому что надо с чего-то начинать
mFers = np.random.randint(1, 4, size=(mPaths.shape[0], mPaths.shape[0]))
if trace:
	print("Матрица феромонов:\r\n", mFers)

current_false_step = 0 # отсчитываем количество неподходящих расчётов
for x in range(STEPS):
	if trace:
		print("\r\n\r\nПроход №", x)
		
	current = 0			# текущий город (начинаем с нулевого)
	path = [current]		# путь муравьиного коммивояжёра
	path_len = 0			# длина пути коммивояжёра

	for k in range(mPaths.shape[0] - 1):
		# считаем сумму значений длин из текущей строки для тех значений, которых нет в пройденном пути (для нормализации вероятностей в следующем пункте)
		sum_cities = sum(mFers[current][i] / mPaths[current][i] for i in range(mPaths.shape[0]) if i not in path)

		# расчитываем вероятности перехода в города, исходя из кол-ва феромонов и длины пути
		chances = list((mFers[current][i] / mPaths[current][i] / sum_cities, i) for i in range(mPaths.shape[0]) if i not in path)
		if trace:
			print("Вероятность, город =", chances)

		# выбираем случайное число
		rnd = random.random()
		if trace:
			print("Случайное число =", round(rnd,3))

		# выбираем интервал, в который попадает случайное число
		i = 0
		while i < len(chances)-1:
			if rnd <= sum(chances[j][0] for j in range(i+1)):
				break
			i += 1

		# задаём следующий пункт назначения
		next_city = chances[i][1]
		if trace:
			print("Следующий город - № %s\r\n" % next_city)

		path_len += mPaths[current][next_city]	# увеличиваем длину маршрута
		path.append(next_city)			# добавляем пункт в маршрут
		current = next_city

	path.append(0)					# в конце добавляем возврат в исходную точку
	path_len += mPaths[current][0]			# и расстояние до неё, конечно

	if trace:
		print("Путь =", path)
		print("Длина пути =", path_len)

	# если мы обнаружили более короткий путь, сохраняем его
	if path_len < min_path_len:
		min_path_len = path_len
		min_path     = path
		current_false_steps = 0 # сбрасываем счётчик
	else:
		current_false_steps += 1 # наращиваем счётчик количества неподходящих расчётов
		if current_false_steps == FALSE_STEPS:	# если дошло до установленного предела,
			if trace:
				print("Сделано шагов:",x)
			break				# прекращаем поиск

	delta_fer = Q / path_len			# рассчитываем приращение феромона
	mFers = mFers * ATTENUATION			# делаем затухание феромона для всей матрицы
	
	# затем проходим по "дорожке" и добавляем феромон только на ней
	i = 0
	while i < len(path)-1:
		cur = path[i]
		i += 1
		nxt = path[i]
		mFers[cur][nxt] += delta_fer


	if trace:
		print("Delta =", delta_fer)
		print("Новые феромоны:\r\n", mFers)

if trace:
	print("Кратчайший путь:", min_path)
	print("Минимальная длина:", min_path_len)
else:
	print(min_path_len)
