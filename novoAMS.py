from datetime import datetime, timedelta
import re
import requests

from bs4 import BeautifulSoup

import random
import requests
import json

from constants import airport_codes, arrayIcaoIata, urlToUse

from createFlightInternationAmsDeparture import createFlightInternationalAmsDeparture
from createFlightInternationlAmsArrival import createFlightInternationalAmsArrival
from getAllFlights import getAllFlights
from updateFlights import updateFlight


# type = "departure" # or "arrival"

# type = "arrival" # or "arrival


def login_user(username, password):
    # GraphQL endpoint URL

    # GraphQL mutation for login
    graphql_mutation = f"""
    mutation LoginUser {{
      login(input: {{
        identifier: "{username}",
        password: "{password}"
      }}) {{
        jwt
        user {{
          id
          username
          email
        }}
      }}
    }}
    """

#     # Headers with the Content-Type set to application/json
    headers = {
        "Content-Type": "application/json",
        # Add any other headers as needed
    }

#     # Create the payload for the POST request
    payload = {
        "query": graphql_mutation
    }

#     # Make the POST request
    response = requests.post(urlToUse, json=payload, headers=headers)

#     # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        json_response = response.json()
        return json_response
    else:
        print("Failed to execute GraphQL mutation. Status code:", response.status_code)
        print("Response:", response.text)
        return None

# # Example usage
username = "admin@admin.com"
password = "Global@#robos@#"
response = login_user(username, password)

token = response["data"]["login"]["jwt"]

# Print or use the response as needed
if response:
    print("JWT Token:", response["data"]["login"]["jwt"])
    user_data = response["data"]["login"]["user"]
    print("User ID:", user_data["id"])
    print("Username:", user_data["username"])
    print("Email:", user_data["email"])



# List of user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.54 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    # Add more user agents as needed
]

headers = {'User-Agent': random.choice(user_agents)}


payload = {
    'type': 'A',
    'username': '',
    'pwd': '',
    'Captcha': ''
}

def url (type):
  return f"https://ams.gru.com.br/{type}.html"

newArrayOnlyIcao = []

for index, row in enumerate(arrayIcaoIata):
    if row['ICAO'] not in newArrayOnlyIcao:
        newArrayOnlyIcao.append(row['ICAO'])

def getIfTheFlightsExists(flight_data, flight_number, flight_AMS_date):
    
    for flight in flight_data:

        if str(flight['attributes']['flightDate']) == str(flight_AMS_date) and str(flight['attributes']['flightNumber']).zfill(4) == str(flight_number):
            return True, flight['id'], flight['attributes']['prefix'], flight['attributes']['BOX']

    print("Flight not found:", flight_number , flight_AMS_date)
    return False


all_flights = getAllFlights(token)


