# ======= System Information =======

import os
import random
import time


class Information:

    def __init__(self, name="Unknown"):
        self.name = name
        self.session_id = None
        self.directory = None
        self.current_time = None

    def message(self):
        return f"Hello {self.name}!\nWelcome to the System Information Program."

    def session(self):
        self.session_id = random.randint(100000, 999999)
        return self.session_id

    def current_directory(self):
        self.directory = os.getcwd()
        return self.directory

    def get_current_time(self):
        self.current_time = time.ctime()
        return self.current_time


name = input("Enter your name: ")

info = Information(name)

message = info.message()
session_id = info.session()
directory = info.current_directory()
current_time = info.get_current_time()

print("\n======= System Information =======")
print(message)
print(f"Session ID: {session_id}")
print(f"Current Directory: {directory}")
print(f"Current Time: {current_time}")
print("==================================")
