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

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class TrackonApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Trackon Rate Calculator")
        self.geometry("450x750")
        self.resizable(False, False)
        
        self.colors = {
            "prime": "#E91E63",
            "standard": "#4CAF50",
            "bg": "#F8F9FA",
            "card": "#FFFFFF",
            "text_primary": "#1A1A1A",
            "text_secondary": "#6C757D"
        }
        self.company = "prime"
        self.logo_img = None
        self.setup_ui()
        
    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        main_scroll = ctk.CTkScrollableFrame(self, fg_color=self.colors["bg"])
        main_scroll.grid(row=0, column=0, sticky="nsew")
        main_scroll.grid_columnconfigure(0, weight=1)
        
        header_card = ctk.CTkFrame(main_scroll, fg_color=self.colors["card"], corner_radius=16)
        header_card.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 15))
        
        logo_frame = ctk.CTkFrame(header_card, fg_color="transparent", height=100)
        logo_frame.pack(fill="x")
        logo_frame.pack_propagate(False)
        
        try:
            if HAS_PIL:
                img_path = resource_path("trackon_logo.png")
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    width_percent = (200 / float(img.size[0]))
                    hsize = int((float(img.size[1]) * float(width_percent)))
                    img = img.resize((200, hsize), Image.Resampling.LANCZOS)
                    self.logo_img = ctk.CTkImage(light_image=img, size=(200, hsize))
                    logo_label = ctk.CTkLabel(logo_frame, image=self.logo_img, text="")
                    logo_label.pack(pady=(10, 5))
                else: raise FileNotFoundError
        except Exception:
            ctk.CTkLabel(logo_frame, text="TRACKON", 
                        font=ctk.CTkFont(size=28, weight="bold"), 
                        text_color=self.colors["text_primary"]).pack(pady=(15, 0))
            
        ctk.CTkLabel(logo_frame, text="S W I F T  •  S A F E  •  S U R E", 
                    font=ctk.CTkFont(size=11), 
                    text_color=self.colors["text_secondary"]).pack(pady=(2, 10))
        
        content_card = ctk.CTkFrame(main_scroll, fg_color=self.colors["card"], corner_radius=16)
        content_card.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(content_card, text="Select Service", 
                    font=ctk.CTkFont(size=14, weight="bold"), 
                    text_color=self.colors["text_primary"], 
                    anchor="w").pack(fill="x", padx=25, pady=(20, 8))
        
        company_frame = ctk.CTkFrame(content_card, fg_color="transparent")
        company_frame.pack(fill="x", padx=25, pady=(0, 15))
        company_frame.grid_columnconfigure(0, weight=1)
        company_frame.grid_columnconfigure(1, weight=1)
        
        self.btn_prime = ctk.CTkButton(company_frame, text="🔴 PRIME", 
                                      command=lambda: self.select_company("prime"),
                                      fg_color="#FCE4EC", text_color="#880E4F",
                                      hover_color="#F8BBD0", corner_radius=10, height=45,
                                      font=ctk.CTkFont(size=13, weight="bold"))
        self.btn_prime.grid(row=0, column=0, padx=(0, 8), sticky="ew")
        
        self.btn_standard = ctk.CTkButton(company_frame, text="🟢 STANDARD", 
                                         command=lambda: self.select_company("standard"),
                                         fg_color="#E8F5E9", text_color="#1B5E20",
                                         hover_color="#C8E6C9", corner_radius=10, height=45,
                                         font=ctk.CTkFont(size=13, weight="bold"))
        self.btn_standard.grid(row=0, column=1, padx=(8, 0), sticky="ew")
        self.update_company_buttons()
        
        ctk.CTkLabel(content_card, text="Service Type", 
                    font=ctk.CTkFont(size=14, weight="bold"), 
                    text_color=self.colors["text_primary"], 
                    anchor="w").pack(fill="x", padx=25, pady=(10, 5))
        
        self.service_var = ctk.StringVar(value="DOX")
        service_menu = ctk.CTkOptionMenu(content_card, variable=self.service_var,
                                        values=["DOX", "Surface (Non-DOX)", "Smart Express"],
                                        fg_color="#F1F3F4", button_color="#E8EAED",
                                        button_hover_color="#DEE2E6", corner_radius=10,
                                        height=42, font=ctk.CTkFont(size=13))
        service_menu.pack(fill="x", padx=25, pady=(0, 10))
        
        ctk.CTkLabel(content_card, text="Zone", 
                    font=ctk.CTkFont(size=14, weight="bold"), 
                    text_color=self.colors["text_primary"], 
                    anchor="w").pack(fill="x", padx=25, pady=(10, 5))
        
        self.zone_var = ctk.StringVar(value="MP")
        zone_menu = ctk.CTkOptionMenu(content_card, variable=self.zone_var,
                                     values=["MP", "ROI", "NE"],
                                     fg_color="#F1F3F4", button_color="#E8EAED",
                                     button_hover_color="#DEE2E6", corner_radius=10,
                                     height=42, font=ctk.CTkFont(size=13))
        zone_menu.pack(fill="x", padx=25, pady=(0, 10))
        
        ctk.CTkLabel(content_card, text="Weight (Kg)", 
                    font=ctk.CTkFont(size=14, weight="bold"), 
                    text_color=self.colors["text_primary"], 
                    anchor="w").pack(fill="x", padx=25, pady=(10, 5))
        
        self.weight_entry = ctk.CTkEntry(content_card, placeholder_text="Enter weight (e.g., 2.5)",
                                        fg_color="#F1F3F4", corner_radius=10, height=42,
                                        font=ctk.CTkFont(size=14))
        self.weight_entry.pack(fill="x", padx=25, pady=(0, 15))
        self.weight_entry.bind("<Return>", lambda e: self.calculate())
        
        self.calc_btn = ctk.CTkButton(content_card, text="CALCULATE RATE 💰",
                                     command=self.calculate, corner_radius=10, height=50,
                                     font=ctk.CTkFont(size=15, weight="bold"))
        self.calc_btn.pack(fill="x", padx=25, pady=(10, 20))
        self.update_calc_button()
        
        self.result_card = ctk.CTkFrame(content_card, fg_color="#F8F9FA", corner_radius=12)
        self.result_card.pack(fill="x", padx=25, pady=(0, 20))
        
        ctk.CTkLabel(self.result_card, text="TOTAL AMOUNT", 
                    font=ctk.CTkFont(size=11), 
                    text_color=self.colors["text_secondary"]).pack(pady=(12, 0))
        
        self.amount_label = ctk.CTkLabel(self.result_card, text="₹0", 
                                        font=ctk.CTkFont(size=42, weight="bold"),
                                        text_color=self.colors["prime"])
        self.amount_label.pack()
        
        self.detail_label = ctk.CTkLabel(self.result_card, text="Select options & enter weight", 
                                        font=ctk.CTkFont(size=12),
                                        text_color=self.colors["text_secondary"])
        self.detail_label.pack(pady=(0, 12))
        
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
        
        if "DOX" in service: svc = "dox"
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
                    
            else: # Standard Logic
                if svc == "dox":
                    base_rates = {"mp": 100, "roi": 260, "ne": 450}
                    if w <= 1:
                        amount = base_rates[zone]
                        detail = "DOX: Flat Rate (0-1kg)"
                    else:
                        extra_slabs = math.ceil((w - 1) / 0.5)
                        addl_rates = {"mp": 80, "roi": 200, "ne": 350}
                        amount = base_rates[zone] + (extra_slabs * addl_rates[zone])
                        detail = f"DOX: 1kg + {extra_slabs} addl slab(s)"
                    self.show_result(amount, detail, self.colors["standard"])
                    
                elif svc == "surface":
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
                    # ✅ SMART EXPRESS RULES UPDATED
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
