import FacturasDefontana as FD
import TarjetasTrello as TT
import FechasRelativas as FR
import positionstack as PS
import ZeoRoutePlanner as ZRP
import time
from datetime import datetime
from importlib import reload

# Consultar Facturas en defontana
def obtenerFacturas():
    FacturasDefontana = FD.lista_facturas()
    return FacturasDefontana

# Consultar tarjetas existentes en Trello
def obtenerTarjetas():
    tarjetasTrello = TT.lista_tarjetas_trello()
    return tarjetasTrello

# Comparar si existe en Trello y crea tarjeta, o actualiza su estado
def cargar_trello(numero, Facturas, tarjetas):
    try:
        nombre, detalle, tipoDocumento, fecha, direccionCliente, comuna, local = FD.detalle_Factura(numero, Facturas[numero])
    except:
        print(numero, Facturas[numero], "Vacío")
        return None
    else:
        if numero not in tarjetas and datetime.strptime(fecha, "%Y-%m-%dT%H:%M:%S").date() > FR.hace4dias:
            if local == "MONS.":
                etiqueta = TT.etiqueta_Monsalve
                lista = TT.mons_idList
                coordenada = ""
            elif local == "PLAYA":
                etiqueta = TT.etiqueta_Playa
                lista = TT.facturas_idList
                coordenada = ""
                # coordenada, latitude, longitude= PS.obtenerCoordenadas(direccionCliente, comuna)
                # ZRP.ingresa_punto(direccionCliente, comuna, latitude, longitude, detalle,fecha,nombre), "\n", detalle, fecha, nombre
            elif local == "Local":
                etiqueta = TT.etiqueta_Santiago
                lista = TT.facturas_idList
                coordenada = ""
                # coordenada, latitude, longitude= PS.obtenerCoordenadas(direccionCliente, comuna)
                # ZRP.ingresa_punto(direccionCliente, comuna, latitude, longitude, detalle,fecha,nombre), "\n", detalle, fecha, nombre
            else:
                etiqueta = ""
                lista = TT.facturas_idList
                coordenada = ""
            TT.post_trello(nombre, detalle, fecha, direccionCliente, comuna, coordenada, idLabels=etiqueta, idList=lista)
        if numero in tarjetas:
            if datetime.strptime(fecha, "%Y-%m-%dT%H:%M:%S").date() < FR.hace1Semana:
                elimina_Trello(numero, tarjetas)

# Archiva tarjetas Trello
def elimina_Trello(numero, tarjetas):
    TT.mod_trello(tarjetas[numero], "true", TT.listo_idList)

# Archiva tarjetas Trello que no estén en el listado de Facturas pendientes
def elimina_Trello2(Facturas, tarjetas):
    for numero in tarjetas:
        if numero not in Facturas:
            elimina_Trello(numero, tarjetas)

# Función principal, que ejecuta las funciones necesarias para correr el código
def principal():
    print("Inicio")
    Facturas = obtenerFacturas()
    print("Correcto Facturas")
    tarjetas = obtenerTarjetas()
    print("Correcto tarjetas")
    for item in Facturas:
        cargar_trello(item, Facturas, tarjetas)
    elimina_Trello2(Facturas, tarjetas)

# Bucle que mantiene el programa actualizándose   
while True:
    print("Actualizando...")
    try:
        principal()
    except Exception as e:
        print(e)
    print("Actualización: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    time.sleep(300) # Tiempo de espera: 5 minutos
    FR = reload(FR)
# principal() #Test