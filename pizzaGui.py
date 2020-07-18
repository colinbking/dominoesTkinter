import tkinter as tk
from tkinter import font  as tkfont # python 3

from pizzapy import Customer, StoreLocator, Order, ConsoleInput
from pizzapy.store import Store, StoreLocator
from pizzapy.address import Address
from tkinter import Tk, Label, Button, StringVar

class Client():
    def __init__(self):
        self.name = ""
        self.address = Address("", "", "", "", "", "us")
        self.phone = ""
        self.place = ""

client = Client()

class Welcome(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.frames = {}

        for F in (StartPage, InfoPage, MenuPage, RestaurantPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to Dominoes!", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Start",
                           command=lambda: controller.show_frame("InfoPage"))
        button.pack()
        self.close_button = tk.Button(self, text="Close", command=parent.quit)
        self.close_button.pack()


class InfoPage(tk.Frame):
    

    def __init__(self, parent, controller):
        self.name = ""
        self.address = ""
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="INFO PAGE", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        self.get_name()
        

    def get_name(self):
        self.prompt = tk.Label(self, text="Please enter your name", font=self.controller.title_font)
        self.prompt.pack()
        
        v = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=v)
        self.entry.bind('<Return>', (lambda event: self.get_address(True)))      # on enter key
        self.entry.pack()
        
       
    def get_address(self, first):
        if first:
            self.name =self.entry.get()
        self.prompt['text'] = "Hi " + self.name + "! Please enter your address in the form: \n" \
        + "HOUSE #, Full Street Name, City, State/Province, ZIP/Postal Code \n" \
        + "EXAMPLE: 700 Pennsylvania Avenue NW, Washington, DC, 20408"
        
        self.entry.bind('<Return>', (lambda event: self.go_to_rst()))      # on enter key
        
    # take address from entry and go to menu
    def go_to_rst(self):
        self.address = self.entry.get()
        self.prompt['text'] = "Cool, we'll deliver to" + self.address +"! \n" + "If that's correct, start ordering!"
        newb = tk.Button(self, text="Let me change that address.",
                           command=lambda: self.get_address(False))
        newb.pack(pady="10")
        newb = tk.Button(self, text="Looks good, lets order!",
                           command=lambda: self.controller.show_frame("RestaurantPage"))
        newb.pack(padx="10")
        # self.controller.show_frame("MenuPage")
        # transferinfo({"name": self.name, "address": self.address})
        client.address = Address(*self.address.split(','))
        client.name = self.name


class RestaurantPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="MENU PAGE", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go back to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        self.prompt = tk.Label(self, text="Lets get started! \n Select the restaurant below that you want to order from by typing it in below", font=controller.title_font)
        self.prompt.pack()
        
        open_rst = str(StoreLocator.nearby_stores(client.address)[0])
        self.prompt = tk.Label(self, text=open_rst, font=controller.title_font)
        self.prompt.pack()


        v = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=v)
        self.entry.bind('<Return>', (lambda event: self.item_lookup()))      # on enter key
        self.entry.pack()
        


    def item_lookup(self):
        name = self.entry.get()
        self.prompt['text'] = "Hi " + name + "! Please enter your address in the form: \n" \
        + "HOUSE #, Full Street Name, City, State/Province, ZIP/Postal Code \n" \
        + "EXAMPLE: 700 Pennsylvania Avenue NW, Washington, DC, 20408"
        
    def get_address(self):
        address = self.entry.get()
        self.prompt['text'] = "Cool, we'll deliver to" + address +"! \n" + "If that's correct, start ordering!"
        self.prompt['command'] = lambda: self.go_to_menu()
        
    def go_to_menu(self):
        self.controller.show_frame("MenuPage")

class MenuPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="MENU PAGE", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go back to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        self.prompt = tk.Label(self, text="Lets get started! \n Enter the category or ingredient of an item you want.", font=controller.title_font)
        self.prompt.pack()
        
        v = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=v)
        self.entry.bind('<Return>', (lambda event: self.item_lookup()))      # on enter key
        self.entry.pack()
        

    def item_lookup(self):
        name = self.entry.get()
        self.prompt['text'] = "Hi " + name + "! Please enter your address in the form: \n" \
        + "HOUSE #, Full Street Name, City, State/Province, ZIP/Postal Code \n" \
        + "EXAMPLE: 700 Pennsylvania Avenue NW, Washington, DC, 20408"
        
    def get_address(self):
        address = self.entry.get()
        self.prompt['text'] = "Cool, we'll deliver to" + address +"! \n" + "If that's correct, start ordering!"
        self.prompt['command'] = lambda: go_to_menu
        
    def go_to_menu(self):
        self.controller.show_frame("RestaurantPage")


def searchMenu(menu):
	print("You are now searching the menu...")
	item = input("Type an item to look for: ").strip().lower()

	if len(item) > 1:
		item = item[0].upper() + item[1:]
		print(f"Results for: {item}\n")
		menu.search(Name=item)
		print()
	else:
		print("No Results")

def addToOrder(order):
	print("Please type the codes of the items you'd like to order...")
	print("Press ENTER to stop ordering.")
	while True:
		item = input("Code: ").upper()
		try:
			order.add_item(item)
		except:
			if item == "":
				break
			print("Invalid Code...")


# customer = ConsoleInput.get_new_customer()

# my_local_dominos = StoreLocator.find_closest_store_to_customer(customer)
# print("\nClosest Store:")
# print(my_local_dominos)

# ans = input("Would you like to order from this store? (Y/N)")
# if ans.lower() not in ["yes", "y"]:
# 	print("Goodbye!")
# 	quit()

# print("\nMENU\n")

# menu = my_local_dominos.get_menu()
# order = Order.begin_customer_order(customer, my_local_dominos, "ca")

# while True:
# 	searchMenu(menu)
# 	addToOrder(order)
# 	answer = input("Would you like to add more items (y/n)? ")
# 	if answer.lower() not in ["yes", "y"]:
# 		break

# total = 0
# print("\nYour order is as follows: ")
# for item in order.data["Products"]:
# 	price = item["Price"]
# 	print(item["Name"] + " $" + price)
# 	total += float(price)

# print("\nYour order total is: $" + str(total) + " + TAX\n")

# payment = input("\nWill you be paying CASH or CREDIT CARD? (CASH, CREDIT CARD)")
# if payment.lower() in ["card", "credit card"]:
# 	card = ConsoleInput.get_credit_card()
# else:
# 	card = False

# ans = input("Would you like to place this order? (y/n)")
# if ans.lower() in ["y", "yes"]:
# 	order.place(card)
# 	my_local_dominos.place_order(order, card)
# 	print("Order Placed!")
# else:
# 	print("Goodbye!")

root = Welcome()
root.geometry("900x900")
my_gui = Welcome()
root.mainloop()