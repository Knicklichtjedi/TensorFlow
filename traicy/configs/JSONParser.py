import JSONSettings as JSs

json_settings = JSs.parse_data("settings.json")
print("Dimension : " + str(JSs.get_dimension()))
print("Dimension Small : " + str(JSs.get_dimension_small()))
print("Border : " + str(JSs.get_border()))
print("Canny : " + str(JSs.get_canny()))
print("Gauss : " + str(JSs.get_binary_gauss()))
print("Threshold : " + str(JSs.get_binary_threshold()))