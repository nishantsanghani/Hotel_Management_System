from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox


class Report:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("1295x550+230+220")

        # ===== Variables =====
        self.total_customer = StringVar()
        self.total_rooms = StringVar()
        self.booked_rooms = StringVar()
        self.available_rooms = StringVar()

        self.var_gender = StringVar()
        self.var_nationality = StringVar()
        self.var_idproof = StringVar()
        self.var_roomtype = StringVar()

        # ===== Title =====
        lbl_title = Label(
            self.root,
            text="CUSTOMER BOOKING REPORT",
            font=("times new roman", 18, "bold"),
            bg="black",
            fg="gold",
            bd=4,
            relief=RIDGE
        )
        lbl_title.place(x=0, y=0, width=1295, height=50)

        # ================= LEFT SUMMARY FRAME =================
        summary_frame = LabelFrame(
            self.root,
            text="Hotel Summary",
            font=("times new roman", 12, "bold"),
            bd=4,
            relief=RIDGE
        )
        summary_frame.place(x=0, y=50, width=300, height=500)

        Label(summary_frame, text="Total Customers",
              font=("arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=15)

        Label(summary_frame, textvariable=self.total_customer,
              font=("arial", 12, "bold"), fg="blue").grid(row=0, column=1)

        Label(summary_frame, text="Total Rooms",
              font=("arial", 12, "bold")).grid(row=1, column=0, padx=10, pady=15)

        Label(summary_frame, textvariable=self.total_rooms,
              font=("arial", 12, "bold"), fg="blue").grid(row=1, column=1)

        Label(summary_frame, text="Booked Rooms",
              font=("arial", 12, "bold")).grid(row=2, column=0, padx=10, pady=15)

        Label(summary_frame, textvariable=self.booked_rooms,
              font=("arial", 12, "bold"), fg="red").grid(row=2, column=1)

        Label(summary_frame, text="Available Rooms",
              font=("arial", 12, "bold")).grid(row=3, column=0, padx=10, pady=15)

        Label(summary_frame, textvariable=self.available_rooms,
              font=("arial", 12, "bold"), fg="green").grid(row=3, column=1)

        # ================= FILTER SECTION =================

        Label(summary_frame, text="Gender",
              font=("arial", 11, "bold")).grid(row=4, column=0, pady=10)

        self.gender_combo = ttk.Combobox(summary_frame,
                                         textvariable=self.var_gender,
                                         state="readonly",
                                         width=18)
        self.gender_combo.grid(row=4, column=1)
        self.gender_combo.bind("<<ComboboxSelected>>", self.apply_filter)

        Label(summary_frame, text="Nationality",
              font=("arial", 11, "bold")).grid(row=5, column=0, pady=10)

        self.nationality_combo = ttk.Combobox(summary_frame,
                                              textvariable=self.var_nationality,
                                              state="readonly",
                                              width=18)
        self.nationality_combo.grid(row=5, column=1)
        self.nationality_combo.bind("<<ComboboxSelected>>", self.apply_filter)

        Label(summary_frame, text="ID Proof",
              font=("arial", 11, "bold")).grid(row=6, column=0, pady=10)

        self.idproof_combo = ttk.Combobox(summary_frame,
                                          textvariable=self.var_idproof,
                                          state="readonly",
                                          width=18)
        self.idproof_combo.grid(row=6, column=1)
        self.idproof_combo.bind("<<ComboboxSelected>>", self.apply_filter)

        Label(summary_frame, text="Room Type",
              font=("arial", 11, "bold")).grid(row=7, column=0, pady=10)

        self.roomtype_combo = ttk.Combobox(summary_frame,
                                           textvariable=self.var_roomtype,
                                           state="readonly",
                                           width=18)
        self.roomtype_combo.grid(row=7, column=1)
        self.roomtype_combo.bind("<<ComboboxSelected>>", self.apply_filter)

        # ================= RIGHT TABLE FRAME =================
        table_frame = Frame(self.root, bd=4, relief=RIDGE)
        table_frame.place(x=300, y=50, width=995, height=500)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.report_table = ttk.Treeview(
            table_frame,
            columns=(
                "ref","name","mother","gender","mobile","email",
                "nationality","idproof","idnumber","address",
                "room","roomtype","meal","checkin","checkout","days"
            ),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.report_table.xview)
        scroll_y.config(command=self.report_table.yview)

        headings = [
            ("ref","Ref"),
            ("name","Name"),
            ("mother","Mother"),
            ("gender","Gender"),
            ("mobile","Mobile"),
            ("email","Email"),
            ("nationality","Nationality"),
            ("idproof","ID Proof"),
            ("idnumber","ID Number"),
            ("address","Address"),
            ("room","Room No"),
            ("roomtype","Room Type"),
            ("meal","Meal"),
            ("checkin","Check In"),
            ("checkout","Check Out"),
            ("days","Days")
        ]

        for col,text in headings:
            self.report_table.heading(col,text=text)
            self.report_table.column(col,width=120)

        self.report_table["show"] = "headings"
        self.report_table.pack(fill=BOTH, expand=1)

        # ===== Load Data =====
        self.fetch_data()
        self.load_summary()
        self.load_filters()

    # ===== Fetch Report Data =====
    def fetch_data(self):

        conn = mysql.connector.connect(
            host="localhost",
            username="root",
            password="Nishant",
            database="management"
        )

        cursor = conn.cursor()

        query = """
        SELECT 
            c.Ref,
            c.Name,
            c.Mother,
            c.Gender,
            c.Mobile,
            c.Email,
            c.Nationality,
            c.Idproof,
            c.Idnumber,
            c.Address,
            r.Room,
            r.roomtype,
            r.meal,
            r.check_in,
            r.check_out,
            r.noOfdays
        FROM customer c
        LEFT JOIN room r
        ON c.Mobile = r.Contact
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        self.report_table.delete(*self.report_table.get_children())

        for row in rows:
            self.report_table.insert("", END, values=row)

        conn.close()

    # ===== Hotel Summary =====
    def load_summary(self):

        conn = mysql.connector.connect(
            host="localhost",
            username="root",
            password="Nishant",
            database="management"
        )

        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM customer")
        self.total_customer.set(cursor.fetchone()[0])

        cursor.execute("SELECT COUNT(*) FROM details")
        total_rooms = cursor.fetchone()[0]
        self.total_rooms.set(total_rooms)

        cursor.execute("SELECT COUNT(*) FROM room")
        booked = cursor.fetchone()[0]
        self.booked_rooms.set(booked)

        self.available_rooms.set(total_rooms - booked)

        conn.close()

    # ===== Load Filters =====
    def load_filters(self):

        conn = mysql.connector.connect(
            host="localhost",
            username="root",
            password="Nishant",
            database="management"
        )

        cursor = conn.cursor()

        # Gender
        cursor.execute("SELECT Gender, COUNT(*) FROM customer GROUP BY Gender")
        data = cursor.fetchall()

        gender_list = ["All"]
        for g in data:
            gender_list.append(f"{g[0]} ({g[1]})")

        self.gender_combo["values"] = gender_list
        self.gender_combo.current(0)


        # Nationality
        cursor.execute("SELECT Nationality, COUNT(*) FROM customer GROUP BY Nationality")
        data = cursor.fetchall()

        nat_list = ["All"]
        for n in data:
            nat_list.append(f"{n[0]} ({n[1]})")

        self.nationality_combo["values"] = nat_list
        self.nationality_combo.current(0)


        # ID Proof
        cursor.execute("SELECT Idproof, COUNT(*) FROM customer GROUP BY Idproof")
        data = cursor.fetchall()

        id_list = ["All"]
        for i in data:
            id_list.append(f"{i[0]} ({i[1]})")

        self.idproof_combo["values"] = id_list
        self.idproof_combo.current(0)


        # Room Type
        cursor.execute("SELECT roomtype, COUNT(*) FROM room GROUP BY roomtype")
        data = cursor.fetchall()

        room_list = ["All"]
        for r in data:
            room_list.append(f"{r[0]} ({r[1]})")

        self.roomtype_combo["values"] = room_list
        self.roomtype_combo.current(0)

        conn.close()

    # ===== Apply Filter =====
    def apply_filter(self, event=""):

        gender = self.var_gender.get()
        nationality = self.var_nationality.get()
        idproof = self.var_idproof.get()
        roomtype = self.var_roomtype.get()

        # Remove count part (Male (2) -> Male)
        if "(" in gender:
            gender = gender.split("(")[0].strip()

        if "(" in nationality:
            nationality = nationality.split("(")[0].strip()

        if "(" in idproof:
            idproof = idproof.split("(")[0].strip()

        if "(" in roomtype:
            roomtype = roomtype.split("(")[0].strip()

        query = """
        SELECT 
            c.Ref,c.Name,c.Mother,c.Gender,c.Mobile,c.Email,
            c.Nationality,c.Idproof,c.Idnumber,c.Address,
            r.Room,r.roomtype,r.meal,r.check_in,r.check_out,r.noOfdays
        FROM customer c
        LEFT JOIN room r
        ON c.Mobile = r.Contact
        WHERE 1=1
        """

        params = []

        if gender != "All":
            query += " AND c.Gender=%s"
            params.append(gender)

        if nationality != "All":
            query += " AND c.Nationality=%s"
            params.append(nationality)

        if idproof != "All":
            query += " AND c.Idproof=%s"
            params.append(idproof)

        if roomtype != "All":
            query += " AND r.roomtype=%s"
            params.append(roomtype)

        conn = mysql.connector.connect(
            host="localhost",
            username="root",
            password="Nishant",
            database="management"
        )

        cursor = conn.cursor()
        cursor.execute(query, params)

        rows = cursor.fetchall()

        self.report_table.delete(*self.report_table.get_children())

        for row in rows:
            self.report_table.insert("", END, values=row)

        conn.close()
        
        
    