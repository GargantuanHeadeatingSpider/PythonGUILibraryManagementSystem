# Imported modules

import random
from tkinter import *
from tkcalendar import *
from tkinter import ttk
from tkinter import messagebox

# Tkinter GUI main window setup. 1080P resolution and launches on fullscreen.
root = Tk()
root.title("World's Greatest Library Record System")
root.geometry("1920x1080")
root.configure(bg="#F74510")
root.state("zoomed")


# Book class and all relevant attributes. Created in input and its components packaged into a list to be added to book list.
class Book:

    def __init__(self, id_num, title, author_forename, author_surname, year, year_published, publisher, copies):
        self.id_num = id_num
        self.title = title
        self.author_forename = author_forename
        self.author_surname = author_surname
        self.year = year
        self.year_published = year_published
        self.publisher = publisher
        self.copies = copies


# User class and all relevant attributes. Created in input and its components packaged into a list to be added to user list.
class User:

    def __init__(self, username, forename, surname, house_number, street, postcode, email, dob):
        self.username = username
        self.forename = forename
        self.surname = surname
        self.house_number = house_number
        self.street = street
        self.postcode = postcode
        self.email = email
        self.dob = dob


# Instance is created with book list, length is the length of the book list to display number of books.
class BookList:

    def __init__(self, lst, ln):
        self.lst = lst
        self.ln = ln


# Instance is created with the user list, length is simply the length of the user list to display number of users.
class UserList:

    def __init__(self, lst, ln):
        self.lst = lst
        self.ln = ln


# Takes data from user and book to create loan object.
class Loans:

    def __init__(self, username, user_fn, user_sn, email, book, count, cur_date, due_date):
        self.username = username
        self.user_fn = user_fn
        self.user_sn = user_sn
        self.email = email
        self.book = book
        self.count = count
        self.cur_date = cur_date
        self.due_date = due_date

# ======================================================================================================================
# Loan lists
borrowed_books = []
overdue_list = []
loan_list = []

# ======================================================================================================================
# User lists
test_user = User("NotABot",
                 "Hugh",
                 "Mann",
                 555,
                 "Wheelie Bin Drive",
                 "NE32 4QE",
                 "BH175@botsahoy.gov",
                 "21/01/2021")

user_list = [[test_user.username, test_user.forename, test_user.surname, test_user.house_number, test_user.street,
              test_user.postcode, test_user.email, test_user.dob]]
print(user_list)
# ======================================================================================================================
# Book list and test objects.
test_book1 = Book("#123456", "John Dies at the End", "David", "Wong", "7/8/07", "7/8/07", "Permuted Press",
                  99999999999999)
test_book2 = Book("#194762", "This Book is Full of Spiders", "David", "Wong", "12/12/12", "12/12/12",
                  "Thomas Dunne Books", 9999999999999999)
test_book3 = Book("#789101", "What the Hell Did I just Read?", "David", "Wong", "1/18/21", "1/12/11",
                  "Thomas Dunne Books", 9999999999999999)
test_book4 = Book("#999998", "Test Book", "Test", "Book", "1/18/21", "1/12/11", "Test Books Press", 1)
test_book5 = Book("#152489", "Just Messing Around Now", "Foolish", "Mortal", "1/18/21", "1/12/11", "Jarra Books", 1)
test_book6 = Book("#239040", "Armadillo Fists", "Carlton", "Mellick", "1/18/21", "1/12/11", "Eraserhead Press", 1)

# Book list is populated with test books to ensure treeview effectiveness. It worked.
book_list = [[test_book1.id_num, test_book1.title, test_book1.author_forename, test_book1.author_surname,
              test_book1.year, test_book1.year_published, test_book1.publisher, test_book1.copies],
             [test_book2.id_num, test_book2.title, test_book2.author_forename, test_book2.author_surname,
              test_book2.year, test_book2.year_published, test_book2.publisher, test_book2.copies],
             [test_book3.id_num, test_book3.title, test_book3.author_forename, test_book3.author_surname,
              test_book3.year, test_book3.year_published, test_book3.publisher, test_book3.copies]]

bl_length = len(book_list)


# ======================================================================================================================
# Obligatory welcome page to ease the user into the program.
def welcome_page():
    home_frame = Frame(root, width="1024", height="720", bg="#292929")

    home_label = Label(home_frame, text="Ultimate Library System: Extreme Edition",
                       padx=24, pady=24, bg="#696969", fg="#f5f5f5", borderwidth=15, relief="ridge")

    home_label.config(font=("arial", 32))
    home_label.place(relx=.5, y=75, anchor="center")
    # Frame pack propagate maintains the size of the widget, preventing it from adjusting to fit the widgets inside.
    home_frame.pack_propagate(False)
    # relx and rely at .5 with center anchor places the frame in the center of the screen.
    home_frame.place(relx=.5, rely=.5, anchor="center")

    # Transitions the user into the main page when enter button is clicked. Destroys old frame, creates new frame.
    def main_transfer():
        home_frame.destroy()
        main_page()

    enter_btn = Button(home_frame, text="Witness the sheer power of lists.", command=main_transfer, padx=30, pady=30)
    enter_btn.config(font=("courier", 20))
    enter_btn.place(relx=.5, rely=.5, anchor="center")


