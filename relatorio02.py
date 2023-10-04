import os
import base64
import matplotlib.pyplot as plt
import seaborn as sns
from jinja2 import Template
from weasyprint import HTML

def gerar_grafico(meses, vendas, meta, grafico):
    #Gera o gráfico de vendas e salva como uma imagem PNG.
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))
    bar = plt.bar(meses, vendas, color=sns.color_palette("pastel")[0])
    plt.bar_label(bar, fmt='%d')
    plt.plot(meses, meta, color='red', marker='o', linestyle='dashed', linewidth=2, markersize=6, label='Meta')
    plt.title('Vendas Mensais em 2023')
    plt.xlabel('Meses')
    plt.ylabel('Vendas (R$)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(grafico, dpi=300, bbox_inches='tight')

def codificar_imagem(grafico):
    #Codifica a imagem em base64. Único jeito que eu consegui inserir a imagem no pdf.
    with open(grafico, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def renderizar_html(string_codificada, dados):
    #Renderiza o HTML com a imagem e os dados codificados.
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
            <img src="data:image/png;base64,{{ string_codificada }}" alt="Gráfico de Vendas">
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
    template = Template(template_html)
    return template.render(string_codificada=string_codificada, dados=dados)

def gerar_pdf(html_renderizado, caminho_pdf):
    #Gera o PDF a partir do HTML renderizado.
    HTML(string=html_renderizado).write_pdf(caminho_pdf)

def gerar_relatorio_pdf():
    
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
             'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    vendas = [1500, 2000, 1700, 2200, 1950, 1800, 2300, 2100, 2400, 2050, 2600, 2750]
    meta = [1800] * 12
    porcentagem_cumprimento = [round((v / m) * 100, 1) for v, m in zip(vendas, meta)]
    
    grafico = 'grafico_vendas.png'
    gerar_grafico(meses, vendas, meta, grafico) #Gera o gráfico com os parâmetros inseridos e o nome repassado na variável "grafico".
    
    string_codificada = codificar_imagem(grafico) #Codifica a imagem/grafico gerado para ser inserido no HTML
    
    html_renderizado = renderizar_html(string_codificada, zip(meses, vendas, meta, porcentagem_cumprimento)) #Renderiza o HTML criado.
    
    caminho_pdf = 'relatorio_vendas.pdf'
    gerar_pdf(html_renderizado, caminho_pdf) #Gera um PDF baseado no HTML renderizado.

if __name__ == '__main__':
    gerar_relatorio_pdf()
