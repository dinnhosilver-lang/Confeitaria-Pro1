import streamlit as st
import pandas as pd

st.set_page_config(page_title="App de Precificação e Pedidos", layout="wide")

st.title("📊 Gestão de Custos e Pedidos")

# --- CADASTRO DE INGREDIENTES ---
st.header("1. Cadastro de Ingredientes")
with st.form("form_ingredientes", clear_on_submit=True):
    col1, col2, col3, col4 = st.columns(4)
    nome_ing = col1.text_input("Nome do Ingrediente")
    preco_ing = col2.number_input("Preço (R$)", min_value=0.0, step=0.01)
    qtd_ing = col3.number_input("Quantidade", min_value=0.0)
    gramatura = col4.selectbox("Gramatura", ["g", "kg", "ml", "L", "un"])
    
    if st.form_submit_button("Salvar Ingrediente"):
        st.success(f"Ingrediente '{nome_ing}' salvo com sucesso!")

st.divider()

# --- CADASTRO DE CLIENTES E PEDIDOS ---
st.header("2. Cadastro de Pedidos")
with st.form("form_pedidos", clear_on_submit=True):
    col_p1, col_p2 = st.columns(2)
    tipo_prod = col_p1.text_input("Tipo de Produto (ex: Bolo)")
    nome_cliente = col_p2.text_input("Nome do Cliente")
    
    col_v1, col_v2, col_v3 = st.columns(3)
    qtd_compra = col_v1.number_input("Quantidade da Compra", min_value=1)
    valor_total = col_v2.number_input("Valor Total (R$)", min_value=0.0, step=0.01)
    situacao = col_v3.radio("Situação", ["Não Pago", "Pago"], horizontal=True)
    
    if st.form_submit_button("Salvar Pedido"):
        cor_status = "✅" if situacao == "Pago" else "❌"
        st.info(f"Pedido de {nome_cliente} registrado! Status: {cor_status}")

# --- VISUALIZAÇÃO ---
st.header("📋 Resumo de Atividades")
st.write("Aqui os dados aparecerão consolidados para sua análise de performance.")
