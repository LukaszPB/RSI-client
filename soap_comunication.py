from zeep import Client, Settings
from zeep.transports import Transport
import requests
from typing import List, Tuple
from PIL import Image
import io
from io import BytesIO
from requests import Session
import xml.etree.ElementTree as ET
import base64
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename
import email
from email import policy
    
def getMovies():
    try:
        client = Client("http://localhost:8080/Ws-SOAP-Projekt-1.0-SNAPSHOT/MovieServiceService?wsdl")
        response = client.service.getMovieList()  # przykładowe zapytanie
        return response
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"
    
def getPDF(id):
    client = Client("http://desktop-4e41r2u:8080/Ws-SOAP-Projekt-1.0-SNAPSHOT/ReservationServiceService?wsdl")
    response = client.service.getReservationPDF(id)

    # Tworzenie ukrytego okna Tkinter
    root = Tk()
    root.withdraw()  # Ukrywamy główne okno (nie potrzebujemy go)

    # Domyślna nazwa pliku
    default_filename = "rezerwacja-seansId:" + str(id) + ".pdf"

    if isinstance(response, str):
        pdf_bytes = base64.b64decode(response)

        # Okno dialogowe zapisu pliku z domyślną nazwą
        file_path = asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], initialfile=default_filename)
        if file_path:
            with open(file_path, "wb") as f:
                f.write(pdf_bytes)
            print(f"PDF zapisany jako '{file_path}'.")

    # Jeśli Zeep zmapował odpowiedź na bytes
    elif isinstance(response, bytes):
        # Okno dialogowe zapisu pliku z domyślną nazwą
        file_path = asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], initialfile=default_filename)
        if file_path:
            with open(file_path, "wb") as f:
                f.write(response)
            print(f"PDF zapisany jako '{file_path}'.")

    # Jeśli odpowiedź jest None
    elif response is None:
        print("Brak odpowiedzi z serwera – być może błędne ID.")

    # Dla innych przypadków
    else:
        print(f"Nieobsługiwany typ danych: {type(response)}")
    
def getImage(filepath):
    wsdl_url = 'http://localhost:8080/Ws-SOAP-Projekt-1.0-SNAPSHOT/MovieServiceService?wsdl'

    client = Client(wsdl=wsdl_url)

    response = client.service.getImage(filepath)

    return response
    
def getActor(id):
    try:
        client = Client("http://localhost:8080/Ws-SOAP-Projekt-1.0-SNAPSHOT/ActorServiceService?wsdl")
        response = client.service.getActor(id)  # przykładowe zapytanie
        return response
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"
def getShowings():
    try:
        client = Client("http://localhost:8080/Ws-SOAP-Projekt-1.0-SNAPSHOT/ShowingServiceService?wsdl")
        response = client.service.getShowingList()  # przykładowe zapytanie
        return response
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"
    
def getShowing(id):
    try:
        client = Client("http://localhost:8080/Ws-SOAP-Projekt-1.0-SNAPSHOT/ShowingServiceService?wsdl")
        response = client.service.getShowing(id)  # przykładowe zapytanie
        return response
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"
    
def addReservation():
    try:
        client = Client("http://localhost:8080/Ws-SOAP-Projekt-1.0-SNAPSHOT/ShowingServiceService?wsdl")
        response = client.service.getShowingList()  # przykładowe zapytanie
        return response
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"
    
def getReservations():
    try:
        client = Client("http://localhost:8080/Ws-SOAP-Projekt-1.0-SNAPSHOT/ReservationServiceService?wsdl")
        response = client.service.findAllReservations()  # przykładowe zapytanie
        return response
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"
    
def getReservation(id):
    print(id)
    try:
        client = Client("http://localhost:8080/Ws-SOAP-Projekt-1.0-SNAPSHOT/ReservationServiceService?wsdl")
        response = client.service.findReservation(id)  # przykładowe zapytanie
        return response
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"
    
def updateReservation(reservation):
    try:
        client = Client("http://localhost:8080/Ws-SOAP-Projekt-1.0-SNAPSHOT/ReservationServiceService?wsdl")
        response = client.service.updateReservation(reservation)  # przykładowe zapytanie
        return response
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"
    
def deleteReservations(id):
    try:
        client = Client("http://localhost:8080/Ws-SOAP-Projekt-1.0-SNAPSHOT/ReservationServiceService?wsdl")
        response = client.service.deleteReservation(id)  # przykładowe zapytanie
        return response
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"

def update_reservation(reservation_id: int, showing_id: int, seat_list: List[Tuple[int, int]]) -> str:
    url = "http://desktop-4e41r2u:8080/Ws-SOAP-Projekt-1.0-SNAPSHOT/ReservationServiceService"

    # Generujemy XML z listą miejsc
    seat_locations_xml = "\n".join(
        f"""<seatLocation>
                <x>{x}</x>
                <y>{y}</y>
            </seatLocation>"""
        for x, y in seat_list
    )

    # Składamy cały SOAP XML dla updateReservation
    xml = f"""<?xml version="1.0" encoding="utf-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:con="http://controller.wssoapprojekt.example.org/">
        <soapenv:Header/>
        <soapenv:Body>
            <con:updateReservation>
                <reservation>
                    <reservationId>{reservation_id}</reservationId>
                    <showingId>{showing_id}</showingId>
                    <seatLocationList>
                        {seat_locations_xml}
                    </seatLocationList>
                </reservation>
            </con:updateReservation>
        </soapenv:Body>
    </soapenv:Envelope>"""

    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": ""
    }

    response = requests.post(url, data=xml.encode("utf-8"), headers=headers)

    print("Status:", response.status_code)
    return response.text

def send_reservation(showing_id: int, seat_list: List[Tuple[int, int]]) -> str:
    url = "http://desktop-4e41r2u:8080/Ws-SOAP-Projekt-1.0-SNAPSHOT/ReservationServiceService"

    # Generujemy listę seatLocation XML
    seat_locations_xml = "\n".join(
        f"""<seatLocation>
                <x>{x}</x>
                <y>{y}</y>
            </seatLocation>"""
        for x, y in seat_list
    )

    # Składamy cały SOAP XML
    xml = f"""<?xml version="1.0" encoding="utf-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                            xmlns:con="http://controller.wssoapprojekt.example.org/">
            <soapenv:Header/>
            <soapenv:Body>
                <con:createReservation>
                    <showingId>{showing_id}</showingId>
                    <reservation>
                        <seatLocationList>
                        {seat_locations_xml}
                        </seatLocationList>
                    </reservation>
                </con:createReservation>
            </soapenv:Body>
            </soapenv:Envelope>"""

    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": ""
    }

    response = requests.post(url, data=xml.encode("utf-8"), headers=headers)

    print("Status:", response.status_code)
    return response.text
# def getMovies():
#     try:
#         # Użycie certyfikatu serwera self-signed
#         session = requests.Session()
#         session.verify = False  # Ścieżka do certyfikatu serwera (w tym samym folderze lub podaj pełną)
        
#         transport = Transport(session=session)
#         client = Client(
#             "http://localhost:8080/Ws-SOAP-Projekt-1.0-SNAPSHOT/MovieServiceService?wsdl",
#             transport=transport
#         )
#         response = client.service.getMovieList()
#         return response

#     except Exception as e:
#         print(f"Error: {e}")
#         return f"Error: {e}"