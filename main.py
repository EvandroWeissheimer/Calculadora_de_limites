import re
import sympy as sp
import tkinter as tk

# Paletas (janela e modal)

THEME = {
    "bg": "#0B1220",          
    "fg": "#E5E7EB",         
    "muted": "#9CA3AF",
    "input_bg": "#111827",     
    "input_fg": "#E5E7EB",     
    "input_insert": "#E5E7EB", 
    "button_bg": "#1F2937",
    "button_fg": "#E5E7EB",
    "button_active_bg": "#2563EB",
    "button_active_fg": "#FFFFFF",
    "accent": "#2563EB",
}

MODAL_COLORS = {
    "bg": "#111827",
    "fg": "#E5E7EB",
    "accent": "#2563EB",
    "accent_error": "#DC2626",
    "button_bg": "#374151",
    "button_fg": "#E5E7EB",
}

# ============== Modal custom ==============
class CustomModal(tk.Toplevel):
    """Janela modal customizada com cores configuráveis."""
    def __init__(self, parent, title, message, kind="info", colors=None):
        super().__init__(parent)
        self.parent = parent
        self.title(title)
        self.resizable(False, False)

        self.colors = colors or MODAL_COLORS
        self.configure(bg=self.colors["bg"])

        # Torna modal
        self.transient(parent)
        self.grab_set()

        # Ícone (i / !)
        accent = self.colors["accent"] if kind != "error" else self.colors["accent_error"]
        icon_canvas = tk.Canvas(self, width=44, height=44, bg=self.colors["bg"], highlightthickness=0)
        icon_canvas.grid(row=0, column=0, padx=(16, 8), pady=(16, 8), sticky="n")
        icon_canvas.create_oval(4, 4, 40, 40, fill=accent, outline=accent)
        icon_canvas.create_text(22, 22, text=("!" if kind == "error" else "i"),
                                fill="white", font=("Arial", 18, "bold"))

        # Mensagem
        lbl = tk.Label(
            self, text=message, bg=self.colors["bg"], fg=self.colors["fg"],
            wraplength=360, justify="left"
        )
        lbl.grid(row=0, column=1, padx=(0, 16), pady=(16, 8), sticky="w")

        # Botão OK
        btn = tk.Button(
            self, text="OK", command=self._close,
            bg=self.colors["button_bg"], fg=self.colors["button_fg"],
            activebackground=accent, activeforeground="white",
            relief="flat", padx=14, pady=6, cursor="hand2"
        )
        btn.grid(row=1, column=0, columnspan=2, pady=(0, 16))
        btn.focus_set()

        # Bind de teclas
        self.bind("<Return>", lambda e: self._close())
        self.bind("<Escape>", lambda e: self._close())

        # Layout
        self.columnconfigure(1, weight=1)

        # Centraliza em relação ao pai
        self.update_idletasks()
        self._center_on_parent()

        # Espera fechar
        self.wait_window(self)

    def _center_on_parent(self):
        px = self.parent.winfo_rootx()
        py = self.parent.winfo_rooty()
        pw = self.parent.winfo_width()
        ph = self.parent.winfo_height()

        sw = self.winfo_width()
        sh = self.winfo_height()

        x = px + (pw - sw) // 2
        y = py + (ph - sh) // 2
        self.geometry(f"+{x}+{y}")

    def _close(self):
        self.grab_release()
        self.destroy()


def show_modal(parent, title, message, kind="info"):
    CustomModal(parent, title, message, kind=kind, colors=MODAL_COLORS)

# ============== Normalização opcional ==============
def normalizar_expressao(txt: str) -> str:
    s = txt.strip()
    s = s.replace('^', '**')
    s = re.sub(r'\bln\s*\(', 'log(', s)
    s = re.sub(r'\bsen\s*\(', 'sin(', s, flags=re.IGNORECASE)
    s = re.sub(r'\btg\s*\(', 'tan(', s, flags=re.IGNORECASE)
    s = re.sub(r'\bctg\s*\(', 'cot(', s, flags=re.IGNORECASE)
    s = s.replace('∞', 'oo').replace('+oo', 'oo')
    s = re.sub(r'(?<=\d),(?=\d)', '.', s)
    return s

