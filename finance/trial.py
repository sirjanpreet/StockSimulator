list = [{"key": "value"}, {"key": "value2"}]

for dict in list:
    for key in dict:
        if (dict[key] == "value3"):
            print("true")