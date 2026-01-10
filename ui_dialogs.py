import customtkinter as ctk

class DialogManager:
    def __init__(self, parent):
        self.parent = parent

    def center_popup(self, popup, width, height):
        self.parent.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (width // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")

    def show_info(self, message):
        info_window = ctk.CTkToplevel(self.parent)
        info_window.title("Info")
        self.center_popup(info_window, 300, 150)
        info_window.transient(self.parent)
        info_window.grab_set()
        info_window.lift()
        
        label = ctk.CTkLabel(info_window, text=message, wraplength=250)
        label.pack(pady=20, padx=20)
        
        ok_btn = ctk.CTkButton(info_window, text="OK", command=info_window.destroy, width=100)
        ok_btn.pack(pady=10)

    def show_error(self, message):
        error_window = ctk.CTkToplevel(self.parent)
        error_window.title("Error")
        self.center_popup(error_window, 400, 200)
        error_window.transient(self.parent)
        error_window.grab_set()
        error_window.lift()
        
        label = ctk.CTkLabel(error_window, text=message, wraplength=350)
        label.pack(pady=20, padx=20)
        
        ok_btn = ctk.CTkButton(error_window, text="OK", command=error_window.destroy, width=100)
        ok_btn.pack(pady=20)

    def show_about(self):
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("About MyDB Manager")
        self.center_popup(dialog, 600, 500)
        dialog.transient(self.parent)
        dialog.grab_set()
        dialog.lift()
        
        ctk.CTkLabel(dialog, text="MyDB Manager", font=("Arial", 20, "bold")).pack(pady=(20, 5))
        ctk.CTkLabel(dialog, text="AI-Powered Database Assistant", font=("Arial", 14)).pack(pady=(0, 15))
        
        info_text = """VERSION INFORMATION:
• Version: 1.0.0
• Build: Stable Release

FEATURES:
• Database Scanning: Automatically find SQLite databases on your PC or in specific folders.
• AI Query Generation: Describe your data needs in plain English, and Gemini will write the SQL.
• SQL Execution: Run queries safely and view results in a grid.
• Data Management: View table schemas, browse data, and export results to CSV.
• Theme Support: Switch between Dark and Light modes.

HOW TO GET A GEMINI API KEY:
1. Visit Google AI Studio (aistudio.google.com).
2. Sign in and click "Get API key" on the left.
3. Click "Create API key" and copy the string.

HOW TO USE THE KEY:
1. Click the "API Key" button in this app's navigation bar.
2. Paste your key and click "Save Key".
3. The key is saved locally for future sessions."""

        textbox = ctk.CTkTextbox(dialog, width=540, height=320, wrap="word")
        textbox.pack(padx=20, pady=10)
        textbox.insert("1.0", info_text)
        textbox.configure(state="disabled")
        
        ctk.CTkButton(dialog, text="Close", command=dialog.destroy).pack(pady=20)

    def show_api_key(self, current_key, save_callback):
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("API Key Setup")
        self.center_popup(dialog, 400, 220)
        dialog.transient(self.parent)
        dialog.grab_set()
        dialog.lift()
        
        label = ctk.CTkLabel(dialog, text="Enter Google Gemini API Key:", font=("Arial", 14))
        label.pack(pady=(20, 10), padx=20)
        
        entry = ctk.CTkEntry(dialog, width=320, show="*")
        entry.pack(pady=10, padx=20)
        
        if current_key:
            entry.insert(0, current_key)
            
        def on_save():
            key = entry.get().strip()
            save_callback(key, dialog)
            
        save_btn = ctk.CTkButton(dialog, text="Save Key", command=on_save)
        save_btn.pack(pady=20)