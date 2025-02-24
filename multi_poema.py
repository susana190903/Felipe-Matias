#importacion de librerias
import numpy as np
import time
import subprocess
import mediapipe as mp 
import cv2
from math import sqrt
import signal
import sys
from pynput.keyboard import Controller
import psutil  # Added to help manage processes

#Se crea un objeto Controller para controlar el teclado.
keyboard = Controller()

# Variable global para almacenar el proceso de Main.py
main_process = None

def ejecutar_otro_script():
    global main_process
     # Lanza el otro script en un proceso separado
    main_process = subprocess.Popen(["python", "Main.py"])




# Lugar donde deseas ejecutar el otro script, por ejemplo, al comienzo del script
print("Ejecutando...mian-felipe")
ejecutar_otro_script()

isfullscreen = "NO"
makefullscreen = False
if isfullscreen == "SI":
    makefullscreen = True

isoptimized = "SI"
makeoptimize = False
if isoptimized == "SI":
    makeoptimize = False

#declaracion del numero de zonas
totalpush = int(11)
touchcaps = []
touchcaps = [
    #primera sección
    #{"cap1": (23, 70), "cap2": (235, 130), "com": ["f"], "last": 0, "detected": False, "timer": 0, "title": "Papa"},
    {"cap1": (23, 70), "cap2": (190, 130), "com": ["e"], "last": 0, "detected": False, "timer": 0, "title": "Felicidad"},
    {"cap1": (23, 160), "cap2": (190, 220), "com": ["j"], "last": 0, "detected": False, "timer": 0, "title": "Minucias"},
    {"cap1": (23, 254), "cap2": (190, 315), "com": ["g"], "last": 0, "detected": False, "timer": 0, "title": "Te acuerdas"},
    #segunda sección
    #{"cap1": (307, 70), "cap2": (510, 128), "com": ["e"], "last": 0, "detected": False, "timer": 0, "title": "Felicidad"},
    {"cap1": (220, 70), "cap2": (400, 130), "com": ["d"], "last": 0, "detected": False, "timer": 0, "title": "La huella"},
    {"cap1": (220, 160), "cap2": (400, 220), "com": ["f"], "last": 0, "detected": False, "timer": 0, "title": "Papa"},
    {"cap1": (220, 254), "cap2": (400, 315), "com": ["h"], "last": 0, "detected": False, "timer": 0, "title": "Tiempo malo"},
    #tercera sección
   # {"cap1": (580, 70), "cap2": (775, 128), "com": ["e"], "last": 0, "detected": False, "timer": 0, "title": "Felicidad"},
    {"cap1": (440, 70), "cap2": (620, 130), "com": ["b"], "last": 0, "detected": False, "timer": 0, "title": "Meditando"},
    {"cap1": (440, 160), "cap2": (620, 220), "com": ["c"], "last": 0, "detected": False, "timer": 0, "title": "Para ti Oaxaca"},
    {"cap1": (420, 254), "cap2": (630, 315), "com": ["a"], "last": 0, "detected": False, "timer": 0, "title": "Saludo y Flor de pina"},
    #recuerda cambiar lo que es la letra tanto en la tercera seccion y rectificar los de las otras secciones en el script_names 
    #igual rectifica las letras (consejo para que no te estreses)
]


scripts_abiertos = set() #obtiene los nombres de los scripts que se abren

# guarda los nosmbres de los scrips para llamarlos posteriomente
script_names = {
    "a": "VOZ/flor de piña.py",
    "b": "VOZ/Meditando.py",
    "c": "VOZ/Para ti oaxaca.py",
    "d": "VOZ/La huella.py",
    "e": "VOZ/Felicidad.py",
    "f": "VOZ/Papá.py",
    "g": "VOZ/Te acuerdas.py",
    "h": "VOZ/Tiempo malo.py",
    "j": "VOZ/Minucias.py",

}

barra = "barra_carga.py"

# Variable para checar si el script externo ya está abierto
script_abierto = False
script_actual = None
script_proceso = None  
ultimo_tiempo_apertura = 0 # Variable para almacenar el último tiempo de apertura
ultimo_tiempo_apertura_exitosa = 0


################ segundo codigo ########################################
print("Ejecutando...")


"""
    estas líneas crean alias para módulos 
    específicos dentro de la biblioteca MediaPipe,
    lo que hace que sea más conveniente utilizar las 
    utilidades de seguimiento de manos y dibujo en el código
        
"""
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

#en esta parte se elige el indice de la camara (por si hay una camara externa)
if makeoptimize:
    cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
else:
    cap = cv2.VideoCapture(0)

