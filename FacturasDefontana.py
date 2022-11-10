import requests
import FechasRelativas as FR
import HeadersKeys as HK

"""
**************************************************************************************
    De momento no considera entregas sin facturar (sólo guía) o notas de crédito.
    Arreglar más adelante
**************************************************************************************
"""

Vendedores = {
			"101": "MAURICIO BRAVO 9 8294 6356",
			"102": "CRISTOBAL BRAVO 9 8258 7699",
			"103": "MATIAS BRAVO 9 8258 3218",
			"104": "GABRIELA 9 3377 0533",
			"105": "RAQUEL 9 4233 7926",
			"106": "FRANCISCO",
			"124869064": "RAQUEL GÓMEZ",
			"201": "C.N.OB.",
			"202": "RICARDO VARGAS",
			"301": "Moroso",
			"VENDEDOR": "VENDEDOR"
}

def lista_facturas():
    listaFacturasAPI = "https://api.defontana.com/api/Sale/GetSalebyDate"
    listaFacturasAPIQS = {"initialDate":FR.anteayer,"endingDate":FR.hoy,"itemsPerPage":"1000","pageNumber":"0", "documentType": "FVAELECT"}
    listaFacturasAPIQS2 = {"initialDate":FR.anteayer,"endingDate":FR.hoy,"itemsPerPage":"1000","pageNumber":"0", "documentType": "FVARSELECT"}
    listaFacturasJson = requests.request("GET", listaFacturasAPI, headers=HK.headersDefontana, params=listaFacturasAPIQS).json()
    listaFacturasJson2 = requests.request("GET", listaFacturasAPI, headers=HK.headersDefontana, params=listaFacturasAPIQS2).json()
    listaFacturasDefon = {}
    for i in listaFacturasJson["saleList"]:
        listaFacturasDefon[str(i["firstFolio"])] = i["documentType"]
    for i in listaFacturasJson2["saleList"]:
        listaFacturasDefon[str(i["firstFolio"])] = i["documentType"]
    return listaFacturasDefon

# Para obtener de la Factura solicitada: ("número de Factura - nombre", "detalle (código, cantidad, descripción)", "fecha de vencimiento")
def detalle_Factura(numero, docType):
    listaFacturasAPI = "https://api.defontana.com/api/Sale/GetSale"
    listaFacturasAPIQS = {"number": numero, "documentType" : docType}
    FacturasJson = requests.request("GET", listaFacturasAPI, headers=HK.headersDefontana, params=listaFacturasAPIQS).json()[0]
    tipoDocumento = FacturasJson["documentType"]
    fechaEmision = FacturasJson["dateTime"][:19]
    codigoCliente = FacturasJson["clientFile"]
    direccionCliente = FacturasJson["contactIndex"]
    vendedorID = FacturasJson["sellerFileId"]
    nombreVendedor = Vendedores[vendedorID]
    comuna = FacturasJson["district"]+", "+FacturasJson["city"]
    glosa = FacturasJson["gloss"]
    local = FacturasJson["shopId"]
    nombreCliente = consulta_Cliente(codigoCliente)
    nombre = f"{numero} - {nombreCliente}"
    try:
        numeroPedido = FacturasJson["attachedDocuments"][0]["attachedDocumentNumber"]
    except:
        numeroPedido = "Sin pedido asociado"
    detalle = f"Dirección: {direccionCliente}, {comuna}\nComentario: {glosa}\nReferencia pedido: {numeroPedido}\nVendedor: {nombreVendedor}"
    return nombre, detalle, tipoDocumento, fechaEmision, direccionCliente, comuna, local

def consulta_Cliente(id):
    cURL = "https://api.defontana.com/api/Sale/GetClientsByFileID"
    params = {"status": "0", "itemsPerPage" : "1", "pageNumber" : "0", "fileID": id}
    ClienteJson = requests.request("GET", cURL, headers=HK.headersDefontana, params=params).json()
    try:
        Cliente = ClienteJson["clientList"][0]["name"]
    except:
        Cliente = "Sin información"
    return Cliente
