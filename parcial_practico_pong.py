import machine
import ssd1306
import machine
import ssd1306
import time
from machine import ADC, Pin, PWM
import framebuf

#las otas del sonido ganador
buzzer = PWM(Pin(15))
notas2=[554,587,554,493,554,587,554,493,554,587,554,493,554,587,554,493,
        554,587,554,659,587,493,587,659,587,493,587,659,587,493,587,659,
        587,493,587,587,493,587,659,587,493,587,659,587,493,587,659,587,
        493,587,659,587,493,587,659,587,493,587]

# Inicialización de la pantalla OLED
i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(23))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

#busca el logo que esta en la esp32
with open('logos/ping-pong.pbm','rb') as f:   # Abre el fichero para lectura en modo binario
    f.readline()                                # Salta la línea del identificador mágico
    f.readline()                                # Salta la línea de las dimensiones de la imagen
    # f.readline()                                 # Salta la línea de comentario (descomentar si existe)
    data = bytearray(f.read())                  # Lee los datos de la imagen
fbuf = framebuf.FrameBuffer(data, 64, 64, framebuf.MONO_HLSB)   # Datos y tamaño de la imagen...

oled.blit(fbuf, 32, 0)                          # Framebuffer y punto de inicio de representación
oled.show()# Muestra el resultado

#hace un deslizamiento por la parte de derecha a izquierda del logo 
for i in range(0,127):
    oled.scroll(1,0)
    oled.show()

# Configuración de los joysticks
joy1_x = machine.ADC(machine.Pin(34))
joy1_y = machine.ADC(machine.Pin(35))
joy2_x = machine.ADC(machine.Pin(32))
joy2_y = machine.ADC(machine.Pin(33))

# Inicialización de las variables del juego
player1_score = 0
player2_score = 0
ball_x = 64
ball_y = 32
ball_vx = 5
ball_vy = 5
paddle1_y = 24
paddle2_y = 24

# Función para dibujar la pantalla del juego
def draw_screen():
    oled.fill(0)
    oled.text("P1: " + str(player1_score), 0, 0)
    oled.text("P2: " + str(player2_score), 85, 0)
    oled.line(ball_x, ball_y, ball_x + ball_vx, ball_y + ball_vy, 1)
    oled.rect(0, paddle1_y, 2, 16, 1)
    oled.rect(126, paddle2_y, 2, 16, 1)
    oled.show()

# Bucle principal del juego
while player1_score < 5 and player2_score < 5:
    # Actualización de la posición de la pelota
    ball_x += ball_vx
    ball_y += ball_vy
    if ball_x < 1 and paddle1_y <= ball_y <= paddle1_y + 16:
        ball_vx = abs(ball_vx)
    elif ball_x < 0:
        player2_score += 1
        ball_x = 64
        ball_y = 32
        ball_vx +=2
        ball_vy +=2
    elif ball_x > 125 and paddle2_y <= ball_y <= paddle2_y + 16:
        ball_vx = -abs(ball_vx)
    elif ball_x > 127:
        player1_score += 1
        ball_x = 64
        ball_y = 32
        ball_vx +=2
        ball_vy +=2
    if ball_y < 0 or ball_y > 63:
        ball_vy = -ball_vy
        
    # Lectura de los valores de los joysticks
    joy1_x_val = joy1_x.read()
    joy1_y_val = joy1_y.read()
    joy2_x_val = joy2_x.read()
    joy2_y_val = joy2_y.read()
    
    # Actualización de las posiciones de las paletas
    paddle1_y = int(joy1_y_val / 4095 * (64 - 16))
    paddle2_y = int(joy2_y_val / 4095 * (64 - 16))
    
    # Dibujado de la pantalla del juego
    draw_screen()
    
    # Espera de 50 ms para actualizar la pantalla
    time.sleep(0.05)
# Función para tocar la melodía del ganador
def toca_melodia():
    for i in range(len(notas2)):
        buzzer.freq(notas2[i])
        buzzer.duty(50)
        time.sleep_ms(100)
    buzzer.duty(0)

# Muestra el mensaje de fin de juego
oled.fill(0)
if player1_score > player2_score:
    oled.text("¡Jugador 1 Gana!", 4, 27)
else:
    oled.text("¡Jugador 2 Gana!", 4, 27)
oled.show()

toca_melodia()
      
    
# Muestra el mensaje de fin de juego++++
#oled.fill(0)
#if player1_score > player2_score:
    #oled.text("Jugador 1 Gana!", 4, 27)

#else:
    #oled.text("Jugador 2 Gana!", 4, 27)
#oled.show()
#while True: 
    #for i in notas2:
        #buzzer.freq(i)
        #utime.sleep(0.15)