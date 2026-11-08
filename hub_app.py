import builtins
import ctypes
import os
import queue
import runpy
import subprocess
import sys
import threading
import time
import tkinter as tk
import traceback
import webbrowser
from pathlib import Path
from tkinter import messagebox, ttk
from urllib.parse import quote_plus


BASE_DIR = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
BOT_DIR = (Path(getattr(sys, "_MEIPASS", BASE_DIR)) / "bots") if getattr(sys, "frozen", False) else BASE_DIR
BOTS = [
    ("Robô — versão 1", "robo.py"),
    ("Bot v2", "bot.v2.py"),
    ("Bot v3", "bot.v3.py"),
    ("Bot v3.5 — web e YouTube", "botv3.5.py"),
]
STORES = {
    "AliExpress": "https://www.aliexpress.com/wholesale?SearchText=",
    "Mercado Livre": "https://lista.mercadolivre.com.br/",
    "Amazon Brasil": "https://www.amazon.com.br/s?k=",
    "Shopee": "https://shopee.com.br/search?keyword=",
}
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_KEYUP = 0x0002


def type_unicode(text, interval=0.035):
    lines = text.split("\n")
    if os.name != "nt":
        from pynput.keyboard import Controller, Key
        keyboard = Controller()
        for line_index, line in enumerate(lines):
            for char in line.rstrip("\r"):
                keyboard.type(char)
                time.sleep(interval)
            if line_index < len(lines) - 1:
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
                time.sleep(interval)
        return

    user32 = ctypes.windll.user32
    for line_index, line in enumerate(lines):
        for char in line.rstrip("\r"):
            encoded = char.encode("utf-16-le")
            units = [int.from_bytes(encoded[i:i + 2], "little") for i in range(0, len(encoded), 2)]
            for unit in units:
                user32.keybd_event(0, unit, KEYEVENTF_UNICODE, 0)
                user32.keybd_event(0, unit, KEYEVENTF_UNICODE | KEYEVENTF_KEYUP, 0)
            time.sleep(interval)
        if line_index < len(lines) - 1:
            user32.keybd_event(0x0D, 0, 0, 0)
            user32.keybd_event(0x0D, 0, KEYEVENTF_KEYUP, 0)
            time.sleep(interval)


class BotWindow:
    """Runs a legacy input()/print() bot inside its own window, without a console."""
    def __init__(self, script_path):
        candidate = Path(script_path)
        self.script_path = candidate if candidate.is_absolute() else BOT_DIR / candidate
        self.output_queue = queue.Queue()
        self.input_requests = queue.Queue()
        self.input_responses = queue.Queue()
        self.root = tk.Tk()
        self.root.title(self.script_path.stem)
        self.root.geometry("780x580")
        self.root.configure(bg="#101827")

        header = tk.Frame(self.root, bg="#17243a", padx=18, pady=12)
        header.pack(fill="x")
        tk.Label(header, text=self.script_path.stem, bg="#17243a", fg="#f4f7fb",
                 font=("Segoe UI", 14, "bold")).pack(anchor="w")

        self.output = tk.Text(self.root, bg="#101827", fg="#e5edf7", insertbackground="white",
                              font=("Consolas", 11), wrap="word", relief="flat", padx=18, pady=16,
                              state="disabled")
        self.output.pack(fill="both", expand=True, padx=12, pady=10)
        row = tk.Frame(self.root, bg="#101827")
        row.pack(fill="x", padx=12, pady=(0, 12))
        self.entry = tk.Entry(row, font=("Segoe UI", 11), relief="flat", state="disabled")
        self.entry.pack(side="left", fill="x", expand=True, ipady=9, padx=(0, 8))
        self.entry.bind("<Return>", self.send_input)
        self.send_button = tk.Button(row, text="Enviar", command=self.send_input, bg="#4f7cff", fg="white",
                                     activebackground="#3d68df", activeforeground="white", relief="flat",
                                     font=("Segoe UI", 10, "bold"), padx=18, pady=8, state="disabled")
        self.send_button.pack(side="right")
        self.root.after(60, self.poll_queues)
        threading.Thread(target=self.run_script, daemon=True).start()

    def write(self, text):
        self.output_queue.put(text)

    def run_script(self):
        owner = self

        class Stream:
            encoding = "utf-8"

            def write(self, text):
                owner.write(text)
                return len(text)

            def flush(self):
                pass

        original_input = builtins.input

        def gui_input(prompt=""):
            if prompt:
                owner.write(prompt)
            owner.input_requests.put(True)
            return owner.input_responses.get()

        try:
            builtins.input = gui_input
            sys.stdout = Stream()
            sys.stderr = Stream()
            runpy.run_path(str(self.script_path), run_name="__main__")
        except SystemExit:
            pass
        except Exception:
            self.write(traceback.format_exc())
        finally:
            builtins.input = original_input
            self.input_requests.put(None)

    def send_input(self, _event=None):
        answer = self.entry.get()
        self.entry.delete(0, "end")
        self.write(answer + "\n")
        self.input_responses.put(answer)
        self.entry.configure(state="disabled")
        self.send_button.configure(state="disabled")

    def poll_queues(self):
        while True:
            try:
                chunk = self.output_queue.get_nowait()
            except queue.Empty:
                break
            self.output.configure(state="normal")
            self.output.insert("end", chunk)
            self.output.see("end")
            self.output.configure(state="disabled")

        while True:
            try:
                request = self.input_requests.get_nowait()
            except queue.Empty:
                break
            if request is None:
                self.output.configure(state="normal")
                self.output.insert("end", "\n\nPrograma encerrado. Você pode fechar esta janela.\n")
                self.output.configure(state="disabled")
            else:
                self.entry.configure(state="normal")
                self.send_button.configure(state="normal")
                self.entry.focus_set()
        self.root.after(60, self.poll_queues)


