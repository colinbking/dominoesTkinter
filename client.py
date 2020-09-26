from pizzapy.address import Address
from tkinter import Tk, Label, Button, StringVar
from pizzapy.payment import CreditCard


class Client():
    def __init__(self):
        self.name = ""
        self.address = Address("", "", "", "", "", "us")
        self.phone = ""
        self.place = ""
        self.card = ""
        self.items = []
        self.total_price = 0

