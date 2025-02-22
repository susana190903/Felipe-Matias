from tkinter import Canvas, Tk, Frame
from math import cos, sin, radians
import timeit

# Crear la ventana principal de la aplicación
ventana = Tk()
ventana.geometry('560x500-10+5')
ventana.config(bg='black')
ventana.overrideredirect(1)

# Crear un marco en la ventana para contener otros elementos
frame = Frame(ventana, height=600, width=600, bg='black', relief='sunken')
frame.grid(columnspan=2, row=0)

# Crear un lienzo (canvas) dentro del marco para dibujar elementos gráficos (marco color blanco)
canvas = Canvas(frame, bg='black', width=545, height=485, bd=1)
canvas.grid(padx=5, pady=5)

# Establecer el tiempo de inicio del programa
inicio_tiempo = timeit.default_timer()

# Establecer la duración de la barra de progreso en segundos
duracion =4.3

# Función que calcula las coordenadas de inicio y fin de la barra de progreso
def calculate_coordinates(nivel):
    centro_x = (100 + 500) / 2 - 30  # Ajusta según sea necesario
    centro_y = (100 + 500) / 2 - 30  # Ajusta según sea necesario
    inicio_x = centro_x + 120 * sin(radians(nivel))
    inicio_y = centro_y - 120 * cos(radians(nivel))
    final_x = centro_x + 120 * sin(radians(nivel + 8))
    final_y = centro_y - 120 * cos(radians(nivel + 8))
    return inicio_x, inicio_y, final_x, final_y

# Función que dibuja la barra de progreso en el lienzo con efecto 3D
def draw_progress_bar_3d(inicio_x, inicio_y, final_x, final_y):
    canvas.create_line(inicio_x, inicio_y, final_x, final_y, fill='orange', width=40, capstyle='round')

# Función que dibuja círculos y texto en el lienzo con efecto 3D
def draw_circles_and_text_3d(centro_x, centro_y, error=False):
    centro_x -= 30  # Ajusta según sea necesario
    centro_y -= 30  # Ajusta según sea necesario

    # Dibuja el círculo exterior con un efecto 3D
    canvas.create_oval(150 - 30, 150 - 30, 450 - 30, 450 - 30, fill='', outline='dark violet', width=15)
    
    # Dibuja el círculo interior con un efecto 3D
    canvas.create_oval(180 - 30, 180 - 30, 420 - 30, 420 - 30, fill='gray22', outline='blue', width=15)
   
    if error:
        canvas.create_text(centro_x, centro_y, text='ABRIENDO', font=('Arial', 27, 'bold'), fill='green')
        canvas.create_text(centro_x, centro_y + 50, text='EL OBJETO', font=('Cambria Math', 22, 'bold'), fill='green')
    else:
        texto = int((nivel / 3.6))
        texto = str(texto) + '%'
        centro_y -= 35  # Puedes ajustar este valor según sea necesario
        canvas.create_text(centro_x, centro_y, text=texto, font=('Arial', 42, 'bold'), fill='deep sky blue')
        canvas.create_text(centro_x, centro_y + 50, text='NO QUITE', font=('Cambria Math', 22, 'bold'), fill='white')
        canvas.create_text(centro_x, centro_y + 80, text='LA MANO', font=('Cambria Math', 25, 'bold'), fill='green')


# Función que actualiza dinámicamente la barra de progreso con efecto 3D
def update_progress_bar_3d():
    global nivel

    # Obtener el tiempo actual
    tiempo_actual = timeit.default_timer()

    # Calcular el tiempo transcurrido desde el inicio del programa
    tiempo_transcurrido = tiempo_actual - inicio_tiempo
    #print(f"Tiempo transcurrido: {tiempo_transcurrido:.6f} segundos")

    # Verificar si el tiempo transcurrido es menor que la duración especificada
    if tiempo_transcurrido < duracion:
        # Calcular el nivel de la barra de progreso en función del tiempo
        nivel = int((tiempo_transcurrido / duracion) * 360)
        nivel %= 360

        # Limpiar el lienzo
        canvas.create_oval(100, 100, 500, 500, fill="", outline='', width=5)

        # Calcular las coordenadas de inicio y fin de la barra de progreso
        inicio_x, inicio_y, final_x, final_y = calculate_coordinates(nivel)

        # Dibujar la barra de progreso en el lienzo con efecto 3D
        draw_progress_bar_3d(inicio_x, inicio_y, final_x, final_y)

        # Calcular las coordenadas del centro
        centro_x = (100 + 500) / 2
        centro_y = (100 + 500) / 2

        # Dibujar círculos y texto en el lienzo con efecto 3D
        draw_circles_and_text_3d(centro_x, centro_y)
        
        # Programar una nueva actualización después de 10 milisegundos
        ventana.after(10, update_progress_bar_3d)
    else:
        # Cuando la duración ha pasado, establecer el nivel en su valor máximo
        nivel = 150

        # Limpiar el lienzo
        canvas.create_oval(100, 100, 500, 500, fill="", outline='', width=5)

        # Calcular las coordenadas de inicio y fin de la barra de progreso
        inicio_x, inicio_y, final_x, final_y = calculate_coordinates(nivel)

        # Dibujar la barra de progreso en el lienzo con efecto 3D
        draw_progress_bar_3d(inicio_x, inicio_y, final_x, final_y)

        # Calcular las coordenadas del centro
        centro_x = (100 + 500) / 2
        centro_y = (100 + 500) / 2

        # Dibujar círculos y texto en el lienzo con mensaje de error y efecto 3D
        draw_circles_and_text_3d(centro_x, centro_y, error=True)

        # Programar la destrucción de la ventana después de 500 milisegundos
        ventana.after(1000, ventana.destroy)

# Iniciar el proceso de actualización de la barra de progreso con efecto 3D
update_progress_bar_3d()

# Iniciar el bucle principal de Tkinter para mantener la interfaz gráfica en ejecución
ventana.mainloop()