class HubApp:
    def __init__(self, root):
        self.root = root
        root.title("Hub dos meus bots")
        root.geometry("620x760")
        root.minsize(560, 680)
        root.configure(bg="#0b1220")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#0b1220")
        style.configure("TLabel", background="#0b1220", foreground="#d8e2f0", font=("Segoe UI", 10))
        style.configure("Title.TLabel", background="#0b1220", foreground="white", font=("Segoe UI", 23, "bold"))
        style.configure("Section.TLabel", background="#0b1220", foreground="#91b4ff", font=("Segoe UI", 12, "bold"))
        style.configure("TButton", font=("Segoe UI", 10), padding=9)
        style.configure("Accent.TButton", background="#4f7cff", foreground="white", padding=10,
                        font=("Segoe UI", 10, "bold"))
        style.map("Accent.TButton", background=[("active", "#3e68dd")])
        style.configure("TCombobox", padding=7)

        frame = ttk.Frame(root, padding=24)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="MEU HUB", style="Title.TLabel").pack(anchor="w")
        ttk.Label(frame, text="Seus bots e atalhos em um só lugar").pack(anchor="w", pady=(2, 18))
        ttk.Label(frame, text="ESCOLHA UM BOT", style="Section.TLabel").pack(anchor="w", pady=(0, 8))
        for label, filename in BOTS:
            ttk.Button(frame, text=label, style="Accent.TButton",
                       command=lambda n=label, f=filename: self.open_bot(n, f)).pack(fill="x", pady=4)

        ttk.Separator(frame).pack(fill="x", pady=17)
        ttk.Label(frame, text="BUSCAR UM PRODUTO", style="Section.TLabel").pack(anchor="w")
        self.store = tk.StringVar(value="AliExpress")
        ttk.Combobox(frame, textvariable=self.store, values=list(STORES), state="readonly").pack(fill="x", pady=(8, 5))
        self.product = ttk.Entry(frame)
        self.product.pack(fill="x", pady=4, ipady=5)
        self.product.insert(0, "Nome do produto")
        self.product.bind("<FocusIn>", self.clear_product_hint)
        ttk.Button(frame, text="Pesquisar na loja", style="Accent.TButton", command=self.search_store).pack(fill="x", pady=4)

        ttk.Separator(frame).pack(fill="x", pady=17)
        ttk.Label(frame, text="AUTO TYPER", style="Section.TLabel").pack(anchor="w")
        ttk.Label(frame, text="Escreva o texto. Depois terá 5 segundos para selecionar o campo de destino.",
                  wraplength=540).pack(anchor="w", pady=(4, 8))
        self.text_box = tk.Text(frame, height=5, wrap="word", font=("Segoe UI", 10), relief="flat",
                                bg="#17243a", fg="white", insertbackground="white", padx=10, pady=9)
        self.text_box.pack(fill="x")
        self.type_button = ttk.Button(frame, text="Começar a digitar", style="Accent.TButton", command=self.start_typer)
        self.type_button.pack(fill="x", pady=8)
        self.status = tk.StringVar(value="Pronto")
        ttk.Label(frame, textvariable=self.status).pack(anchor="w", pady=(2, 0))
        ttk.Button(frame, text="Fechar hub", command=root.destroy).pack(anchor="e", pady=(18, 0))

    def clear_product_hint(self, _event):
        if self.product.get() == "Nome do produto":
            self.product.delete(0, "end")

    def open_bot(self, label, filename):
        path = BOT_DIR / filename
        if not path.is_file():
            messagebox.showerror("Arquivo não encontrado", f"Não encontrei {filename}.\nMantenha os bots na mesma pasta do HubBots.exe.")
            return
        if getattr(sys, "frozen", False):
            command = [sys.executable, "--bot", filename]
        else:
            command = [sys.executable, str(Path(__file__).resolve()), "--bot", str(path)]
        try:
            subprocess.Popen(command, cwd=BASE_DIR,
                             creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            self.status.set(f"{label} aberto em outra janela.")
        except Exception as exc:
            messagebox.showerror("Não foi possível abrir", str(exc))

    def search_store(self):
        product = self.product.get().strip()
        if not product or product == "Nome do produto":
            messagebox.showinfo("Produto", "Digite o nome do produto que deseja buscar.")
            return
        store = self.store.get()
        webbrowser.open(STORES[store] + quote_plus(product))
        self.status.set(f"Busca por {product} aberta em {store}.")

    def start_typer(self):
        text = self.text_box.get("1.0", "end-1c")
        if not text:
            messagebox.showinfo("Auto Typer", "Digite o texto primeiro.")
            return
        self.type_button.configure(state="disabled")
        self.countdown(5, text)

    def countdown(self, remaining, text):
        if remaining:
            self.status.set(f"Clique no campo de destino: {remaining}...")
            self.root.after(1000, self.countdown, remaining - 1, text)
        else:
            self.status.set("Digitando...")
            threading.Thread(target=self.type_text, args=(text,), daemon=True).start()

    def type_text(self, text):
        try:
            type_unicode(text)
            self.root.after(0, lambda: self.status.set("Texto digitado."))
        except Exception as exc:
            self.root.after(0, lambda: messagebox.showerror("Auto Typer", str(exc)))
        finally:
            self.root.after(0, lambda: self.type_button.configure(state="normal"))


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--bot":
        BotWindow(sys.argv[2])
        tk.mainloop()
    else:
        window = tk.Tk()
        HubApp(window)
        window.mainloop()
