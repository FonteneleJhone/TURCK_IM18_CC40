
import subprocess
from pyModbusTCP.server import ModbusServer
from pymodbus.client.sync import ModbusTcpClient
import socket
import time
import json

hostname = socket.gethostname()
server_ip_address = "192.168.0.9"
server_port = 502

server = ModbusServer(server_ip_address, server_port, no_block=True)
client = ModbusTcpClient(server_ip_address, server_port)

def write_to_json_file(filename, an_object):
    with open(filename, 'w') as file:
        json.dump(an_object, file, indent=2, separators=(',', ':'))

try:
    print("Starting Modbus server...")
    server.start()
    print("Modbus server started!")

    while True:
        process_temp = subprocess.Popen(['/home/scripts/ambient_read.sh', 'temp'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process_hum = subprocess.Popen(['/home/scripts/ambient_read.sh', 'hum'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process_distance = subprocess.Popen(['/home/scripts/distance_read.sh', 'short', '1'], stdout=subprocess.PIPE, stderr=subproce$

        stdout_temp, stderr_temp = process_temp.communicate()
        stdout_hum, stderr_hum = process_hum.communicate()
        stdout_distance, stderr_distance = process_distance.communicate()

        if process_temp.returncode == 0:
            output_temp = stdout_temp.decode('utf-8')
            output_hum = stdout_hum.decode('utf-8')
            output_distance = stdout_distance.decode('utf-8')

            colon_index = output_temp.find(',')
            colon_index_hum = output_hum.find(',')
            colon_index_distance = output_distance.find(',')
            colon_index_distance_unit = output_distance.find('mm')

            if colon_index != -1 and colon_index_hum != -1 and colon_index_distance != -1:
                temperature = float(output_temp[colon_index + 2:colon_index + 7].strip())
                humidity = float(output_hum[colon_index_hum + 2: colon_index_hum + 7].strip())
                distance = float(output_distance[colon_index_distance + 1: colon_index_distance_unit].strip())

                client.write_register(0, int(100 * temperature))
                client.write_register(1, int(100 * humidity))
                client.write_register(2, int(10 * distance))
                sensor = {"im18_ccm40": {"Temperatura": str(temperature), "Umidade": str(humidity), "Distancia": str(distance)}}
                write_to_json_file('api.json', sensor)

        time.sleep(1)  # Wait for 1 second between iteration

except KeyboardInterrupt:
    print("Stopping Modbus server...")
    server.stop()
    client.close()
    print("Modbus server stopped.")
