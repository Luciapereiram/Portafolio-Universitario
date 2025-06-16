import paho.mqtt.client as mqtt
import time

def main():
    """ Simulacion del sistema domotico en general. """

    print("\n-- SIMULACION COMPLETA DEL SISTEMA DOMOTICO --\n")
    time.sleep(5)

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Simulador")
    client.connect(host="test.mosquitto.org", port=1883)

    print("\nAgregando dispositivos al sistema...\n")
    client.publish('redes2/2311/13/discord_request',
                   payload="add_device sensor 1")
    client.publish('redes2/2311/13/discord_request',
                   payload="add_device switch 1")
    client.publish('redes2/2311/13/discord_request',
                   payload="add_device clock 1")
    
    time.sleep(2)

    print("\nRecogiendo estado del switch1...\n")
    client.publish('redes2/2311/13/discord_request',
                   payload="get_state switch 1")
    
    print("\nEstableciendo estado del switch1 a on...\n")
    client.publish('redes2/2311/13/discord_request',
                   payload="set_state switch 1 on")
    
    time.sleep(5)

    print("\nRecogiendo estado del switch1 de nuevo...\n")
    client.publish('redes2/2311/13/discord_request',
                   payload="get_state switch 1")

    print("\nAgregando reglas al sistema...\n")
    client.publish('redes2/2311/13/discord_request',
                   payload="add_rule if sensor1 == 22 or sensor1 == 23 then switch1 = on")
    client.publish('redes2/2311/13/discord_request',
                   payload="add_rule if sensor1 >= 27 then switch1 = off")

    print("\nEstableciendo estado del sensor1 a 27 grados...\n")
    client.publish('redes2/2311/13/discord_request',
                   payload="set_state sensor 1 27")
    
    time.sleep(5)
    
    print("\nRecogiendo estados del switch1 y del sensor1...\n")
    client.publish('redes2/2311/13/discord_request',
                   payload="get_state sensor 1")
    client.publish('redes2/2311/13/discord_request',
                   payload="get_state switch 1")
    
    print("\n-- SIMULACION FINALIZADA (Ver proceso en el resto de terminales) --\n")

if __name__ == '__main__':
    main()
