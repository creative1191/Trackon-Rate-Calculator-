import customtkinter as ctk
import math
import os
import sys

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Theme Setup
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class TrackonApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Trackon Rate Calculator")
        # ✅ FIX: Size chhota kiya hai taaki screen par fit ho jaye
        self.geometry("450x680") 
        self.resizable(False, False)
        
        self.colors = {
            "prime": "#E91E63",
            "standard": "#4CAF50",
            "bg": "#F0F2F5",
            "card": "#FFFFFF",
            "text_main": "#111827",
            "text_sub": "#6B7280",
            "input_bg": "#F3F4F6",
            "input_border": "#E5E7EB"
        }
        self.company = "prime"
        self.logo_img = None
        self.setup_ui()
        
    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Scrollable Frame
        main_scroll = ctk.CTkScrollableFrame(self, fg_color=self.colors["bg"], scrollbar_button_color="#D1D5DB")
        main_scroll.grid(row=0, column=0, sticky="nsew")
        main_scroll.grid_columnconfigure(0, weight=1)
        
        # --- HEADER ---
        # Header ka height thoda reduce kiya
        header_card = ctk.CTkFrame(main_scroll, fg_color=self.colors["card"], corner_radius=16, border_width=0)
        header_card.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 10))
        
        logo_frame = ctk.CTkFrame(header_card, fg_color="transparent", height=90)
        logo_frame.pack(fill="x")
        logo_frame.pack_propagate(False)
        
        try:
            if HAS_PIL:
                img_path = resource_path("trackon_logo.png")
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    img = img.resize((200, int(200 * img.size[1] / img.size[0])), Image.Resampling.LANCZOS)
                    self.logo_img = ctk.CTkImage(light_image=img, size=(200, int(200 * img.size[1] / img.size[0])))
                    logo_label = ctk.CTkLabel(logo_frame, image=self.logo_img, text="")
                    logo_label.pack(pady=(5, 0))
                else: raise FileNotFoundError
        except Exception:
            ctk.CTkLabel(logo_frame, text="TRACKON", font=ctk.CTkFont(size=24, weight="bold"), text_color=self.colors["text_main"]).pack(pady=(10, 0))
            
        ctk.CTkLabel(logo_frame, text="S W I F T  •  S A F E  •  S U R E", font=ctk.CTkFont(size=10), text_color=self.colors["text_sub"]).pack(pady=(0, 5))
        
        # --- MAIN FORM CARD ---
        content_card = ctk.CTkFrame(main_scroll, fg_color=self.colors["card"], corner_radius=16, border_width=0)
        content_card.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15))
        
        self.add_section_title(content_card, "Select Service")
        
        company_frame = ctk.CTkFrame(content_card, fg_color="transparent")
        company_frame.pack(fill="x", padx=20, pady=(0, 15))
        company_frame.grid_columnconfigure(0, weight=1)
        company_frame.grid_columnconfigure(1, weight=1)
        
        self.btn_prime = ctk.CTkButton(company_frame, text="🔴 PRIME", command=lambda: self.select_company("prime"),
                                      fg_color="#FCE4EC", text_color="#880E4F", hover_color="#F8BBD0", 
                                      corner_radius=10, height=45, font=ctk.CTkFont(size=13, weight="bold"))
        self.btn_prime.grid(row=0, column=0, padx=(0, 8), sticky="ew")
        
        self.btn_standard = ctk.CTkButton(company_frame, text="🟢 STANDARD", command=lambda: self.select_company("standard"),
                                         fg_color="#E8F5E9", text_color="#1B5E20", hover_color="#C8E6C9", 
                                         corner_radius=10, height=45, font=ctk.CTkFont(size=13, weight="bold"))
        self.btn_standard.grid(row=0, column=1, padx=(8, 0), sticky="ew")
        self.update_company_buttons()
        
        self.add_section_title(content_card, "Shipment Details")
        
        # Service Type
        self.service_var = ctk.StringVar(value="DOX")
        self.create_input_row(content_card, "Service Type", is_menu=True, values=["DOX", "Surface (Non-DOX)", "Smart Express"])
        
        # Zone
        self.zone_var = ctk.StringVar(value="MP")
        self.create_input_row(content_card, "Zone", is_menu=True, values=["MP", "ROI", "NE"])
        
        # Weight
        self.weight_entry = self.create_input_row(content_card, "Weight (Kg)", is_entry=True, placeholder="Enter weight")
        self.weight_entry.bind("<Return>", lambda e: self.calculate())
        
        # Button (Height thoda kam kiya)
        self.calc_btn = ctk.CTkButton(content_card, text="CALCULATE RATE 💰",
                                     command=self.calculate, corner_radius=10, height=45,
                                     font=ctk.CTkFont(size=14, weight="bold"))
        self.calc_btn.pack(fill="x", padx=20, pady=(5, 15))
        self.update_calc_button()
        
        # Result (Compact Size)
        self.result_card = ctk.CTkFrame(content_card, fg_color="#F9FAFB", corner_radius=12, border_width=1, border_color=self.colors["input_border"])
        self.result_card.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(self.result_card, text="TOTAL AMOUNT", font=ctk.CTkFont(size=11, weight="bold"), text_color=self.colors["text_sub"]).pack(pady=(10, 0))
        
        self.amount_label = ctk.CTkLabel(self.result_card, text="₹0", font=ctk.CTkFont(size=36, weight="bold"), text_color=self.colors["prime"])
        self.amount_label.pack(pady=(2, 2))
        
        self.detail_label = ctk.CTkLabel(self.result_card, text="Select options & enter weight", font=ctk.CTkFont(size=12), text_color=self.colors["text_sub"])
        self.detail_label.pack(pady=(0, 10))
        
    def add_section_title(self, parent, text):
        ctk.CTkLabel(parent, text=text, font=ctk.CTkFont(size=14, weight="bold"), 
                     text_color=self.colors["text_main"], anchor="w").pack(fill="x", padx=20, pady=(10, 5))

    def create_input_row(self, parent, label_text, is_menu=False, is_entry=False, values=None, placeholder=""):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=(0, 8))
        
        ctk.CTkLabel(frame, text=label_text, font=ctk.CTkFont(size=12, weight="bold"), 
                     text_color=self.colors["text_main"], anchor="w").pack(fill="x", pady=(0, 4))
        
        if is_entry:
            entry = ctk.CTkEntry(frame, placeholder_text=placeholder,
                                fg_color=self.colors["input_bg"], border_color=self.colors["input_border"],
                                border_width=1, corner_radius=10, height=40,
                                font=ctk.CTkFont(size=13), text_color=self.colors["text_main"],
                                placeholder_text_color="#9CA3AF")
            entry.pack(fill="x")
            return entry
        else:
            menu = ctk.CTkOptionMenu(frame, variable=self.service_var if label_text == "Service Type" else self.zone_var,
                                    values=values,
                                    fg_color=self.colors["input_bg"], button_color=self.colors["input_bg"],
                                    button_hover_color="#E5E7EB", corner_radius=10,
                                    height=40, width=25,
                                    font=ctk.CTkFont(size=13, weight="bold"),
                                    text_color=self.colors["text_main"],
                                    dropdown_text_color=self.colors["text_main"],
                                    dropdown_fg_color=self.colors["card"],
                                    dropdown_hover_color=self.colors["input_bg"])
            menu.pack(fill="x")
            return menu

    def select_company(self, company):
        self.company = company
        self.update_company_buttons()
        self.update_calc_button()
        self.amount_label.configure(text_color=self.colors[company])
        
    def update_company_buttons(self):
        if self.company == "prime":
            self.btn_prime.configure(fg_color=self.colors["prime"], text_color="white", hover_color="#C2185B")
            self.btn_standard.configure(fg_color="#E8F5E9", text_color="#1B5E20", hover_color="#C8E6C9")
        else:
            self.btn_standard.configure(fg_color=self.colors["standard"], text_color="white", hover_color="#388E3C")
            self.btn_prime.configure(fg_color="#FCE4EC", text_color="#880E4F", hover_color="#F8BBD0")
            
    def update_calc_button(self):
        if self.company == "prime":
            self.calc_btn.configure(fg_color=self.colors["prime"], hover_color="#AD1457")
        else:
            self.calc_btn.configure(fg_color=self.colors["standard"], hover_color="#2E7D32")
        
    def calculate(self):
        try:
            weight_text = self.weight_entry.get().strip()
            if not weight_text:
                self.show_error("Please enter weight")
                return
            w = float(weight_text)
            if w <= 0:
                self.show_error("Weight must be greater than 0")
                return
        except ValueError:
            self.show_error("Please enter a valid number")
            return
            
        zone = self.zone_var.get().lower()
        service = self.service_var.get()
        
        if service == "DOX": svc = "dox"
        elif "Surface" in service: svc = "surface"
        else: svc = "smart"
            
        try:
            if self.company == "prime":
                if svc == "dox":
                    rates = {"mp": 250, "roi": 300, "ne": 350}
                    slabs = math.ceil(w / 0.5)
                    amount = slabs * rates[zone]
                    detail = f"DOX: {slabs} slab(s) × ₹{rates[zone]}"
                    self.show_result(amount, detail, self.colors["prime"])
                else:
                    self.show_error("Prime only supports DOX service")
                    
            else:
                if svc == "dox":
                    if zone == "roi":
                        if w <= 0.5: amount, detail = 180, "DOX: 0-500gm Flat"
                        elif w <= 1.0: amount, detail = 300, "DOX: Addl 500gm"
                        else:
                            extra_slabs = math.ceil((w - 1.0) / 0.5)
                            amount = 300 + (extra_slabs * 130)
                            detail = f"DOX: 1kg Base + {extra_slabs} addl"
                    elif zone == "ne":
                        if w <= 0.5: amount, detail = 250, "DOX: 0-500gm Flat"
                        else:
                            extra_slabs = math.ceil((w - 0.5) / 0.5)
                            amount = 250 + (extra_slabs * 200)
                            detail = f"DOX: 500gm Base + {extra_slabs} addl"
                    elif zone == "mp":
                        amount, detail = 100, "DOX: MP Flat Rate"
                    self.show_result(amount, detail, self.colors["standard"])
                    
                elif svc == "surface":
                    if w < 2:
                        self.show_error("Surface service sirf 2kg se upar ke liye hai")
                        return
                    cw = math.ceil(w)
                    rate = 0
                    slab_info = ""
                    if zone == "mp":
                        if cw <= 5: rate, slab_info = 100, "0-5kg"
                        elif cw <= 10: rate, slab_info = 85, "5-10kg"
                        else: raise ValueError("Weight > 10kg")
                    elif zone == "roi":
                        if cw <= 3: rate, slab_info = 150, "0-3kg"
                        elif cw <= 7: rate, slab_info = 100, "3-7kg"
                        elif cw <= 10: rate, slab_info = 90, "7-10kg"
                        else: raise ValueError("Weight > 10kg")
                    elif zone == "ne":
                        if cw <= 3: rate, slab_info = 185, "0-3kg"
                        elif cw <= 7: rate, slab_info = 125, "3-7kg"
                        elif cw <= 10: rate, slab_info = 115, "7-10kg"
                        else: raise ValueError("Weight > 10kg")
                    amount = rate * cw
                    detail = f"Surface: ₹{rate}/kg ({slab_info}) × {cw}kg"
                    self.show_result(amount, detail, self.colors["standard"])
                    
                elif svc == "smart":
                    if w > 2:
                        self.show_error("Smart Express sirf 2kg tak available hai")
                        return
                    if zone == "mp":
                        self.show_error("Smart Express MP zone mein apply nahi hota")
                        return
                    cw = math.ceil(w)
                    rates = {"roi": 150, "ne": 200}
                    amount = rates[zone] * cw
                    detail = f"Smart: ₹{rates[zone]}/kg × {cw}kg"
                    self.show_result(amount, detail, self.colors["standard"])
                    
        except ValueError as e:
            self.show_error(str(e))
            
    def show_result(self, amount, detail, color):
        self.amount_label.configure(text=f"₹{amount}", text_color=color)
        self.detail_label.configure(text=detail)
        self.result_card.configure(fg_color="#E8F5E9" if self.company == "standard" else "#FCE4EC")
        
    def show_error(self, message):
        self.amount_label.configure(text="⚠️", text_color="#F44336")
        self.detail_label.configure(text=message)
        self.result_card.configure(fg_color="#FFEBEE")

if __name__ == "__main__":
    app = TrackonApp()
    app.mainloop()
