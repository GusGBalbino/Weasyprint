
import os
import base64
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from jinja2 import Template
from weasyprint import HTML

def dados_csv(filepath):
    """Lê os dados de um arquivo CSV e retorna um DataFrame."""
    return pd.read_csv(filepath)

def gerar_grafico(meses, vendas, meta, grafico):
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
    with open(grafico, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def renderizar_html(string_codificada, dados):
    template_html = """[... omitido por simplicidade ...]"""
    template = Template(template_html)
    return template.render(string_codificada=string_codificada, dados=dados)

def gerar_pdf(html_renderizado, caminho_pdf):
    HTML(string=html_renderizado).write_pdf(caminho_pdf)

def gerar_relatorio_pdf(caminho_csv):
    df = dados_csv(caminho_csv)
    meses = df['Mes'].tolist()
    vendas = df['Vendas'].tolist()
    meta = df['Meta'].tolist()
    porcentagem_cumprimento = [round((v / m) * 100, 1) for v, m in zip(vendas, meta)]
    grafico = 'grafico_vendas.png'
    gerar_grafico(meses, vendas, meta, grafico)
    string_codificada = codificar_imagem(grafico)
    html_renderizado = renderizar_html(string_codificada, zip(meses, vendas, meta, porcentagem_cumprimento))
    caminho_pdf = 'relatorio_vendas.pdf'
    gerar_pdf(html_renderizado, caminho_pdf)

if __name__ == '__main__':
    gerar_relatorio_pdf('caminho_para_seu_arquivo.csv')
