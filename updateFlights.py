from datetime import datetime, timedelta
import json
import requests

from constants import ENUM_TYPE_FLIGHT_WARNING, urlToUse

# type can be "departures" or "arrivals"

def updateFlightHistory(token, id, type, old, new):
    typeToSend = next((item for item in ENUM_TYPE_FLIGHT_WARNING if item['NAME'] == type), None).get('ID')
    
    objectToCreate = {
        "id": id,
        "old": old,
        "new": new,
        "flightWarningTypes": typeToSend,
        "publishedAt": datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + "Z",
    }

    query = """
        mutation createFlightWarning(
            $flightId: ID!
            $old: String
            $new: String
            $flightWarningTypes: [ID]
            $warningDate: DateTime
            $publishedAt: DateTime
            ) {
            createFlightWarning(
                data: {
                old: $old
                new: $new
                flight: $flightId
                flightWarningTypes: $flightWarningTypes
                warningDate: $warningDate
                publishedAt: $publishedAt
                }
            ) {
                data {
                id
                }
            }
            }
        """
        
    variables = {
            "flightId": objectToCreate['id'],
            "old": objectToCreate['old'],
            "new": objectToCreate['new'],
            "flightWarningTypes": [objectToCreate['flightWarningTypes']],
            "warningDate": objectToCreate['publishedAt'],
            "publishedAt": objectToCreate['publishedAt'],
        }
    
    headers = {
        "Authorization": f"Bearer {token}",
    }
    
    response = requests.post(urlToUse, json={'query': query, 'variables': variables}, headers=headers)
    
    jsonObejct = json.dumps(variables, indent=4)
    
    if response.status_code == 200:
        json_response = response.json()
        print("Flight updated successfully:", json_response)
        print("\n")
    else:
        print("Request failed:", response.status_code, response.text)
        with open('log.txt', 'a') as f:
            f.write(f"Request failed: {response.status_code} {response.text}\n {jsonObejct}\n")
        return None



def updateFlight(token, gate, newBox, newPrefix, etd, eta, std, sta, flightId, oldPrefix, oldBox):

    print('PREFIXS', oldPrefix, newPrefix)
    print('BOXS', oldBox, newBox)
    
    prefixFormatted = 'N/A' if oldPrefix == '-' else oldPrefix
    
    newPrefixFormatted = 'N/A' if newPrefix == '-' else newPrefix
    
    if newPrefixFormatted != prefixFormatted:
        updateFlightHistory(token, flightId, "prefix", prefixFormatted, newPrefixFormatted)
    if newBox != oldBox:
        updateFlightHistory(token, flightId, "box", oldBox, newBox)

    objectToCreate = {
        "id": flightId,
        "gate": gate,
        "box": newBox,
        "prefix": newPrefix,
        "ETD": etd,
        "ETA": eta,\
        "STD": std,
        "STA": sta,
    }

    query = """
        mutation UpdateFlightDetails(
            $id: ID!
            $gate: String
            $box: String
            $prefix: String
            $ETD: Time
            $ETA: Time
            $STD: Time
            $STA: Time
            ) {
            updateFlight(
                id: $id
                data: {
                gate: $gate
                BOX: $box
                prefix: $prefix
                ETD: $ETD
                ETA: $ETA
                STD: $STD
                STA: $STA
                }
            ) {
                data {
                id
                attributes {
                    gate
                    BOX
                    prefix
                    ETD
                    ETA
                    STD
                    STA
                }
                }
            }
            }
        """
        
    variables = {
            "id": objectToCreate['id'],
            "gate": objectToCreate['gate'],
            "box": objectToCreate['box'],
            "prefix": objectToCreate['prefix'],
            "ETD": objectToCreate['ETD'],
            "ETA": objectToCreate['ETA'],
            "STD": objectToCreate['STD'],
            "STA": objectToCreate['STA'],
        }
    
    headers = {
        "Authorization": f"Bearer {token}",
    }
    
    response = requests.post(urlToUse, json={'query': query, 'variables': variables}, headers=headers)
    
    jsonObejct = json.dumps(response.json(), indent=4)
    
    if response.status_code == 200:
        json_response = response.json()
        print("Flight updated successfully:", json_response)
        print("\n")
    else:
        print("Request failed:", response.status_code, response.text)
        with open('log.txt', 'a') as f:
            f.write(f"Request failed: {response.status_code} {response.text}\n {jsonObejct}\n")
        return None
