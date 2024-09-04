from datetime import datetime, timedelta
import requests
from constants import ENUM_TYPE_AIRCRAFT, ENUM_TYPE_AIRLINE, urlToUse

def createFlightInternationalAmsDeparture(flight):
    
    try:
        aircraftToSend = next((item for item in ENUM_TYPE_AIRCRAFT if item['NAME'] == flight['aircraft_model']), None).get('ID')

        airLineToSend = next((item for item in ENUM_TYPE_AIRLINE if item['icao'] == flight['airline_code_icao']), None).get('id')

        bodyType = next((item for item in ENUM_TYPE_AIRCRAFT if item['NAME'] == flight['aircraft_model']), None).get('BODY')
    except:
        fs = open("log.txt", "a")
        fs.write(f"Flight {flight['flight_number']} - {flight['airline_code_icao']} - {flight['aircraft_model']}\n")
        fs.close()
        return None
    
    today_date = flight['dateFlight']

    flight_datetime_str = f"{today_date} {flight['time']}"

    flight_datetime_STD = datetime.strptime(flight_datetime_str, '%d/%m/%Y %H:%M')

    STD = flight_datetime_STD.strftime('%H:%M:%S.000')

    ## If the estimated time is not available, use the scheduled time
    if flight['estimated_time'] == '-':
        ETD = STD
    else:
        flight_datetime_ETD = datetime.strptime(flight['estimated_time'], '%H:%M')
        ETD = flight_datetime_ETD.strftime('%H:%M:%S.000')

    # ---------------------------------------------------------------

    # Assuming flight['time'] is in the format HH:mm
    
    ETD_MINUS_40 = datetime.strptime(ETD, '%H:%M:%S.000') - timedelta(minutes=40)
    
    STD_MINUS_40 = datetime.strptime(STD, '%H:%M:%S.000') - timedelta(minutes=40)

    STA = STD_MINUS_40.strftime('%H:%M:%S.000')
    
    ETA = ETD_MINUS_40.strftime('%H:%M:%S.000')

    flightNumber = flight['flight_number']
    flightNumber_without_zeros = flightNumber.lstrip("0")

    destination = flight['origin'] ## The origin of the flight is the destination of the flight in the system
    
    flightDateFormated = datetime.strptime(today_date, '%d/%m/%Y')
    
    flightDateFormated = flightDateFormated.strftime('%Y-%m-%d')
    
    prefixFormatted = 'N/A' if flight['prefix'] == '-' else flight['prefix']
    
    # Create the objectToCreate dictionary
    objectToCreate = {
        "description": f"{flight['airline_code']}{flight['flight_number']}",
        "flightNumber": flightNumber_without_zeros,  # Ensure flight number is a string
        "actionType": "Departure",
        "prefix": prefixFormatted,
        "flightDate": flightDateFormated,  # Use the current date
        "STA": STA,
        "ETA": ETA,
        "route": "Local",
        "BOX": flight['box'],
        "flightOrigin": "GRU",
        "flightDestiny": destination,
        "typeLanding": "Fixed",
        "isInternational": True,
        "gate": flight['gate'],
        "code": flight['flight_number'],
        "ETD": ETD,
        "STD": STD,
        "bodyType": bodyType,
        "airline": airLineToSend,
        "aircraft": aircraftToSend,
        "isTurnAround": False,
        "lastDataOrigin": "AMS",
        "publishedAt": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000') + "Z",
    }


    # GraphQL mutation string without f-strings
    graphql_mutation_template = '''
        mutation CreateFlight($data: FlightInput!) {
            createFlight(data: $data) {
                data {
                    id
                }
            }
        }
    '''

    # Define the variables separately
    variables = {
        "data": {
            "description": objectToCreate['description'],
            "flightNumber": objectToCreate['flightNumber'],
            "actionType": objectToCreate['actionType'],
            "prefix": objectToCreate['prefix'],
            "flightDate": objectToCreate['flightDate'],
            "STA": objectToCreate['STA'],
            "ETA": objectToCreate['ETA'],
            "route": objectToCreate['route'],
            "BOX": objectToCreate['BOX'],
            "flightOrigin": objectToCreate['flightOrigin'],
            "flightDestiny": objectToCreate['flightDestiny'],
            "typeLanding": objectToCreate['typeLanding'],
            "isInternational": objectToCreate['isInternational'],
            "gate": objectToCreate['gate'],
            "code": objectToCreate['code'],
            "ETD": objectToCreate['ETD'],
            "STD": objectToCreate['STD'],
            "bodyType": objectToCreate['bodyType'],
            "airline": objectToCreate['airline'],
            "aircraft": objectToCreate['aircraft'],
            "isTurnAround": objectToCreate['isTurnAround'],
            "lastDataOrigin": objectToCreate['lastDataOrigin'],
            "publishedAt": objectToCreate['publishedAt'],
        }
    }

    # Combine the mutation and variables for the POST request
    payload = {
        "query": graphql_mutation_template,
        "variables": variables
    }

    headersAuthorization = {
    "Authorization": f"Bearer {flight['token']}"
    }

    response = requests.post(urlToUse, json=payload, headers=headersAuthorization)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        json_response = response.json()
        print("Flight created successfully:", json_response)
        print('\n')
        return json_response
    else:
        print(f"Failed to execute GraphQL mutation. Status code: {response.status_code} {flight['flight_number']}")
        print(f"Response: {response.text}")
        with open('error.txt', 'a') as f:
            f.write(f"Failed to execute GraphQL mutation. Status code: {response.status_code} {flight['flight_number']}\n")
            f.write(f"Response: {response.text}\n")
            f.write(f"Object Created: {objectToCreate}\n")
        return None

