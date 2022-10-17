import requests
import HeadersKeys as HK

def obtenerCoordenadas(direccion, comuna):
    url = "http://api.positionstack.com/v1/forward"
    querystring = {
        "access_key" : HK.positionstack,
        "query" : direccion+", "+comuna+", chile",
        "country" : "CL"
    }
    response = requests.request("GET", url, params=querystring).json()
    location = str(response["data"][0]["latitude"])+","+str(response["data"][0]["longitude"])
    return location
