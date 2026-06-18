import tkinter as tk
from tkinter import ttk, messagebox
import math
import os
import sys

# Check for PIL (Pillow)
try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class TrackonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trackon Rate Calculator")
        self.root.geometry("400x580")
        self.root.resizable(False, False)
        self.root.configure(bg="#F5F7FA")
        
        self.colors = {
            "bg": "#F5F7FA",
            "card_bg": "#FFFFFF",
            "primary": "#1A237E",
            "text_dark": "#263238",
            "text_light": "#90A4AE",
            "prime_color": "#C2185B",
            "std_color": "#2E7D32"
        }

        self.company = tk.StringVar(value="prime")
        self.logo_img = None
        self.create_widgets()

    def create_widgets(self):
        # --- 1. Header / Logo Area ---
        header_frame = tk.Frame(self.root, bg=self.colors["card_bg"], height=130)
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)
        
        logo_label = tk.Label(header_frame, bg=self.colors["card_bg"])
        logo_label.pack(pady=(15, 0))
        
        try:
            if HAS_PIL:
                img_path = resource_path("trackon_logo.png")
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    width_percent = (280 / float(img.size[0]))
                    hsize = int((float(img.size[1]) * float(width_percent)))
                    img = img.resize((280, hsize), Image.Resampling.LANCZOS)
                    self.logo_img = ImageTk.PhotoImage(img)
                    logo_label.config(image=self.logo_img)
                else:
                    raise FileNotFoundError
        except Exception:
            logo_label.config(text="📦 TRACKON", font=("Segoe UI", 28, "bold"), 
                              fg=self.colors["primary"], bg=self.colors["card_bg"])
            
        footer_text = tk.Label(header_frame, text="S W I F T . S A F E . S U R E", 
                               font=("Segoe UI", 9, "bold"), bg=self.colors["card_bg"], 
                               fg=self.colors["text_light"])
        footer_text.pack(pady=(5, 0))

        # --- 2. Main Card Container ---
        main_frame = tk.Frame(self.root, bg=self.colors["bg"])
        main_frame.pack(fill="both", expand=True, padx=15, pady=5)

        card = tk.Frame(main_frame, bg=self.colors["card_bg"], relief="flat")
        card.pack(fill="both", expand=True)

        # 2.1 Company Toggle
        lbl_company = tk.Label(card, text="Select Company", font=("Segoe UI", 10, "bold"), 
                               bg=self.colors["card_bg"], fg="#546E7A", anchor="w")
        lbl_company.pack(fill="x", padx=25, pady=(15, 5))

        toggle_frame = tk.Frame(card, bg=self.colors["card_bg"])
        toggle_frame.pack(fill="x", padx=25, pady=5)

        self.btn_prime = tk.Radiobutton(toggle_frame, text="🔴 PRIME", variable=self.company, value="prime",
                                        indicatoron=0, width=12, bg="#FCE4EC", fg="#880E4F",
                                        selectcolor="#E91E63", activebackground="#F48FB1",
                                        font=("Segoe UI", 10, "bold"), bd=0, relief="flat", cursor="hand2")
        self.btn_prime.pack(side="left", padx=2)

        self.btn_std = tk.Radiobutton(toggle_frame, text="🟢 STANDARD", variable=self.company, value="standard",
                                      indicatoron=0, width=12, bg="#E8F5E9", fg="#1B5E20",
                                      selectcolor="#00C853", activebackground="#A5D6A7",
                                      font=("Segoe UI", 10, "bold"), bd=0, relief="flat", cursor="hand2")
        self.btn_std.pack(side="right", padx=2)
        
        self.update_company_style()
        self.company.trace('w', lambda *args: self.update_company_style())

        # 2.2 Inputs
        self.add_input_row(card, "Service Type")
        self.service = ttk.Combobox(card, state="readonly", font=("Segoe UI", 11))
        self.service['values'] = ('DOX', 'Surface (Non-DOX)', 'Smart Express')
        self.service.current(0)
        self.service.pack(fill="x", padx=25, pady=(2, 10))
        
        self.add_input_row(card, "Destination Zone")
        self.zone = ttk.Combobox(card, state="readonly", font=("Segoe UI", 11))
        self.zone['values'] = ('MP', 'ROI', 'NE')
        self.zone.current(0)
        self.zone.pack(fill="x", padx=25, pady=(2, 10))

        self.add_input_row(card, "Weight (Kg)")
        self.entry_wt = tk.Entry(card, font=("Segoe UI", 14, "bold"), justify="center", 
                                 bg="#F5F7FA", relief="flat", bd=1)
        self.entry_wt.pack(fill="x", padx=25, pady=(2, 10))
        self.entry_wt.bind("<Return>", lambda e: self.calculate())

        # 2.3 Calculate Button
        calc_btn = tk.Button(card, text="💰 CALCULATE RATE", command=self.calculate,
                             bg=self.colors["primary"], fg="white", font=("Segoe UI", 13, "bold"),
                             activebackground="#0D47A1", relief="flat", cursor="hand2", height=2)
        calc_btn.pack(fill="x", padx=25, pady=10)

        # 2.4 Result Display
        res_frame = tk.Frame(card, bg="#ECEFF1", relief="flat")
        res_frame.pack(fill="x", padx=25, pady=15)
        
        self.lbl_result_label = tk.Label(res_frame, text="TOTAL AMOUNT", 
                                         font=("Segoe UI", 8, "bold"), bg="#ECEFF1", fg="#546E7A")
        self.lbl_result_label.pack(pady=(8, 0))
        
        self.lbl_amt = tk.Label(res_frame, text="₹0", font=("Segoe UI", 38, "bold"), 
                                bg="#ECEFF1", fg=self.colors["primary"])
        self.lbl_amt.pack()
        
        self.lbl_detail = tk.Label(res_frame, text="Select options & enter weight", 
                                   font=("Segoe UI", 9), bg="#ECEFF1", fg="#78909C")
        self.lbl_detail.pack(pady=(0, 8))

        # Footer
        footer = tk.Label(self.root, text="© 2026 Trackon Courier System", 
                          font=("Segoe UI", 8), bg=self.colors["bg"], fg="#B0BEC5")
        footer.pack(pady=5)

    def add_input_row(self, parent, text):
        lbl = tk.Label(parent, text=text, font=("Segoe UI", 10, "bold"), 
                       bg=parent.cget("bg"), fg="#546E7A", anchor="w")
        lbl.pack(fill="x", padx=25, pady=(10, 0))

    def update_company_style(self):
        if self.company.get() == 'prime':
            self.colors["primary"] = self.colors["prime_color"]
            self.btn_prime.config(bg="#F48FB1")
            self.btn_std.config(bg="#E0E0E0")
        else:
            self.colors["primary"] = self.colors["std_color"]
            self.btn_std.config(bg="#A5D6A7")
            self.btn_prime.config(bg="#E0E0E0")

    def calculate(self):
        try:
            w_raw = self.entry_wt.get().strip()
            if not w_raw: return
            w = float(w_raw)
            if w <= 0: raise ValueError
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid weight!")
            return

        comp = self.company.get()
        zone_val = self.zone.get().lower()
        zone = 'mp' if zone_val.startswith('mp') else ('roi' if zone_val.startswith('roi') else 'ne')
        
        svc_val = self.service.get()
        if 'DOX' in svc_val: svc = 'dox'
        elif 'Surface' in svc_val: svc = 'surface'
        else: svc = 'smart'

        amt = 0
        detail = ""
        color = self.colors["primary"]

        try:
            # ==========================
            # PRIME LOGIC
            # ==========================
            if comp == 'prime':
                if svc == 'dox':
                    rates = {'mp': 250, 'roi': 300, 'ne': 350}
                    slabs = math.ceil(w / 0.5)
                    amt = slabs * rates[zone]
                    detail = f"DOX: {slabs} slab(s) × ₹{rates[zone]}"
                    color = self.colors["prime_color"]
                
                elif svc in ['surface', 'smart']:
                    messagebox.showinfo("Info", "Prime sirf DOX service ke liye available hai.")
                    return

            # ==========================
            # STANDARD LOGIC
            # ==========================
            else:
                color = self.colors["std_color"]
                if svc == 'dox':
                    base_rates = {'mp': 100, 'roi': 260, 'ne': 450}
                    if w <= 1:
                        amt = base_rates[zone]
                        detail = f"DOX: Flat Rate (0-1kg)"
                    else:
                        extra_wt = w - 1
                        extra_slabs = math.ceil(extra_wt / 0.5)
                        addl_rates = {'mp': 80, 'roi': 200, 'ne': 350} 
                        amt = base_rates[zone] + (extra_slabs * addl_rates[zone])
                        detail = f"DOX: 1kg Flat + {extra_slabs} addl slab(s)"
                    
                elif svc == 'surface':
                    cw = math.ceil(w)
                    rate = 0
                    slab_info = ""
                    
                    if zone == 'mp':
                        if cw <= 5: rate, slab_info = 100, "0-5kg"
                        elif cw <= 10: rate, slab_info = 85, "5-10kg"
                        else: raise ValueError("Weight > 10kg not supported")
                        
                    elif zone == 'roi':
                        if cw <= 3: rate, slab_info = 150, "0-3kg"
                        elif cw <= 7: rate, slab_info = 100, "3-7kg"
                        elif cw <= 10: rate, slab_info = 90, "7-10kg"
                        else: raise ValueError("Weight > 10kg not supported")
                        
                    elif zone == 'ne':
                        if cw <= 3: rate, slab_info = 185, "0-3kg"
                        elif cw <= 7: rate, slab_info = 125, "3-7kg"
                        elif cw <= 10: rate, slab_info = 115, "7-10kg"
                        else: raise ValueError("Weight > 10kg not supported")

                    amt = rate * cw
                    detail = f"Surface: ₹{rate}/kg ({slab_info}) × {cw}kg"

                elif svc == 'smart':
                    cw = math.ceil(w)
                    rates = {'mp': 81, 'roi': 104, 'ne': 126}
                    amt = rates[zone] * cw
                    detail = f"Smart: ₹{rates[zone]}/kg × {cw}kg"

            self.update_result(amt, detail, color)

        except ValueError as e:
            messagebox.showwarning("Limit", str(e))

    def update_result(self, amount, detail_text, color):
        self.lbl_amt.config(text=f"₹{amount}", fg=color)
        self.lbl_detail.config(text=detail_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = TrackonApp(root)
    root.mainloop()