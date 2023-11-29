# python laboratornaya_rabota.txt
import copy
import numpy as np
from random import randint
from tkinter import * 
#import tkinter as tk
import matplotlib.pyplot as plt
import time
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from prettytable import PrettyTable

#A1=[[32.0, 28.0, 4.0, 26.0, 4.0], [17.0, 19.0, 4.0, 17.0, 4.0], [4.0, 4.0, 5.0, 4.0, 4.0], [17.0, 14.0, 4.0, 14.0, 4.0], [21.0, 16.0, 4.0, 13.0, 4.0]] #res=39
#A1=[[2.0, 5.0, 3.0, 10.0, 4.0], [6.0, 4.0, 8.0, 1.0, 1.0], [4.0, 6.0, 5.0, 3.0, 5.0], [3.0, 2.0, 6.0, 4.0, 3.0], [3.0, 1.0, 1.0, 4.0, 4.0]] #res = 9
A1=[[3.0, 7.0, 4.0, 11.0, 8.0], [7.0, 6.0, 9.0, 2.0, 5.0], [4.0, 8.0, 6.0, 6.0, 9.0], [2.0, 7.0, 6.0, 4.0, 5.0], [4.0, 3.0, 2.0, 5.0, 8.0]] #res=18

global Matrix
global Font
Font='Arial 12'
global font_width
font_width=12//1.3  #ширина одной буквы шрифта
global font_height
font_height = 12

global w_sklad
global h_sklad
global Matrix_label
global N
global a1 #нижняя граница
global a2 #верхняя граница
global b1
global b2

class mesh():
	def __init__(self, x1, y1):
		self.string=x1  #номер строки
		self.column=y1  #номер столбца

def generate_matrix(a1, a2, n):
    A = []
    for i in range(n):
        row = [randint(a1, a2)] * n
        A.append(row)
    return A

def generate_B(b1, b2, n):
    B = []
    delta = (b2 - b1)
    for i in range(n):
        row = [b2 - i * delta / (n + 1)]
        step = (row[0] - b1) / n
        for j in range(1, n + 1):
            row.append(row[j - 1] - step)
        B.append(row)
    return B

def dop_zadanie_matrix(A, B):
    n = len(A[0])
    n1 = n // 2
    for i in range(n):
        for j in range(1, n):
            k = 1
            for m in range(j + 2):
                k *= B[i][m]
            A[i][j] *= k
    for i in range(n):
        for j in range(n):
            A[i][j] = float(A[i][j])
    return A

def min_null(arr): #игнорит нули
	min=10000000000
	n = len(arr)
	for i in range(0, n):
		if(arr[i]!=0)and(arr[i]<min):
			min=arr[i]
	return min

def sort_key(k):
	return(k.column)

