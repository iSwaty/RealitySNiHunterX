import customtkinter as ctk
import threading
import socket
import ssl
import ipaddress
import maxminddb
import os
import time
import concurrent.futures
import OpenSSL.crypto
import webbrowser
import pyperclip
import tkinter as tk
import random
import re
import math
import json
from tkinter import filedialog
from urllib.request import urlretrieve
from datetime import datetime

# Импортируем cryptography для работы с расширениями
from cryptography import x509 as crypto_x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import ExtensionOID
from cryptography.x509 import DNSName

# --- СЛОВАРЬ ПЕРЕВОДОВ / TRANSLATIONS ---
LANG = {
    "ru": {
        "title": "Reality SNI Hunter v5.3 (Clean Core)",
        "vps_ip": "IP адрес VPS:",
        "paste": "Вставить",
        "start": "НАЧАТЬ ПОИСК",
        "stop": "ОСТАНОВИТЬ",
        "scanning": "Сканирование...",
        "neighbor_scan": "Соседние подсети (±5)",
        "wide_scan": "Широкий поиск (ASN /16)",
        "limit": "Лимит",
        "all": "Все",
        "only_country": "Только страна VPS",
        "status_load": "Загрузка баз...",
        "status_ready": "Готов к работе.",
        "status_error": "Ошибка!",
        "copy_list": "Копировать список",
        "copy_one": "Копир.",
        "save_json": "JSON",
        "save_txt": "TXT",
        "nothing_found": "Ничего не найдено",
        "checked": "Проверено",
        "found": "Найдено",
        "copied": "Скопировано",
        "err_enter_ip": "Введите IP!",
        "mode_neighbor": "Режим: Соседние подсети...",
        "mode_wide": "Режим: Широкий поиск...",
        "gen_targets": "Генерация целей...",
        "finish": "Сканирование завершено.",
        "col_sni": "SNI Домен ⇅",
        "col_ip": "IP Адрес ⇅",
        "col_asn": "ASN Провайдер ⇅",
        "col_score": "Рейтинг ⇅",
        "col_act": "Действия"
    },
    "en": {
        "title": "Reality SNI Hunter v5.3 (Clean Core)",
        "vps_ip": "VPS IP Address:",
        "paste": "Paste",
        "start": "START SCAN",
        "stop": "STOP",
        "scanning": "Scanning...",
        "neighbor_scan": "Neighbor Subnets (±5)",
        "wide_scan": "Wide Scan (ASN /16)",
        "limit": "Limit",
        "all": "All",
        "only_country": "Match VPS Country",
        "status_load": "Loading databases...",
        "status_ready": "Ready.",
        "status_error": "Error!",
        "copy_list": "Copy List",
        "copy_one": "Copy",
        "save_json": "JSON",
        "save_txt": "TXT",
        "nothing_found": "Nothing found",
        "checked": "Checked",
        "found": "Found",
        "copied": "Copied",
        "err_enter_ip": "Enter IP!",
        "mode_neighbor": "Mode: Neighbor Scan...",
        "mode_wide": "Mode: Wide Scan...",
        "gen_targets": "Generating targets...",
        "finish": "Scan finished.",
        "col_sni": "SNI Domain ⇅",
        "col_ip": "IP Address ⇅",
        "col_asn": "ASN Provider ⇅",
        "col_score": "Score ⇅",
        "col_act": "Actions"
    },
    "cn": {
        "title": "Reality SNI 扫描器 v5.3 (最终修正版)",
        "vps_ip": "VPS IP地址:",
        "paste": "粘贴",
        "start": "开始扫描",
        "stop": "停止扫描",
        "scanning": "扫描中...",
        "neighbor_scan": "邻近网段 (±5)",
        "wide_scan": "广域扫描 (ASN /16)",
        "limit": "限制",
        "all": "全部",
        "only_country": "仅限VPS所在国家",
        "status_load": "加载数据库...",
        "status_ready": "就绪.",
        "status_error": "错误!",
        "copy_list": "复制列表",
        "copy_one": "复制",
        "save_json": "JSON",
        "save_txt": "TXT",
        "nothing_found": "未找到结果",
        "checked": "已检查",
        "found": "发现",
        "copied": "已复制",
        "err_enter_ip": "请输入IP!",
        "mode_neighbor": "模式: 邻近网段...",
        "mode_wide": "模式: 广域扫描...",
        "gen_targets": "生成目标IP...",
        "finish": "扫描完成.",
        "col_sni": "SNI 域名 ⇅",
        "col_ip": "IP 地址 ⇅",
        "col_asn": "ASN 运营商 ⇅",
        "col_score": "评分 ⇅",
        "col_act": "操作"
    }
}