"""
estas líneas de código están 
ajustando la resolución de los 
fotogramas de video capturados  
"""
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1400)

"""
   este bloque de código se encarga 
   de la gestión de variables relacionadas
   con el seguimiento de gestos y la 
   interacción con las zonas de control 
   en el programa.
"""
counter = 0 
lastgestureX = 0
lastgestureY = 0
lastgestureZ = 0
moveDelta = 30
lastmoveX = 0
lastmoveY = 0
lastmoveZ = 0
waitframe = True
moveX = 0
moveY = 0
moveZ = 0
newZ = True
refZ = 0
absZ = 0
initialpose = True
zoomcounter = 0



#funcion para cerra la barra de progreso por si la mano se quita de 
#las zonas
def cerrar_contador():
    global script_abierto, script_actual, script_proceso, ultimo_tiempo_apertura

    try:
        if script_actual == barra and script_abierto:
                cerrar_script_externo()
    except Exception as e:
        print("Error al cerrar el script del contador:", e)


#funcion para calcular la distancia netre dos puntos
def calc_distance(p1, p2):
    return sqrt((p1[0]-p2[0])*2+(p1[1]-p2[1])*2)


def cerrar_main_script():
    global main_process
    try:
        if main_process:
            # Intentar terminar el proceso principal
            main_process.terminate()
            main_process.wait(timeout=3)  # Esperar hasta 3 segundos para que termine
            
            # Si el proceso aún está vivo, forzar el cierre
            if main_process.poll() is None:
                main_process.kill()
                main_process.wait()
    except Exception as e:
        print(f"Error al cerrar Main.py: {e}")

#funcion para 
def abrir_script_externo(letra):
    global script_abierto, script_actual, script_proceso, ultimo_tiempo_apertura

    try:
        if script_actual:
            print(f"Ya hay un script abierto: {script_actual}")
            if script_abierto != script_actual:
                cerrar_script_externo()
                
            tiempo_actual = time.time()
            if tiempo_actual - ultimo_tiempo_apertura < 3:
                print("Debe esperar 3 segundos antes de abrir otro script.")
                return

        script_name = script_names.get(letra, " ")
        if script_name == barra and script_name in scripts_abiertos:
            print(f"El script {barra} ya está abierto.")
            return

        if script_name:
            # Si el script a abrir no es la barra de progreso, cerrar este script y Main.py
            if script_name != barra:
                print(f"Abriendo {script_name} y cerrando multi_poema.py y Main.py")
                script_proceso = subprocess.Popen(["python", script_name])
                # Cerrar Main.py
                cerrar_main_script()
                # Liberar recursos antes de cerrar
                cap.release()
                cv2.destroyAllWindows()
                # Terminar este script
                sys.exit(0)
            else:
                # Si es la barra de progreso, comportamiento normal
                script_proceso = subprocess.Popen(["python", script_name])
                scripts_abiertos.add(script_name)
                script_abierto = True
                script_actual = script_name
        else:
            print(f"No se encontró el script para la letra '{letra}'")
    except Exception as e:
        print("Error al abrir el script externo:", e)

#funcion para cerrar el script actual 
def cerrar_script_externo():
    global script_abierto, script_actual, script_proceso
    try:
        if script_abierto:
      
            if script_proceso:
                script_proceso.send_signal(signal.SIGTERM)
                script_proceso.wait()
                script_proceso = None
            script_abierto = False
            script_actual = None
            
        else:
            print("No hay ningún script abierto")
    except Exception as e:
        print("Error al cerrar el script externo:", e)

hand_inside_region = False


with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=1) as hands:

    while cap.isOpened():

        ret, frame = cap.read()

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        

        frameWidth = image.shape[1]
        frameHeight = image.shape[0]

        image = cv2.flip(image, 1)

        image.flags.writeable = False

        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        pos = (0, 0)
        cv2.rectangle(image, pos, (frameWidth, frameHeight), (0, 0, 0), -1)

        hands_inside_regions = [False] * len(touchcaps)

        totalHands = 0



        if results.multi_handedness:
            totalHands = len(results.multi_handedness)

            """""
            if totalHands == 2:
                if results.multi_handedness[0].classification[0].label == results.multi_handedness[1].classification[0].label:
                    totalHands = 1
                     """""

        if results.multi_hand_landmarks:
            if initialpose:
                initialpose = False
            #if len(results.multi_hand_landmarks) == 1:
            hand = results.multi_hand_landmarks[0]

            if totalHands == 1:
                for num, hand in enumerate(results.multi_hand_landmarks):
                    indexTip = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    indexTipXY = mp_drawing._normalized_to_pixel_coordinates(indexTip.x, indexTip.y, frameWidth, frameHeight)

                    thumbTip = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.THUMB_TIP]
                    thumbTipXY = mp_drawing._normalized_to_pixel_coordinates(thumbTip.x, thumbTip.y, frameWidth, frameHeight)

                    if indexTipXY and thumbTipXY is not None:
                        indexXY = (indexTipXY[0], indexTipXY[1])
                        thumbXY = (thumbTipXY[0], thumbTipXY[1])
                        

               # else:
                       # print("Hay más de una mano presente. Selecciona solo una mano para el seguimiento.")