# Top layer of the functionality, creates frame, calls tree creation function and initialises list objects for use in populating trees.
def main_page():
    viewer_frame = Frame(root, width="1800", height="900", bg="#292929")

    book_lst = BookList(book_list, len(book_list))
    blst = book_lst.lst
    bln = book_lst.ln

    user_lst = UserList(user_list, len(user_list))
    ulst = user_lst.lst
    uln = user_lst.ln

    llst = loan_list
    lln = len(loan_list)
# ======================================================================================================================
    # Trees and the sub-functions they operate on are defined here.
    def make_trees():
        # Books are made in this function, opening a sub-frame with the entry fields the user must fill to create a book object.
        def book_creation():
            # This section defines the frame, labels and entries.
            # Book creation frame
            book_frame = Frame(root, width="600", height="660", bg="#292929", borderwidth=2.5, relief="ridge")

            # Used to close the book creation page and reactivate the create book button. Activated by home button
            def home_transfer():
                book_creator_btn["state"] = "normal"
                book_frame.destroy()

            home_btn = Button(book_frame, padx=10, pady=10, bg="#F74510", fg="white", text="HOME",
                              command=home_transfer,
                              borderwidth=10)
            home_btn.config(font=("arial", 20))
            home_btn.place(x=10, y=10)

            book_title = Label(book_frame, padx="10", pady="10", text="Please enter the book's details below.",
                               borderwidth=5,
                               relief="raised")

            # Book details are created here. ID is done with RNG, set to consistently create six digit numbers prefaced with a "#".
            # The rest is handled via labels and entries, with two calendars for date added and date published.
            # TKcalendar is an unofficial extension of Tkinter which has made entering dates immeasurably easier.
            id_num = str("#") + str(random.randint(100000, 999999))
            id_label = Label(book_frame, text=id_num, padx=5, pady=5, borderwidth=2.5, relief="ridge")

            # Title
            title_label = Label(book_frame, text="Title: ", padx=5, pady=5, borderwidth=2.5, relief="groove")
            title_entry = Entry(book_frame)

            # Author Forename
            author_fn_label = Label(book_frame, text="Author Forename: ", padx=5, pady=5, borderwidth=2.5,
                                    relief="groove")
            author_fn_entry = Entry(book_frame)

            # Author Surname
            author_sn_label = Label(book_frame, text="Author surname: ", padx=5, pady=5, borderwidth=2.5,
                                    relief="groove")
            author_sn_entry = Entry(book_frame)

            # Date Added
            year_label = Label(book_frame, text="Date added: ", padx=5, pady=5, borderwidth=2.5, relief="groove")
            year_calendar = Calendar(book_frame, selectmode="day", date_pattern="dd/MM/yyyy")

            # Date Published
            year_published_label = Label(book_frame, text="Publication Date: ", padx=5, pady=5, borderwidth=2.5,
                                         relief="groove")
            year_published_cal = Calendar(book_frame, selectmode="day", date_pattern="dd/MM/yyyy")

            # Publisher
            publisher_label = Label(book_frame, text="Publisher: ", padx=5, pady=5, borderwidth=2.5, relief="groove")
            publisher_entry = Entry(book_frame)

            # Copies
            copies_label = Label(book_frame, text="Available Copies: ", padx=5, pady=5, borderwidth=2.5,
                                 relief="groove")
            copies_entry = Entry(book_frame)

            # Widget placement order. All of the widgets defined above are placed here in label-entry pairs.

            # Title Label
            book_title.place(relx=.7, y=30, anchor="center")

            # Book ID
            id_label.place(relx=.7, y=75, anchor="center")

            # Title
            title_label.place(relx=.7, y=120, anchor="center")
            title_entry.place(relx=.7, y=150, anchor="center")

            # Author Forename
            author_fn_label.place(relx=.7, y=200, anchor="center")
            author_fn_entry.place(relx=.7, y=230, anchor="center")

            # Author Surname
            author_sn_label.place(relx=.7, y=275, anchor="center")
            author_sn_entry.place(relx=.7, y=305, anchor="center")

            # Year
            year_label.place(relx=.25, y=150, anchor="center")
            year_calendar.place(relx=.25, y=265, anchor="center")

            # Date published
            year_published_label.place(relx=.16, y=380)
            year_published_cal.place(relx=.04, y=420)

            # Publisher
            publisher_label.place(relx=.7, y=430, anchor="center")
            publisher_entry.place(relx=.7, y=460, anchor="center")

            # Available Copies
            copies_label.place(relx=.7, y=515, anchor="center")
            copies_entry.place(relx=.7, y=545, anchor="center")

            # Saves information from entry boxes and compiles into a book object,
            # with each element meeting corresponding positional argument.
            def get_book_input():
                message = messagebox
                id_number = id_num
                title = title_entry.get()
                author_fn = author_fn_entry.get()
                author_sn = author_sn_entry.get()
                year = year_calendar.get_date()
                year_published = year_published_cal.get_date()
                publisher = publisher_entry.get()
                copies = copies_entry.get()
                # Used to create a messagebox if no int is entered in the copies entrybox.
                try:
                    int_copies = int(copies)
                except ValueError:
                    message.showerror("Error", "Please only input whole numbers")

                # The object that is created from this process. It is packed into a list in the pack book function.
                book = Book(id_number, title, author_fn, author_sn, year, year_published, publisher, int_copies)

                return book

