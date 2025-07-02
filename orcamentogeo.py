import tkinter as tk
from tkinter import messagebox
import math
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import datetime

# Função para formatar valor em moeda brasileira (R$ 13.406,75)
def formata_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ---------------- TABELA DE AVERBAÇÃO ----------------
def calcular_averbacao(valor):
    tabela = [
        (0.01, 28493.00, 71.40),
        (28493.01, 37806.00, 132.03),
        (37806.01, 47116.00, 166.49),
        (47116.01, 56428.00, 199.10),
        (56428.01, 65739.00, 231.71),
        (65739.01, 75052.00, 264.30),
        (75052.01, 93675.00, 329.51),
        (93675.01, 112298.00, 386.06),
        (112298.01, 130921.00, 439.77),
        (130921.01, 149546.00, 490.60),
        (149546.01, 168169.00, 538.58),
        (168169.01, 205414.00, 641.75),
        (205414.01, 242661.00, 739.25),
        (242661.01, 279909.00, 831.05),
        (279909.01, 317153.00, 917.24),
        (317153.01, 354400.00, 997.73),
        (354400.01, 447517.00, 1225.34),
        (447517.01, 540633.00, 1438.76),
        (540633.01, 633747.00, 1638.08),
        (633747.01, 726865.00, 1823.33),
        (726865.01, 819981.00, 1953.03),
        (819981.01, 1006213.00, 2270.08),
        (1006213.01, 1192445.00, 2539.72),
        (1192445.01, 1378677.00, 2762.73),
        (1378677.01, 1564910.00, 2939.29),
        (1564910.01, 1751140.00, 3070.78),
        (1751140.01, 1937376.00, 3156.13),
        (1937376.01, 2123605.00, 3195.50),
        (2123605.01, 2309842.00, 3268.03),
        (2309842.01, 2496071.00, 3370.81),
        (2496071.01, 2682304.00, 3498.60),
        (2682304.01, float('inf'), 3626.42)
    ]
    for minimo, maximo, valor_faixa in tabela:
        if minimo <= valor <= maximo:
            return valor_faixa
    return 0

# ---------------- FUNÇÃO PRINCIPAL ----------------
def calcular():
    try:
        area = float(area_entry.get())
        salario = float(salario_entry.get())
        vti = float(vti_entry.get())
        desmembramentos = int(desmembramentos_entry.get())

        dentro_br = br_var.get()
        incluir_averbacao = averbacao_var.get()
        incluir_ccir = ccir_var.get()
        incluir_itr = itr_var.get()
        incluir_car = car_var.get()
        incluir_firma = firma_var.get()

        # Serviço técnico
        if area <= 16:
            servico_tecnico = 3040.00
        else:
            servico_tecnico = math.sqrt(area) * (salario / 2)

        # Averbação
        averbacao_total = 0
        valor_base = area * vti
        if incluir_averbacao:
            valor_faixa = calcular_averbacao(valor_base)
            certidoes = 1 + desmembramentos
            averbacao_total = valor_faixa + (certidoes * 39.50)

        # BR-429
        valor_br = 2500.00 if dentro_br else 0

        # Regularizações individuais
        valor_ccir = 304.00 if incluir_ccir else 0
        valor_itr = 304.00 if incluir_itr else 0
        valor_car = 304.00 if incluir_car else 0

        # Reconhecimento de firma
        valor_firma = 200.00 if incluir_firma else 0

        # Desmembramentos
        valor_desmembramento = desmembramentos * 2508.00

        # Total geral
        total = sum([
            servico_tecnico,
            averbacao_total,
            valor_ccir,
            valor_itr,
            valor_car,
            valor_firma,
            valor_br,
            valor_desmembramento
        ])

        # Resultado formatado
        resultado = f''' 
Cliente: {nome_entry.get()}
Identificação do imóvel: {identificacao_entry.get()}
Situação/finalidade: {situacao_entry.get()}

🧮 ORÇAMENTO DETALHADO:
- Serviço técnico: {formata_brl(servico_tecnico)}
- Averbação + certidões: {formata_brl(averbacao_total)}
- CCIR: {formata_brl(valor_ccir)}
- ITR: {formata_brl(valor_itr)}
- CAR: {formata_brl(valor_car)}
- Reconhecimento de firma: {formata_brl(valor_firma)}
- Desmembramentos: {formata_brl(valor_desmembramento)}
- Imóveis lançado no SIGEF pelo Terra Legal: {formata_brl(valor_br)}

💰 TOTAL GERAL: {formata_brl(total)}
'''
        messagebox.showinfo("Orçamento Gerado", resultado)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos corretamente.")

