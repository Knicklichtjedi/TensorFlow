import JSONSettings as JSs
import time

json_settings = JSs.parse_data("settings.json")
print("Dimension : " + str(JSs.get_data(JSs.JSONValues.IMAGE_DIMENSION)))
print("Dimension Small : " + str(JSs.get_data(JSs.JSONValues.IMAGE_DIMENSION_SMALL)))
print("Border : " + str(JSs.get_data(JSs.JSONValues.IMAGE_BORDER)))
print("Canny : " + str(JSs.get_data(JSs.JSONValues.FILTER_CANNY)))
print("Gauss : " + str(JSs.get_data(JSs.JSONValues.FILTER_BIN_GAUSS)))
print("Threshold : " + str(JSs.get_data(JSs.JSONValues.FILTER_BIN_THRESHOLD)))

# Read data and return a certain value
print("Pre-Write " + str(JSs.get_data(JSs.JSONValues.IMAGE_DIMENSION, "settings.json")))
JSs.write_data("settings.json", JSs.JSONValues.IMAGE_DIMENSION, 35)

time.sleep(1)

print("Post-Write " + str(JSs.get_data(JSs.JSONValues.IMAGE_DIMENSION)))
JSs.write_data("settings.json", JSs.JSONValues.IMAGE_DIMENSION, 28)

