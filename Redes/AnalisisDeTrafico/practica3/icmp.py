'''
    icmp.py
    
    Funciones necesarias para implementar el nivel ICMP
    Autor: Javier Ramos <javier.ramos@uam.es>
    2022 EPS-UAM
'''
from ip import *
from threading import Lock
import struct

ICMP_PROTO = 1

ICMP_ECHO_REQUEST_TYPE = 8
ICMP_ECHO_REPLY_TYPE = 0

timeLock = Lock()
icmp_send_times = {}

class Config:
    ICMP_SIZE = -1

def process_ICMP_message(us,header,data,srcIp):
    '''
        Nombre: process_ICMP_message
        Descripción: Esta función procesa un mensaje ICMP. Esta función se ejecutará por cada datagrama IP que contenga
        un 1 en el campo protocolo de IP
        Esta función debe realizar, al menos, las siguientes tareas:
            -Calcular el checksum de ICMP y comprobar si es correcto:
            -Extraer campos tipo y código de la cabecera ICMP
            -Loggear (con logging.debug) el valor de tipo y código
            -Si el tipo es ICMP_ECHO_REQUEST_TYPE:
                -Generar un mensaje de tipo ICMP_ECHO_REPLY como respuesta. Este mensaje debe contener
                los datos recibidos en el ECHO_REQUEST. Es decir, "rebotamos" los datos que nos llegan.
                -Enviar el mensaje usando la función sendICMPMessage
            -Si el tipo es ICMP_ECHO_REPLY_TYPE:
                -Extraer del diccionario icmp_send_times el valor de tiempo de envío usando como clave los campos srcIP e icmp_id e icmp_seqnum
                contenidos en el mensaje ICMP. Restar el tiempo de envio extraído con el tiempo de recepción (contenido en la estructura pcap_pkthdr)
                -Se debe proteger el acceso al diccionario de tiempos usando la variable timeLock
                -Mostrar por pantalla la resta. Este valor será una estimación del RTT
            -Si es otro tipo:
                -No hacer nada

        Argumentos:
            -us: son los datos de usuarios pasados por pcap_loop (en nuestro caso este valor será siempre None)
            -header: estructura pcap_pkthdr que contiene los campos len, caplen y ts.
            -data: array de bytes con el conenido del mensaje ICMP
            -srcIP: dirección IP que ha enviado el datagrama actual.
        Retorno: Ninguno
    '''


    # Calcular el checksum de ICMP y comprobar si es correcto

    aux = data[:2] + bytes([0,0]) + data[4:]
    cs = chksum(aux)

    if data[2:4] != cs.to_bytes(2, "little"):
        print("Checksum incorrecto en process_ICMP_message")
        return
    
    type = int.from_bytes(data[0:1], 'big')
    code = int.from_bytes(data[1:2], 'big')

    logging.debug("(process_ICMP_message) Valor type: " + str(type))
    logging.debug("(process_ICMP_message) Valor code: " + str(code))

    if type == ICMP_ECHO_REQUEST_TYPE:
        sendICMPMessage(data[8:], ICMP_ECHO_REPLY_TYPE, code, int.from_bytes(data[4:6], 'big'), int.from_bytes(data[6:8], 'big'), srcIp)
    
    elif type == ICMP_ECHO_REPLY_TYPE:
        with timeLock:
            tiempo = icmp_send_times[srcIp + int.from_bytes(data[4:6], 'big') + int.from_bytes(data[6:8], 'big')]
        logging.debug("(process_ICMP_message) Valor time: " + str(time.time()-tiempo))
    
    return




def sendICMPMessage(data,type,code,icmp_id,icmp_seqnum,dstIP):
    '''
        Nombre: sendICMPMessage
        Descripción: Esta función construye un mensaje ICMP y lo envía.
        Esta función debe realizar, al menos, las siguientes tareas:
            -Si el campo type es ICMP_ECHO_REQUEST_TYPE o ICMP_ECHO_REPLY_TYPE:
                -Construir la cabecera ICMP
                -Añadir los datos al mensaje ICMP
                -Calcular el checksum y añadirlo al mensaje donde corresponda
                -Si type es ICMP_ECHO_REQUEST_TYPE
                    -Guardar el tiempo de envío (llamando a time.time()) en el diccionario icmp_send_times
                    usando como clave el valor de dstIp+icmp_id+icmp_seqnum
                    -Se debe proteger al acceso al diccionario usando la variable timeLock

                -Llamar a sendIPDatagram para enviar el mensaje ICMP
                
            -Si no:
                -Tipo no soportado. Se devuelve False

        Argumentos:
            -data: array de bytes con los datos a incluir como payload en el mensaje ICMP
            -type: valor del campo tipo de ICMP
            -code: valor del campo code de ICMP 
            -icmp_id: entero que contiene el valor del campo ID de ICMP a enviar
            -icmp_seqnum: entero que contiene el valor del campo Seqnum de ICMP a enviar
            -dstIP: entero de 32 bits con la IP destino del mensaje ICMP
        Retorno: True o False en función de si se ha enviado el mensaje correctamente o no
    '''
    icmp_message = bytes()
    icmp_header = bytes()

    if type != ICMP_ECHO_REPLY_TYPE and type != ICMP_ECHO_REQUEST_TYPE:
        print("No es REQUEST ni REPLY")
        return False
    #agregar el campo type
    icmp_header += type.to_bytes(1, "little")
    #agregar el campo code
    icmp_header += code.to_bytes(1, "little")
    #agregar el checksum posteriormente
    icmp_header += bytes([0x0,0x0])
    # agregar identification
    icmp_header += icmp_id.to_bytes(2, "big")
    # agregar sequence number
    icmp_header += icmp_seqnum.to_bytes(2, "big")
    # si es impar añadir un byte a 0
    if len(data) % 2 != 0:
        data += bytes([0x0])
    # si hay opcion de padding (0-9) se añade
    while len(data)+len(icmp_header) < Config.ICMP_SIZE:
        for i in range(10):
            if len(data)+len(icmp_header) >= Config.ICMP_SIZE:
                break
            data += bytes([i])
    # calcular checksum
    cs = chksum(icmp_header+data)
    # añadir al mensaje la cabecera con el checksum y los datos con padding si es impar
    icmp_message = icmp_header[0:2]+cs.to_bytes(2, "little")+icmp_header[4:] + data
    
    # Guardar el tiempo de envio
    if type == ICMP_ECHO_REQUEST_TYPE:
        with timeLock:
            icmp_send_times[dstIP+icmp_id+icmp_seqnum] = time.time()
    # Enviar y retornar
    return sendIPDatagram(dstIP, icmp_message, ICMP_PROTO)


   
def initICMP():
    '''
        Nombre: initICMP
        Descripción: Esta función inicializa el nivel ICMP
        Esta función debe realizar, al menos, las siguientes tareas:
            -Registrar (llamando a registerIPProtocol) la función process_ICMP_message con el valor de protocolo 1

        Argumentos:
            -Ninguno
        Retorno: Ninguno
    '''
    registerIPProtocol(process_ICMP_message, ICMP_PROTO)