# ============== App ==============
def calcular_limite():
    """Lê a função e o ponto da GUI e calcula o limite."""
    x = sp.symbols('x', real=True)
    func_input_raw = entrada_funcao.get()
    ponto_input_raw = entrada_ponto.get()
    lado = var_lado.get()  # '', '+', '-'

    func_input = normalizar_expressao(func_input_raw)
    ponto_input = normalizar_expressao(ponto_input_raw)

    # Parse função
    try:
        func = sp.sympify(func_input, locals={'x': x})
    except (sp.SympifyError, SyntaxError):
        show_modal(janela, "Erro", "Função inválida.", kind="error")
        return

    # Parse ponto (aceita 0, 2, 1/2, pi/3, oo, -oo, inf, -inf)
    aliases = {
        'oo': sp.oo, '+oo': sp.oo, 'inf': sp.oo, '+inf': sp.oo,
        '-oo': -sp.oo, '-inf': -sp.oo
    }
    try:
        ponto = aliases.get(ponto_input.lower(), sp.sympify(ponto_input))
    except (sp.SympifyError, SyntaxError, ValueError):
        show_modal(janela, "Erro", "Ponto inválido.", kind="error")
        return

    direcao = lado if lado in ('+', '-') else '+-'

    try:
        limite = sp.limit(func, x, ponto, dir=direcao)
        seta = {'+': ' +', '-': ' -'}.get(lado, '')
        resultado_var.set(f"lim[x→{ponto_input}{seta}] {func_input} = {sp.sstr(limite)}")
    except Exception as e:
        show_modal(janela, "Erro ao calcular", f"Ocorreu um erro:\n{e}", kind="error")

def main():
    global janela, entrada_funcao, entrada_ponto, var_lado, resultado_var

    janela = tk.Tk()
    janela.title("Calculadora de Limites")
    janela.geometry("560x400")
    janela.configure(bg=THEME["bg"])

    # Helpers para aplicar tema facilmente
    def mk_label(parent, text, **kw):
        kw.setdefault('bg', THEME["bg"])
        kw.setdefault('fg', THEME["fg"])
        return tk.Label(parent, text=text, **kw)

    def mk_entry(parent, width, **kw):
        kw.setdefault('bg', THEME["input_bg"])
        kw.setdefault('fg', THEME["input_fg"])
        kw.setdefault('insertbackground', THEME["input_insert"])
        kw.setdefault('relief', 'flat')
        kw.setdefault('highlightthickness', 1)
        kw.setdefault('highlightbackground', '#2A3446')
        kw.setdefault('highlightcolor', THEME["accent"])
        return tk.Entry(parent, width=width, **kw)

    def mk_button(parent, text, cmd, **kw):
        kw.setdefault('bg', THEME["button_bg"])
        kw.setdefault('fg', THEME["button_fg"])
        kw.setdefault('activebackground', THEME["button_active_bg"])
        kw.setdefault('activeforeground', THEME["button_active_fg"])
        kw.setdefault('relief', 'flat')
        kw.setdefault('padx', 14)
        kw.setdefault('pady', 6)
        kw.setdefault('cursor', 'hand2')
        return tk.Button(parent, text=text, command=cmd, **kw)

    container = tk.Frame(janela, bg=THEME["bg"])
    container.pack(fill="both", expand=True, padx=16, pady=16)

    # Título
    mk_label(container, "Calculadora de Limites", font=("Arial", 14, "bold")).pack(pady=(0, 10))

    # Função
    mk_label(container, "Função f(x):").pack(anchor="w")
    entrada_funcao = mk_entry(container, width=56)
    entrada_funcao.insert(0, "sin(x)/x")
    entrada_funcao.pack(fill="x", pady=(2, 10))

    # Ponto
    mk_label(container, "Ponto para o qual x tende (ex: 0, 2, pi/3, oo, -oo):").pack(anchor="w")
    entrada_ponto = mk_entry(container, width=20)
    entrada_ponto.insert(0, "0")
    entrada_ponto.pack(pady=(2, 10), anchor="w")

    # Lado
    mk_label(container, "Tendência (lado):").pack(anchor="w")
    var_lado = tk.StringVar(value="")

    lado_frame = tk.Frame(container, bg=THEME["bg"])
    lado_frame.pack(anchor="w", pady=(2, 12))

    # Radiobuttons
    def mk_radio(text, value):
        return tk.Radiobutton(
            lado_frame, text=text, variable=var_lado, value=value,
            bg=THEME["bg"], fg=THEME["fg"],
            activebackground=THEME["bg"], activeforeground=THEME["fg"],
            selectcolor=THEME["bg"], highlightthickness=0, cursor="hand2"
        )

    mk_radio("Ambos os lados", "").pack(side="left", padx=6)
    mk_radio("Pela direita (+)", "+").pack(side="left", padx=6)
    mk_radio("Pela esquerda (-)", "-").pack(side="left", padx=6)

    # Botão calcular
    mk_button(container, "Calcular Limite", calcular_limite).pack(pady=6)

    # Resultado
    resultado_var = tk.StringVar()
    tk.Label(
        container, textvariable=resultado_var, bg=THEME["bg"], fg=THEME["accent"],
        wraplength=520, justify="center"
    ).pack(pady=8)

    # Rodapé discreto (usa fg custom sem conflito)
    mk_label(container, "Dica: use ** para potência (ex.: x**2) • pi, E, oo", fg=THEME["muted"]).pack(pady=(8, 0))

    janela.mainloop()

if __name__ == '__main__':
    main()
