urlToUse = "*****" ## Homolog PRODUCTION

ENUM_TYPE_ACTIONTYPE = {
    "ARRIVAL": "Arrival",
    "DEPARTURE": "Departure",
}

ENUM_TYPE_TYPELANDING = {
    "FIXED": "Fixed",
    "REMOTE": "Remote",
}

ENUM_TYPE_FLIGHT_WARNING = [
    {
        "NAME": 'box',
        "ID": 2,
    },
    {
        "NAME": 'prefix',
        "ID": 1,
    }
]

ENUM_TYPE_AIRCRAFT = [
    {
        "ID": 1,
        "NAME": "A319",
        "BODY": "narrow",
    },
    {
        "ID": 2,
        "NAME": "A320",
        "BODY": "narrow",
    },
    {
        "ID": 3,
        "NAME": "A321",
        "BODY": "narrow",
    },
    {
        "ID": 4,
        "NAME": "B767",
        "BODY": "wide",
    },
    {
        "ID": 5,
        "NAME": "B777",
        "BODY": "wide",
    },
    {
        "ID": 6,
        "NAME": "B787",
        "BODY": "wide",
    },
    {
        "ID": 7,
        "NAME": "B787-9",
        "BODY": "wide",
    },
    {
        "ID": 8,
        "NAME": "B787-8",
        "BODY": "wide",
    },
    {
        "ID": 9,
        "NAME": "A333",
        "BODY": "wide",
    },
    {
        "ID": 10,
        "NAME": "B772",
        "BODY": "wide",
    },
    {
        "ID": 11,
        "NAME": "B77W",
        "BODY": "wide",
    },
    {
        "ID": 12,
        "NAME": "A339",
        "BODY": "wide",
    },
    {
        "ID": 13,
        "NAME": "B789",
        "BODY": "wide",
    },
    {
        "ID": 14,
        "NAME": "B78X",
        "BODY": "wide",
    },
    {
        "ID": 15,
        "NAME": "B738",
        "BODY": "narrow",
    },
    {
        "ID": 16,
        "NAME": "B764",
        "BODY": "wide",
    },
    {
        "ID": 17,
        "NAME": "B38M",
        "BODY": "narrow",
    },
    {
        "ID": 18,
        "NAME": "E190",
        "BODY": "narrow",
    },
    {
        "ID": 19,
        "NAME": "A20N",
        "BODY": "narrow",
    },
    {
        "ID": 20,
        "NAME": "B735",
        "BODY": "wide",
    },
    {
        'ID': 21,
        'NAME': 'A359',
        'BODY': 'wide',
    },
    {
        'ID': 22,
        'NAME': 'B733',
        'BODY': 'narrow',
    },
    {
        'ID': 23,
        'NAME': 'B773',
        'BODY': 'wide',
    },
    {
        'ID': 24,
        'NAME': 'B748',
        'BODY': 'wide',
    },
    {
        'ID': 25,
        'NAME': 'A332',
        'BODY': 'wide',
    }
]


ENUM_TYPE_AIRLINE = [
    {
        "id": 18,
        "name": "ITA",
        "icao": "ITY",
    },
    {
        "id": 13,
        "name": "LUFTANSA",
        "icao": "DLH",
    },
    {
        "id": 16,
        "name": "TAP",
        "icao": "TAP",
    },
    {
        "id": 17,
        "name": "UNITED",
        "icao": "UNI",
    },
    {
        "id": 20,
        "name": "DELTA AIRLINE",
        "icao": "DAL",
    },
    {
        "id": 21,
        "name": "SWISS AIRLINE",
        "icao": "SWR",
    },
    {
        "id": 22,
        "name": "AMERICAN AIRLINE",
        "icao": "AAL",
    },
    {
        "id": 23,
        "name": "AIR EUROPA LINEAS",
        "icao": "AEA",
    },
    {
        "id": 24,
        "name": "UNITED AIRLINE",
        "icao": "UAL",
    },
    {
        "id": 25,
        "name": "AEROLINEAS ARGENTINAS S/A",
        "icao": "ARG",
    },
    {
        "id": 27,
        "name": "KLM CIA REAL HOLANDESA",
        "icao": "KLM",
    },
    {
        "id": 28,
        "icao": "SID",
        "name": "SIDERAl LINHAS AEREAS",
    },
    {
        "id": 29,
        "icao": "DTA",
        "name": "TAAG LINHAS AEREAS DE ANGOLA",
    },
    {
        "id": 1,
        "icao": "LAN",
        "name": "LAN CHILE",
    },
    {
        'id': 31,
        'icao': 'FBZ',
        'name': 'FLYBOND',
    },
    {
        'id': 32,
        'icao': 'AFR',
        'name': 'AIR FRANCE',
    },
    {
        'id': 19,
        'icao': 'LTG',
        'name': 'ABSA',
    },
    {
        'id': 33,
        'icao': 'GTI',
        'name': 'ATLAS AIR',
    },
    {
        'id': 34,
        'icao': 'MWM',
        'name': 'MODERN',
    }
]