def vengersky_algoritm(A):
	n=len(A[0])
	M=copy.deepcopy(A) #так как матрицу A мы портим
	pp=0
	null_arr=[]
	while(len(null_arr)!=n):
		null_arr.clear()
		pp=pp+1
		#первый пункт, вычитание минимума из строки
		for i in range(0, n):
			min_str=min(A[i])
			for j in range(0, n):
				A[i][j]=A[i][j]-min_str
		for j in range(0, n): #если в каких-то столбцах нет нулей, то они там появятся (по аналогии со строкой)
			flag=False
			for i in range(0, n):
				if(A[i][j]==0):
					flag=True
			if(flag==False):
				column=[]
				for k in range(0, n):
					column.append(A[k][j])
				min_str=min(column)
				for i in range(0, n):
					A[i][j]=A[i][j]-min_str
				column.clear()

		#второй пункт

		null_count=[]
		for i in range(0, n):
			count=0
			for j in range(0, n):
				if(A[i][j]==0):
					count=count+1
			null_count.append(count)

		zero_in_A=True
		A_temp=copy.deepcopy(A) #рекурсивный метод
		num_zero_string=[] #массив номеров вычеркнутых строк
		num_zero_column=[] #массив номеров вычеркнутых столбцов
		while(zero_in_A): #вычеркиваем строки и столбцы из матрицы, убирая все нули (заполняем -1)
			null_count=[] #сначала смотрим строки
			for i in range (0, n): #ищем число нулей в каждой строке
				count=0
				for j in range(0, n):
					if(A_temp[i][j]==0):
						count=count+1
				null_count.append(count)
			for j in range (0, n): #ищем число нулей в каждом столбце
				count=0
				for i in range(0, n):
					if(A_temp[i][j]==0):
						count=count+1
				null_count.append(count)
			max_zero=max(null_count)#находим max ЧИСЛО нулей
			num_max=-1
			for i in range(0, 2*n):
				if(null_count[i]==max_zero):
					num_max=i
					break
			#куда-то сюда вставить еще одну проверку
			if(num_max<n): #в строке с max числом нулей все элементы делаем =-1
				if(null_count[num_max]==1):
					#находим номер столбца, в котором содержится этот ноль
					col_num=-1
					for i in range(0, n):
						if(A_temp[num_max][i]==0.0):
							col_num=i
							break
					#находим число -1 в столбце
					col_count=0
					for i in range(0, n):
						if(A_temp[i][col_num]==-1):
							col_count=col_count+1
					#находим число -1 в строке
					str_count=0
					for j in range(0, n):
						if(A_temp[num_max][j]==-1):
							str_count=str_count+1
					if(str_count > col_count):   #вычеркиваем строку
						for j in range(0, n):
							A_temp[num_max][j]=-1
						num_zero_string.append(num_max)
					else:   #вычеркиваем столбец
						for i in range(0, n):
							A_temp[i][col_num]=-1
						num_zero_column.append(col_num)

				else:
					num_zero_string.append(num_max)
					for j in range(0, n):
						A_temp[num_max][j]=-1
			#теперь здесь переделать
			else:  #в столбце с max числом нулей все элементы делаем =-1
				if(null_count[num_max]==1):
					#находим номер строки, в которой содержится этот ноль
					str_num=-1
					for i in range(0, n):
						if(A_temp[i][num_max]==0.0):
							str_num=i
							break
					#находим число -1 в столбце
					col_count=0
					for i in range(0, n):
						if(A_temp[i][num_max]==-1):
							col_count=col_count+1
					#находим число -1 в строке
					str_count=0
					for j in range(0, n):
						if(A_temp[str_num][j]==-1):
							str_count=str_count+1
					if(str_count > col_count):   #вычеркиваем строку
						for j in range(0, n):
							A_temp[str_num][j]=-1
						num_zero_string.append(str_num)
					else:   #вычеркиваем столбец
						for i in range(0, n):
							A_temp[i][num_max]=-1
						num_zero_column.append(num_max)
				else:
					num_zero_column.append(num_max-n)
					for i in range(0, n):
						A_temp[i][num_max-n]=-1

			#Проверка матрицы A_temp на наличие нулей
			zero_in_A=False
			for i in range(0, n):
				for j in range(0, n):
					if (A_temp[i][j]==0):
						zero_in_A=True
						break
				if (zero_in_A==True):
					break
		#находим минимум среди всех ненулевых элементов в A_temp
		no_zero_arr=[]
		for i in range(0, n):
			for j in range(0, n):
				if (A_temp[i][j]!=-1):
					no_zero_arr.append(A_temp[i][j])
		if(len(no_zero_arr)!=0):
			min_temp=min(no_zero_arr)
			for i in range(0, n): #вычитаем min_temp из невычеркнутых элементов
				for j in range(0, n):
					if (A_temp[i][j]!=-1):
						A_temp[i][j]=A_temp[i][j]-min_temp

		no_zero_arr.clear()
		#переход к исходной матрице
		for i in range(0, n): #
			for j in range(0, n):
				if (A_temp[i][j]!=-1):
					A[i][j]=A_temp[i][j]

		# к элементам в пересечениях зачеркнутых линий прибавляем min
		for i in range(0, len(num_zero_string)):
			for j in range(0, len(num_zero_column)):
				A[num_zero_string[i]][num_zero_column[j]]=A[num_zero_string[i]][num_zero_column[j]]+min_temp
	
		#Начало пункта 3, выделяем нули
		A_temp2=copy.deepcopy(A)
		while(1):
			null_count=[] #сначала смотрим строки (находим число нулей)
			for i in range (0, n):
				count=0
				for j in range(0, n):
					if(A_temp2[i][j]==0):
						count=count+1
				null_count.append(count)
			for j in range (0, n): #потом смотрим столбцы в порядке возрастания  (находим число нулей)
				count=0
				for i in range(0, n):
					if(A_temp2[i][j]==0):
						count=count+1
				null_count.append(count)
	
			null_in_matrix=False
			for i in range(0, 2*n):
				if(null_count[i]!=0):
					null_in_matrix=True
			if(null_in_matrix==False):
				break
	
			min1=min_null(null_count) #(min)
			num_min1=0
			num_min2=0
			for i in range(0, 2*n):
				if(null_count[i]==min1):
					num_min1=i
					break
			num_null=[]
			if(num_min1<n): #(выбрано 0 в строке), НЕ ПРОВЕРЕНО  (num_min1-в строке, num_min2 - в столбце)
				null_count2=[]
				for j in range(0, n):
					if(A_temp2[num_min1][j]==0):
						num_null.append(j)
				for i in range(0, len(num_null)): #записываем число нулей в строках
					null_count2.append(null_count[num_null[i]])
				min2=min_null(null_count2)#находим минимальное число нулей среди столбцов (min)
				for i in range(0, len(null_count2)):#находим номер элемента массива, содержащий номер столбца с минимальным числом нулей
					if(null_count2[i]==min2):
						num_min2=i
						break
				num_min2=num_null[num_min2]#находим номер строки
				num_min1=num_min1
				for i in range (0, n):
					A_temp2[num_min1][i]=-1
				for i in range (0, n):
					A_temp2[i][num_min2]=-1
				null_arr.append(mesh(num_min1, num_min2))

			else: #ищем num_min2 (выбрано 0 в столбце)  (num_min1-в столбцe, num_min2 - в строке)
				null_count2=[]
				for i in range(0, n): #находим номера строк, в которых есть нули
					if(A_temp2[i][num_min1-n]==0):
						num_null.append(i)
				for i in range(0, len(num_null)): #записываем число нулей в строках
					null_count2.append(null_count[num_null[i]])
				min2=min_null(null_count2)#находим минимальное число нулей среди строк  (min)
				for i in range(0, len(null_count2)):#находим номер элемента массива, содержащий номер строки с минимальным числом нулей
					if(null_count2[i]==min2):
						num_min2=i
						break
				num_min2=num_null[num_min2]#находим номер строки
				num_min1=num_min1-n
				for i in range (0, n):
					A_temp2[num_min2][i]=-1
				for i in range (0, n):
					A_temp2[i][num_min1]=-1
				null_arr.append(mesh(num_min2, num_min1))
			null_count.clear()
		A_temp2.clear()
		A_temp.clear()
		num_zero_string.clear()
		num_zero_column.clear()
		#КОНЕЦ ЦИКЛА
	return(null_arr)


