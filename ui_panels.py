import customtkinter as ctk

class LeftPanel(ctk.CTkFrame):
    def __init__(self, parent, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.callbacks = callbacks
        self.create_widgets()

    def create_widgets(self):
        # Navigation Bar
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        for option in ["About", "Theme", "API Key"]:
            btn = ctk.CTkButton(
                nav_frame,
                text=option,
                width=50,
                height=25,
                fg_color=("#ECECF1", "#3c3c3c"),
                text_color=("#343541", "#FFFFFF"),
                hover_color=("#D9D9E3", "#4c4c4c"),
                command=lambda opt=option: self.callbacks['nav_click'](opt)
            )
            btn.pack(side="left", padx=2, expand=True, fill="x")
            
        # Model Dropdown
        self.model_var = ctk.StringVar(value="gemini-2.5-flash")
        self.model_dropdown = ctk.CTkOptionMenu(
            nav_frame,
            values=[
                "gemini-2.5-pro",
                "gemini-2.5-flash",
                "gemini-2.5-flash-lite",
                "gemini-2.5-flash-live",
                "gemini-2.5-flash-native-audio",
                "gemini-2.5-flash-image-preview",
                "gemini-2.5-flash-preview-text-to-speech",
                "gemini-2.5-pro-preview-text-to-speech",
                "gemini-2.0-flash",
                "gemini-2.0-flash-preview-image-generation",
                "gemini-2.0-flash-lite",
                "gemini-2.0-flash-live",
                "gemini-1.5-flash",
                "gemini-1.5-flash-8b",
                "gemini-1.5-pro"
            ],
            variable=self.model_var,
            width=100,
            height=25,
            fg_color=("#ECECF1", "#3c3c3c"),
            button_color=("#ECECF1", "#3c3c3c"),
            button_hover_color=("#D9D9E3", "#4c4c4c"),
            text_color=("#343541", "#FFFFFF"),
            dropdown_fg_color=("#FFFFFF", "#252526"),
            dropdown_text_color=("#343541", "#FFFFFF")
        )
        self.model_dropdown.pack(side="left", padx=2, expand=True, fill="x")
            
        # Database Selection
        db_label = ctk.CTkLabel(self, text="Select Database", font=("Arial", 16, "bold"))
        db_label.pack(pady=(20,5))
        
        self.db_combo = ctk.CTkComboBox(
            self, 
            values=[],
            fg_color=("#FFFFFF", "#3c3c3c"),
            button_color=("#ECECF1", "#4c4c4c"),
            border_color=("#ECECF1", "#3c3c3c"),
            dropdown_fg_color=("#FFFFFF", "#252526")
        )
        self.db_combo.set("")
        self.db_combo.pack(pady=5, padx=20, fill="x")
        
        # Scan buttons frame
        scan_frame = ctk.CTkFrame(self, fg_color="transparent")
        scan_frame.pack(pady=10, padx=20, fill="x")

        self.scan_btn = ctk.CTkButton(
            scan_frame,
            text="Scan for Databases",
            command=self.callbacks['scan_db'],
            fg_color=("#ECECF1", "#3c3c3c"),
            hover_color=("#D9D9E3", "#4c4c4c"),
            text_color=("#343541", "#FFFFFF")
        )
        self.scan_btn.pack(side="left", padx=(0, 5), expand=True, fill="x")
        
        self.folder_btn = ctk.CTkButton(
            scan_frame,
            text="Folder",
            command=self.callbacks['scan_folder'],
            fg_color=("#ECECF1", "#3c3c3c"),
            hover_color=("#D9D9E3", "#4c4c4c"),
            text_color=("#343541", "#FFFFFF")
        )
        self.folder_btn.pack(side="right", padx=(5, 0), expand=True, fill="x")
        
        # Prompt input
        prompt_label = ctk.CTkLabel(self, text="Enter Your Natural Language Prompt", font=("Arial", 16, "bold"))
        prompt_label.pack(pady=(20,5))
        
        self.prompt_input = ctk.CTkTextbox(self, height=100, fg_color=("#FFFFFF", "#3c3c3c"), text_color=("#343541", "#cccccc"), border_width=1, border_color=("#ECECF1", "#3c3c3c"))
        self.prompt_input.pack(pady=10, padx=20, fill="x")
        
        # Generate button
        generate_btn = ctk.CTkButton(self, text="Generate SQL Query", command=self.callbacks['generate'], fg_color=("#000000", "#007acc"), hover_color=("#333333", "#0062a3"), height=40)
        generate_btn.pack(pady=10, padx=20, fill="x")
        
        # Generated SQL section
        sql_label = ctk.CTkLabel(self, text="Generated SQL Query", font=("Arial", 16, "bold"))
        sql_label.pack(pady=(20,5))
        
        self.sql_output = ctk.CTkTextbox(self, height=200, fg_color=("#ECECF1", "#1e1e1e"), text_color=("#343541", "#cccccc"))
        self.sql_output.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Execute button
        execute_btn = ctk.CTkButton(self, text="Execute SQL Query", command=self.callbacks['execute'], fg_color=("#10a37f", "#388a34"), hover_color=("#0d8a6a", "#2b6a28"), height=40)
        execute_btn.pack(pady=10, padx=20, fill="x")

class RightPanel(ctk.CTkFrame):
    def __init__(self, parent, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.callbacks = callbacks
        self.create_widgets()
        
    def create_widgets(self):
        # Results section
        results_label = ctk.CTkLabel(self, text="Query Results / Table View", font=("Arial", 16, "bold"))
        results_label.pack(pady=(20,5))
        
        self.results_display = ctk.CTkTextbox(self, font=("Consolas", 12), wrap="none", state="disabled", fg_color=("#FFFFFF", "#1e1e1e"), text_color=("#343541", "#cccccc"))
        self.results_display.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Table Selection
        table_label = ctk.CTkLabel(self, text="Select Table", font=("Arial", 16, "bold"))
        table_label.pack(pady=(20,5))
        
        self.table_combo = ctk.CTkComboBox(self, values=[], fg_color=("#FFFFFF", "#3c3c3c"), button_color=("#ECECF1", "#4c4c4c"), border_color=("#ECECF1", "#3c3c3c"), dropdown_fg_color=("#FFFFFF", "#252526"))
        self.table_combo.set("")
        self.table_combo.pack(pady=5, padx=20, fill="x")
        
        table_actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        table_actions_frame.pack(pady=10, padx=20, fill="x")
        
        scan_table_btn = ctk.CTkButton(table_actions_frame, text="Scan Tables", command=self.callbacks['scan_tables'], fg_color=("#ECECF1", "#3c3c3c"), hover_color=("#D9D9E3", "#4c4c4c"), text_color=("#343541", "#FFFFFF"), height=40)
        scan_table_btn.pack(side="left", padx=(0, 5), expand=True, fill="x")
        
        show_table_btn = ctk.CTkButton(table_actions_frame, text="Show Table Data", command=self.callbacks['show_table'], fg_color=("#000000", "#007acc"), hover_color=("#333333", "#0062a3"), height=40)
        show_table_btn.pack(side="right", padx=(5, 0), expand=True, fill="x")
        
        export_btn = ctk.CTkButton(self, text="Export to CSV", command=self.callbacks['export'], fg_color=("#10a37f", "#388a34"), hover_color=("#0d8a6a", "#2b6a28"), height=40)
        export_btn.pack(pady=10, padx=20, fill="x")