# ======================================================================================================================
            # Allows the checking of details before either submitting or returning to edit book details.
            def book_confirm():
                confirm_frame = Frame(root, width=600, height=400)

                confirm_label = Label(confirm_frame, padx=40, pady=30, text="Are these details are correct?")
                confirm_label.pack()

                # Uses get technique to show contents of entry boxes
                id_num_lab = Label(confirm_frame, text=id_num)
                title_lab = Label(confirm_frame, text=title_entry.get())
                author_fn_lab = Label(confirm_frame, text=author_fn_entry.get())
                author_sn_lab = Label(confirm_frame, text=author_sn_entry.get())
                year_lab = Label(confirm_frame, text=year_calendar.get_date())
                year_published_lab = Label(confirm_frame, text=year_published_cal.get_date())
                publisher_lab = Label(confirm_frame, text=publisher_entry.get())
                copies_lab = Label(confirm_frame, text=copies_entry.get())

                # The above labels are sequentially packed in order here.
                id_num_lab.pack()
                title_lab.pack()
                author_fn_lab.pack()
                author_sn_lab.pack()
                year_lab.pack()
                year_published_lab.pack()
                publisher_lab.pack()
                copies_lab.pack()

# ======================================================================================================================
                # Packages book into list and creates book list object
                def pack_book():
                    # Gets book object.
                    content = get_book_input()

                    # Packages book object components into a list.
                    blst = [content.id_num, content.title, content.author_forename, content.author_surname,
                            content.year, content.year_published, content.publisher, content.copies]

                    # Append this list to the book list and book tree
                    book_list.append(blst)
                    book_tree.insert(parent="", index="end", text="", value=blst)

                    # Destroys current frames and opens menu return frame
                    confirm_frame.destroy()
                    book_frame.destroy()
                    menu_return()

                yes_btn = Button(confirm_frame, padx=10, pady=10, text="Yes", command=pack_book)
                yes_btn.pack(side="left", padx=10)

                no_btn = Button(confirm_frame, padx=10, pady=10, text="No", command=confirm_frame.destroy)
                no_btn.pack(side="right", padx=10)

                confirm_frame.pack_propagate(False)
                confirm_frame.place(relx=.5, rely=.5, anchor="center")

# ======================================================================================================================
            def menu_return():
                # Gives user a chance to add another book or return to main view.
                menu_return_frame = Frame(root, width=800, height=600)

                menu_label = Label(menu_return_frame, text="Would you like to add another book?")
                menu_label.pack()

                def menu_transfer():
                    # Returns button to normal state, allowing another book to be made.
                    book_creator_btn["state"] = "normal"
                    menu_return_frame.destroy()
                    book_frame.destroy()

                menu_btn = Button(menu_return_frame, padx=10, pady=10, text="Return to menu", command=menu_transfer)
                menu_btn.pack(side="left")

                def reset_book():
                    # Resets the book creation process.
                    menu_return_frame.destroy()
                    book_frame.destroy()
                    book_creation()

                new_book_btn = Button(menu_return_frame, padx=10, pady=10, text="Add new book", command=reset_book)
                new_book_btn.pack(side="right")

                menu_return_frame.pack_propagate(False)
                menu_return_frame.place(relx=.5, rely=.5, anchor="center")

            submit_btn = Button(book_frame, text="Submit", padx=10, pady=10, command=book_confirm, borderwidth=10,
                                relief="raised")
            submit_btn.config(font=("courier", 14))
            submit_btn.place(relx=.7, y=605, anchor="center")

            # Centers the primary frame
            book_frame.pack_propagate(False)
            book_frame.place(relx=.5, rely=.5, anchor="center")
            bk = get_book_input
            return bk

# ======================================================================================================================
        # BOOK TREE

        book_tree = ttk.Treeview(viewer_frame)
        book_tree["columns"] = ("Book ID",
                                "Title",
                                "Author Forename",
                                "Author Surname",
                                "Date Added",
                                "Date Published",
                                "Publisher",
                                "Copies")

        # Book tree headings and columns for storing book object attributes.
        book_tree.heading("Book ID", text="ID")
        book_tree.heading("Title", text="Title")
        book_tree.heading("Author Forename", text="Author Forename")
        book_tree.heading("Author Surname", text="Author Surname")
        book_tree.heading("Date Added", text="Date Added")
        book_tree.heading("Date Published", text="Date Published")
        book_tree.heading("Publisher", text="Publisher")
        book_tree.heading("Copies", text="Copies")

        book_tree.column("#0", width=1)
        book_tree.column("#1", width=55)
        book_tree.column("#2", width=100)
        book_tree.column("#3", width=100)
        book_tree.column("#4", width=100)
        book_tree.column("#5", width=100)
        book_tree.column("#6", width=100)
        book_tree.column("#7", width=100)
        book_tree.column("#8", width=100)

        # Count is used for book tree entry IID. For loop inserts list data into appropriate columns,
        # count gives each row its own unique number without requirement to manually enter it.
        count = 0
        for book in blst:
            book_tree.insert(parent="", index="end", iid=count, text="", value=book)
            count += 1

        # Gets selected item and removes from the book tree.
        def delete_book():
            target = book_tree.selection()
            for item in target:
                for i in range(bln):
                    if book_list[i] == book_tree.item(item)["values"][0]:
                        book_list.clear()
                        break
                book_tree.delete(item)

        # Disables create book button and opens create book frame. Prevents multiple instances of book creator.
        def creator_transition():
            book_creator_btn.config(state="disabled")
            book_creation()

