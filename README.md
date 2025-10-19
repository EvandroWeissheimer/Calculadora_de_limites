# Calculadora de Limites (SymPy + Tkinter)

App desktop simples para **calcular limites** de funções de uma variável real usando **SymPy** com interface em **Tkinter**.  
Suporta limites em pontos finitos, em \(+\infty\) e \(-\infty\), e escolha do **lado da tendência**.

---

## 📦 Requisitos

- **Python 3.10+**
- **SymPy**
- **Tkinter** (já vem com o Python no Windows; no Linux/macOS pode exigir pacote do sistema)

### Instalação rápida

```bash
# (opcional) criar e ativar um venv
python3 -m venv .venv
source .venv/bin/activate         # Linux/macOS
# .venv\Scripts\activate        # Windows

# instalar dependências
pip install sympy
```

#### Tkinter por SO

- **Ubuntu/Debian**
  ```bash
  sudo apt install python3-tk
  ```
- **Fedora**
  ```bash
  sudo dnf install python3-tkinter
  ```
- **Arch**
  ```bash
  sudo pacman -S tk
  ```
- **Windows**
  - Já incluído no Python do python.org.
- **macOS (Homebrew)**
  ```bash
  brew install tcl-tk
  # use o Python do Homebrew e siga as instruções pós-instalação do brew, se aparecerem
  ```

---

## ▶️ Executar

Coloque o `main.py` na pasta do projeto e rode:

```bash
python main.py
```

A janela principal abrirá. Para encerrar, feche a janela (clicar no **X**).  
**Nota:** se você apertar `Ctrl+C` no terminal enquanto a janela estiver aberta, verá `KeyboardInterrupt` — isso é normal.

---

## 🧠 Como funcionam as **entradas** (inputs)

A interface tem três campos:

1) **Função f(x)**  
2) **Ponto** para o qual x tende  
3) **Tendência (lado)**: ambos, direita (+) ou esquerda (-)

### 1) Campo “Função f(x)”
- **Variável:** `x` (real).
- **Operadores:** `+  -  *  /  **`  
  > **Potência é `**`** (ex.: `x**2`). Não use `^`.
- **Parênteses:** `(` `)`
- **Números:** inteiros (`2`), racionais (`1/3`), decimais (`0.25`) — **use ponto**, não vírgula.
- **Constantes:** `pi`, `E` (número de Euler), `oo` (∞) (infinito positivo), `-oo` (−∞) (infinito negativo), `GoldenRatio` (razão áurea), `EulerGamma` (constante de Euler–Mascheroni).
- **Funções** (padrão SymPy):
  - trigonométricas: `sin`, `cos`, `tan`, `cot`, `sec`, `csc`, inversas `asin`, `acos`, `atan`, …
  - hiperbólicas: `sinh`, `cosh`, `tanh`, …
  - exponenciais/log: `exp(x)`, `log(x)` (natural), `log(x, 2)` (base 2)
  - outras: `sqrt(x)`, `abs(x)`, `sign(x)`, `floor(x)`, `ceiling(x)`, `Heaviside(x)`, `Max(a,b)`, `Min(a,b)`
  - **Por partes:** `Piecewise((expr1, cond1), (expr2, True))`

**Exemplos válidos**
- `sin(x)/x`
- `(1 - cos(x))/x**2`
- `abs(x)/x`
- `log(x, 2)`
- `Piecewise((x**2, x<0), (x, True))`

### 2) Campo “Ponto”
Aceita valores **numéricos** ou **constantes** do SymPy:
- `0`, `2`, `-3.5`, `1/2`, `sqrt(2)`, `pi/3`, `E`
- Infinito: `oo`, `-oo` (também `inf`, `-inf`)
- **Não** use a variável `x` aqui; precisa ser algo que avalie para um número/constante.

**Exemplos**
- `0`
- `pi/3`
- `oo`
- `-oo`
- `1/2`

### 3) Tendência (lado)
- **Ambos os lados** (padrão): calcula `dir="+-"`  
- **Direita**: `+` (limite quando x → a⁺)  
- **Esquerda**: `-` (limite quando x → a⁻)

---

## ✅ Exemplos de uso

