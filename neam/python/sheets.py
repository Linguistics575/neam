import gspread
from oauth2client.service_account import ServiceAccountCredentials

credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/adoxography/Downloads/My Project-1742a8dd306c.json')

gc = gspread.authorize(credentials)