# ======================================================================================================================
        # Inserts data of selected book into entry boxes for updating.
        def select_book():

            pub_date_ent.configure(state="normal")

            # Clears entries before inserting new data.
            title_ent.delete(0, END)
            author_fn_ent.delete(0, END)
            author_sn_ent.delete(0, END)
            publisher_ent.delete(0, END)
            copies_ent.delete(0, END)

            # Gets selected tree item.
            selected = book_tree.focus()
            values = book_tree.item(selected, "values")

            # Transfers book tree data to entries.
            title_ent.insert(0, values[1])
            author_fn_ent.insert(0, values[2])
            author_sn_ent.insert(0, values[3])
            year_cal.selection_set(values[4])
            pub_date_ent.insert(0, values[5])
            publisher_ent.insert(0, values[6])
            copies_ent.insert(0, values[7])

            pub_date_ent.configure(state="disabled")

        # Replaces data of selected book with data from the entries.
        # Values are the get functions of entryboxes placed in order.
        def update_book():

            pub_date_ent.configure(state="normal")
            # Messagebox for error handling, tells user where they went wrong.
            msg = messagebox
            try:
                copies = int(copies_ent.get())
            except ValueError:
                msg.showerror("Error", "Please enter an integer.")
            selected = book_tree.focus()
            values = book_tree.item(selected, "values")
            book_tree.item(selected, text="", values=(
                values[0], title_ent.get(), author_fn_ent.get(), author_sn_ent.get(), year_cal.get_date(), pub_date_ent.get(),
                publisher_ent.get(), copies))

            title_ent.delete(0, END)
            author_fn_ent.delete(0, END)
            author_sn_ent.delete(0, END)
            publisher_ent.delete(0, END)
            pub_date_ent.delete(0, END)
            pub_date_ent.configure(state="disabled")

        # Buttons, labels and entries for book selection and editing are defined here.
        delete_bk = Button(viewer_frame, padx=10, pady=10, bg="red", fg="white", text="Delete Book",
                           command=delete_book, borderwidth=4, relief="groove")
        delete_bk.config(font=("arial", 14))
        delete_bk.place(relx=.25, y=32.5, anchor="center")

        book_creator_btn = Button(viewer_frame, padx=10, pady=10, text="Add New Book", command=creator_transition,
                                  borderwidth=2, relief="groove")
        book_creator_btn.place(x=730, y=330, anchor="center")

        select_btn = Button(viewer_frame, padx=10, pady=10, text="Select Book", command=select_book, borderwidth=2,
                            relief="groove")
        select_btn.place(x=70, y=325, anchor="center")

        update_btn = Button(viewer_frame, padx=10, pady=10, text="Update Book Record", command=update_book,
                            borderwidth=2, relief="groove")
        update_btn.place(x=400, y=325, anchor="center")

        title_lbl = Label(viewer_frame, padx=5, pady=5, text="Title: ", borderwidth=2, relief="groove")
        title_ent = Entry(viewer_frame)

        author_fn_lbl = Label(viewer_frame, padx=5, pady=5, text="Author Forename: ", borderwidth=2, relief="groove")
        author_fn_ent = Entry(viewer_frame)

        author_sn_lbl = Label(viewer_frame, padx=5, pady=5, text="Author Surname: ", borderwidth=2, relief="groove")
        author_sn_ent = Entry(viewer_frame)

        year_lbl = Label(viewer_frame, padx=5, pady=5, text="Year", borderwidth=2, relief="groove")
        year_cal = Calendar(viewer_frame, selectmode="day", date_pattern="dd/MM/yyyy")

        publisher_lbl = Label(viewer_frame, padx=5, pady=5, text="Publisher: ", borderwidth=2, relief="groove")
        publisher_ent = Entry(viewer_frame)

        copies_lbl = Label(viewer_frame, padx=5, pady=5, text="Copies: ", borderwidth=2, relief="groove")
        copies_ent = Entry(viewer_frame)

        pub_date_lbl = Label(viewer_frame, padx=5, pady=5, text="Publication Date: ", borderwidth=2, relief="groove")
        pub_date_ent = Entry(viewer_frame)
        pub_date_ent.configure(state="disabled")

        # Entries and labels for selecting and editing tree items are positioned here.
        title_lbl.place(x=10, y=400)
        title_ent.place(x=130, y=405)

        author_fn_lbl.place(x=10, y=440)
        author_fn_ent.place(x=130, y=445)

        author_sn_lbl.place(x=10, y=480)
        author_sn_ent.place(x=130, y=485)

        year_lbl.place(x=405, y=400)
        year_cal.place(x=295, y=445)

        publisher_lbl.place(x=10, y=520)
        publisher_ent.place(x=130, y=525)

        copies_lbl.place(x=10, y=560)
        copies_ent.place(x=130, y=565)

        pub_date_lbl.place(x=10, y=600)
        pub_date_ent.place(x=130, y=605)

        book_tree.place(relx=.225, rely=.2, anchor="center")

        book_count = len(book_tree.get_children())

        book_count_lbl = Label(viewer_frame, padx=5, pady=5, text=book_count)
        book_count_lbl.place(x=20, y=20)
