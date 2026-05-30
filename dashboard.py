import streamlit as st
import plotly.express as px
import pandas as pd
import os

# ==============================================================================
# LEGENDA E ESTRUTURA DO ARQUIVO
# ==============================================================================
# Este script gerencia o Dashboard de Contratos PROADMI/UPE.
# Suas principais seções e blocos de funcionalidades estão divididos em:
# 1. CONFIGURAÇÕES: Inicialização da página do Streamlit.
# 2. ESTILIZAÇÃO: CSS customizado injetado via Markdown para componentes e KPIs.
# 3. CABEÇALHO: Elementos visuais de título da aplicação.
# 4. CARREGAMENTO DE DADOS: Upload de arquivos e fallback para base local.
# 5. PROCESSAMENTO DE DADOS: Tratamento, conversões de tipos e novas colunas.
# 6. COMPONENTES SIDEBAR: Filtros laterais e lógicas de índices de datas.
# 7. APLICAÇÃO DOS FILTROS: FILTRAGEM dinâmica do DataFrame principal.
# 8. CÁLCULO E EXIBIÇÃO DE KPIS: Métricas resumidas apresentadas em cards.
# 9. SEÇÃO ADMINISTRATIVA: Visualizações focadas em eficiência operacional.
# 10. SEÇÃO FINANCEIRA: Visualizações focadas em gastos e execução financeira.
# 11. SEÇÃO ESTRATÉGICA: Gráficos de tendências temporais e distribuições gerais.
# 12. APRESENTAÇÃO E DOWNLOAD DA BASE: Visualização bruta e exportação CSV.
# ==============================================================================

# ==============================================================================
# 1. CONFIGURAÇÕES
# ==============================================================================

st.set_page_config(
    page_title="PROADMI - Contratos",
    page_icon="📊",
    layout="wide"
)

# ==============================================================================
# 2. ESTILIZAÇÃO (CSS)
# ==============================================================================

