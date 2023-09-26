import os
import base64
import matplotlib.pyplot as plt
import seaborn as sns
from jinja2 import Template
from weasyprint import HTML

# Dados fictícios
meses = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]
vendas = [1500, 2000, 1700, 2200, 1950, 1800, 2300, 2100, 2400, 2050, 2600, 2750]
meta = [1800] * 12  # Meta de vendas fixa
porcentagem_cumprimento = [round((v / m) * 100, 1) for v, m in zip(vendas, meta)]

# Configurações do Seaborn
sns.set_theme(style="whitegrid")

# Criar um gráfico de barras com sombra
plt.figure(figsize=(10, 6))
bar = plt.bar(meses, vendas, color=sns.color_palette("pastel")[0])
plt.bar_label(bar, fmt='%d')

# Adicionar um gráfico de linha para a meta de vendas
plt.plot(meses, meta, color='red', marker='o', linestyle='dashed', linewidth=2, markersize=6, label='Meta')

# Adicionar título e rótulos aos eixos
plt.title('Vendas Mensais em 2023')
plt.xlabel('Meses')
plt.ylabel('Vendas (R$)')
plt.xticks(rotation=45)
plt.legend()

# Ajustar o layout e salvar o gráfico como uma imagem PNG com alta resolução
plt.tight_layout()
caminho_grafico = 'grafico_vendas.png'
plt.savefig(caminho_grafico, dpi=300, bbox_inches='tight')

# Codificar a imagem em base64
with open(caminho_grafico, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()

# Template HTML com estilos e layout aprimorados
template_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Relatório de Vendas</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            font-family: Arial, sans-serif;
        }
        .container {
            width: 80%;
            margin-top: 20px;
            margin: auto;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px auto;
        }
        th, td {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }
        th {
            background-color: #f2f2f2;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        img {
            max-width: 100%;
            height: 100%;
            margin: 20px auto;
        }
        h1 {
            text-align: center;
        }
    </style>
</head>
<body>
    <h1>Relatório de Vendas 2023</h1>
    <div class="container">
        <img src="data:image/png;base64,{{ encoded_string }}" alt="Gráfico de Vendas">
    </div>
    <div class="container">
        <table>
            <tr>
                <th>Mês</th>
                <th>Vendas (R$)</th>
                <th>Meta (R$)</th>
                <th>% Cumprimento</th>
            </tr>
            {% for mes, venda, m, pct in dados %}
            <tr>
                <td>{{ mes }}</td>
                <td>{{ venda }}</td>
                <td>{{ m }}</td>
                <td>{{ pct }}%</td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
"""

# Dados para renderizar o template
dados_render = {
    'encoded_string': encoded_string,
    'dados': zip(meses, vendas, meta, porcentagem_cumprimento)
}

# Renderizar o template HTML com os dados
template = Template(template_html)
html_renderizado = template.render(**dados_render)

# Caminho para salvar o PDF
caminho_pdf = 'relatorio_vendas.pdf'

# Usar WeasyPrint para gerar o PDF a partir do HTML renderizado
HTML(string=html_renderizado).write_pdf(caminho_pdf)
