#Import all the needed modules
import pyodbc
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class Truncat0rApp:

    #Initialize object and its attributes
    def __init__(self, root):
        self.connection = None
        self.tables = []
        self.tab_rows = []
        self.count = 0
        self.current_DB = ""
        self.current_dbname = ""
        self.create_widgets(root)

    #GUI layout
    def create_widgets(self, root):
        root.title("Truncat0r (v1.0)")
        root.geometry("450x500")
        root.resizable(False, False)
        
        #Close window event
        root.protocol("WM_DELETE_WINDOW", self.close)

        #Buttons
        self.header0 = tk.Label(root, text="1. Inserisci il nome del DB sul quale vuoi operare:")
        self.header0.pack(pady=5, anchor=tk.CENTER)

        self.field_frame = tk.Frame(root)
        self.field_frame.pack(pady=5, anchor=tk.CENTER)

        self.dbname_field = tk.Entry(self.field_frame, width=14)
        self.dbname_field.pack(padx=5, side=tk.LEFT)

        self.header1 = tk.Label(root, text="2. Inserisci l'indirizzo IP:")
        self.header1.pack(pady=5, anchor=tk.CENTER)

        self.entry_field = tk.Entry(root, width=14)
        self.entry_field.pack(anchor=tk.CENTER, pady=5)

        self.connect_button = tk.Button(root, text="Connettiti al DB", command=self.connect_to_db)
        self.connect_button.pack(anchor=tk.CENTER)

        self.header2 = tk.Label(root, text="3. Elimina le righe delle tabelle.")
        self.header2.pack(pady=5, anchor=tk.CENTER)

        self.truncate_button = tk.Button(root, text="Tronca le tabelle", command=self.truncate_table)
        self.truncate_button.pack(anchor=tk.CENTER)

        self.header3 = tk.Label(root, text="4. Termina la connessione.")
        self.header3.pack(pady=5, anchor=tk.CENTER)

        self.disconnect_button = tk.Button(root, text="Disconnettiti dal DB", command=self.disconnect)
        self.disconnect_button.pack(anchor=tk.CENTER)

        #Log
        self.log_box = tk.Frame(root, width=100, height=100, bg='white')
        self.log_box.pack(pady=5, anchor=tk.CENTER)

        self.scrollbar = tk.Scrollbar(self.log_box)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.log_text = tk.Text(self.log_box, wrap=tk.WORD, height=15, width=55, state=tk.DISABLED, yscrollcommand=self.scrollbar.set)
        self.log_text.pack()

        self.scrollbar.config(command=self.log_text.yview)

    #Retrieve and validate dbname and IP from input
    def get_entry(self):
        entry = self.entry_field.get()
        if len(entry) > 15:
            messagebox.showerror("Errore", "Inserisci un indirizzo IP corretto.")
            return 1
        else:
            return entry
    
    def get_dbname(self):
        dbname = self.dbname_field.get()
        return dbname

    #Connect to the specified DB
    def connect_to_db(self):
        if self.connection:
            messagebox.showerror("Errore", f"Sei già connesso al DB {self.current_dbname}.")
            return
        
        entry = self.get_entry()
        if not entry:
            messagebox.showerror("Errore", "Inserisci un indirizzo IP corretto.")
            return
        
        dbname = self.get_dbname()
        if not dbname:
            messagebox.showerror("Errore", "Inserisci un nome corretto.")
            return
        
        #This works for PostgreSQL only, change the params accordingly to your DB
        try:
            connection_string = (
                "DRIVER={PostgreSQL ODBC Driver(UNICODE)};"
                f"DATABASE={dbname};"
                f"SERVER={entry};"
                "PORT=5432;"
                "UID=postgres;"
                "PWD=password;"
            )
            self.connection = pyodbc.connect(connection_string)
            self.count += 1
            current_time = datetime.now().strftime("%H:%M:%S")
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, f"{self.count}# [{current_time}] - Connessione stabilita col DB {dbname}.\n")
            self.log_text.config(state=tk.DISABLED)
            self.log_text.yview_moveto(1.0)
            self.connection.autocommit = False
            self.connection.commit()
            self.current_dbname = dbname
            self.current_DB = entry
            self.fetch_data()
        except Exception as e:
            messagebox.showerror("Errore", f"Connessione al DB fallita: {e}")

    #Retrieve all the specified type of tables in the DB and their rows
    def fetch_data(self):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name LIKE '%sample%'")
                self.connection.commit()
                self.tables = [row[0] for row in cursor.fetchall()]
                for tab in self.tables:
                    self.count += 1
                    current_time = datetime.now().strftime("%H:%M:%S")
                    self.log_text.config(state=tk.NORMAL)
                    self.log_text.insert(tk.END, f"{self.count}# [{current_time}] - Recuperata la tabella {tab}.\n")
                    self.log_text.config(state=tk.DISABLED)
                    self.log_text.yview_moveto(1.0)

                    cursor.execute(f"SELECT COUNT(*) FROM {tab}")
                    self.connection.commit()
                    rows = cursor.fetchone()[0]
                    current_time = datetime.now().strftime("%H:%M:%S")
                    self.log_text.config(state=tk.NORMAL)
                    self.log_text.insert(tk.END, f"{self.count}# [{current_time}] - Numero di righe: {rows}.\n")
                    self.log_text.config(state=tk.DISABLED)
                    self.log_text.yview_moveto(1.0)

            except Exception as e:
                messagebox.showerror("Errore", f"Connessione al DB fallita: {e}")

    #Launch SQL query to truncate the tables
    def truncate_table(self):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                for table in self.tables:
                    cursor.execute(f"TRUNCATE TABLE {table}")
                    self.connection.commit()
                    self.count += 1
                    current_time = datetime.now().strftime("%H:%M:%S")
                    self.log_text.config(state=tk.NORMAL)
                    self.log_text.insert(tk.END, f"{self.count}# [{current_time}] - Troncata la tabella {table}.\n")
                    self.log_text.config(state=tk.DISABLED)
                    self.log_text.yview_moveto(1.0)
            except Exception as e:
                messagebox.showerror("Errore", f"{e}")
        else:
            messagebox.showerror("Errore", "Non sei connesso ad alcun DB.")

    #Disconnect from the DB
    def disconnect(self):
        if self.connection:
            try:
                self.connection.commit()
                self.connection.close()
                self.connection = None
                self.tables.clear()
                self.count += 1
                current_time = datetime.now().strftime("%H:%M:%S")
                self.log_text.config(state=tk.NORMAL)
                self.log_text.insert(tk.END, f"{self.count}# [{current_time}] - Connessione terminata col DB {self.current_dbname}.\n")
                self.log_text.config(state=tk.DISABLED)
                self.log_text.yview_moveto(1.0)
            except Exception as e:
                messagebox.showerror("Errore", f"{e}")
        else:
            messagebox.showerror("Errore", "Non sei connesso ad alcun DB.")

    #Close window event
    def close(self):
        if self.connection:
            self.connection.commit()
            self.connection.close()
        root.destroy()

#GUI window loop
root = tk.Tk()
app = Truncat0rApp(root)
root.mainloop()