# ======================================================================================================================

        # Functionality for creating book and creating user are completely identical.
        def create_user():
            # This section defines the frame, labels and entries.

            user_frame = Frame(root, width="700", height="680", bg="#292929", borderwidth=2.5, relief="ridge")

            def home_transfer():
                user_frame.destroy()
                add_user_btn["state"] = "normal"

            home_btn = Button(user_frame, padx=10, pady=10, bg="#F74510", fg="white", text="HOME",
                              command=home_transfer,
                              borderwidth=10)
            home_btn.config(font=("arial", 20))
            home_btn.place(x=525, y=10)

            user_title = Label(user_frame, padx="10", pady="10", text="Please enter the user's details below.",
                               borderwidth=5,
                               relief="raised")

            username_label = Label(user_frame, text="Username: ", padx=5, pady=5, borderwidth=2.5, relief="groove")
            username_entry = Entry(user_frame)

            user_fn_label = Label(user_frame, text="Forename: ", padx=5, pady=5, borderwidth=2.5, relief="groove")
            user_fn_entry = Entry(user_frame)

            user_sn_label = Label(user_frame, text="Surname: ", padx=5, pady=5, borderwidth=2.5, relief="groove")
            user_sn_entry = Entry(user_frame)

            house_num_label = Label(user_frame, text="House Number: ", padx=5, pady=5, borderwidth=2.5, relief="groove")
            house_num_entry = Entry(user_frame)

            street_name_label = Label(user_frame, text="Street Name: ", padx=5, pady=5, borderwidth=2.5,
                                      relief="groove")
            street_name_entry = Entry(user_frame)

            postcode_label = Label(user_frame, text="Postcode: ", padx=5, pady=5, borderwidth=2.5, relief="groove")
            postcode_entry = Entry(user_frame)

            email_label = Label(user_frame, text="Email Address: ", padx=5, pady=5, borderwidth=2.5, relief="groove")
            email_entry = Entry(user_frame)

            dob_label = Label(user_frame, text="Date of Birth: ", padx=5, pady=5, borderwidth=2.5, relief="groove")
            dob_cal = Calendar(user_frame, selectmode="day", date_pattern="dd/MM/yyyy")

            # ======================================================================================================================

            # Widget placement order. All of the widgets defined above are placed here in label-entry pairs.

            # User Label
            user_title.place(relx=.5, y=30, anchor="center")

            # Username
            username_label.place(relx=.2, y=90, anchor="center")
            username_entry.place(relx=.5, y=90, anchor="center")

            # User Forename
            user_fn_label.place(relx=.2, y=150, anchor="center")
            user_fn_entry.place(relx=.5, y=150, anchor="center")

            # User Surname
            user_sn_label.place(relx=.2, y=210, anchor="center")
            user_sn_entry.place(relx=.5, y=210, anchor="center")

            # House Number
            house_num_label.place(relx=.16, y=270, anchor="center")
            house_num_entry.place(relx=.5, y=270, anchor="center")

            # Street Name
            street_name_label.place(relx=.18, y=330, anchor="center")
            street_name_entry.place(relx=.5, y=330, anchor="center")

            postcode_label.place(relx=.2, y=390, anchor="center")
            postcode_entry.place(relx=.5, y=390, anchor="center")

            email_label.place(relx=.17, y=450, anchor="center")
            email_entry.place(relx=.5, y=450, anchor="center")

            dob_label.place(relx=.185, y=510, anchor="center")
            dob_cal.place(relx=.6, y=570, anchor="center")

            # ======================================================================================================================
            # Saves information from entry boxes and compiles into a user object,
            # with each element meeting corresponding positional argument.
            def get_user_input():
                username = username_entry.get()
                user_fn = user_fn_entry.get()
                user_sn = user_sn_entry.get()
                house_num = house_num_entry.get()
                int_house = int(house_num)
                street_name = street_name_entry.get()
                postcode = postcode_entry.get()
                email = email_entry.get()
                dob = dob_cal.get_date()
                user_obj = User(username, user_fn, user_sn, int_house, street_name, postcode, email, dob)

                return user_obj

            # Allows the checking of details before either submitting or returning to edit user details.
            def user_confirm():
                confirm_frame = Frame(root, width=600, height=400)

                confirm_label = Label(confirm_frame, padx=40, pady=30, text="Are these details are correct?")
                confirm_label.pack()

                # Uses get technique to show contents of entry boxes
                username_lab = Label(confirm_frame, text=username_entry.get())
                user_fn_lab = Label(confirm_frame, text=user_fn_entry.get())
                user_sn_lab = Label(confirm_frame, text=user_sn_entry.get())
                house_num_lab = Label(confirm_frame, text=house_num_entry.get())
                street_name_lab = Label(confirm_frame, text=street_name_entry.get())
                postcode_lab = Label(confirm_frame, text=postcode_entry.get())
                email_lab = Label(confirm_frame, text=email_entry.get())
                dob_lab = Label(confirm_frame, text=dob_cal.get_date())

                username_lab.pack()
                user_fn_lab.pack()
                user_sn_lab.pack()
                house_num_lab.pack()
                street_name_lab.pack()
                postcode_lab.pack()
                email_lab.pack()
                dob_lab.pack()

                # Packages user into list.
                def pack_user():
                    content = get_user_input()
                    uslst = [content.username, content.forename, content.surname, content.house_number,
                             content.street, content.postcode, content.email, content.dob]
                    user_list.append(uslst)
                    user_tree.insert(parent="", index="end", text="", value=uslst)

                    confirm_frame.destroy()
                    user_frame.destroy()
                    menu_return()

                # ======================================================================================================================

                yes_btn = Button(confirm_frame, padx=10, pady=10, text="Yes", command=pack_user)
                yes_btn.pack(side="left")

                no_btn = Button(confirm_frame, padx=10, pady=10, text="No", command=confirm_frame.destroy)
                no_btn.pack(side="right")

                confirm_frame.pack_propagate(False)
                confirm_frame.place(relx=.5, rely=.5, anchor="center")

            def menu_return():
                menu_return_frame = Frame(root, width=600, height=400)

                menu_label = Label(menu_return_frame, text="Would you like to add another user?")
                menu_label.pack()

                def menu_transfer():
                    add_user_btn["state"] = "normal"
                    menu_return_frame.destroy()
                    user_frame.destroy()

                menu_btn = Button(menu_return_frame, padx=10, pady=10, text="No", command=menu_transfer)
                menu_btn.pack(side="left")

                def reset_user():
                    menu_return_frame.destroy()
                    user_frame.destroy()
                    create_user()

                new_user_btn = Button(menu_return_frame, padx=10, pady=10, text="Yes", command=reset_user)
                new_user_btn.pack(side="right")

                menu_return_frame.pack_propagate(False)
                menu_return_frame.place(relx=.5, rely=.5, anchor="center")

            submit_btn = Button(user_frame, text="Submit", padx=10, pady=10, command=user_confirm, borderwidth=10,
                                relief="raised")
            submit_btn.config(font=("courier", 14))
            submit_btn.place(relx=.15, y=605, anchor="center")

            # Centers the primary frame
            user_frame.pack_propagate(False)
            user_frame.place(relx=.5, rely=.5, anchor="center")

