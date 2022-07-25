from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = 'keys.json'
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


def isBlank (myString):
    return not (myString and myString.strip())

def isNotBlank (myString):
    return bool(myString and myString.strip())

def extractSheetID(link: str):
    """Extracts ID from a Google Sheet Document"""
    link = link.split("/")
    for i in range(len(link)):
        if(link[i] == "d"):
            return (link[i+1])
    return -1

def extractMapPools(link: str, sheetPage: str):
    """
    Returns an array containing all map pools extracted from given Google Sheets document.
    link - Google Sheets Document
    sheetPage - The name of the page containing the map pool
    """
    SAMPLE_SPREADSHEET_ID = extractSheetID(link)
    SAMPLE_RANGE_NAME = sheetPage
    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        mapTypeIndex = 0
        mapIdIndex = 0
        list = []

        while(mapTypeIndex == 0 or mapIdIndex == 0):
            for row in values:
                # Skips an empty row
                if(len(row) == 0):
                    continue
                #Searches for map type index and map ID index
                i = 0
                for val in row:
                    if(len(val) != 0):
                        if(val == "NM1"):
                            mapTypeIndex = i  
                        if(val.isnumeric() and len(val) >= 5):
                            mapIdIndex = i
                    i += 1
        mapPool = []        
        for row in values:
            if(len(row) == 0 or len(row) < mapIdIndex or len(row) < mapTypeIndex):
                continue
            mapType = row[mapTypeIndex]
            mapId = row[mapIdIndex]
            if(mapType == "NM1" or mapType == "NM1".lower()):
                mapPool = []
                list.append(mapPool)

            if(not isBlank(mapType) and mapId.isnumeric()):
                mapPool.append([mapType,mapId])
        return list
            
    except HttpError as err:
        print(err)