# ---------------- CONFIGURAÇÃO DO PDF ----------------
def gerar_pdf():
    nome = nome_entry.get()
    identificacao = identificacao_entry.get()
    situacao = situacao_entry.get()
    data = datetime.date.today().strftime('%d/%m/%Y')

    try:
        area = float(area_entry.get())
        salario = float(salario_entry.get())
        vti = float(vti_entry.get())
        desmembramentos = int(desmembramentos_entry.get())

        dentro_br = br_var.get()
        incluir_averbacao = averbacao_var.get()
        incluir_ccir = ccir_var.get()
        incluir_itr = itr_var.get()
        incluir_car = car_var.get()
        incluir_firma = firma_var.get()

        # Serviço técnico
        if area <= 16:
            servico_tecnico = 3040.00
        else:
            servico_tecnico = math.sqrt(area) * (salario / 2)

        # Averbação
        averbacao_total = 0
        valor_base = area * vti
        if incluir_averbacao:
            valor_faixa = calcular_averbacao(valor_base)
            certidoes = 1 + desmembramentos
            averbacao_total = valor_faixa + (certidoes * 39.50)

        # BR-429
        valor_br = 2500.00 if dentro_br else 0

        # Regularizações
        valor_ccir = 304.00 if incluir_ccir else 0
        valor_itr = 304.00 if incluir_itr else 0
        valor_car = 304.00 if incluir_car else 0
        valor_firma = 200.00 if incluir_firma else 0
        valor_desmembramento = desmembramentos * 2508.00

        total = sum([
            servico_tecnico,
            averbacao_total,
            valor_ccir,
            valor_itr,
            valor_car,
            valor_firma,
            valor_br,
            valor_desmembramento
        ])

        # Criar PDF
        nome_arquivo = f"orcamento_{nome.replace(' ', '_')}.pdf"
        c = canvas.Canvas(nome_arquivo, pagesize=A4)
        largura, altura = A4

        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, altura - 50, "Orçamento de Georreferenciamento")
        c.setFont("Helvetica", 10)
        c.drawString(50, altura - 70, f"Cliente: {nome}")
        c.drawString(50, altura - 85, f"Data: {data}")
        c.drawString(50, altura - 100, f"Identificação do imóvel: {identificacao}")
        c.drawString(50, altura - 115, f"Situação/finalidade: {situacao}")

        y = altura - 150
        c.setFont("Helvetica", 11)
        c.drawString(50, y, f"Serviço técnico: {formata_brl(servico_tecnico)}"); y -= 15
        c.drawString(50, y, f"Averbação + certidões: {formata_brl(averbacao_total)}"); y -= 15
        c.drawString(50, y, f"CCIR: {formata_brl(valor_ccir)}"); y -= 15
        c.drawString(50, y, f"ITR: {formata_brl(valor_itr)}"); y -= 15
        c.drawString(50, y, f"CAR: {formata_brl(valor_car)}"); y -= 15
        c.drawString(50, y, f"Reconhecimento de firma: {formata_brl(valor_firma)}"); y -= 15
        c.drawString(50, y, f"Desmembramentos: {formata_brl(valor_desmembramento)}"); y -= 15
        c.drawString(50, y, f"Cadastro SIGEF (Terra Legal): {formata_brl(valor_br)}"); y -= 25

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"TOTAL GERAL: {formata_brl(total)}")

        c.save()
        messagebox.showinfo("PDF Gerado", f"PDF salvo como: {nome_arquivo}")
    except Exception as e:
        messagebox.showerror("Erro", f"Verifique os dados preenchidos para gerar o PDF.\n{e}")

# ---------------- INTERFACE TKINTER ----------------
root = tk.Tk()
root.title("Orçamento de Georreferenciamento")

# Campos principais
tk.Label(root, text="Nome do cliente:").grid(row=0, column=0)
nome_entry = tk.Entry(root, width=40)
nome_entry.grid(row=0, column=1, columnspan=2)

tk.Label(root, text="Área (ha):").grid(row=1, column=0)
area_entry = tk.Entry(root)
area_entry.grid(row=1, column=1)

tk.Label(root, text="Salário mínimo (R$):").grid(row=2, column=0)
salario_entry = tk.Entry(root)
salario_entry.insert(0, "1518.00")
salario_entry.grid(row=2, column=1)

tk.Label(root, text="Valor médio VTI/ha:").grid(row=3, column=0)
vti_entry = tk.Entry(root)
vti_entry.insert(0, "17769.94")
vti_entry.grid(row=3, column=1)

tk.Label(root, text="Qtde de desmembramentos:").grid(row=4, column=0)
desmembramentos_entry = tk.Entry(root)
desmembramentos_entry.insert(0, "0")
desmembramentos_entry.grid(row=4, column=1)

tk.Label(root, text="Identificação do imóvel:").grid(row=5, column=0)
identificacao_entry = tk.Entry(root, width=40)
identificacao_entry.grid(row=5, column=1, columnspan=2)

tk.Label(root, text="Situação/finalidade:").grid(row=6, column=0)
situacao_entry = tk.Entry(root, width=40)
situacao_entry.grid(row=6, column=1, columnspan=2)

# Checkboxes
br_var = tk.BooleanVar()
tk.Checkbutton(root, text="Cadastro SIGEF (Terra Legal)", variable=br_var).grid(row=7, column=0, columnspan=2, sticky="w")

averbacao_var = tk.BooleanVar()
tk.Checkbutton(root, text="Incluir Averbação no Cartório", variable=averbacao_var).grid(row=8, column=0, columnspan=2, sticky="w")

ccir_var = tk.BooleanVar()
itr_var = tk.BooleanVar()
car_var = tk.BooleanVar()
tk.Checkbutton(root, text="Incluir CCIR", variable=ccir_var).grid(row=9, column=0, sticky="w")
tk.Checkbutton(root, text="Incluir ITR", variable=itr_var).grid(row=9, column=1, sticky="w")
tk.Checkbutton(root, text="Incluir CAR", variable=car_var).grid(row=9, column=2, sticky="w")

firma_var = tk.BooleanVar()
tk.Checkbutton(root, text="Reconhecimento de firma", variable=firma_var).grid(row=10, column=0, columnspan=2, sticky="w")

# Botão
tk.Button(root, text="Calcular Orçamento", command=calcular, bg="#4CAF50", fg="white", padx=10, pady=5).grid(row=11, column=0, columnspan=3, pady=10)
tk.Button(root, text="Gerar PDF", command=gerar_pdf, bg="#2196F3", fg="white", padx=10, pady=5).grid(row=12, column=0, columnspan=3, pady=5)

root.mainloop()