def vengersky_algoritm_max(A):
	max=0
	n=len(A)
	A1=copy.deepcopy(A)
	for i in range(0, n):
		for j in range(0, n):
			if(A1[i][j]>max):
				max=A1[i][j]
	for i in range(0, n):
		for j in range(0, n):
			A1[i][j]=-A1[i][j]
	for i in range(0, n):
		for j in range(0, n):
			A1[i][j]=A1[i][j] + max
	"""for i in range(0, n):
		for j in range(0, n):
			print(A1[i][j], "   ", end="")
		print("")"""
	index=vengersky_algoritm(copy.deepcopy(A1))
	index1=sorted(index, key=sort_key)
	S=[]
	for i in range(1, (n+1)):
		S_tmp=0.0
		for j in range(0, i):
			S_tmp=S_tmp+A[index1[j].string][index1[j].column]
		S.append(S_tmp)
	return(S)

def vengersky_algoritm_get_index(A):
	max=0
	n=len(A)
	A1=copy.deepcopy(A)
	for i in range(0, n):
		for j in range(0, n):
			if(A1[i][j]>max):
				max=A1[i][j]
	for i in range(0, n):
		for j in range(0, n):
			A1[i][j]=-A1[i][j]
	for i in range(0, n):
		for j in range(0, n):
			A1[i][j]=A1[i][j] + max
	"""for i in range(0, n):
		for j in range(0, n):
			print(A1[i][j], "   ", end="")
		print("")"""
	index=vengersky_algoritm(copy.deepcopy(A1))
	index1=sorted(index, key=sort_key)
	return(index1)


def vengersky_algoritm_min(A):
	n=len(A)
	index=vengersky_algoritm(copy.deepcopy(A))
	index1=sorted(index, key=sort_key)
	S=[]
	for i in range(1, (n+1)):
		S_tmp=0
		for j in range(0, i):
			S_tmp=S_tmp+A[index1[j].string][index1[j].column]
		S.append(S_tmp)
	return(S)