# ======================================================================================================================
        # USER TREE
        user_tree = ttk.Treeview(viewer_frame)
        user_tree["columns"] = ("Username",
                                "Forename",
                                "Surname",
                                "House Number",
                                "Street Address",
                                "Postcode",
                                "Email",
                                "Date of Birth")

        # Book tree headings for storing book object attributes.
        user_tree.heading("Username", text="Username")
        user_tree.heading("Forename", text="Forename")
        user_tree.heading("Surname", text="Surname")
        user_tree.heading("House Number", text="House Number")
        user_tree.heading("Street Address", text="Street Address")
        user_tree.heading("Postcode", text="Postcode")
        user_tree.heading("Email", text="Email")
        user_tree.heading("Date of Birth", text="DOB")

        user_tree.column("#0", width=1)
        user_tree.column("#1", width=120)
        user_tree.column("#2", width=75)
        user_tree.column("#3", width=75)
        user_tree.column("#4", width=75)
        user_tree.column("#5", width=75)
        user_tree.column("#6", width=75)
        user_tree.column("#7", width=75)
        user_tree.column("#8", width=75)

        count = 0
        for user in ulst:
            user_tree.insert(parent="", index="end", iid=count, text="", value=user)
            count += 1

        # Inserts data of selected user into entry boxes for updating.
        def select_user():
            # Clears entries before inserting new data.
            email_ent.configure(state="normal")
            dob_ent.configure(state="normal")

            username_ent.delete(0, END)
            fn_ent.delete(0, END)
            sn_ent.delete(0, END)
            house_num_ent.delete(0, END)
            street_ent.delete(0, END)
            postcode_ent.delete(0, END)
            email_ent.delete(0, END)
            dob_ent.delete(0, END)

            # Gets selected tree item.
            selected = user_tree.focus()
            values = user_tree.item(selected, "values")

            # Transfers book tree data to entries.
            username_ent.insert(0, values[0])
            fn_ent.insert(0, values[1])
            sn_ent.insert(0, values[2])
            house_num_ent.insert(0, values[3])
            street_ent.insert(0, values[4])
            postcode_ent.insert(0, values[5])
            email_ent.insert(0, values[6])
            dob_ent.insert(0, values[7])

            email_ent.configure(state="disabled")
            dob_ent.configure(state="disabled")

        # Replaces data of selected user with data from the entries.
        def modify_user():
            msg = messagebox
            try:
                house_no = int(house_num_ent.get())
            except ValueError:
                msg.showerror("Error", "Please enter an integer.")
            selected = user_tree.focus()
            values = book_tree.item(selected, "values")
            user_tree.item(selected, text="", values=(username_ent.get(), fn_ent.get(), sn_ent.get(), house_no, street_ent.get(), postcode_ent.get(), email_ent.get(), dob_ent.get()))

            username_ent.delete(0, END)
            fn_ent.delete(0, END)
            sn_ent.delete(0, END)
            house_num_ent.delete(0, END)
            street_ent.delete(0, END)
            postcode_ent.delete(0, END)

            email_ent.configure(state="normal")
            dob_ent.configure(state="normal")
            email_ent.delete(0, END)
            dob_ent.delete(0, END)
            email_ent.configure(state="disabled")
            dob_ent.configure(state="disabled")

        # Gets selected tree item and deletes.
        def delete_user():
            target = user_tree.selection()
            for item in target:
                for i in range(uln):
                    if user_list[i] == user_tree.item(item)["values"][0]:
                        user_list.pop(i)
                        break
                user_tree.delete(item)

        # Transition. Disables button while opening the user creation screen to avoid creating duplicates.
        # Reactivated upon deactivating the screen via completion or the exit button.
        def create_transition():
            add_user_btn.config(state="disabled")
            create_user()

        delete_user_btn = Button(viewer_frame, padx=10, pady=10, bg="red", fg="white", text="Delete User",
                                 borderwidth=4, relief="groove",
                                 command=delete_user)
        delete_user_btn.config(font=("arial", 14))
        delete_user_btn.place(relx=.75, y=33, anchor="center")

        add_user_btn = Button(viewer_frame, padx=10, pady=10, text="Add New User", command=create_transition, borderwidth=2, relief="groove")
        add_user_btn.place(x=1185, y=325, anchor="center")

        select_user_btn = Button(viewer_frame, padx=10, pady=10, text="Select User", command=select_user, borderwidth=2, relief="groove")
        select_user_btn.place(x=1450, y=325, anchor="center")

        modify_user_btn = Button(viewer_frame, padx=10, pady=10, text="Modify User", command=modify_user, borderwidth=2, relief="groove")
        modify_user_btn.place(x=1735, y=325, anchor="center")

        username_lbl = Label(viewer_frame, padx=5, pady=5, text="Username: ", borderwidth=2, relief="groove")
        username_ent = Entry(viewer_frame)

        fn_lbl = Label(viewer_frame, padx=5, pady=5, text="Forename: ", borderwidth=2, relief="groove")
        fn_ent = Entry(viewer_frame)

        sn_lbl = Label(viewer_frame, padx=5, pady=5, text="Surname: ", borderwidth=2, relief="groove")
        sn_ent = Entry(viewer_frame)

        house_num_lbl = Label(viewer_frame, padx=5, pady=5, text="House Number: ", borderwidth=2, relief="groove")
        house_num_ent = Entry(viewer_frame)

        street_lbl = Label(viewer_frame, padx=5, pady=5, text="Street Address: ", borderwidth=2, relief="groove")
        street_ent = Entry(viewer_frame)

        postcode_lbl = Label(viewer_frame, padx=5, pady=5, text="Postcode: ", borderwidth=2, relief="groove")
        postcode_ent = Entry(viewer_frame)

        email_lbl = Label(viewer_frame, padx=5, pady=5, text="Email: ", borderwidth=2, relief="groove")
        email_ent = Entry(viewer_frame)
        email_ent.configure(state="disabled")

        dob_lbl = Label(viewer_frame, padx=5, pady=5, text="Date of Birth: ", borderwidth=2, relief="groove")
        dob_ent = Entry(viewer_frame)
        dob_ent.configure(state="disabled")

        username_lbl.place(x=875, y=45)
        username_ent.place(x=1000, y=50)

        fn_lbl.place(x=875, y=90)
        fn_ent.place(x=1000, y=95)

        sn_lbl.place(x=875, y=135)
        sn_ent.place(x=1000, y=140)

        house_num_lbl.place(x=875, y=190)
        house_num_ent.place(x=1000, y=195)

        street_lbl.place(x=875, y=235)
        street_ent.place(x=1000, y=240)

        postcode_lbl.place(x=875, y=280)
        postcode_ent.place(x=1000, y=285)

        email_lbl.place(x=875, y=325)
        email_ent.place(x=1000, y=330)

        dob_lbl.place(x=875, y=370)
        dob_ent.place(x=1000, y=375)

        user_tree.place(relx=.81, rely=.2, anchor="center")

        user_count = len(user_tree.get_children())
        user_count_lbl = Label(viewer_frame, padx=5, pady=5, text=user_count)
        user_count_lbl.place(x=1725, y=20)