##Retirado Avianca, Emirates, Qatar e Air Canada por pedido de Patricia, porém mantido na lista de Airlines no BD.

airport_codes = {
    "Atlanta": "ATL",
    "Nova York": "JFK",  # Using John F. Kennedy International Airport
    "Newark": "EWR",
    "Washington": "DCA",  # Using Ronald Reagan Washington National Airport
    "Toronto": "YYZ",  # Using Toronto Pearson International Airport
    "Buenos Aires": "EZE",  # Using Ministro Pistarini International Airport
    "Mendoza": "MDZ",
    "Amsterdã": "AMS",  # Using Amsterdam Airport Schiphol
    "Lisboa": "LIS",  # Using Lisbon Portela Airport
    "Miami": "MIA",
    "Zurich": "ZRH",  # Using Zurich Airport
    "Madrid": "MAD",  # Using Adolfo Suárez Madrid–Barajas Airport
    "Chicago": "ORD",  # Using O'Hare International Airport
    "Dallas": "DFW",  # Using Dallas/Fort Worth International Airport
    "Houston": "IAH",  # Using George Bush Intercontinental Airport,
    "Porto": "OPO",  # Using Francisco Sá Carneiro Airport
    "MONTREAL": "YUL",  # Using Montréal-Pierre Elliott Trudeau International Airport
    "Córdoba": "COR",  # Using Ingeniero Aeronáutico Ambrosio L.V. Taravella International Airport
    "Ilha de Comandatuba": "UNA",  # Using Una-Comandatuba Airport
    "Salta": "SLA",  # Using Martín Miguel de Güemes International Airport
    "Roma": "FCO",  # Using Leonardo da Vinci–Fiumicino Airport
    "Paris": "CDG",  # Using Charles de Gaulle Airport
    "Manaus": "MAO",  # Using Eduardo Gomes International Airport
    "Santiago": "SCL",  # Using Comodoro Arturo Merino Benítez International Airport
    "Luanda": "LAD",  # Using Quatro de Fevereiro International Airport
    'Frankfurt': 'FRA',  # Using Frankfurt Airport
    'São José do Rio Preto': 'SJP',  # Using São José do Rio Preto Airport
}

arrayIcaoIata = [
    {
        'ICAO': 'AAL',
        'IATA': 'AA',
    },
    {
        'ICAO': 'LTG',
        'IATA': 'M3',
    },
    {
        'ICAO': 'ARG',
        'IATA': 'AR',
    },
    {
        'ICAO': 'AEA',
        'IATA': 'UX',
    },
    {
        'ICAO': 'GTI',
        'IATA': '5Y',
    },
    {
        'ICAO': 'LRC',
        'IATA': 'LR',
    },
    {
        'ICAO': 'DAL',
        'IATA': 'DL',
    },
    {
        'ICAO': 'KLM',
        'IATA': 'KL',
    },
    {
        'ICAO': 'GEC',
        'IATA': 'G0',
    },
    {
        'ICAO': 'MWM',
        'IATA': 'WD',
    },
    {
        'ICAO': 'SID',
        'IATA': 'OS',
    },
    {
        'ICAO': 'SWR',
        'IATA': 'LX',
    },
    {
        'ICAO': 'TAP',
        'IATA': 'TP',
    },
    {
        'ICAO': 'UAL',
        'IATA': 'UA',
    },
    {
        'ICAO': 'DLH',
        'IATA': 'LH',
    },
    {
        'ICAO': 'DTA',
        'IATA': 'DT',
    },
    {
        'ICAO': 'LAN',
        'IATA': 'LA',
    },
    {
        'ICAO': 'ITY',
        'IATA': 'AZ',
    },
    {
        'ICAO': 'FBZ',
        'IATA': 'FO',
    },
    {
        'ICAO': 'AFR',
        'IATA': 'AF',
    },
    {
        'ICAO': 'GTI',
        'IATA': '5Y',
    }
]