| f(x)                    | ponto | lado | Resultado esperado (ideia)        |
|-------------------------|-------|------|-----------------------------------|
| `sin(x)/x`              | `0`   | ambos| `1`                               |
| `(1-cos(x))/x**2`       | `0`   | ambos| `1/2`                             |
| `abs(x)/x`              | `0`   | `+`  | `1`                               |
| `abs(x)/x`              | `0`   | `-`  | `-1`                              |
| `1/x`                   | `0`   | ambos| diverge (∞ ou -∞ conforme o lado) |
| `log(x)`                | `oo`  | ambos| `oo`                              |
| `log(x)`                | `0`   | `+`  | `-oo`                             |

> O resultado é exibido em texto logo abaixo do botão **Calcular Limite**.  
> Em caso de **erro**, aparece um **modal** (com cores customizadas) explicando o motivo.

---

## 🧩 Normalização de entrada (qualidades de vida)

O app inclui um “patch” para aceitar variações comuns:

- Converte `^` → `**`
- `ln(` → `log(`
- Termos PT-BR: `sen(` → `sin(`, `tg(` → `tan(`, `ctg(` → `cot(`
- Converte `∞` → `oo`
- Troca **vírgula decimal** entre dígitos por **ponto** (ex.: `1,5` → `1.5`) sem afetar coisas como `log(x, 2)`

> Ainda assim, **prefira** digitar com a sintaxe padrão da SymPy quando possível.

---

## 🎨 Tema e cores

- A janela principal usa um **tema dark** (veja o dicionário `THEME` no topo do arquivo).
- As mensagens de erro/aviso/sucesso usam um **modal customizado** com paleta separada (`MODAL_COLORS`).
- Para mudar cores, **edite os dicionários** `THEME` e `MODAL_COLORS`.
- Para **mostrar um modal de sucesso** após cada cálculo, deixe **ativa** a linha:
  ```python
  show_modal(janela, "Pronto", "Limite calculado com sucesso!", kind="info")
  ```
  (Ela já está presente em `calcular_limite()`; comente se não quiser.)

> **macOS:** widgets nativos podem ignorar `bg/fg` em botões padrão. O exemplo usa widgets “clássicos” do `tkinter` para maximizar compatibilidade. Se quiser `ttk`, será preciso configurar `Style`.

---

## ⛑️ Tratamento de erros

- **Função inválida:** modal “Função inválida.”
- **Ponto inválido:** modal “Ponto inválido.”
- **Erro no cálculo:** modal com a exceção (`Erro ao calcular`).
- **KeyboardInterrupt:** aparece no terminal se você interromper o `mainloop()` com `Ctrl+C`. Não é bug.

---

## 🧪 Dicas & Depuração

Verifique se as bibliotecas estão acessíveis:

```bash
python -c "import tkinter as tk; print('tkinter OK')"
python -c "import sympy as sp; print('sympy', sp.__version__)"
```

Se uma cor não aplicar:
- Confirme que o widget é do **tkinter “clássico”** (não `ttk`).
- No Linux, o **tema do sistema** geralmente respeita as cores definidas.

---

## 🧷 Problemas comuns

- **TypeError: tkinter.Label() got multiple values for keyword argument 'fg'**  
  Acontece quando a função fábrica já define `fg` e você passa `fg` de novo. O projeto usa `setdefault` nas fábricas (`mk_label`, `mk_entry`, `mk_button`), então você pode **sobrescrever** `fg` sem conflito.

- **SyntaxError / SympifyError ao digitar função**  
  Verifique sintaxe SymPy: potência `**`, decimal com **ponto**, funções em inglês (`sin`, `cos`, `log`), etc.

---

## 📝 Atalhos úteis

- **Enter** no modal: fecha o modal.  
- **Esc** no modal: fecha o modal.

---

## 📁 Estrutura recomendada

```
CalculadoraLimites/
├─ main.py
├─ README.md
└─ .venv/        (opcional)
```

---

## 📜 Licença

Uso educacional/livre. Ajuste e distribua conforme necessário no seu contexto.

---

## 🙋 FAQ rápido

**Posso usar `sen(x)`?**  
Sim, o app converte `sen(` para `sin(` automaticamente.

**Posso digitar `∞`?**  
Sim, é convertido para `oo`.

**Posso usar vírgula como decimal (`1,5`)?**  
Sim, se for **dentro de números**. Em parâmetros de funções (ex.: `log(x, 2)`), a vírgula permanece.

**Funciona com limite lateral?**  
Sim. Selecione `+` (direita) ou `-` (esquerda). Se deixar “Ambos os lados”, o SymPy usa `'+-'`.