def greedy_algorithm(A): #жадный алгоритм
	n=len(A[0])
	S=[]
	sum=0
	for j in range(0, n):
		max=-1
		for i in range(0, n):
			if (A[i][j]>max):
				max=A[i][j]
		sum=sum+max
		S.append(sum)
		#находим номер строки, в которой содержится max
		num_str_max=0
		for i in range(0, n):
			if (A[i][j]==max):
				num_str_max=i
				break
		for i in range(0, n):
			A[num_str_max][i]=-1
		
	return(S)


def econom_algorithm(A): #бережливый алгоритм
	n=len(A)
	S=[]
	sum=0
	for j in range(0, n):
		min=10000000000.0
		for i in range(0, n):
			if (A[i][j]<min):
				min=A[i][j]
		sum=sum+min
		S.append(sum)
		#находим номер строки, в которой содержится min
		num_str_min=0
		for i in range(0, n):
			if (A[i][j]==min):
				num_str_min=i
				break
		for i in range(0, n):
			A[num_str_min][i]=10000000000.0
	return(S)



def draw_graph(window, N, s_veng_min, s_veng_max, s_greedy, s_econom):
	fig1, ax = plt.subplots()
	fig1.set_size_inches(5, 4)
	frame1 = Frame(window)

	frame1.place(x=w_sklad - w_sklad//2.5, y=h_sklad//6) #pack(side=TOP, fill=BOTH, expand=1)
	canvas1 = FigureCanvasTkAgg(fig1, master=window)
	canvas1.get_tk_widget().place(x=w_sklad - w_sklad//3, y=h_sklad//6) #pack(side=TOP, fill=BOTH, expand=1) #2.5
    		# Plot data on Matplotlib Figure
    		#Посторение matplotlib-графика

    		#Заголовок графика
	plt.title('Графики работы алгоритмов', fontsize=12)
   	 	#Подписи Осей X и Y
	plt.xlabel('Время', fontsize=12, color='brown')
	plt.ylabel('S', fontsize=12, color='brown')
    		# Массив точек x от 1 до N
	x = []
	for i in range(1, (N + 1)):
		x.append(i)
	
	plt.plot(x, s_veng_max, label= "Венгерский (находит максимум)")
	plt.plot(x, s_veng_min, label= "Венгерский (находит минимум)")
	plt.plot(x, s_greedy, label= "Бережливый")
	plt.plot(x, s_econom, label= "Жадный")
	
	plt.grid("True")
	plt.legend()




def error_greedy(res_veng_max, res_greedy):
    abs_err = res_veng_max - res_greedy # Нахожу абс погрешность алгоритма
    res1 = abs_err / res_veng_max       # Нахожу отн погрешность алгоритма
    res2 = round(res1, 2)               # Округляю погрешность до 2 знаков после запятой
    return res2

#-------------------------ОТНОСИТЕЛЬНАЯ ПОГРЕШНОСТЬ БЕРЕЖЛИВОГО АЛГОРИТМА------------------------------------------------
def error_econom(res_veng_max, res_econom):
    abs_err = res_veng_max - res_econom # Нахожу абс погрешность алгоритма
    res1 = abs_err / res_veng_max       # Нахожу отн погрешность алгоритма
    res2 = round(res1, 2)               # Округляю погрешность до 2 знаков после запятой
    return  res2


#-----------------------------ЗАПИСЬ В ФАЙЛ---------------------------------------------------------------------
def write_to_file(res_econom ,res_greedy ,res_veng_max, econom_err, greedy_err):
    mytable = PrettyTable()
    #Шапка таблицы
    mytable.field_names = ["Результат Бережливого алгоритма", "Результат Жадного алгоритма",
                           "Результат Оптимального алгоритма", "Относительная погрешность Бережливого алгоритма ",
                           "Относительная погрешность Жадного алгоритма "]

    #Добавление строки с полученными данными в таблицу
    mytable.add_row([ res_econom ,res_greedy ,res_veng_max, econom_err, greedy_err])

    with open('Table.txt', 'a+') as fp:
        # создаем строку для записи в файл
        table = mytable.get_string()
        # пишем данные
        fp.write(table)

        # дописываем символ начала строки
        fp.write('\n')

#-----------------------------СОХРАНЕНИЕ ГРАФИКА---------------------------------------------------------------------
def save_graph():
    graph_num = randint(1, 20)
    graph_name = "График " + str(graph_num)
    plt.savefig(graph_name)





def set_n(window, set_size_matrix_label, but, get_sz, n_vvod, y_vvod_n):  #первая кнопка в программе 
	global N
	N =int(n_vvod.get())
	get_sz.destroy()
	but.destroy()
	set_size_matrix_label.destroy()
	big_matrix=False
	
	if(N>15): 
		big_matrix=True
		str1="матрица не будет выведена на экран из-за слишком большого размера: "
		big_m = Label(text = str1,  font = Font)
		big_m.place(x=10, y=50)
		
		get_a1_good=StringVar()
		str1 = "Введите НИЖНЮЮ границу значений сахаристости (не более 2 порядков): "
		a1_print_label = Label(text = str1, font = Font)
		a1_print_label.place(x=10, y=y_vvod_n)
		set_a1 = Entry(width=5, textvariable=get_a1_good,  font = Font)
		set_a1.place(x=(len(str1)-2)*font_width, y=y_vvod_n)
	
		get_a2_good=StringVar()
		str1 = "Введите ВЕРХНЮЮ границу значений сахаристости (не более 2 порядков): "
		a2_print_label = Label(text = str1, font = Font)
		a2_print_label.place(x=10, y=y_vvod_n+3*font_height)
		set_a2 = Entry(width=5, textvariable=get_a2_good,  font = Font)
		set_a2.place(x=(len(str1)-3)*font_width, y=y_vvod_n+3*font_height)
	
		set_sahar_button = Button(window, background="yellow", text = "отправить", command = lambda *args: set_sahar(window, a1_print_label, a2_print_label, get_a1_good, get_a2_good, set_a1, set_a2, set_sahar_button, y_vvod_n, big_matrix, big_m), font = Font)
		set_sahar_button.place(x=(len(str1)+8)*font_width, y=y_vvod_n)

	if(N<=1): 
		str1="Вы ввели слишком маленькую или отрицательную размерность матрицы. попробуйте еще раз: "
		set_size_matrix_label_err2 = Label(text = str1,  font = Font)
		set_size_matrix_label_err2.place(x=10, y=y_vvod_n)
		n_vvod_err2=StringVar() 
		get_size_err2 = Entry(width=5,background="yellow", textvariable=n_vvod_err2,  font = Font)
		get_size_err2.place(x=(len(str1)-5)*font_width, y=y_vvod_n)
		set_n_button_err2 = Button(window, text = "отправить", command = lambda *args: set_n(window, set_size_matrix_label_err2, set_n_button_err2, get_size_err2, n_vvod_err2,y_vvod_n, big_matrix), font = Font)  #по сути, это рекурсия
		set_n_button_err2.place(x=(len(str1)+5)*font_width, y=y_vvod_n)  #кнопка отправки размера матрицы
		 
	if ((N<=15)and(N>1)):

		str1=""
		big_m = Label(text = str1,  font = Font)
		big_m.place(x=10, y=50)
		
		get_a1_good=StringVar()
		str1 = "Введите НИЖНЮЮ границу значений сахаристости (не более 2 порядков): "
		a1_print_label = Label(text = str1, font = Font)
		a1_print_label.place(x=10, y=y_vvod_n)
		set_a1 = Entry(width=5, textvariable=get_a1_good,  font = Font)
		set_a1.place(x=(len(str1)-2)*font_width, y=y_vvod_n)
	
		get_a2_good=StringVar()
		str1 = "Введите ВЕРХНЮЮ границу значений сахаристости (не более 2 порядков): "
		a2_print_label = Label(text = str1, font = Font)
		a2_print_label.place(x=10, y=y_vvod_n+3*font_height)
		set_a2 = Entry(width=5, textvariable=get_a2_good,  font = Font)
		set_a2.place(x=(len(str1)-3)*font_width, y=y_vvod_n+3*font_height)
	
		set_sahar_button = Button(window, background="yellow", text = "отправить", command = lambda *args: set_sahar(window, a1_print_label, a2_print_label, get_a1_good, get_a2_good, set_a1, set_a2, set_sahar_button, y_vvod_n, big_matrix, big_m), font = Font)
		set_sahar_button.place(x=(len(str1)+8)*font_width, y=y_vvod_n)


def set_sahar(window, a1_print_label, a2_print_label, get_a1_good, get_a2_good, set_a1, set_a2, set_sahar_button, y_vvod_n, big_matrix, big_m):  #обработчик второй кнопки в программе 
	global a1
	global a2
	global Matrix
	global Matrix_label
	#print("get_a1_good.get() = ", get_a1_good.get())
	a1=int(get_a1_good.get()) #get_a1_good.get()
	a2=int(get_a2_good.get()) #get_a2_good.get()
	set_sahar_button.destroy()
	set_a1.destroy()
	a1_print_label.destroy()
	set_a2.destroy()
	a2_print_label.destroy()

	if(big_matrix==False):
		str1 = "Сгенерированная матрица: "
		m_label = Label(text = str1, font = Font)
		m_label.place(x=20, y=20)
	else:
		str1 = ""
		m_label = Label(text = str1, font = Font)
		m_label.place(x=20, y=20)

	Matrix=generate_matrix(a1, a2, N)
	a_max_len=len(str(a2))
	x0=40
	y0=10
	x1=x0
	y1=y0

	if(a1>a2):
		tmp=a2
		a2=a1
		a1=tmp

	set_b1=StringVar() #было get
	str1 = "Введите НИЖНЮЮ границу значений коэффициэнта деградации (дробную часть вводите через точку): "
	b1_print_label = Label(text = str1, font = Font)
	b1_print_label.place(x=10, y=y_vvod_n)
	get_b1 = Entry(width=5, textvariable=set_b1,  font = Font)
	get_b1.place(x=(len(str1)-5)*font_width, y=y_vvod_n)
	
	set_b2=StringVar() #было get
	str1 = "Введите ВЕРХНЮЮ границу значений коэффициэнта деградации (дробную часть вводите через точку): "
	b2_print_label = Label(text = str1, font = Font)
	b2_print_label.place(x=10, y=y_vvod_n+3*font_height)
	get_b2 = Entry(width=5, textvariable=set_b2,  font = Font)
	get_b2.place(x=(len(str1)-6)*font_width, y=y_vvod_n+3*font_height)
	set_b12_button = Button(window, background="yellow", text = "построить график", command = lambda *args: set_b12(window, b1_print_label, b2_print_label, get_b1, get_b2, set_b1, set_b2, set_b12_button, m_label, y_vvod_n, big_matrix, big_m), font = Font)
	set_b12_button.place(x=(len(str1)+5)*font_width, y=y_vvod_n)

	if(big_matrix==False):
		k=0 #счетчик элементов массива Matrix_label
		y1=y1+3*font_height
		Matrix_label=[]
		for i in range(0, N):
			for j in range(0, N):
				Matrix_label.append(Label(text = str(Matrix[i][j]), font = Font))
				Matrix_label[k].place(x=x1, y=y1)
				x1=x1+(a_max_len+2)*font_width #возможно, +2 сделать
				k=k+1
			x1=x0
			y1=y1+3*font_height

	
def set_b12(window, b1_print_label, b2_print_label, get_b1, get_b2, set_b1, set_b2, set_b12_button, m_label, y_vvod_n, big_matrix, big_m):  #обработчик третьей кнопки в программе
	global b1
	global b2 
	global Matrix_label
	if(big_matrix==False):
		for i in range(0, len(Matrix_label)):
			Matrix_label[i].destroy()
		Matrix_label.clear()
	b1=float(set_b1.get())
	b2=float(set_b2.get())
	set_b12_button.destroy()
	get_b1.destroy()
	b1_print_label.destroy()
	get_b2.destroy()
	b2_print_label.destroy()
	big_m.destroy()
	
	m_label.destroy()

	if(b1>b2):
		tmp=b2
		b2=a1
		b1=tmp
	B = generate_B(b1, b2, N)
	P = dop_zadanie_matrix(Matrix, B)
	
	s_veng_min = vengersky_algoritm_min(copy.deepcopy(P)) #возвращает массив частичных сумм
	s_veng_max = vengersky_algoritm_max(copy.deepcopy(P)) #возвращает массив частичных сумм
	
	s_greedy = greedy_algorithm(copy.deepcopy(P))
	s_econom = econom_algorithm(copy.deepcopy(P))
	draw_graph(window, N, s_veng_min, s_veng_max,  s_econom, s_greedy)
	index = vengersky_algoritm_get_index(copy.deepcopy(P))
	#k=0 #счетчик элементов массива Matrix_label

	str1 = "Оптимальное решение состоит из следующих элементов матрицы P: "
	res_label = Label(text = str1, font = Font)
	res_label.place(x=10, y=20)
	
	y1=20+3*font_height
	x0=10
	x1=x0
	Matrix_label=[]
	k=0
	while(k<N):
		str1 = "P"+"["+str(index[k].string)+"]"+"["+ str(index[k].column)+"]"
		Matrix_label.append(Label(text = str1, font = Font))
		Matrix_label[k].place(x=x1, y=y1)
		x1=x1+(len(str1)+2)*font_width #возможно, +2 сделать
		k=k+1
		if(k%8==0):
			x1=x0
			y1=y1+2.5*font_height
	
	write_to_file(s_econom[N-1], s_greedy[N-1], s_veng_max[N-1], error_econom(s_veng_max[N-1], s_econom[N-1]), error_greedy(s_veng_max[N-1], s_greedy[N-1]))
	save_graph()

	reset_button = Button(window, text = "начать новый эксперимент", background="yellow",  command = lambda *args: reset(window, reset_button, m_label, res_label), font = Font)
	reset_button.place(x=w_sklad//3, y=h_sklad - h_sklad//7)  #кнопка отправки размера матрицы

	

def reset(window, reset_button, m_label, res_label): #удаление всех виджетов и вызов самой первой функции
	reset_button.destroy()
	global Matrix_label
	res_label.destroy()
	m_label.destroy()
	plt.close('all')
	del_count=int(h_sklad//(font_height*1.5))
	for i in range(0, del_count):
		del_grafik = Label(text = "                                                                                                                                                                                                                                           ", background="white",  foreground= "white",font = Font).place(x=w_sklad - w_sklad//2.5, y=int(font_height*1.5*i))#3
	
	for i in range(0, len(Matrix_label)):
		Matrix_label[i].destroy()
	y_vvod_n=h_sklad-h_sklad//7 #7 - подобрана экспериментально, это значит, что 1/7 часть экрана под ввод данных
	set_size_matrix_label = Label(text = "Введите размерность квадратной матрицы: ",  font = Font)
	set_size_matrix_label.place(x=10, y=y_vvod_n)
	n_vvod=StringVar()
	get_size = Entry(width=5, textvariable=n_vvod,  font = Font)
	get_size.place(x=40*font_width, y=y_vvod_n)  #поле ввода размера матрицы   
	#Отсчет от верхнего левого края экрана  !!
	set_n_button = Button(window, text = "отправить", background="yellow", command = lambda *args: set_n(window, set_size_matrix_label, set_n_button, get_size, n_vvod, y_vvod_n), font = Font)
	set_n_button.place(x=61*font_width, y=y_vvod_n)  #кнопка отправки размера матрицы
	
	


global h_sklad
global w_sklad
window = Tk() 
window.state('zoomed')#полноэкранный режим
window.resizable (False, False)
h_sklad = int(window.winfo_screenheight())  #считываем размер окна
w_sklad = int(window.winfo_screenwidth())   #считываем размер окна 
canvas = Canvas(height=h_sklad, width=w_sklad, bg="white", highlightthickness=0) 
canvas.place(x=0, y=0)


y_vvod_n=h_sklad-h_sklad//7 #7 - подобрана экспериментально, это значит, что 1/7 часть экрана под ввод данных
set_size_matrix_label = Label(text = "Введите размерность квадратной матрицы: ",  font = Font)
set_size_matrix_label.place(x=10, y=y_vvod_n)
n_vvod=StringVar() 
get_size = Entry(width=5, textvariable=n_vvod,  font = Font)
get_size.place(x=40*font_width, y=y_vvod_n)  #поле ввода размера матрицы   
#Отсчет от верхнего левого края экрана  !!
set_n_button = Button(window, background="yellow", text = "отправить", command = lambda *args: set_n(window, set_size_matrix_label, set_n_button, get_size, n_vvod, y_vvod_n), font = Font)
set_n_button.place(x=61*font_width, y=y_vvod_n)  #кнопка отправки размера матрицы
window.mainloop() 

#A1=generate_matrix(50)
"""M=dop_zadanie_matrix(A1, 0.8, 0.6)
n = len(M[0])"""

#print("res = ", lean_algorithm(A1))