#en este ciclo principal se agrego el temporizador para que el script 
# sea llamado o se ejecute despues de mantener la mano por 5 segundos en la zona de gestos
                        for i, r in enumerate(touchcaps):
                           
                            if r["cap1"][0] < indexXY[0] < r["cap2"][0] and r["cap1"][1] < indexXY[1] < r["cap2"][1]:
                                if not r["detected"]:
                                    r["detected"] = True
                                    tiempo_actual = time.time()
                                    tiempo_transcurrido_desde_ultima_apertura = tiempo_actual - ultimo_tiempo_apertura_exitosa
                                    # Verificar si el script de la barra de progreso no está abierto
                                    if not script_abierto or script_actual != barra or tiempo_transcurrido_desde_ultima_apertura >= 5:
                                          
                                            script_proceso = subprocess.Popen(["python", barra])
                                            #cerrar_script_externo()
                                            scripts_abiertos.add(barra)
                                            script_abierto = True
                                            script_actual = barra
                                            ultimo_tiempo_apertura_exitosa = tiempo_actual
                                    r["timer"] = time.time()  # Iniciar el temporizador
                                             
                                  
                                else:
                                    elapsed_time = time.time() - r["timer"]
                                    if elapsed_time >= 5:  # Si han pasado 5 segundos
                                        lastcom = r["last"]
                                        command = r["com"][lastcom]
                                        r["last"] = r["last"] + 1
                                        if r["last"] >= len(r["com"]):
                                            r["last"] = 0
                                           

                                        if command in script_names:
                                            abrir_script_externo(command)


                                        print(command)
                                        keyboard.press(command)
                                        #time.sleep(0.1)
                                        keyboard.release(command)


                                hands_inside_regions[i] = True
                                elapsed_time = time.time() - r["timer"]
                                color_factor = int((elapsed_time % 5) * 51)
                                dynamic_color = (0, 255 - color_factor, color_factor)
                                

 
                                enlarged_cap1 = (r["cap1"][0] - 10, r["cap1"][1] - 10)
                                enlarged_cap2 = (r["cap2"][0] + 10, r["cap2"][1] + 10)


                                cv2.rectangle(image, enlarged_cap1, enlarged_cap2, dynamic_color, -1)    # Bordes verdes
                            else:
                                cv2.rectangle(image, r["cap1"], r["cap2"], (255, 255, 255), 1)




                        mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                            mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                            mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2))
        
            elif totalHands == 2:
                handX = [0, 0]
                handY = [0, 0]
                isHands = [False, False]
                
                for num, hand in enumerate(results.multi_hand_landmarks):
                    indexTip = results.multi_hand_landmarks[num].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    indexTipXY = mp_drawing._normalized_to_pixel_coordinates(indexTip.x, indexTip.y, frameWidth, frameHeight)

                    thumbTip = results.multi_hand_landmarks[num].landmark[mp_hands.HandLandmark.THUMB_TIP]
                    thumbTipXY = mp_drawing._normalized_to_pixel_coordinates(thumbTip.x, thumbTip.y, frameWidth, frameHeight)

                    if indexTipXY and thumbTipXY is not None:
                        indexXY = (indexTipXY[0], indexXY[1])
                        thumbXY = (thumbTipXY[0], indexTipXY[1])

                        for i, r in enumerate(touchcaps):
                            if r["cap1"][0] < indexXY[0] < r["cap2"][0] and r["cap1"][1] < indexXY[1] < r["cap2"][1]:
                                if not r["detected"]:
                                    r["detected"] = True
                                    r["timer"] = time.time()  # Iniciar el temporizador
                                else:
                                    elapsed_time = time.time() - r["timer"]
                                    if elapsed_time >= 5:  # Si han pasado 5 segundos
                                        lastcom = r["last"]
                                        command = r["com"][lastcom]
                                        r["last"] = r["last"] + 1
                                        if r["last"] >= len(r["com"]):
                                            r["last"] = 0

                                        if command in script_names :
                                            abrir_script_externo(command)

                                        print(command)
                                        keyboard.press(command)
                                        time.sleep(0.1)
                                        keyboard.release(command)

                                hands_inside_regions[i] = True

                        mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS, 
                            mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                            mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2))

        else:
            if not initialpose:
                initialpose = True
                print("Posición inicial")

        hand_inside_region = any(hands_inside_regions)

        if not hand_inside_region:
            cerrar_contador()
            for r in touchcaps:
                r["detected"] = False

        for r in touchcaps:
             cv2.rectangle(image, r["cap1"], r["cap2"], (255, 255, 255), 1)

             title_position_x = (r["cap1"][0] + r["cap2"][0]) // 2 - len(r["title"]) * 5
             title_position_y = (r["cap1"][1] + r["cap2"][1]) // 2 + 5  # Ajusta según sea necesario


             cv2.putText(image, r["title"], (title_position_x, title_position_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        
        if not makefullscreen:
            
            try:
                # LOGO 1
                logo_tecnm = cv2.imread('ADICIONALES/LOGO_TECNM.png', cv2.IMREAD_COLOR)
                if logo_tecnm is not None:
                    altura_img1 = 100
                    ancho_img1 = 100
                    logo_tecnm = cv2.resize(logo_tecnm, (ancho_img1, altura_img1))
                else:
                    print("Advertencia: No se pudo cargar LOGO_TECNM.png")
                    logo_tecnm = np.zeros((100, 100, 3), dtype=np.uint8)

                # LOGO 2
                logo_ittux = cv2.imread('ADICIONALES/logo_ittuxx.png', cv2.IMREAD_COLOR)
                if logo_ittux is not None:
                    altura_img2 = 100
                    ancho_img2 = 100
                    logo_ittux = cv2.resize(logo_ittux, (ancho_img2, altura_img2))
                else:
                    print("Advertencia: No se pudo cargar logo_ittux.jpg")
                    logo_ittux = np.zeros((100, 100, 3), dtype=np.uint8)

                # LOGO 3
                logo_museo = cv2.imread('ADICIONALES/logo_museo.png', cv2.IMREAD_COLOR)
                if logo_museo is not None:
                    altura_img3 = 100
                    ancho_img3 = 100
                    logo_museo = cv2.resize(logo_museo, (ancho_img3, altura_img3))
                else:
                    print("Advertencia: No se pudo cargar logo_museo.png")
                    logo_museo = np.zeros((100, 100, 3), dtype=np.uint8)

                # Calcular posiciones asegurando que quepan dentro de los límites del marco
                espacio_entre_logos = 130  # Espacio entre logos
                ancho_total = ancho_img1 + ancho_img2 + ancho_img3 + 2 * espacio_entre_logos
                inicio_x = (frameWidth - ancho_total) // 2

                # Definir posiciones de los logos
                LOGO_TECNM = (inicio_x, frameHeight - altura_img1 - 5)  # 10 píxeles de padding desde abajo
                LOGO_MUSEO = (inicio_x + ancho_img1 + espacio_entre_logos, frameHeight - altura_img2 - 3)
                LOGO_ITTUX = (inicio_x + ancho_img1 + ancho_img2 + 2 * espacio_entre_logos, frameHeight - altura_img3 - 10)

                # Crear imagen base
                base_image = np.zeros((frameHeight, frameWidth, 3), dtype=np.uint8)

                # Colocar logos con verificación de límites
                for pos, logo in [(LOGO_TECNM, logo_tecnm), (LOGO_MUSEO, logo_museo), (LOGO_ITTUX, logo_ittux)]:
                    x, y = pos
                    h, w = logo.shape[:2]
                    
                    # Asegurar que no excedamos los límites del marco
                    if x >= 0 and y >= 0 and x + w <= frameWidth and y + h <= frameHeight:
                        base_image[y:y+h, x:x+w] = logo

                # Combinar imágenes
                combined_image = cv2.add(base_image, image)
                cv2.imshow('Poemas Felipe Matias Velasco', combined_image)

            except Exception as e:
                print(f"Error al manejar los logos: {str(e)}")
                cv2.imshow('Poemas Felipe Matias Velasco', image)  # Mostrar imagen original si falla el manejo de logos
            #window.overrideredirect(1)  # Elimina los bordes y la barra de título

     
        if cv2.waitKey(1) & 0xFF == ord(' '):
            break
#se cambio la condicion para que no se cierre el script
#actual si dejas la  mano sobre la zona
if script_abierto:
    cerrar_script_externo()

cap.release()
cv2.destroyAllWindows()