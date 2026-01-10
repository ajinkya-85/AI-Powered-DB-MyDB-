import customtkinter as ctk
from QueryGenerator import QueryGenerator
from DB_operation import DBOperation
from searching import find_databases
from ui_panels import LeftPanel, RightPanel
from ui_dialogs import DialogManager
from config_manager import ConfigManager
import threading
from typing import List, Union
import os
from tkinter import filedialog
import tkinter
import csv

class DatabaseUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Theme settings
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        # Window setup
        self.title("MyDB Manager")
        width = 1000
        height = 785
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.configure(fg_color=("#FFFFFF", "#1e1e1e"))
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create PanedWindow for adjustable layout
        self.paned_window = tkinter.PanedWindow(self, orient=tkinter.HORIZONTAL, sashwidth=4, bg="#1e1e1e", bd=0, sashrelief="flat", opaqueresize=False, proxybackground="#007acc")
        self.paned_window.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Initialize Managers
        self.dialog_manager = DialogManager(self)
        self.config_manager = ConfigManager()
        
        # Initialize components
        self.create_ui_components()
        
        # Store current query
        self.current_query = ""
        
        # Load configuration
        self.load_config()
        
        # Data storage for export
        self.last_headers = None
        self.last_data = None
        
        # Check for first run
        if self.first_run:
            self.after(200, self.dialog_manager.show_about)
            self.config_manager.update("first_run", False)

    def create_ui_components(self):
        # Left Panel Callbacks
        left_callbacks = {
            'nav_click': self.handle_nav_click,
            'scan_db': self.scan_databases,
            'scan_folder': self.scan_specific_folder,
            'generate': self.handle_generate_query,
            'execute': self.handle_execute_query
        }
        self.left_panel = LeftPanel(self.paned_window, callbacks=left_callbacks, fg_color=("#F7F7F8", "#252526"), corner_radius=0, bg_color=("#FFFFFF", "#1e1e1e"))
        self.paned_window.add(self.left_panel, minsize=300, width=320, padx=5, pady=5, stretch="always")
        
        # Right Panel Callbacks
        right_callbacks = {
            'scan_tables': self.scan_tables,
            'show_table': self.show_table,
            'export': self.export_to_csv
        }
        self.right_panel = RightPanel(self.paned_window, callbacks=right_callbacks, fg_color=("#FFFFFF", "#1e1e1e"), corner_radius=0, bg_color=("#FFFFFF", "#1e1e1e"))
        self.paned_window.add(self.right_panel, minsize=500, padx=5, pady=5, stretch="always")
    
    def show_table(self):
        table_name = self.right_panel.table_combo.get().strip()
        if not table_name:
            self.dialog_manager.show_error("Please enter a table name")
            return
            
        selected_db = self.left_panel.db_combo.get()
        
        def table_task():
            try:
                db = DBOperation(selected_db)
                columns, rows = db.get_table_data(table_name)
                self.after(0, self.display_table_data, columns, rows)
            except Exception as e:
                self.after(0, self.dialog_manager.show_error, f"Failed to show table: {str(e)}")
                
        threading.Thread(target=table_task, daemon=True).start()
    
    def display_table_data(self, columns: list, rows: list):
        self.last_headers = columns
        self.last_data = rows
        
        self.right_panel.results_display.configure(state="normal")
        self.right_panel.results_display.delete("1.0", "end")
        
        # Calculate column widths
        col_widths = [len(str(col)) for col in columns]
        for row in rows:
            for i, val in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(val)))
        
        # Add padding for better readability
        col_widths = [w + 2 for w in col_widths]
                
        # Display column headers
        header = " | ".join(str(col).ljust(col_widths[i]) for i, col in enumerate(columns))
        separator = "-+-".join("-" * width for width in col_widths)
        
        self.right_panel.results_display.insert("end", header + "\n")
        self.right_panel.results_display.insert("end", separator + "\n")
        
        # Display rows with proper alignment
        for row in rows:
            row_text = " | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row))
            self.right_panel.results_display.insert("end", row_text + "\n")
        self.right_panel.results_display.configure(state="disabled")

    def format_results_table(self, results: List) -> str:
        if not results:
            return "No results found"
            
        # Calculate column widths for all data
        col_count = len(results[0])
        col_widths = [0] * col_count
        
        for row in results:
            for i, val in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(val)))
                
        # Add padding for better readability
        col_widths = [w + 2 for w in col_widths]
                
        # Format as aligned table
        output = []
        for row in results:
            formatted_row = " | ".join(str(item).ljust(col_widths[i]) for i, item in enumerate(row))
            output.append(formatted_row)
                
        return "\n".join(output)

    def animate_generation(self, step):
        if not getattr(self, 'is_generating', False):
            return
            
        dots = "." * (step % 4)
        text = f"Generating SQL Query{dots}"
        self.left_panel.sql_output.delete("1.0", "end")
        self.left_panel.sql_output.insert("1.0", text)
        self.after(500, self.animate_generation, step + 1)

    def handle_generate_query(self):
        prompt = self.left_panel.prompt_input.get("1.0", "end-1c").strip()
        if not prompt:
            self.dialog_manager.show_error("Please enter a query prompt")
            return
            
        self.is_generating = True
        self.animate_generation(0)
            
        def generation_task():
            try:
                qg = QueryGenerator(self.left_panel.model_var.get())
                qg.set_user_input(prompt)
                sql_query = qg.get_response()
                self.current_query = sql_query
                self.is_generating = False
                self.after(0, self.update_sql_display, sql_query)
            except Exception as e:
                self.is_generating = False
                self.after(0, self.dialog_manager.show_error, f"Query generation failed: {str(e)}")
                
        threading.Thread(target=generation_task, daemon=True).start()
        
    def handle_execute_query(self):
        if not self.current_query.strip():
            self.dialog_manager.show_error("No SQL query to execute")
            return
            
        selected_db = self.left_panel.db_combo.get()
        
        def execution_task():
            try:
                db = DBOperation(selected_db)
                results = db.execute_query(self.current_query)
                self.after(0, self.update_results_display, results)
            except Exception as e:
                self.after(0, self.dialog_manager.show_error, f"Query execution failed: {str(e)}")
                
        threading.Thread(target=execution_task, daemon=True).start()
        
    def update_sql_display(self, query: str):
        self.left_panel.sql_output.delete("1.0", "end")
        self.left_panel.sql_output.insert("1.0", query)
        
    def update_results_display(self, results: Union[tuple, str]):
        if isinstance(results, tuple):
            columns, rows = results
            self.display_table_data(columns, rows)
        else:
            self.right_panel.results_display.configure(state="normal")
            self.right_panel.results_display.delete("1.0", "end")
            self.right_panel.results_display.insert("1.0", str(results))
            self.right_panel.results_display.configure(state="disabled")
            self.last_headers = None
            self.last_data = None

    def scan_databases(self):
        self.left_panel.scan_btn.configure(state="disabled", text="Scanning...")
        
        def scan_task():
            try:
                dbs = find_databases()
                # Use full paths so DBOperation can find them
                db_paths = [str(p) for p in dbs]
                
                def update_ui():
                    self.left_panel.scan_btn.configure(state="normal", text="Scan for Databases")
                    if db_paths:
                        self.left_panel.db_combo.configure(values=db_paths)
                        self.left_panel.db_combo.set(db_paths[0])
                    else:
                        self.dialog_manager.show_error("No databases found on this PC")
                
                self.after(0, update_ui)
            except Exception as e:
                self.after(0, lambda: self.left_panel.scan_btn.configure(state="normal", text="Scan for Databases"))
                self.after(0, self.dialog_manager.show_error, f"Scan failed: {str(e)}")
        
        threading.Thread(target=scan_task, daemon=True).start()

    def scan_specific_folder(self):
        folder_path = filedialog.askdirectory()
        if not folder_path:
            return
            
        self.left_panel.folder_btn.configure(state="disabled", text="Scanning...")
        
        def scan_task():
            try:
                db_paths = []
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        if file.lower().endswith(('.db', '.sqlite', '.sqlite3')):
                            db_paths.append(os.path.join(root, file))
                
                def update_ui():
                    self.left_panel.folder_btn.configure(state="normal", text="Folder")
                    if db_paths:
                        self.left_panel.db_combo.configure(values=db_paths)
                        self.left_panel.db_combo.set(db_paths[0])
                    else:
                        self.dialog_manager.show_error("No databases found in selected folder")
                
                self.after(0, update_ui)
            except Exception as e:
                self.after(0, lambda: self.left_panel.folder_btn.configure(state="normal", text="Folder"))
                self.after(0, self.dialog_manager.show_error, f"Scan failed: {str(e)}")
        
        threading.Thread(target=scan_task, daemon=True).start()
            
    def scan_tables(self):
        selected_db = self.left_panel.db_combo.get()
        if not selected_db:
            self.dialog_manager.show_error("Please select a database first")
            return
            
        def scan_task():
            try:
                db = DBOperation(selected_db)
                tables = db.get_all_tables()
                
                def update_ui():
                    self.right_panel.table_combo.configure(values=tables)
                    if tables:
                        self.right_panel.table_combo.set(tables[0])
                    else:
                        self.right_panel.table_combo.set("")
                        self.dialog_manager.show_error("No tables found in selected database")
                
                self.after(0, update_ui)
            except Exception as e:
                self.after(0, self.dialog_manager.show_error, f"Failed to scan tables: {str(e)}")
        
        threading.Thread(target=scan_task, daemon=True).start()
        
    def export_to_csv(self):
        if not self.last_data:
            self.dialog_manager.show_error("No data to export")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    if self.last_headers:
                        writer.writerow(self.last_headers)
                    writer.writerows(self.last_data)
                self.dialog_manager.show_info("Export successful!")
            except Exception as e:
                self.dialog_manager.show_error(f"Export failed: {str(e)}")

    def toggle_theme(self):
        current_mode = ctk.get_appearance_mode()
        new_mode = "Light" if current_mode == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)
        
        new_bg = "#FFFFFF" if new_mode == "Light" else "#1e1e1e"
        new_proxy = "#000000" if new_mode == "Light" else "#007acc"
        self.paned_window.configure(bg=new_bg, proxybackground=new_proxy)

    def handle_nav_click(self, option):
        if option == "Theme":
            self.toggle_theme()
        elif option == "About":
            self.dialog_manager.show_about()
        elif option == "API Key":
            self.show_api_key_dialog_wrapper()

    def load_config(self):
        if "key" in os.environ:
            del os.environ["key"]
            
        self.first_run = True
        
        config = self.config_manager.load()
        if "api_key" in config and config["api_key"]:
            os.environ["key"] = config["api_key"]
        if "first_run" in config:
            self.first_run = config["first_run"]

    def show_api_key_dialog_wrapper(self):
        current_key = os.environ.get("key", "")
        
        def save_callback(key, dialog):
            if not key:
                self.dialog_manager.show_error("Please enter a valid API key")
                return False
            os.environ["key"] = key
            try:
                self.config_manager.update("api_key", key)
            except Exception as e:
                self.dialog_manager.show_error(f"Failed to save config: {e}")
                return False
            dialog.destroy()
            self.dialog_manager.show_info("API Key saved for this session")
            return True
            
        self.dialog_manager.show_api_key(current_key, save_callback)

if __name__ == "__main__":
    app = DatabaseUI()
    app.mainloop()