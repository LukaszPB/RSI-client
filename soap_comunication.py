from zeep import Client

def pobierz_wiadomosc():
    try:
        client = Client("http://localhost:8080/Ws-SOAP-Projekt-1.0-SNAPSHOT/HelloWorldImplService?wsdl")
        odpowiedz = client.service.wzorcowaMetoda(123)  # przykładowe zapytanie
        return odpowiedz
    except Exception as e:
        return f"Błąd: {e}"
    
def getMovies():
    try:
        client = Client("http://localhost:8080/Ws-SOAP-Projekt-1.0-SNAPSHOT/MovieServiceService?wsdl")
        response = client.service.getMovieList()  # przykładowe zapytanie
        return response
    except Exception as e:
        return f"Error: {e}"