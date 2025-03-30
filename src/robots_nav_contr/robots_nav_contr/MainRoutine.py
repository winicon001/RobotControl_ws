import Archive.testbench


data = Archive.testbench.readouts("sm", data)

print(data)


# while True:

#     ################################
#     # Arrang MPU6050 data
#     ################################

#     arduino_read_values = arduinosensorsdata.reading.checkdata()
#     dist = arduino_read_values[0]
#     yaw = float(arduino_read_values[1])
#     pitch = float(arduino_read_values[2])
#     row = float(arduino_read_values[3])


