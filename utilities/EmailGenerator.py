import os
from datetime import datetime


def generate_email_with_time_stamp():
    time_stam = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    return "manik" + time_stam + "@gmail.com"




