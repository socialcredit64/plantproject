import serial
import gspread
from datetime import date
from oauth2client.service_account import ServiceAccountCredentials

# Set up serial communication


try:
    print("Attempting to open serial port...")
    ser = serial.Serial('/dev/ttyACM0', 9600) # Change '/dev/ttyACM0' to your serial port
    print("Serial port opened successfully!")
except serial.SerialException as e:
    print("Serial port error:", e)
    exit()

# Set up Google Sheets API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/home/s2184895/plantproject-413115-4b2355108208.json', scope)
client = gspread.authorize(creds)
sheet = client.open('thing').sheet1

# Read from Arduino and Write to Google Sheets
while True:
    if ser.in_waiting:
        try:
            current_date = date.today()

            data = ser.readline().decode('utf-8').strip()
            data = data[:-2]+'",time":'+str(current_date)+data[-2:]
            print(data)
            # Extract sensorName value
            sensor_name = data.split(':')[1].split(',')[0].strip('\"')
            
            # Check if sensorName is "ambientTemp", "infraredTemp", or "Uv"
            if sensor_name == "infraredTemp" or sensor_name == "Uv":
                components = data.split(',')
                
                #sheet.append_row(components)
                #sheet.append_row([data])
                
                components_transposed = [[item] for item in components]
                # Append transposed components to the Google Sheets document
                
                components_transposed = [components]  # Initialize with a list containing components
                components_transposed = list(zip(*components_transposed))  # Transpose the list

                #sheet.append_row([current_date])
                print(current_date)
                
                print(type([data]))
              
                sheet.append_rows(components_transposed)

                
        except UnicodeDecodeError as e:
            print(f"UnicodeDecodeError: {e}")
        except IndexError as e:
            print(f"IndexError: {e}")


