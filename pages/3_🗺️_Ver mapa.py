import streamlit as st
import pdfplumber
from PIL import Image

st.set_page_config('Mapa | Rener', '🗺️', 'wide')

# Caminho do PDF
pdf_path = "data\\original\\NDVI_16-10-24.pdf"

# Abre o PDF e converte cada página em imagem com resolução mais alta
with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages):
        # Converte a página para imagem com resolução aumentada
        img = page.to_image(resolution=200).original  # Aumente o valor para melhorar a qualidade (ex: 200 ou 300)

        # Exibe a imagem no Streamlit
        st.image(img, use_column_width=True)
