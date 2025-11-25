def check_alert(pm25_value):
    if pm25_value > 250:
        return "Severe! Send Red Alert."
    elif pm25_value > 150:
        return "Very Poor! Send Orange Alert."
    elif pm25_value > 100:
        return "Poor! Send Yellow Alert."
    else:
        return "Air quality normal."
