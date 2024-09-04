from datetime import datetime, timedelta
import requests
from constants import urlToUse

# Get all flight international that Orbital has in the next 24 hours

def getAllFlights(token):
    #GraphQl Endpoint Url
    
    graphql_query_template = '''
        query flights(
            $pageSize: Int
            $fromDate: DateTime
            $toDate: DateTime
            $isInternational: BooleanFilterInput
            ) {
            flights(
                pagination: { page: 1, pageSize: $pageSize }
                filters: {
                    createdAt: { gte: $fromDate, lte: $toDate }
                    isInternational: $isInternational
                }
            ) {
                data {
                    id
                    attributes {
                        STA
                        STD
                        ETA
                        ETD
                        flightNumber
                        flightDate
                        prefix
                        BOX
                        description
                    }
                }
            }
        }
    '''
    
    date_today = datetime.today()
    
    hour_now = datetime.now()
    
    date_today_minus_1 = date_today - timedelta(days= 1)
    
    date_today_plus_1 = date_today + timedelta(days=2)
    
    date_today_formated = date_today_minus_1.strftime('%Y-%m-%dT%H:%M:00Z')
    
    date_today_plus_1_formated = date_today_plus_1.strftime('%Y-%m-%dT%H:%M:00Z')
    
    print(date_today_formated)
    
    objectToCreate = {
        "pageSize": 1000,
        "fromDate": date_today_formated,
        "toDate": date_today_plus_1_formated,
        "isInternational": True,
    }
    
    variables = {
        "pageSize": objectToCreate['pageSize'],
        "fromDate": objectToCreate['fromDate'],
        "toDate": objectToCreate['toDate'],
        "isInternational": {
            "eq": objectToCreate['isInternational']
        }
    }

    # Combine the query and variables for the POST request
    payload = {
        "query": graphql_query_template,
        "variables": variables
    }

    headersAuthorization = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
    }
    
    response = requests.post(urlToUse, json=payload, headers=headersAuthorization)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Error", response.status_code, response.text)
        return None

