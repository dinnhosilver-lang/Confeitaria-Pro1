import streamlit as st
import pandas as pd

# Configuração da página e Estilo Visual
st.set_page_config(page_title="Sistema de Precificação & Vendas", layout="wide")

# Inicialização de dados (Memória do App)
if 'produtos' not in st.session_state:
    st.session_state.produtos = []
if 'pedidos' not in st.session_state:
    st.session_state.pedidos = []

# --- MENU LATERAL ---
with st.sidebar:
    st.title("🚀 Gestão iFood & Doceria")
    opcao = st.radio("Selecione o que deseja fazer:", 
                     ["📦 Cadastro de Insumos", "💰 Calculadora de Precificação", "📝 Pedidos e Clientes"])
    st.markdown("---")
    st.info("Dica: Cadastre os insumos antes de precificar o produto final.")

# --- 1. ABA: CADASTRO DE PRODUTO (INSUMOS) ---
if opcao == "📦 Cadastro de Insumos":
    st.title("📦 Cadastro de Insumos / Ingredientes")
    st.subheader("Cadastre aqui a matéria-prima (ex: Farinha, Chocolate)")
    
    with st.form("form_insumos", clear_on_submit=True):
        col1, col2 = st.columns(2)
        nome = col1.text_input("Nome do Ingrediente")
        preco = col2.number_input("Preço pago na embalagem (R$)", min_value=0.0, format="%.2f")
        
        col3, col4 = st.columns(2)
        qtd = col3.number_input("Quantidade total da embalagem", min_value=0.0)
        unidade = col4.selectbox("Unidade", ["g", "kg", "ml", "L", "un"])
        
        if st.form_submit_button("Salvar Insumo"):
            if nome and qtd > 0:
                custo_unitario = preco / qtd
                st.session_state.produtos.append({
                    "Item": nome, "Preço": preco, "Qtd": qtd, "Un": unidade, "Custo_Unit": custo_unitario
                })
                st.success(f"Insumo '{nome}' cadastrado!")
            else:
                st.error("Preencha o nome e a quantidade corretamente.")

    if st.session_state.produtos:
        st.write("### Itens Cadastrados")
        st.dataframe(pd.DataFrame(st.session_state.produtos), use_container_width=True)

# --- 2. ABA: PRECIFICAÇÃO ---
elif opcao == "💰 Calculadora de Precificação":
    st.title("💰 Calculadora de Precificação de Venda")
    
    if not st.session_state.produtos:
        st.warning("⚠️ Você precisa cadastrar Insumos primeiro para poder precificar!")
    else:
        st.subheader("Selecione o ingrediente e quanto usará na receita:")
        
        # Lógica simples de cálculo de ficha técnica
        lista_nomes = [p['Item'] for p in st.session_state.produtos]
        sel_item = st.selectbox("Escolha o Ingrediente:", lista_nomes)
        qtd_usada = st.number_input("Quantidade que vai usar na receita:", min_value=0.0)
        
        # Busca o custo unitário do item selecionado
        custo_ref = next(item['Custo_Unit'] for item in st.session_state.produtos if item['Item'] == sel_item)
        custo_final_item = custo_ref * qtd_usada
        
        st.metric("Custo deste ingrediente na receita", f"R$ {custo_final_item:.2f}")
        
        st.markdown("---")
        markup = st.slider("Margem de Lucro desejada (%)", 10, 300, 100)
        preco_sugerido = custo_final_item * (1 + markup/100)
        st.header(f"Preço de Venda Sugerido: R$ {preco_sugerido:.2f}")

# --- 3. ABA: CADASTRO DE CLIENTE E PEDIDOS ---
elif opcao == "📝 Pedidos e Clientes":
    st.title("📝 Cadastro de Pedidos")
    
    with st.form("form_pedidos", clear_on_submit=True):
        col_c1, col_c2 = st.columns(2)
        nome_c = col_c1.text_input("Nome do Cliente")
        tel_c = col_c2.text_input("Telefone")
        
        prod_c = st.text_input("Produto que ele quer (ex: 1 Bolo de Cenoura)")
        
        col_v1, col_v2 = st.columns(2)
        valor_c = col_v1.number_input("Valor a Pagar (R$)", min_value=0.0, format="%.2f")
        pago_c = col_v2.selectbox("Situação do Pagamento", ["Não Pago", "Pago"])
        
        if st.form_submit_button("Confirmar Pedido"):
            st.session_state.pedidos.append({
                "Cliente": nome_c, "Telefone": tel_c, "Produto": prod_c, 
                "Valor": valor_c, "Status": pago_c
            })
            st.success("Pedido registrado!")

    # Exibição Visual dos Pedidos
    if st.session_state.pedidos:
        st.write("### Lista de Pedidos Atual")
        for p in st.session_state.pedidos:
            cor = "green" if p['Status'] == "Pago" else "red"
            # Cria um "card" visual para cada pedido
            st.markdown(f"""
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 10px; border-left: 10px solid {cor}; margin-bottom: 10px">
                    <h4 style="margin:0">{p['Cliente']} - {p['Telefone']}</h4>
                    <p style="margin:5px 0"><b>Produto:</b> {p['Produto']} | <b>Valor:</b> R$ {p['Valor']:.2f}</p>
                    <b style="color:{cor}">{p['Status'].upper()}</b>
                </div>
            """, unsafe_allow_html=True)