def flightsArrival():
  today = datetime.now().strftime("%d/%m/%Y")

  today_more_one_day = datetime.now() + timedelta(days=1)
  today_more_one_day = today_more_one_day.strftime("%d/%m/%Y")

  timeout_seconds = 30

  response = requests.post("https://ams.gru.com.br/arrival.html", data=payload, headers=headers, timeout=timeout_seconds)


  if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')

      print("Page Title:", soup.title.text)


  # tbody = soup.find('tbody')

      if all_flights:
        all_flights_dict = all_flights['data']['flights']['data']
      
      for index,row in enumerate(soup.find_all('tr')):
          # Extract data from each cell in the row
          cells = row.find_all(['td', 'th'])

          if len(cells) == 1:
              date_string = cells[0].text.strip()
              date_match = re.search(r'\d{2}/\d{2}/\d{4}', date_string)

              if date_match:
                  extracted_date = date_match.group()
                  print("Extracted Date:", extracted_date)

                  # Convert extracted_date to datetime object for comparison
                  extracted_date_datetime = datetime.strptime(extracted_date, "%d/%m/%Y")
                  print("More one Day", today_more_one_day)
                  if extracted_date == today_more_one_day:
                      print('Date is one day ahead of today:', today)
                      today = extracted_date_datetime.strftime("%d/%m/%Y")
                  else:
                      print('Date is not one day ahead of today.')
              else:
                  print("Date not found in the string.")

          if len(cells) >= 12 and cells[2].find('div') and cells[2].find('div').text.strip() in newArrayOnlyIcao:
                      try:
                        matching_item = next((item for item in arrayIcaoIata if item['ICAO'] == cells[2].find('div').text.strip()), None)
                        if matching_item:
                            airline_code = matching_item['IATA']
                        else:
                            airline_code = cells[2].find('div').text.strip()
                      except:
                        with open('log.txt', 'a') as f:
                            f.write('Eror ICAO')
                            f.write(f'Flight {cells[3].text.strip()} - {cells[2].find("div").text.strip()}\n')
                        continue

                      dateFlight=today
                      time = cells[0].text.strip() if cells[0].text.strip() else '-'
                      origin = airport_codes[cells[1].text.strip()]
                      airline_code_icao = cells[2].find('div').text.strip()
                      flight_number = cells[3].text.strip()
                      codeshare = cells[4].text.strip()
                      terminal = cells[5].find('div').text.strip() if cells[5].find('div') else None
                      gate = cells[6].text.strip()
                      box = cells[7].text.strip()
                      prefix = cells[8].text.strip()
                      aircraft_model = cells[9].text.strip()
                      estimated_time = cells[10].text.strip()
                      observation = cells[11].text.strip()
                      
                      flightDateFormated = datetime.strptime(today, '%d/%m/%Y')
                      
                      flightDateFormated = flightDateFormated.strftime('%Y-%m-%d')
                      
                      isFlightExists = getIfTheFlightsExists(all_flights_dict, str(flight_number), flightDateFormated)

                      if isFlightExists == False:
                          createFlightInternationalAmsArrival({
                                'time': time,
                                'origin': origin,
                                'airline_code': airline_code,
                                'flight_number': flight_number,
                                'codeshare': codeshare,
                                'terminal': terminal,
                                'gate': gate,
                                'box': box,
                                'prefix': prefix,
                                'aircraft_model': aircraft_model,
                                'airline_code_icao': airline_code_icao,
                                'estimated_time': estimated_time,
                                'observation': observation,
                                'dateFlight': dateFlight,
                                'token': token,
                          })

                      if isFlightExists:
                          today_date = dateFlight
                          
                          flight_datetime_str = f"{today_date} {time}"

                          flight_datetime_STA = datetime.strptime(flight_datetime_str, '%d/%m/%Y %H:%M')
                          
                          STA = flight_datetime_STA.strftime('%H:%M:%S.000')
                          
                          if estimated_time == '-':
                            estimated_time_str = time
                          else:
                            estimated_time_str = estimated_time if estimated_time else time
                          
                          
                          if estimated_time == '-':
                            ETA = STA
                          else:
                            flight_datetime_ETA = datetime.strptime(estimated_time_str, '%H:%M')
                            ETA = flight_datetime_ETA.strftime('%H:%M:%S.000')
                          
                          STA_PLUS_75 = datetime.strptime(STA, '%H:%M:%S.000') + timedelta(minutes=75)
    
                          ETA_PLUS_75 = datetime.strptime(ETA, '%H:%M:%S.000') + timedelta(minutes=75)
                        
                          STD = STA_PLUS_75.strftime('%H:%M:%S.000')
                        
                          ETD = ETA_PLUS_75.strftime('%H:%M:%S.000')

                          updateFlight(
                                token,
                                gate,
                                box,
                                prefix,
                                ETD,
                                ETA,
                                STD,
                                STA,
                                isFlightExists[1],
                                isFlightExists[2],
                                isFlightExists[3],
                          )