st.markdown("""
<style>
/* HIERARQUIA DE FONTES: Títulos de seções de gráficos mais próximos e integrados */
h3 {
    font-size: 1.25rem !important;
    font-weight: 600 !important;
    margin-bottom: 0px !important; 
    padding-bottom: 5px !important;
}

/* Remover borda arredondada da imagem da logo */        
[data-testid="stSidebar"] img {
    border-radius: 0px !important;
}

/* Botões em estado normal (Secondary) */
[data-testid="stSidebar"] div.stButton > button[kind="secondary"] {
    background-color: transparent !important;
    border: 1px solid #d0d5dd !important;
    color: #475467 !important;
    font-weight: 500 !important;
    padding: 2px 15px !important;
    border-radius: 6px !important;
    transition: 0.2s !important;
}

body[data-theme="dark"] [data-testid="stSidebar"] div.stButton > button[kind="secondary"] {
    color: #E3E3EA !important;
    border-color: #475467 !important;
}

/* Hover no botão normal */
[data-testid="stSidebar"] div.stButton > button[kind="secondary"]:hover {
    border-color: #3676B2 !important;
    color: #3676B2 !important;
    background-color: rgba(54, 118, 178, 0.05) !important;
}

/* Botão ATIVO selecionado (Primary) */
[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
    background-color: #3676B2 !important; 
    border: 1px solid #3676B2 !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    padding: 2px 15px !important;
    border-radius: 6px !important;
    transition: 0.2s !important;
}
            
/* Reduz o espaço em branco entre um botão e outro */
[data-testid="stSidebar"] div.stButton {
    margin-bottom: -12px !important; /* Altere esse valor para -15px se quiser ainda mais junto, ou -8px para afastar um pouco */
}

/* Componentes select e multiselect (borda padrão) */
[data-baseweb="select"] > div {
    border-color: #bcd8e0 !important;
}

/* Efeito de hover nos componentes select e multiselect */
[data-baseweb="select"] > div:hover {
    border-color: #3578AE !important;
}

/* Foco nos componentes select e multiselect para remover contorno padrão */
[data-baseweb="select"]:focus-within > div {
    border-color: #3578AE !important;
    box-shadow: 0 0 0 1px #3578AE !important;
}

/* Espaçamento do container principal da página */
.block-container{
    padding-top:1.5rem;
    padding-bottom:2rem;
}

/* Configuração dos títulos de seção customizados */
.section-title{
    font-size:30px;
    font-weight:700;
    margin-top:25px;
    margin-bottom:10px;
    transition:0.2s;
}

/* Cor do título da seção para o tema claro */
body[data-theme="light"] .section-title{
    color:#17324D;
    text-shadow:none;
}

/* Cor do título da seção para o tema escuro */
body[data-theme="dark"] .section-title{
    color:#FFFFFF;
    text-shadow:0 1px 3px rgba(0,0,0,0.35);
}

/* Configuração do subtítulo de seções */
.section-subtitle{
    font-size:15px;
    color:#98A2B3;
    margin-bottom:20px;
}

/* Divisor de seções customizado em formato de linha */
.section-divider{
    margin-top:25px;
    margin-bottom:25px;
    border-top:2px solid rgba(255,255,255,0.10);
}

/* Configuração visual do Card de KPI */
.kpi-card{
    background:#3577B1;
    border:1px solid #ffffff;
    border-radius:16px;
    padding:22px;
    margin-bottom:10px;
    min-height:130px;
    box-shadow:0 4px 12px rgba(0,0,0,0.12);
    transition:0.2s;
}

.kpi-card:hover{
    transform:translateY(-2px);
    box-shadow:0 6px 18px rgba(0,0,0,0.14);
}

.kpi-title{
    font-size:12px; 
    color:#E3E3EA;
    font-weight:600;
    margin-bottom:12px;
    letter-spacing:0.2px;
}

.kpi-value{
    font-size:20px; 
    font-weight:700;
    color:#FFFFFF;
    line-height:1.25;
    word-wrap:break-word;
}

/* Classes utilitárias para títulos mais próximos de gráficos */
.chart-sub-title {
    text-align: center;
    font-size: 14px;
    font-weight: bold;
    color: #475467;
    margin-bottom: -15px;
    z-index: 10;
    position: relative;
}

body[data-theme="dark"] .chart-sub-title {
    color: #E3E3EA;
}

/* Estilo do indicador de ajuda Tooltip */
.tooltip{
    cursor:help;
    border-bottom:none !important;
    text-decoration:none !important;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. CABEÇALHO
# ==============================================================================

st.title("Dashboard de Contratos")
st.markdown(
    "Monitoramento administrativo, financeiro e estratégico dos contratos da UPE "
    "pela Pró-Reitoria de Administração e Finanças (PROADMI)"
)

# ==============================================================================
# 4. CARREGAMENTO DE DADOS
# ==============================================================================

# Uso de colunas na sidebar para encolher e centralizar a imagem da logo
col1, col2, col3 = st.sidebar.columns([1, 2.5, 1])
with col2:
    # Caso sua imagem esteja em um diretório diferente, altere o caminho aqui
    st.image("assets/proadmi-logo.png", use_container_width=True)

st.sidebar.markdown(
    "<div style='text-align: center; font-size: 13px; color: #98A2B3; margin-top: -10px; margin-bottom: 10px; font-weight: 500;'>"
    "Pró-Reitoria de Administração e Finanças (PROADMI)"
    "</div>",
    unsafe_allow_html=True
)

st.sidebar.divider()

with st.sidebar.expander("Alterar Planilha", expanded=False):
    st.caption("Envie uma nova base para análise.")
    fl = st.file_uploader(
        "Selecionar arquivo",
        type=["csv", "xlsx"],
        label_visibility="collapsed"
    )

if fl is not None:
    if fl.name.endswith(".csv"):
        df = pd.read_csv(fl)
    else:
        df = pd.read_excel(fl)
else:
    df = pd.read_csv("PGC_PROADMI.csv")

# ==============================================================================
# 5. PROCESSAMENTO DE DADOS
# ==============================================================================

df["ini_vigencia"] = pd.to_datetime(df["ini_vigencia"], errors="coerce")
df["fim_vigencia"] = pd.to_datetime(df["fim_vigencia"], errors="coerce")

df["ANO"] = df["ini_vigencia"].dt.year.astype("Int64")
df["MÊS"] = df["ini_vigencia"].dt.month

meses = {
    1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
    7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
}
df["MÊS_NOME"] = df["MÊS"].map(meses)

df["DURAÇÃO (DIAS)"] = (df["fim_vigencia"] - df["ini_vigencia"]).dt.days

# Limpeza financeira
df["val_executado"] = pd.to_numeric(df["val_executado"], errors="coerce").fillna(0)
df["val_total"] = pd.to_numeric(df["val_total"], errors="coerce").fillna(0)
df["% EXECUÇÃO"] = (df["val_executado"] / df["val_total"]) * 100
df["% EXECUÇÃO"] = df["% EXECUÇÃO"].replace([float("inf"), -float("inf")], 0).fillna(0)

# CLASSIFICAÇÃO INTELIGENTE DE VIGÊNCIAS PARA O BLOCO ADMINISTRATIVO
def derivar_tipo_vigencia(dias):
    if pd.isna(dias): return "Não Informado"
    dias = float(dias)
    if dias >= 365 and (dias % 365 <= 5 or dias % 365 >= 360): 
        return "Anos"
    elif dias >= 30 and (dias % 30 <= 3 or dias % 30 >= 27):
        return "Meses"
    else:
        return "Dias"

def derivar_tempo_vigencia(dias):
    if pd.isna(dias): return "Não Informado"
    dias = float(dias)
    if 360 <= dias <= 366: return "12 Meses"
    if 720 <= dias <= 731: return "24 Meses"
    if 1080 <= dias <= 1096: return "36 Meses"
    if 1440 <= dias <= 1461: return "48 Meses"
    if 1800 <= dias <= 1826: return "60 Meses"
    if dias >= 30 and (dias % 30 <= 3 or dias % 30 >= 27):
        return f"{int(dias//30)} Meses"
    return f"{int(dias)} Dias"

df["vigencia"] = pd.to_numeric(df["vigencia"], errors="coerce")
df["tipo_vigencia"] = df["vigencia"].apply(derivar_tipo_vigencia)
df["tempo_vigencia"] = df["vigencia"].apply(derivar_tempo_vigencia)

# ==============================================================================
# 6. COMPONENTES SIDEBAR (NAVEGAÇÃO E FILTROS)
# ==============================================================================

# Inicializa a memória da aba atual, se for o primeiro carregamento
if "visualizacao" not in st.session_state:
    st.session_state.visualizacao = "Dashboard Completo"

# Função que muda a aba guardada na memória
def set_view(view_name):
    st.session_state.visualizacao = view_name

st.sidebar.markdown('<div style="font-size: 14px; font-weight: 600; color: #475467; margin-bottom: 5px;">Navegação</div>', unsafe_allow_html=True)

# Geração automática dos botões de navegação
abas = ["Dashboard Completo", "Administrativo", "Financeiro", "Estratégico"]
for aba in abas:
    st.sidebar.button(
        label=aba,
        on_click=set_view,
        args=(aba,),
        type="primary" if st.session_state.visualizacao == aba else "secondary",
        use_container_width=True
    )

# A variável "visualizacao" continua existindo para alimentar os blocos if
visualizacao = st.session_state.visualizacao

# Declaração das variáveis de controle de exibição de cada seção
mostrar_admin = (visualizacao == "Dashboard Completo" or visualizacao == "Administrativo")
mostrar_fin = (visualizacao == "Dashboard Completo" or visualizacao == "Financeiro")
mostrar_est = (visualizacao == "Dashboard Completo" or visualizacao == "Estratégico")

st.sidebar.divider()

st.sidebar.header("Filtros")

unidade = st.sidebar.multiselect("Unidade", sorted(df["uni_beneficiada"].dropna().unique()))
categoria = st.sidebar.multiselect("Categoria", sorted(df["cat_objeto"].dropna().unique()))
situacao = st.sidebar.multiselect("Situação", sorted(df["situacao"].dropna().unique()))
contratada = st.sidebar.multiselect("Contratada", sorted(df["contratada"].dropna().unique()))

anos_disponiveis = sorted(df["ANO"].dropna().unique())
idx_2025 = anos_disponiveis.index(2025) if 2025 in anos_disponiveis else 0
idx_2026 = anos_disponiveis.index(2026) if 2026 in anos_disponiveis else min(1, len(anos_disponiveis) - 1)

st.sidebar.divider()
st.sidebar.subheader("Comparação por ano")
ano_1 = st.sidebar.selectbox("Ano 1", anos_disponiveis, index=idx_2025)
ano_2 = st.sidebar.selectbox("Ano 2", anos_disponiveis, index=idx_2026)

# ==============================================================================
# 7. APLICAÇÃO DOS FILTROS
# ==============================================================================

df_filtro = df.copy()
if unidade: df_filtro = df_filtro[df_filtro["uni_beneficiada"].isin(unidade)]
if categoria: df_filtro = df_filtro[df_filtro["cat_objeto"].isin(categoria)]
if situacao: df_filtro = df_filtro[df_filtro["situacao"].isin(situacao)]
if contratada: df_filtro = df_filtro[df_filtro["contratada"].isin(contratada)]

# ==============================================================================
# 8. CÁLCULO E EXIBIÇÃO DE KPIS
# ==============================================================================

valor_total = df_filtro["val_total"].sum()
valor_exec = df_filtro["val_executado"].sum()
n_contratos = df_filtro.shape[0]

top_unidade = df_filtro.groupby("uni_beneficiada").size().sort_values(ascending=False)
top_unidade_nome = top_unidade.index[0] if len(top_unidade) > 0 else "-"

top_contratada = df_filtro.groupby("contratada").size().sort_values(ascending=False)
if len(top_contratada) > 0:
    primeira_colocada = str(top_contratada.index[0]).strip().upper()
    if primeira_colocada == "OUTROS" and len(top_contratada) > 1:
        top_contratada_nome = top_contratada.index[1]
    else:
        top_contratada_nome = top_contratada.index[0]
else:
    top_contratada_nome = "-"

ano_lider = df_filtro.groupby("ANO").size().sort_values(ascending=False)
ano_lider_nome = str(ano_lider.index[0]) if len(ano_lider) > 0 else "-"

k1, k2, k3 = st.columns(3)
k4, k5, k6 = st.columns(3)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title"><span class="tooltip" title="Quantidade total de contratos após aplicação dos filtros">📄 Total de Contratos</span></div>
        <div class="kpi-value">{n_contratos}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title"><span class="tooltip" title="Soma do valor total contratado após aplicação dos filtros">💰 Valor Total Contratado</span></div>
        <div class="kpi-value">R$ {valor_total:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title"><span class="tooltip" title="Valor já executado ou liquidado dos contratos filtrados">📊 Valor Executado dos Contratos</span></div>
        <div class="kpi-value">R$ {valor_exec:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title"><span class="tooltip" title="Ano com maior quantidade de contratos">📅 Ano com mais Contratos</span></div>
        <div class="kpi-value">{ano_lider_nome}</div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title"><span class="tooltip" title="Contratada com maior quantidade de contratos nos filtros atuais">🏢 Maior Contratada</span></div>
        <div class="kpi-value" style="font-size: 15px; line-height: 1.2;">{top_contratada_nome}</div>
    </div>
    """, unsafe_allow_html=True)