# ======================================================================================================================
        # Loan Tree Setup, with functions to get the title of a selected book and the identifiable data of a selected user.
        # First, the relevant entry box is unlocked and the data is deleted.
        # Then the values of the selected tree item are added to the corresponding entries.
        # Once done, the entries will disable. The process is the same for book and user.
        def get_book():
            l_title_entry["state"] = "normal"
            l_title_entry.delete(0, END)

            # Gets selected tree item.
            selected = book_tree.focus()
            values = book_tree.item(selected, "values")

            # Transfers book tree data to entries.

            l_title_entry.insert(0, values[1])
            l_title_entry["state"] = "disabled"

        # This function will get relevant user details from the user tree
        def get_user():
            l_username_entry["state"] = "normal"
            l_username_entry.delete(0, END)

            l_ufn_entry["state"] = "normal"
            l_ufn_entry.delete(0, END)

            l_usn_entry["state"] = "normal"
            l_usn_entry.delete(0, END)

            l_email_entry["state"] = "normal"
            l_email_entry.delete(0, END)

            # Gets selected tree item.
            selected = user_tree.focus()
            values = user_tree.item(selected, "values")

            # Transfers book tree data to entries.

            l_username_entry.insert(0, values[0])
            l_username_entry["state"] = "disabled"

            l_ufn_entry.insert(0, values[1])
            l_ufn_entry["state"] = "disabled"

            l_usn_entry.insert(0, values[2])
            l_usn_entry["state"] = "disabled"

            l_email_entry.insert(0, values[6])
            l_email_entry["state"] = "disabled"

        # This function should access the book tree item and reduce copies by one.
        def borrow_book():
            borrowed_books.append(l_title_entry.get())
            ccount = int(len(borrowed_books))
            print(borrowed_books)
            loan = Loans(l_username_entry.get(), l_ufn_entry.get(), l_usn_entry.get(), l_email_entry.get(),
                         l_title_entry.get(), ccount, l_cur_date_cal.get_date(), l_due_date_cal.get_date())
            loan_lst = [loan.username, loan.user_fn, loan.user_sn, loan.email, loan.book, loan.count, loan.cur_date,
                        loan.due_date]
            llst.append(loan_lst)
            for item in llst:
                loan_tree.insert(parent="", index="end", iid=ccount, text="", value=item)

            print(llst)
            return loan

        # This function will be called by selecting the book childed to a user and pressing button.
        # Will add one to copies of book in tree.
        def return_book():
            pass