def flightsDeparture():

  today = datetime.now().strftime("%d/%m/%Y")

  today_more_one_day = datetime.now() + timedelta(days=1)

  today_more_one_day = today_more_one_day.strftime("%d/%m/%Y")

  timeout_seconds = 30

  response = requests.post(url('departure'), data=payload, headers=headers, timeout=timeout_seconds)

  if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')

      print("Page Title:", soup.title.text)

  # tbody = soup.find('tbody')

      if all_flights:
            all_flights_dict = all_flights['data']['flights']['data']

            for index,row in enumerate(soup.find_all('tr')):
                # Extract data from each cell in the row
                cells = row.find_all(['td', 'th'])

                if len(cells) == 1:
                    date_string = cells[0].text.strip()
                    date_match = re.search(r'\d{2}/\d{2}/\d{4}', date_string)

                    if date_match:
                        extracted_date = date_match.group()
                        print("Extracted Date:", extracted_date)

                        # Convert extracted_date to datetime object for comparison
                        extracted_date_datetime = datetime.strptime(extracted_date, "%d/%m/%Y")
                        print("More one Day", today_more_one_day)
                        if extracted_date == today_more_one_day:
                            print('Date is one day ahead of today:', today)
                            today = extracted_date_datetime.strftime("%d/%m/%Y")
                        else:
                            print('Date is not one day ahead of today.')
                    else:
                        print("Date not found in the string.")

                if len(cells) >= 12 and cells[2].find('div') and cells[2].find('div').text.strip() in newArrayOnlyIcao:
                            try:
                                matching_item = next((item for item in arrayIcaoIata if item['ICAO'] == cells[2].find('div').text.strip()), None)
                                if matching_item:
                                    airline_code = matching_item['IATA']
                                else:
                                    airline_code = cells[2].find('div').text.strip()
                            except:
                                with open('log.txt', 'a') as f:
                                    f.write('Eror ICAO')
                                    f.write(f'Flight {cells[3].text.strip()} - {cells[2].find("div").text.strip()}\n')
                                continue
                            
                            dateFlight=today
                            time = cells[0].text.strip() if cells[0].text.strip() else '-'
                            origin = airport_codes[cells[1].text.strip()]
                            airline_code_icao = cells[2].find('div').text.strip()
                            flight_number = cells[3].text.strip()
                            codeshare = cells[4].text.strip()
                            terminal = cells[5].find('div').text.strip() if cells[5].find('div') else None

                            gate = cells[7].text.strip()
                            box = cells[8].text.strip()
                            prefix = cells[10].text.strip()
                            aircraft_model = cells[11].text.strip()
                            estimated_time = cells[12].text.strip()
                            observation = cells[13].text.strip()


                            flightDateFormated = datetime.strptime(today, '%d/%m/%Y')
                      
                            flightDateFormated = flightDateFormated.strftime('%Y-%m-%d')
                            
                            isFlightExists = getIfTheFlightsExists(all_flights_dict, str(flight_number), flightDateFormated)
                            
                            if isFlightExists == False:
                                createFlightInternationalAmsDeparture({
                                    'time': time,
                                    'origin': origin,
                                    'airline_code': airline_code,
                                    'flight_number': flight_number,
                                    'codeshare': codeshare,
                                    'terminal': terminal,
                                    'gate': gate,
                                    'box': box,
                                    'prefix': prefix,
                                    'aircraft_model': aircraft_model,
                                    'airline_code_icao': airline_code_icao,
                                    'estimated_time': estimated_time,
                                    'observation': observation,
                                    'dateFlight': dateFlight,
                                    'token': token,
                                })
                                
                            if isFlightExists:
                                today_date = dateFlight
                                
                                flight_datetime_str = f"{today_date} {time}"
                                
                                flight_datetime_STD = datetime.strptime(flight_datetime_str, '%d/%m/%Y %H:%M')
                                
                                STD = flight_datetime_STD.strftime('%H:%M:%S.000')
                                
                                if estimated_time == '-':
                                    estimated_time_str = time
                                else:
                                    estimated_time_str = estimated_time if estimated_time else time
                                
                                flight_datetime_ETD = datetime.strptime(estimated_time_str, '%H:%M')
                                
                                ETD = flight_datetime_ETD.strftime('%H:%M:%S.000')
                                
                                STD_MINUS_40 = datetime.strptime(STD, '%H:%M:%S.000') - timedelta(minutes=40)
                                
                                ETD_MINUS_40 = datetime.strptime(ETD, '%H:%M:%S.000') - timedelta(minutes=40)
                                
                                STA = STD_MINUS_40.strftime('%H:%M:%S.000')
                                
                                ETA = ETD_MINUS_40.strftime('%H:%M:%S.000')

                                updateFlight(
                                    token,
                                    gate,
                                    box,
                                    prefix,
                                    ETD,
                                    ETA,
                                    STD,
                                    STA,
                                    isFlightExists[1],
                                    isFlightExists[2],
                                    isFlightExists[3],
                                )

print("Init Script")
print("Flights Arrival")
print("\n")
flightsArrival()

print("\n")
print("Finish Flights Arrival")


print("\n")
print("Flights Departure")
print("\n")

flightsDeparture()

print("\n")
print("Finish Flights Departure")

print("\n")
print("Finish Script")