# --- Настройки ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class RealityScannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.current_lang = "ru" # Default language
        self.t = lambda k: LANG[self.current_lang].get(k, k)

        self.title(self.t("title"))
        self.geometry("1280x850")
        self.minsize(1000, 650)

        self.mmdb_country_path = "Country.mmdb"
        self.mmdb_asn_path = "ASN.mmdb"
        
        self.is_scanning = False
        self.vps_ip_int = 0
        self.vps_country = None
        self.vps_asn = None
        self.found_snis = set()
        self.current_results = [] 
        
        self.sort_state = {"col": 3, "reverse": False}

        # --- Сетка ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # ==============================
        # 1. ВЕРХНЯЯ ПАНЕЛЬ
        # ==============================
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.top_frame.grid_columnconfigure(1, weight=1)

        # Input Block
        input_frame = ctk.CTkFrame(self.top_frame, fg_color="transparent")
        input_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        self.lbl_ip = ctk.CTkLabel(input_frame, text=self.t("vps_ip"), font=("Arial", 14, "bold"))
        self.lbl_ip.pack(side="left", padx=(0, 10))
        
        self.entry_ip = ctk.CTkEntry(input_frame, placeholder_text="1.2.3.4", height=35, font=("Arial", 13), width=250)
        self.entry_ip.pack(side="left", padx=(0, 10))
        
        self.label_vps_info = ctk.CTkLabel(input_frame, text="", font=("Arial", 12), text_color="#2CC985")
        self.label_vps_info.pack(side="left", padx=10)

        self.entry_ip.bind("<KeyRelease>", self.on_ip_key_release)
        self.entry_ip.bind("<Button-3>", self.show_context_menu)
        
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label=self.t("paste"), command=self.paste_from_clipboard)

        # Settings Block
        self.settings_frame = ctk.CTkFrame(self.top_frame, fg_color="transparent")
        self.settings_frame.grid(row=0, column=2, sticky="e")

        # Language Selector
        self.lang_var = ctk.StringVar(value="Русский")
        self.combo_lang = ctk.CTkOptionMenu(self.settings_frame, values=["Русский", "English", "简体中文"], 
                                            width=110, command=self.change_language, variable=self.lang_var)
        self.combo_lang.pack(side="left", padx=5)

        self.scan_mode = ctk.CTkOptionMenu(self.settings_frame, values=[self.t("neighbor_scan"), self.t("wide_scan")], width=200)
        self.scan_mode.set(self.t("neighbor_scan"))
        self.scan_mode.pack(side="left", padx=5)

        self.combo_limit = ctk.CTkOptionMenu(self.settings_frame, values=["50", "100", "500", self.t("all")], width=80)
        self.combo_limit.set("50")
        self.combo_limit.pack(side="left", padx=5)

        self.check_country_var = ctk.BooleanVar(value=True)
        self.chk_country = ctk.CTkCheckBox(self.settings_frame, text=self.t("only_country"), variable=self.check_country_var, onvalue=True, offvalue=False)
        self.chk_country.pack(side="left", padx=10)

        self.btn_scan = ctk.CTkButton(self.settings_frame, text=self.t("start"), command=self.start_scan_thread, 
                                      fg_color="#2CC985", hover_color="#229A65", height=35, font=("Arial", 13, "bold"), width=140)
        self.btn_scan.pack(side="left", padx=(10, 0))

        # ==============================
        # 2. СТАТУС БАР
        # ==============================
        self.status_bar = ctk.CTkFrame(self, height=40, fg_color="#212121", corner_radius=5)
        self.status_bar.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")
        
        self.label_status = ctk.CTkLabel(self.status_bar, text=self.t("status_load"), text_color="#aaaaaa", font=("Arial", 12))
        self.label_status.pack(side="left", padx=10)
        
        self.btn_json = ctk.CTkButton(self.status_bar, text=self.t("save_json"), width=60, height=24, fg_color="#444", command=self.save_json, state="disabled")
        self.btn_json.pack(side="right", padx=5, pady=5)
        
        self.btn_txt = ctk.CTkButton(self.status_bar, text=self.t("save_txt"), width=60, height=24, fg_color="#444", command=self.save_txt, state="disabled")
        self.btn_txt.pack(side="right", padx=5, pady=5)

        self.btn_copy_all = ctk.CTkButton(self.status_bar, text=self.t("copy_list"), width=100, height=24, fg_color="#444", command=self.copy_all_domains, state="disabled")
        self.btn_copy_all.pack(side="right", padx=5, pady=5)

        self.progressbar = ctk.CTkProgressBar(self.status_bar, height=8, progress_color="#2CC985", width=150)
        self.progressbar.pack(side="right", padx=10)
        self.progressbar.set(0)

        # ==============================
        # 3. ТАБЛИЦА
        # ==============================
        self.table_container = ctk.CTkFrame(self, fg_color="transparent")
        self.table_container.grid(row=2, column=0, padx=20, pady=5, sticky="nsew")
        self.table_container.grid_rowconfigure(1, weight=1)
        self.table_container.grid_columnconfigure(0, weight=1)

        self.header_frame = ctk.CTkFrame(self.table_container, height=40, fg_color="#2b2b2b", corner_radius=5)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        
        cols = [30, 15, 15, 10, 10]
        for i, w in enumerate(cols): self.header_frame.grid_columnconfigure(i, weight=w)

        self.render_table_headers()

        self.scroll_frame = ctk.CTkScrollableFrame(self.table_container, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", pady=(5, 0))
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        # ==============================
        # 4. ЛОГ
        # ==============================
        self.log_box = ctk.CTkTextbox(self, height=80, font=("Consolas", 10), text_color="#888888", fg_color="#1a1a1a")
        self.log_box.grid(row=3, column=0, padx=20, pady=15, sticky="ew")

        self.check_databases()

    # --- LANGUAGE SYSTEM ---
    def change_language(self, choice):
        if choice == "English": self.current_lang = "en"
        elif choice == "简体中文": self.current_lang = "cn"
        else: self.current_lang = "ru"
        
        self.update_ui_text()

    def update_ui_text(self):
        self.title(self.t("title"))
        self.lbl_ip.configure(text=self.t("vps_ip"))
        self.context_menu.entryconfigure(0, label=self.t("paste"))
        
        self.scan_mode.configure(values=[self.t("neighbor_scan"), self.t("wide_scan")])
        self.scan_mode.set(self.t("neighbor_scan"))
        self.combo_limit.configure(values=["50", "100", "500", self.t("all")])
        self.chk_country.configure(text=self.t("only_country"))
        
        if self.is_scanning: self.btn_scan.configure(text=self.t("scanning"))
        else: self.btn_scan.configure(text=self.t("start"))

        self.label_status.configure(text=self.t("status_ready"))
        self.btn_json.configure(text=self.t("save_json"))
        self.btn_txt.configure(text=self.t("save_txt"))
        self.btn_copy_all.configure(text=self.t("copy_list"))
        
        self.render_table_headers()
        
        if self.current_results:
             for widget in self.scroll_frame.winfo_children(): widget.destroy()
             self.render_table_rows(self.current_results)

    def render_table_headers(self):
        for widget in self.header_frame.winfo_children(): widget.destroy()
        
        headers = [
            (self.t("col_sni"), 0), 
            (self.t("col_ip"), 1), 
            (self.t("col_asn"), 2), 
            (self.t("col_score"), 3), 
            (self.t("col_act"), 4)
        ]
        
        for text, col in headers:
            if col == 4:
                ctk.CTkLabel(self.header_frame, text=text, font=("Arial", 12, "bold"), text_color="white").grid(row=0, column=col, padx=5, pady=5)
            else:
                btn = ctk.CTkButton(self.header_frame, text=text, font=("Arial", 12, "bold"), 
                                    fg_color="transparent", hover_color="#444", anchor="w",
                                    command=lambda c=col: self.sort_data(c))
                btn.grid(row=0, column=col, padx=2, pady=2, sticky="ew")

    # --- UTILS ---
    def show_context_menu(self, event): self.context_menu.tk_popup(event.x_root, event.y_root)
    def paste_from_clipboard(self): 
        try: 
            text = pyperclip.paste()
            self.entry_ip.insert(0, text)
            self.on_ip_key_release(None)
        except: pass
    
    def log(self, msg): self.after(0, lambda: self._log_internal(msg))
    def _log_internal(self, msg):
        self.log_box.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        self.log_box.see("end")

    def on_ip_key_release(self, event):
        ip = self.entry_ip.get().strip()
        try:
            ipaddress.IPv4Address(ip)
            c = "UNK"; asn_str = ""
            if os.path.exists(self.mmdb_country_path):
                with maxminddb.open_database(self.mmdb_country_path) as r:
                    d = r.get(ip)
                    if d: c = d['country']['iso_code']
            if os.path.exists(self.mmdb_asn_path):
                _, asn_str = self.get_asn_info(ip)
            self.label_vps_info.configure(text=f"✅ {c} | {asn_str}")
        except:
            self.label_vps_info.configure(text="")

    # --- EXPORT ---
    def copy_all_domains(self):
        if not self.current_results: return
        text = "\n".join([r['sni'] for r in self.current_results])
        pyperclip.copy(text)
        self.label_status.configure(text=f"{self.t('copied')} {len(self.current_results)} SNI")

    def save_json(self):
        if not self.current_results: return
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if filename:
            try:
                export_data = [{"sni": r['sni'], "ip": r['ip'], "score": r['score'], "asn": r['asn_str']} for r in self.current_results]
                with open(filename, 'w', encoding='utf-8') as f: json.dump(export_data, f, indent=4)
                self.log(f"JSON saved: {filename}")
            except Exception as e: self.log(f"Error: {e}")

    def save_txt(self):
        if not self.current_results: return
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    for r in self.current_results: f.write(f"{r['sni']}\n")
                self.log(f"TXT saved: {filename}")
            except Exception as e: self.log(f"Error: {e}")

    # --- SORT ---
    def sort_data(self, col_idx):
        if not self.current_results: return
        if self.sort_state["col"] == col_idx: self.sort_state["reverse"] = not self.sort_state["reverse"]
        else:
            self.sort_state["col"] = col_idx
            self.sort_state["reverse"] = False
        
        key = None
        if col_idx == 0: key = lambda x: x['sni']
        elif col_idx == 1: key = lambda x: int(ipaddress.IPv4Address(x['ip']))
        elif col_idx == 2: key = lambda x: x['asn_num']
        elif col_idx == 3: key = lambda x: x['score']

        if key:
            self.current_results.sort(key=key, reverse=self.sort_state["reverse"])
            for widget in self.scroll_frame.winfo_children(): widget.destroy()
            self.render_table_rows(self.current_results)

    # --- DB ---
    def check_databases(self): threading.Thread(target=self.dl_dbs, daemon=True).start()
    def dl_dbs(self):
        if not os.path.exists(self.mmdb_country_path):
            try: urlretrieve("https://github.com/Loyalsoldier/geoip/releases/latest/download/Country.mmdb", self.mmdb_country_path)
            except: pass
        if not os.path.exists(self.mmdb_asn_path):
            try: urlretrieve("https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-ASN.mmdb", self.mmdb_asn_path)
            except: pass
        self.after(0, lambda: self.label_status.configure(text=self.t("status_ready")))

    def get_asn_info(self, ip):
        try:
            with maxminddb.open_database(self.mmdb_asn_path) as reader:
                data = reader.get(ip)
                if data:
                    org = data.get('autonomous_system_organization', 'Unknown').split(" ")[0]
                    return data.get('autonomous_system_number', 0), f"AS{data.get('autonomous_system_number', 0)} {org}"
        except: pass
        return 0, "Unknown"

    # --- SCANNING ---
    def start_scan_thread(self):
        if self.is_scanning: return
        ip = self.entry_ip.get().strip()
        if not ip: return self.log(self.t("err_enter_ip"))

        for w in self.scroll_frame.winfo_children(): w.destroy()
        self.log_box.delete("1.0", "end")
        self.found_snis.clear()
        self.current_results = []
        for btn in [self.btn_copy_all, self.btn_json, self.btn_txt]: btn.configure(state="disabled")

        self.is_scanning = True
        self.btn_scan.configure(state="disabled", text=self.t("scanning"), fg_color="gray")
        self.progressbar.start()

        threading.Thread(target=self.scan_logic, args=(ip,), daemon=True).start()

    def scan_logic(self, vps_ip):
        try:
            self.vps_ip_int = int(ipaddress.IPv4Address(vps_ip))
            # Refresh VPS context
            try:
                with maxminddb.open_database(self.mmdb_country_path) as r:
                    d = r.get(vps_ip)
                    if d: self.vps_country = d['country']['iso_code']
                self.vps_asn, _ = self.get_asn_info(vps_ip)
            except: pass

            target_ips = set()
            mode_val = self.scan_mode.get()
            
            if self.t("wide_scan") in mode_val:
                self.log(self.t("mode_wide"))
                try:
                    parent = ipaddress.ip_network(f"{vps_ip}/16", strict=False)
                    count = 0
                    while count < 1500:
                        rip = str(ipaddress.IPv4Address(random.randint(int(parent.network_address), int(parent.broadcast_address))))
                        target_ips.add(rip)
                        count += 1
                except: pass
            else:
                self.log(self.t("mode_neighbor"))
                parts = vps_ip.split('.')
                c_octet = int(parts[2])
                for c in range(max(0, c_octet - 5), min(255, c_octet + 6)):
                    try:
                        net = ipaddress.ip_network(f"{parts[0]}.{parts[1]}.{c}.0/24", strict=False)
                        if c == c_octet:
                            for ip in net: target_ips.add(str(ip))
                        else:
                            all_hosts = list(net.hosts())
                            if len(all_hosts) > 50:
                                for _ in range(50): target_ips.add(str(random.choice(all_hosts)))
                    except: pass

            targets = list(target_ips)
            random.shuffle(targets)
            self.log(f"{self.t('gen_targets')} {len(targets)}")

            valid_list = []
            
            # Limit
            limit_str = self.combo_limit.get()
            if limit_str == self.t("all") or limit_str == "All" or limit_str == "全部":
                limit = 9999
            else:
                try: limit = int(limit_str)
                except: limit = 50

            with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
                futures = {executor.submit(self.process_ip, ip): ip for ip in targets}
                done = 0
                for future in concurrent.futures.as_completed(futures):
                    done += 1
                    if done % 50 == 0: 
                        self.after(0, lambda d=done, t=len(targets): self.label_status.configure(
                            text=f"{self.t('checked')}: {d}/{t} | {self.t('found')}: {len(valid_list)}"))
                    
                    res_list = future.result()
                    if res_list:
                        for res in res_list:
                            if res['sni'] not in self.found_snis:
                                self.found_snis.add(res['sni'])
                                valid_list.append(res)
                                self.log(f"✅ {res['sni']} (S:{res['score']:.1f})")

            valid_list.sort(key=lambda x: (not x['asn_match'], x['score']))
            self.current_results = valid_list[:limit]
            self.after(0, lambda: self.render_table_rows(self.current_results))
            self.log(self.t("finish"))

        except Exception as e: self.log(f"Err: {e}")
        finally: self.after(0, self.stop_scan)

    def stop_scan(self):
        self.is_scanning = False
        self.btn_scan.configure(state="normal", text=self.t("start"), fg_color="#2CC985")
        self.progressbar.stop()
        self.progressbar.set(1)
        if self.current_results: 
            for btn in [self.btn_copy_all, self.btn_json, self.btn_txt]: btn.configure(state="normal")

    def render_table_rows(self, results):
        if not results:
            ctk.CTkLabel(self.scroll_frame, text=self.t("nothing_found"), font=("Arial", 14)).pack(pady=20)
            return

        for i, item in enumerate(results):
            row = ctk.CTkFrame(self.scroll_frame, fg_color="#2b2b2b" if i%2==0 else "transparent", corner_radius=0)
            row.pack(fill="x", pady=1)
            cols = [30, 15, 15, 10, 10]
            for idx, w in enumerate(cols): row.grid_columnconfigure(idx, weight=w)

            e = ctk.CTkEntry(row, fg_color="transparent", border_width=0, font=("Consolas", 13, "bold"), text_color="#4ea8de")
            e.insert(0, item['sni']); e.configure(state="readonly")
            e.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

            col = "#2CC985" if self.vps_country and item['country'] == self.vps_country else "white"
            ctk.CTkLabel(row, text=f"{item['ip']} [{item['country']}]", text_color=col).grid(row=0, column=1)

            ac = "#00FF00" if item['asn_match'] else "#aaaaaa"
            ctk.CTkLabel(row, text=item['asn_str'], text_color=ac, font=("Arial", 11, "bold" if item['asn_match'] else "normal")).grid(row=0, column=2)

            ctk.CTkLabel(row, text=f"{item['latency']}ms (D:{item['dist_penalty']:.1f})", font=("Arial", 11)).grid(row=0, column=3)

            b = ctk.CTkFrame(row, fg_color="transparent")
            b.grid(row=0, column=4)
            ctk.CTkButton(b, text=self.t("copy_one"), width=50, height=24, fg_color="#444", command=lambda s=item['sni']: self.copy_sn(s)).pack(side="left", padx=2)
            ctk.CTkButton(b, text="🌐", width=30, height=24, fg_color="#333", command=lambda s=item['sni']: webbrowser.open(f"https://{s}")).pack(side="left", padx=2)

    def copy_sn(self, text):
        pyperclip.copy(text)
        self.label_status.configure(text=f"{self.t('copied')}: {text}")

    # --- CORE (Clean Hybrid Approach) ---
    def process_ip(self, ip):
        found = []
        try:
            country = "UNK"; asn_num = 0; asn_str = ""
            try:
                with maxminddb.open_database(self.mmdb_country_path) as r:
                    g = r.get(ip)
                    if g: country = g['country']['iso_code']
                asn_num, asn_str = self.get_asn_info(ip)
            except: pass

            if self.check_country_var.get() and self.vps_country and country != self.vps_country: return []

            timeout = 1.5
            start_time = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((ip, 443))
            
            ctx = ssl.create_default_context()
            ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
            ctx.set_alpn_protocols(['h2', 'http/1.1']) 
            conn = ctx.wrap_socket(sock, server_hostname=ip)
            
            if conn.selected_alpn_protocol() != "h2":
                conn.close(); sock.close(); return []

            latency = int((time.time() - start_time) * 1000)
            cert_bin = conn.getpeercert(binary_form=True)
            conn.close(); sock.close()

            # Hybrid Approach: Load via OpenSSL (tolerant), convert to Cryptography (modern)
            try:
                # 1. Load via OpenSSL (Handles negative serials)
                x509_openssl = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, cert_bin)
                
                # 2. Convert to Cryptography Object for safe parsing
                cert = x509_openssl.to_cryptography()
            except Exception:
                return [] # Corrupt cert

            # Cloudflare Check via Org
            try:
                for attribute in cert.subject.get_attributes_for_oid(crypto_x509.oid.NameOID.ORGANIZATION_NAME):
                    if "Cloudflare" in str(attribute.value): return []
            except: pass

            candidates = set()
            
            # Common Name
            try:
                for attribute in cert.subject.get_attributes_for_oid(crypto_x509.oid.NameOID.COMMON_NAME):
                    candidates.add(str(attribute.value))
            except: pass
            
            # SANs (Modern way)
            try:
                san_ext = cert.extensions.get_extension_for_oid(ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
                for name in san_ext.value:
                    if isinstance(name, DNSName): candidates.add(name.value)
            except: pass

            target_ip_int = int(ipaddress.IPv4Address(ip))
            dist_raw = abs(self.vps_ip_int - target_ip_int)
            dist_penalty = round(math.log(dist_raw + 1) if dist_raw > 0 else 0, 1)
            final_score = latency + dist_penalty
            is_asn_match = (self.vps_asn and asn_num == self.vps_asn)

            for d in candidates:
                to_check = []
                if d.startswith("*."):
                    clean = d[2:]
                    to_check.append(clean)
                else:
                    to_check.append(d)

                for dom in to_check:
                    if dom.startswith("www."): dom = dom[4:]
                    if self.is_clean(dom):
                        found.append({
                            "ip": ip, "sni": dom, "latency": latency, "dist_penalty": dist_penalty,
                            "score": final_score, "country": country, "asn_num": asn_num,
                            "asn_str": asn_str, "asn_match": is_asn_match
                        })
        except: pass
        return found

    def is_clean(self, d):
        d = d.lower()
        if d.replace('.','').isdigit(): return False
        if len(d) < 4 or '.' not in d: return False
        if re.search(r'[a-f0-9]{10,}', d): return False
        if re.search(r'\d{1,3}[-.]\d{1,3}[-.]\d{1,3}', d): return False
        
        # Расширенный список известных сайтов/сервисов для фильтрации
        known_sites = [
            # === ГЛОБАЛЬНЫЕ ГИГАНТЫ ===
            "google.", "youtube.", "gstatic.", "android.", "gmail.", "ggpht.",
            "facebook.", "fbcdn.", "whatsapp.", "instagram.", "meta.", "fbsbx.",
            "twitter.", "x.com", "twimg.", "t.co",
            "apple.", "icloud.", "mzstatic.", "itunes.", "appstore.",
            "microsoft.", "windows.", "office.", "live.", "outlook.", "azure.", "msn.",
            "amazon.", "aws.", "cloudfront.", "alexa.", "audible.",
            "netflix.", "nflxso.", "nflxvideo.", "nflxext.",
            "cloudflare.", "akamai.", "fastly.", "edgekey.", "edgesuite.",
            
            # === ИНФОРМАЦИОННЫЕ И РАЗРАБОТЧИКИ ===
            "wikipedia.", "wiki.", "wikimedia.", "wiktionary.",
            "github.", "gitlab.", "bitbucket.", "stackoverflow.", "stackexchange.",
            "reddit.", "redd.it", "linkedin.", "medium.", "substack.",
            "discord.", "slack.", "zoom.", "teams.", "skype.",
            "tiktok.", "snapchat.", "pinterest.", "tumblr.", "vimeo.",
            "twitch.", "spotify.", "soundcloud.", "deezer.",
            "ign.com", "gamespot.", "polygon.", "kotaku.", "pcgamer.",
            "steam.", "epicgames.", "origin.", "uplay.", "gog.", "battle.net",
            
            # === РОССИЙСКИЕ САЙТЫ (ПОЛНЫЙ СПИСОК) ===
            # Поиск и экосистемы
            "yandex.", "ya.ru", "yandex.net", "yastatic.",
            "mail.ru", "vk.com", "vk.", "vkuser.", "ok.ru", "odnoklassniki.",
            "rambler.", "ru.", "my.com", "bk.ru", "list.ru", "inbox.ru",
            
            # Банки и Финансы
            "sberbank.", "sber.", "tinkoff.", "alfabank.", "vtb.",
            "gazprombank.", "rosbank.", "raiffeisen.", "openbank.",
            "uralsib.", "rencredit.", "homecredit.", "sovcombank.",
            "gosuslugi.", "nalog.ru", "pfr.gov.", "fss.gov.", "rf.",
            
            # Маркетплейсы и Торговля
            "wildberries.", "ozon.", "avito.", "yandex.market",
            "aliexpress.", "lamoda.", "citilink.", "dns-shop.",
            "mvideo.", "eldorado.", "technopark.", "holodilnik.",
            "detmir.", "kari.", "sportmaster.", "leroymerlin.",
            
            # СМИ и Новости
            "lenta.", "ria.", "tass.", "rt.", "rbc.",
            "kommersant.", "vedomosti.", "forbes.", "interfax.",
            "mk.ru", "kp.ru", "aif.ru", "argumenti.",
            "rg.ru", "iz.ru", "vesti.ru", "tvcentr.", "5-tv.",
            "ntv.ru", "ren.tv", "ctc.ru", "domashniy.",
            
            # IT и Сообщества
            "habr.", "vc.ru", "dtf.", "pikabu.", "spark-interfax.",
            "cnews.", "3dnews.", "ixbt.", "overclockers.",
            "cyberforum.", "prog.hu", "xakep.",
            
            # Развлечения и Кино
            "kinopoisk.", "ivi.", "okko.", "more.tv", "start.ru",
            "premier.one", "tvzavr.", "rutube.", "smotrim.",
            "afisha.", "timeout.", "kinoafisha.",
            
            # Такси и Транспорт
            "uber.", "yandex.taxi", "citymobil.", "gettaxi.",
            "aeroexpress.", "rzd.", "pobeda.aero", "aeroflot.",
            "s7.ru", "uralairlines.", "redwings.",
            
            # Безопасность и Антивирусы
            "kaspersky.", "drweb.", "eset.", "avast.", "avg.",
            "positive.", "bi.", "fsecure.",
            
            # Другое
            "telegram.", "2gis.", "dzen.", "telega.",
            "delivery-club.", "samokat.", "yandex.eda", "edadeal.",
            "wb.ru", "ozon.ru", "sbermarket.", "selfie."
        ]
        if any(b in d for b in known_sites): return False
        
        bad = ["ptr.", "static", "dynamic", "pool", "res", "host", "node", "ip-", 
               "cloudflare", "akamaized", "fastly", "local", "test", "cdn", "user",
               "traefik", "default", "svc", "cluster", "k8s"]
        if any(b in d for b in bad): return False
        return True
if __name__ == "__main__":
    app = RealityScannerApp()
    app.mainloop()