# ======================================================================================================================
        # LOAN TREE
        loan_tree = ttk.Treeview(viewer_frame)
        loan_tree["columns"] = ("Username",
                                "Forename",
                                "Surname",
                                "Email",
                                "Book",
                                "Count",
                                "Current Date",
                                "Due Date")

        # Loan tree headings.
        loan_tree.heading("Username", text="Username")
        loan_tree.heading("Forename", text="Forename")
        loan_tree.heading("Surname", text="Surname")
        loan_tree.heading("Email", text="Email")
        loan_tree.heading("Book", text="Book")
        loan_tree.heading("Count", text="Count")
        loan_tree.heading("Current Date", text="Current Date")
        loan_tree.heading("Due Date", text="Due Date")

        loan_tree.column("#0", width=1)
        loan_tree.column("#1", width=100)
        loan_tree.column("#2", width=100)
        loan_tree.column("#3", width=100)
        loan_tree.column("#4", width=100)
        loan_tree.column("#5", width=100)
        loan_tree.column("#6", width=100)
        loan_tree.column("#7", width=100)

        # Checks loan list for items and adds items and their values to the corresponding columns of the tree.
        # Labels, buttons and entries are defined and placed here.
        count = 0
        for loan in llst:
            loan_tree.insert(parent="", index="end", iid=count, text="", value=loan)
            count += 1

        get_book_btn = Button(viewer_frame, text="Get Book", command=get_book, borderwidth=2, relief="groove")
        get_book_btn.place(x=1075, y=670)

        get_user_btn = Button(viewer_frame, text="Get User", command=get_user, borderwidth=2, relief="groove")
        get_user_btn.place(x=1075, y=740)

        borrow_btn = Button(viewer_frame, text="Borrow Book", command=borrow_book, borderwidth=2, relief="groove")
        borrow_btn.place(x=1062.5, y=810)

        l_title_label = Label(viewer_frame, text="Book Title: ", padx=3, pady=3, borderwidth=2, relief="groove")
        l_title_entry = Entry(viewer_frame)
        l_title_entry.config(state="disabled")

        l_username_label = Label(viewer_frame, text="Username: ", padx=3, pady=3, borderwidth=2, relief="groove")
        l_username_entry = Entry(viewer_frame)
        l_username_entry.config(state="disabled")

        l_ufn_label = Label(viewer_frame, text="User Forename: ", padx=3, pady=3, borderwidth=2, relief="groove")
        l_ufn_entry = Entry(viewer_frame)
        l_ufn_entry.config(state="disabled")

        l_usn_label = Label(viewer_frame, text="User Surname: ", padx=3, pady=3, borderwidth=2, relief="groove")
        l_usn_entry = Entry(viewer_frame)
        l_usn_entry.config(state="disabled")

        l_email_label = Label(viewer_frame, text="Email Address: ", padx=3, pady=3, borderwidth=2, relief="groove")
        l_email_entry = Entry(viewer_frame)
        l_email_entry.config(state="disabled")

        l_bb_label = Label(viewer_frame, text="Books Borrowed: ", padx=3, pady=3, borderwidth=2, relief="groove")
        l_bb_entry = Entry(viewer_frame)
        l_bb_entry.config(state="disabled")

        l_cur_date_label = Label(viewer_frame, text="Current Date", padx=3, pady=3, borderwidth=2, relief="groove")
        l_cur_date_cal = Calendar(viewer_frame, selectmode="none", date_pattern="dd/MM/yyyy")

        l_due_date_label = Label(viewer_frame, text="Due Date", padx=3, pady=3, borderwidth=2, relief="groove")
        l_due_date_cal = Calendar(viewer_frame, selectmode="day", date_pattern="dd/MM/yyyy")

        loan_tree.place(relx=.7, rely=.61, anchor="center")

        l_title_label.place(x=770, y=675)
        l_title_entry.place(x=900, y=680)

        l_username_label.place(x=770, y=705)
        l_username_entry.place(x=900, y=710)

        l_ufn_label.place(x=770, y=735)
        l_ufn_entry.place(x=900, y=740)

        l_usn_label.place(x=770, y=765)
        l_usn_entry.place(x=900, y=770)

        l_email_label.place(x=770, y=795)
        l_email_entry.place(x=900, y=800)

        l_bb_label.place(x=770, y=825)
        l_bb_entry.place(x=900, y=830)

        l_cur_date_label.place(x=1240, y=665)
        l_cur_date_cal.place(x=1160, y=710)

        l_due_date_label.place(x=1550, y=665)
        l_due_date_cal.place(x=1460, y=710)

# ======================================================================================================================

    make_trees()
    viewer_frame.pack_propagate(False)
    viewer_frame.place(relx=.5, rely=.5, anchor="center")


# Brings the program to life
welcome_page()

# Needed to run GUI
root.mainloop()
