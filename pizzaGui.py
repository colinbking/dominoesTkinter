import tkinter as tk
from tkinter import font  as tkfont # python 3
from tkinter import ttk


from pizzapy import Customer, StoreLocator, Order, ConsoleInput
from pizzapy.store import Store, StoreLocator
from pizzapy.address import Address
from tkinter import Tk, Label, Button, StringVar
from pizzapy.payment import CreditCard

def handle_focus_in(entry):
    entry.delete(0, tk.END)
    entry.config(fg='black')

def handle_focus_out(entry):
    entry.delete(0, tk.END)
    entry.config(fg='grey')
    entry.insert(0, "Example")

def handle_enter(entry):
    handle_focus_out(entry)




class Client():
    def __init__(self):
        self.name = ""
        self.address = Address("", "", "", "", "", "us")
        self.phone = ""
        self.place = ""
        self.card = ""
        self.items = []

client = None

class Welcome(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.frames = {}
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        for F in (StartPage, InfoPage, MenuPage, RestaurantPage, FinalizeOrderPage, PaymentPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        global client
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        if type(frame) == RestaurantPage:
            frame.show_stores()
        elif type(frame) == FinalizeOrderPage:
            frame.displayOrder(client.order)
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to Dominoes!", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = ttk.Button(self, text="Start",
                           command=lambda: controller.show_frame("InfoPage"))
        button.pack()
        self.close_button = ttk.Button(self, text="Close", command=parent.quit)
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
        self.prompt = tk.Label(self, text="Please enter your first AND last name", font=self.controller.title_font)
        self.prompt.pack()
        
        v = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=v)
        self.entry.bind('<Return>', (lambda event: self.get_address(True)))      # on enter key
        self.entry.pack()
        
       
    def get_address(self, first):
        if first:
            self.name =self.entry.get()
            self.first_name = self.name.split(" ")[0]
            self.last_name = self.name.split(" ")[1]
        self.prompt['text'] = "Hi " + self.name + "! \n Please enter your address using this format: \n" \
        + "HOUSE #, Full Street Name, City, State/Province, ZIP/Postal Code \n" \
        + "EXAMPLE: 700 Pennsylvania Avenue NW, Washington, DC, 20408"
        
        self.entry.bind('<Return>', (lambda event: self.go_to_rst()))      # on enter key
        
    # take address from entry and go to menu
    def go_to_rst(self):
        global client
        self.address = self.entry.get()
        self.prompt['text'] = "Cool, we'll deliver to: \n" + self.address +"! \n" + "If that's correct, start ordering!"
        client = Customer(self.first_name, self.last_name, "email", "3468748803", self.address)
        # print("Type", type(client), client)
        # print("NAME", client.first_name)
        newb = ttk.Button(self, text="Let me change that address.",
                           command=lambda: self.get_address(False))
        newb.pack(pady="10")
        newb = ttk.Button(self, text="Looks good, lets order!",
                           command=lambda: self.controller.show_frame("RestaurantPage"))
        newb.pack(padx="10")
        # self.controller.show_frame("MenuPage")
        # transferinfo({"name": self.name, "address": self.address})

class RestaurantPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="RST PAGE", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go back to the start page", command=lambda: controller.show_frame("StartPage"))
        button.pack()
        self.prompt = tk.Label(self, text="Lets get started! \n Select the restaurant below that you want to order from by typing the store number in below!", font=controller.title_font)
        self.prompt.pack()
        

    def show_stores(self):
        global client
        print("Type", type(client), client)
        print("NAME", client.first_name)
        nbs = StoreLocator.nearby_stores(client.address)
        open_rst = str(nbs[0]) if len(nbs) > 0 else "No stores open near you right now!"
        self.prompt = tk.Label(self, text=open_rst, font=self.controller.title_font)
        self.prompt.pack()
        v = tk.StringVar()
        pick_loc_btn = ttk.Button(self, text="This location looks good", command = self.confirm_rst(nbs[0]))
        pick_loc_btn.pack()
        

    def confirm_rst(self, chosen_rst):
        self.prompt = tk.Label(self, text="You've chosen this location: \n " + str(chosen_rst), font=self.controller.title_font)
        self.prompt.pack() 
        client.chosen_rst = chosen_rst
        newb = ttk.Button(self, text="Begin Ordering",
                           command=lambda: self.go_to_menu())
        newb.pack(pady="10")

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
        self.prompt = tk.Label(self, text= "Please enter the category or ingredient of an item you want.", font=controller.title_font)
        self.prompt.pack()
        
        v = tk.StringVar()

        # full_name_entry.bind("<Return>", handle_enter)

        self.search_entry = ttk.Entry(self, textvariable=v)
        self.search_entry.insert(0, "Example: Hawaiian Pizza")
        # self.search_entry.bind("<FocusIn>", handle_focus_in(self.search_entry))
        # self.search_entry.bind("<FocusOut>", handle_focus_out(self.search_entry))
        self.search_entry.bind('<Return>', (lambda event: self.item_lookup()))      # on enter key
        
        self.search_entry.pack()
        self.order = None
        self.total = 0
        button = ttk.Button(self, text="I'm Done",
                    command=lambda: self.finish_order())
        button.pack()

        entry_prompt = ttk.Label(self, text= "After searching, type in the code of an item you want below, and hit enter to add it to your order", font=self.controller.title_font)
        entry_prompt.pack(pady = "10", padx = "10")
        select_entry = ttk.Entry(self, textvariable=tk.StringVar())
        select_entry.bind('<Return>', (lambda event: self.add_item_to_cart(self.order, select_entry.get())))      # on enter key
        select_entry.pack(pady = "20")

        self.items_prompt = tk.Label(self, text= "")
        self.items_prompt.pack(pady = "10")


    def item_lookup(self):
        global client
        if not self.order:
            self.order = Order(client.chosen_rst,client)
            self.menu = client.chosen_rst.get_menu()
        
        # reset the items list view, then search for items
        self.items_prompt['text'] = ""
        item = self.search_entry.get().strip().lower()
        if len(item) > 1:
            item = item[0].upper() + item[1:]
            self.prompt = tk.Label(self, text= f"Results for: {item}\n", font=self.controller.title_font)
            menu_items = self.menu.search(Name=item)
            all_items = ""
            for thing in menu_items:
                # print(thing.price, thing.code, thing.name)
                all_items += "\n" + thing.name + " " + thing.code
            self.items_prompt['text'] = all_items

        # if searching with empty string
        else:
            self.prompt = tk.Label(self, text= "Type in an item name and hit enter to search for it", font=self.controller.title_font)
            self.item_lookup()
      
    def add_item_to_cart(self, order, code):
        order.add_item(code)
        print(self.order.data['Products'])

    def remove_item_from_cart(self, order, code):
        order.remove_item(code)
        
    def finish_order(self):
        global client
        client.order = self.order
        self.controller.show_frame("FinalizeOrderPage")

class FinalizeOrderPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Here's your order so far:", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.order_label = tk.Label(self, text="", font=controller.title_font)
        self.order_label.pack(side="top", fill="x", pady=10)

        button = ttk.Button(self, text="Add more items",
                           command=lambda: controller.show_frame("MenuPage"))
        button.pack()
        button = ttk.Button(self, text="Looks good, lets checkout",
                           command=lambda: controller.show_frame("PaymentPage"))
        button.pack()
        self.close_button = ttk.Button(self, text="Close", command=parent.quit)
        self.close_button.pack()

    def displayOrder(self, order):
        self.order_label['text'] = ""
        total = 0
        for item in order.data["Products"]:
            price = item["Price"]
            name = item["Name"]
            total += float(price)
            self.order_label['text'] += "Item: " + name + "$" + price + "\n"
        self.order_label['text'] += "GRAND TOTAL (pre-tax): $" + str(total)


class PaymentPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="How would you like to pay?", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button = ttk.Button(self, text="Credit Card",
                           command=lambda: self.pay_with_card())
        button.pack()
        button = ttk.Button(self, text="Cash",
                           command=lambda: self.pay_with_cash())
        button.pack()
        self.card = None
    
    def pay_with_card(self):
        global client
        self.get_credit_card()
        client.order.place(self.card)
        client.chosen_rst.place_order(client.order, True)
        pass

    def pay_with_cash(self):

        client.chosen_rst.place_order(client.order, False)

    def get_credit_card(self) -> CreditCard:
        """
        gets a valid credit card from the user via console
        """
        label = tk.Label(self, text="Please enter your credit card information. This information will NOT be saved.\n", font=self.controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        card_num_entry = ttk.Entry(self, textvariable=tk.StringVar())
        card_num_entry.insert(0, "ENTER CREDIT CARD NUMBER HERE")
        card_num_entry.pack()

        date_entry = ttk.Entry(self, textvariable=tk.StringVar())
        date_entry.insert(0, "ENTER EXPIRY DATE (MM/YY) HERE")
        date_entry.pack()

        cvv_entry = ttk.Entry(self, textvariable=tk.StringVar())
        cvv_entry.insert(0, "ENTER CREDIT CARD 3 DIGIT CVV HERE")
        cvv_entry.pack()

        zip_entry = ttk.Entry(self, textvariable=tk.StringVar())
        zip_entry.insert(0, "ENTER ZIP CODE HERE")
        zip_entry.pack()
        
        button = ttk.Button(self, text="Done Entering Card Info",
                           command=lambda: self.extract_card_info(card_num_entry, date_entry, cvv_entry, zip_entry))
        button.pack()
        
    def extract_card_info(self, card_entry, date_entry, cvv_entry, zip_entry):
        card_number = card_entry.get().strip()
        card_expiry= date_entry.get().strip().replace("/","")
        cvv = cvv_entry.get().strip()
        zip_code = zip_entry.get().strip()

        try:
            self.card = CreditCard(card_number, card_expiry, cvv, zip_code)
            label = tk.Label(self, text="Card Validated!\n", font=self.controller.title_font)
            label.pack(side="top", fill="x", pady=10)
            print("heres card", self.card)
        except Exception as e:
            label = tk.Label(self, text="Card was invalid! Please try again \n", font=self.controller.title_font)
            label.pack(side="top", fill="x", pady=10)
            # return self.extract_card_info(card_entry, date_entry, cvv_entry, zip_entry)

        # return True on success
        return True



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
root.mainloop()