with k6:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title"><span class="tooltip" title="Unidade que possui o maior número de contratos">🏛️ Unidade Destaque</span></div>
        <div class="kpi-value">{top_unidade_nome}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ==============================================================================
# 9. SEÇÃO ADMINISTRATIVA
# ==============================================================================

if mostrar_admin:
    st.markdown('<div class="section-title">📋 Visão Administrativa e Operacional</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Análise detalhada da quantidade, categorização, vigência e base legal dos contratos.</div>', unsafe_allow_html=True)

    # Identidade visual Steven Universe: Tons de Azul Pastel (ex: Pérola/Lapis)
    paleta_azul = ['#022254', '#3676B2', '#537AF3', '#caf0f8', '#A4FFFA']
    azul_primario = "#3676B2"
    azul_secundario = "#caf0f8"

    escala_azul_pastel = ['#447DAB', '#61BFF9', '#A7FFFE']

    # --- BLOCO 1: QUANTIDADE DE CONTRATOS POR ANO ---
    st.markdown('### 📅 Quantidade de Contratos por Ano')
    a1, a2 = st.columns([2, 1])

    with a1:
        st.markdown('<div class="chart-sub-title">Evolução Histórica Total</div>', unsafe_allow_html=True)
        contratos_ano = df_filtro.groupby("ANO").size().reset_index(name="Quantidade").sort_values("ANO")
        contratos_ano["ANO_STR"] = contratos_ano["ANO"].astype(str)
        
        fig1 = px.area(contratos_ano, x="ANO_STR", y="Quantidade", markers=True, color_discrete_sequence=[azul_primario])
        fig1.update_layout(margin=dict(t=30, b=10, l=10, r=10), xaxis_title=None, yaxis_title=None)
        fig1.update_xaxes(type='category')
        st.plotly_chart(fig1, use_container_width=True)

    with a2:
        st.markdown(f'<div class="chart-sub-title">Comparativo {ano_1} x {ano_2}</div>', unsafe_allow_html=True)
        comp = df_filtro[df_filtro["ANO"].isin([ano_1, ano_2])].groupby("ANO").size().reset_index(name="Quantidade")
        comp["ANO"] = comp["ANO"].astype(str)
        fig3 = px.bar(comp, x="ANO", y="Quantidade", text="Quantidade", color="ANO", color_discrete_sequence=[azul_primario, azul_secundario])
        fig3.update_traces(textposition='outside')
        fig3.update_layout(margin=dict(t=30, b=10, l=10, r=10), showlegend=False, xaxis_title=None, yaxis_title=None)
        fig3.update_xaxes(type='category')
        st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    # --- BLOCO 2: QUANTIDADE DE CONTRATOS POR CATEGORIA ---
    st.markdown('### 🏷️ Contratos por Categoria do Objeto')
    st.markdown('<div class="chart-sub-title" style="margin-bottom: 5px;">Distribuição Hierárquica de Categorias</div>', unsafe_allow_html=True)
    cat_obj = df_filtro.groupby("cat_objeto").size().reset_index(name="Quantidade")
    
    fig_cat = px.treemap(
        cat_obj, 
        path=[px.Constant("Todas as Categorias"), "cat_objeto"], 
        values="Quantidade", 
        color="Quantidade", 
        color_continuous_scale=escala_azul_pastel
    )
    fig_cat.update_layout(margin=dict(t=25, b=10, l=0, r=0))
    st.plotly_chart(fig_cat, use_container_width=True)

    st.divider()

    # --- BLOCO 3: CLASSIFICAÇÃO DA LEI ---
    st.markdown('### ⚖️ Contratos Vigentes por Classificação da Lei')
    
    df_lei = df_filtro[
        (df_filtro["situacao"].str.upper().str.contains("EM EXECUÇÃO", na=False)) & 
        (df_filtro["lei"].isin(["8666/93", "14133/21"]))
    ]
    
    l1, l2 = st.columns(2)
    lei_count = df_lei.groupby("lei").size().reset_index(name="Quantidade")

    with l1:
        st.markdown('<div class="chart-sub-title">Proporção de Contratos Ativos</div>', unsafe_allow_html=True)
        fig_lei1 = px.pie(lei_count, names="lei", values="Quantidade", hole=0.5, color_discrete_sequence=[azul_primario, azul_secundario])
        fig_lei1.update_traces(textposition='inside', textinfo='percent+label')
        fig_lei1.update_layout(margin=dict(t=30, b=10, l=10, r=10), showlegend=False)
        st.plotly_chart(fig_lei1, use_container_width=True)

    with l2:
        st.markdown('<div class="chart-sub-title">Volume de Contratos Ativos</div>', unsafe_allow_html=True)
        fig_lei2 = px.bar(lei_count, x="Quantidade", y="lei", orientation='h', text="Quantidade", color="lei", color_discrete_sequence=[azul_primario, azul_secundario])
        fig_lei2.update_traces(textposition='auto')
        fig_lei2.update_layout(margin=dict(t=30, b=10, l=10, r=10), showlegend=False, xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig_lei2, use_container_width=True)

    st.divider()

    # --- BLOCO 4: VIGÊNCIA ---
    st.markdown('### ⏳ Quantidade de Contratos por Vigência')
    v1, v2 = st.columns(2)
    
    with v1:
        st.markdown('<div class="chart-sub-title">Contratos por Tipo de Vigência</div>', unsafe_allow_html=True)
        tipo_vig = df_filtro.groupby("tipo_vigencia").size().reset_index(name="Quantidade").sort_values("Quantidade", ascending=False)
        fig_v1 = px.bar(tipo_vig, x="tipo_vigencia", y="Quantidade", text="Quantidade", color="tipo_vigencia", color_discrete_sequence=paleta_azul)
        fig_v1.update_traces(textposition='outside')
        fig_v1.update_layout(margin=dict(t=30, b=10, l=10, r=10), showlegend=False, xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig_v1, use_container_width=True)
        
    with v2:
        st.markdown('<div class="chart-sub-title">Ranking de Tempos Contratuais (Top 10)</div>', unsafe_allow_html=True)
        tempo_vig = df_filtro.groupby("tempo_vigencia").size().reset_index(name="Quantidade").sort_values("Quantidade", ascending=False).head(10).sort_values("Quantidade", ascending=True)
        fig_v2 = px.bar(tempo_vig, x="Quantidade", y="tempo_vigencia", orientation='h', text="Quantidade", color="Quantidade", color_continuous_scale=escala_azul_pastel)
        fig_v2.update_traces(textposition='outside')
        fig_v2.update_layout(margin=dict(t=30, b=10, l=10, r=10), xaxis_title=None, yaxis_title=None, coloraxis_showscale=False)
        st.plotly_chart(fig_v2, use_container_width=True)

    st.markdown('<div class="chart-sub-title" style="margin-top: 15px;">Tipo de Vigência x Categoria do Objeto</div>', unsafe_allow_html=True)
    vig_cat = df_filtro.groupby(["cat_objeto", "tipo_vigencia"]).size().reset_index(name="Quantidade")
    fig_v3 = px.bar(vig_cat, x="cat_objeto", y="Quantidade", color="tipo_vigencia", barmode="stack", color_discrete_sequence=paleta_azul)
    fig_v3.update_layout(margin=dict(t=30, b=10, l=10, r=10), xaxis_title=None, yaxis_title=None, legend_title="Tipo", xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig_v3, use_container_width=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ==============================================================================
# 10. SEÇÃO FINANCEIRA
# ==============================================================================

if mostrar_fin:
    st.markdown('<div class="section-title">💰 Análise Econômico-Financeira</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Acompanhamento do volume de recursos empenhados, liquidações e distribuição por categoria.</div>', unsafe_allow_html=True)

    # Identidade visual Steven Universe: Tons de Roxo Pastel (ex: Ametista)
    paleta_roxa = ['#7E3F96', '#C2A0DF', '#916DAB', '#B02EF1', '#4A1A64']
    roxo_primario = "#916DAB"
    roxo_secundario = "#C2A0DF"

    escala_roxa_pastel = ['#4A1C5D', '#EAE1FD', '#7E3F96']

    # --- BLOCO 1: VALOR CONTRATADO ---
    st.markdown('### 🗂️ Comportamento dos Valores Contratados')
    st.markdown('<div class="chart-sub-title">Soma dos Valores Totais por Ano (Tamanho indica Volume)</div>', unsafe_allow_html=True)
    
    valor_ano = df_filtro.groupby("ANO")["val_total"].sum().reset_index().sort_values("ANO")
    valor_ano["ANO_STR"] = valor_ano["ANO"].astype(str)
    
    fig_f1 = px.scatter(
        valor_ano, 
        x="ANO_STR", 
        y="val_total", 
        size="val_total", 
        color="val_total",
        color_continuous_scale=escala_roxa_pastel,
        size_max=40
    )
    fig_f1.add_traces(px.line(valor_ano, x="ANO_STR", y="val_total", color_discrete_sequence=[roxo_primario]).data)
    fig_f1.update_layout(margin=dict(t=30, b=10, l=10, r=10), xaxis_title=None, yaxis_title=None, coloraxis_showscale=False)
    fig_f1.update_xaxes(type='category')
    st.plotly_chart(fig_f1, use_container_width=True)

    st.divider()

    # --- BLOCO 2: VALOR EXECUTADO POR ANO ---
    st.markdown('### 📈 Evolução da Execução Financeira')
    st.markdown('<div class="chart-sub-title">Histórico de Valores Liquidados/Executados por Ano</div>', unsafe_allow_html=True)
    
    exec_ano = df_filtro.groupby("ANO")["val_executado"].sum().reset_index().sort_values("ANO")
    exec_ano["ANO_STR"] = exec_ano["ANO"].astype(str)
    
    fig_f3 = px.area(exec_ano, x="ANO_STR", y="val_executado", markers=True, color_discrete_sequence=[roxo_primario])
    fig_f3.update_traces(line_shape='spline')
    fig_f3.update_layout(margin=dict(t=25, b=10, l=10, r=10), xaxis_title=None, yaxis_title=None)
    fig_f3.update_xaxes(type='category')
    st.plotly_chart(fig_f3, use_container_width=True)

    st.divider()

    # --- BLOCO 3: VALOR POR CATEGORIA ---
    st.markdown('### 🏷️ Investimento por Categoria do Objeto')
    st.markdown('<div class="chart-sub-title">Top 3 Categorias com Maior Concentração de Recursos Financeiros</div>', unsafe_allow_html=True)
    
    valor_cat = df_filtro.groupby("cat_objeto")["val_total"].sum().reset_index()
    valor_cat = valor_cat.sort_values("val_total", ascending=False).head(3)
    
    fig_f4 = px.bar(
        valor_cat,
        x="cat_objeto",
        y="val_total",
        text="val_total",
        color="val_total",
        color_continuous_scale=escala_roxa_pastel
    )
    fig_f4.update_traces(texttemplate='R$ %{text:,.2f}', textposition='outside')
    fig_f4.update_layout(
        margin=dict(t=30, b=10, l=10, r=10),
        xaxis_title=None,
        yaxis_title="Valor Contratado (R$)",
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_f4, use_container_width=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ==============================================================================
# 11. SEÇÃO ESTRATÉGICA
# ==============================================================================

if mostrar_est:
    st.markdown('<div class="section-title">🎯 Visão Estratégica e Sazonalidade</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Evolução temporal do comportamento dos contratos e direcionamento de fornecedores.</div>', unsafe_allow_html=True)

    # Identidade visual Steven Universe: Tons de Rosa Pastel (ex: Steven/Rose)
    #paleta_rosa = ['#CA2846', '#E8566D', '#F3425C', '#CE1A85', '#DB59A3']
    paleta_rosa = ['#CE1A85', '#DB59A3']
    rosa_primario = "#DB59A3"

    # Paleta Mix Pastel (Garnet, Amethyst, Pearl, Peridot) para diferenciar as linhas de categoria!
    paleta_su_mix = ['#75C885', '#FCD964', '#F23CF9', '#A23C3C', '#E3642A', '#AEE7E7']

    e1, e2 = st.columns(2)

    with e1:
        st.markdown('<div class="chart-sub-title">Contratos Mês a Mês (Início de Vigência)</div>', unsafe_allow_html=True)
        mensal = df_filtro.groupby("MÊS").size().reset_index(name="Quantidade")
        
        todos_meses = pd.DataFrame({"MÊS": list(meses.keys())})
        mensal = todos_meses.merge(mensal, on="MÊS", how="left").fillna(0)
        
        fig_e1 = px.bar(
            mensal,
            x="MÊS",
            y="Quantidade",
            text="Quantidade",
            color_discrete_sequence=[rosa_primario]
        )
        fig_e1.update_traces(textposition='outside')
        fig_e1.update_layout(
            margin=dict(t=30, b=10, l=10, r=10),
            xaxis=dict(tickmode="array", tickvals=list(meses.keys()), ticktext=list(meses.values())),
            xaxis_title=None, yaxis_title=None
        )
        st.plotly_chart(fig_e1, use_container_width=True)

    with e2:
        st.markdown('<div class="chart-sub-title">Top 5 Contratadas</div>', unsafe_allow_html=True)
        
        df_fornecedores = df_filtro[~df_filtro["contratada"].str.upper().str.strip().isin(["OUTROS", "DIVERSOS"])]
        # Pega as 5 maiores, mas inverte a ordem para a barra maior ficar no topo no gráfico horizontal
        top5 = df_fornecedores.groupby("contratada").size().reset_index(name="Quantidade").sort_values("Quantidade", ascending=False).head(5).sort_values("Quantidade", ascending=True)
        
        # Gráfico de barras horizontais estiloso para o Top 5
        fig_e2 = px.bar(
            top5,
            x="Quantidade",
            y="contratada",
            orientation="h",
            color="contratada",
            color_discrete_sequence=paleta_rosa,
            text="Quantidade"
        )
        fig_e2.update_traces(textposition='outside')
        fig_e2.update_layout(
            margin=dict(t=30, b=10, l=10, r=10),
            showlegend=False, 
            xaxis_title=None, 
            yaxis_title=None
        )
        st.plotly_chart(fig_e2, use_container_width=True)

    st.divider()

    st.markdown('<div class="chart-sub-title">Comportamento Mensal por Categoria</div>', unsafe_allow_html=True)
    cat_mes = df_filtro.groupby(["MÊS", "cat_objeto"]).size().reset_index(name="Quantidade")
    
    # Utilizando a Paleta Mix Pastel para que cada categoria fique bem distinta, mas dentro da paleta do desenho
    fig_e3 = px.line(
        cat_mes,
        x="MÊS",
        y="Quantidade",
        color="cat_objeto",
        markers=True,
        color_discrete_sequence=paleta_su_mix
    )
    fig_e3.update_layout(
        margin=dict(t=30, b=10, l=10, r=10),
        xaxis=dict(tickmode="array", tickvals=list(meses.keys()), ticktext=list(meses.values())),
        xaxis_title=None,
        yaxis_title="Qtd. de Contratos",
        legend_title="Categoria"
    )
    st.plotly_chart(fig_e3, use_container_width=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ==============================================================================
# 12. APRESENTAÇÃO E DOWNLOAD DA BASE
# ==============================================================================

st.markdown('<div class="section-title">📄 Dados</div>', unsafe_allow_html=True)

with st.expander("Visualizar dados filtrados"):
    st.dataframe(df_filtro, use_container_width=True)

csv = df_filtro.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Baixar dados filtrados",
    data=csv,
    file_name="contratos_filtrados.csv",
    mime="text/csv"
)