import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestão de Precificação", layout="wide")

with st.sidebar:
st.title("📌 Menu")
aba = st.radio("Ir para:", ["🏠 Cadastro", "🍎 Insumos Salvos", "💰 Pagamentos"])

if 'ingredientes' not in st.session_state:
st.session_state.ingredientes = []
if 'pedidos' not in st.session_state:
st.session_state.pedidos = []

if aba == "🏠 Cadastro":
st.title("📊 Cadastro de Dados")
with st.expander("➕ Novo Ingrediente", expanded=True):
n = st.text_input("Nome do Ingrediente")
p = st.number_input("Preço (R$)", min_value=0.0)
q = st.number_input("Quantidade", min_value=0.0)
g = st.selectbox("Unidade", ["g", "kg", "ml", "L", "un"])
if st.button("Salvar Ingrediente"):
st.session_state.ingredientes.append({"Nome": n, "Preço": p, "Qtd": q, "Unidade": g})
st.success("Salvo!")

elif aba == "🍎 Insumos Salvos":
st.title("🍎 Lista de Insumos")
st.table(pd.DataFrame(st.session_state.ingredientes))

elif aba == "💰 Pagamentos":
st.title("💰 Pedidos Pagos")
df = pd.DataFrame(st.session_state.pedidos)
if not df.empty:
pagos = df[df["Situação"] == "Pago"]
st.dataframe(pagos)
st.metric("Total", f"R$ {pagos['Valor'].sum():.2f}")
