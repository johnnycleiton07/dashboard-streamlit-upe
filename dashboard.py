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

/* HIERARQUIA DE FONTES: Reduz o tamanho do subheader (título dos gráficos) para criar contraste */
h3 {
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    margin-bottom: 15px !important;
}

/* Customização dos botões radio (borda padrão do círculo) */
[data-baseweb="radio"] > div:first-child {
    border-color: #3578AE !important;
}

/* Efeito Hover na linha/opção do Radio Button */
[data-baseweb="radio"]:hover {
    background-color: rgba(188, 216, 224, 0.15) !important;
    border-radius: 4px;
}

/* Customização do botão radio ativo usando a cor sugerida #bcd8e0 */
[data-baseweb="radio"]:has(input:checked) > div:first-child {
    border-color: #bcd8e0 !important;
    background-color: #bcd8e0 !important;
} 

/* Cor interna do ponto de seleção quando ativo */
[data-baseweb="radio"]:has(input:checked) > div:first-child > div {
    background-color: #17324D !important;
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

/* Configuração dos títulos de seção customizados (Mantido em 30px para destaque) */
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

/* Efeito de elevação ao passar o mouse sobre o KPI Card */
.kpi-card:hover{
    transform:translateY(-2px);
    box-shadow:0 6px 18px rgba(0,0,0,0.14);
}

/* Título interno do KPI */
.kpi-title{
    font-size:14px;
    color:#E3E3EA;
    font-weight:600;
    margin-bottom:12px;
    letter-spacing:0.2px;
}

/* Valor em destaque no KPI Card */
.kpi-value{
    font-size:28px;
    font-weight:700;
    color:#FFFFFF;
    line-height:1.25;
    word-wrap:break-word;
}

/* Subtextos ou pequenas descrições nos KPIs */
.kpi-small{
    font-size:14px;
    color:#475467;
    margin-top:8px;
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

# Exibição do logo institucional no menu lateral
st.sidebar.image(
    "assets/proadmi-logo.png",
    use_container_width=True
)

# Legenda institucional adicionada logo abaixo do logotipo da barra lateral
st.sidebar.markdown(
    "<div style='text-align: center; font-size: 13px; color: #98A2B3; margin-top: -10px; margin-bottom: 10px; font-weight: 500;'>"
    "Pró-Reitoria de Administração e Finanças (PROADMI)"
    "</div>",
    unsafe_allow_html=True
)

st.sidebar.divider()

# Bloco expansível lateral para upload alternativo de planilhas
with st.sidebar.expander("Alterar Planilha", expanded=False):
    st.caption("Envie uma nova base para análise.")
    fl = st.file_uploader(
        "Selecionar arquivo",
        type=["csv", "xlsx"],
        label_visibility="collapsed"
    )

# Verificação e leitura do arquivo enviado ou carregamento do arquivo local padrão
if fl is not None:
    if fl.name.endswith(".csv"):
        df = pd.read_csv(fl)
    else:
        df = pd.read_excel(fl)
else:
    os.chdir(r"C:\Users\johnn\Documents\GitHub\dashboard-streamlit-upe")
    df = pd.read_csv("PGC_Contratos_Limpos.csv")

# ==============================================================================
# 5. PROCESSAMENTO DE DADOS
# ==============================================================================

# Conversão dos campos temporais para formato datetime coerente
df["DATA DE INÍCIO"] = pd.to_datetime(df["DATA DE INÍCIO"], errors="coerce")
df["DATA DE TÉRMINO"] = pd.to_datetime(df["DATA DE TÉRMINO"], errors="coerce")

# Criação das colunas de ano e mês numérico derivados da data de início
df["ANO"] = df["DATA DE INÍCIO"].dt.year.astype("Int64")
df["MÊS"] = df["DATA DE INÍCIO"].dt.month

# Dicionário de mapeamento para renomear meses numéricos para extenso abreviado
meses = {
    1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
    7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
}
df["MÊS_NOME"] = df["MÊS"].map(meses)

# Cálculo do intervalo de dias de validade dos contratos
df["DURAÇÃO (DIAS)"] = (df["DATA DE TÉRMINO"] - df["DATA DE INÍCIO"]).dt.days

# Cálculo da representação percentual da execução financeira do contrato
df["% EXECUÇÃO"] = (df["VALOR EXECUTADO"] / df["VALOR TOTAL"]) * 100

# Limpeza e substituição de valores infinitos ou nulos gerados por divisões inválidas
df["% EXECUÇÃO"] = df["% EXECUÇÃO"].replace([float("inf"), -float("inf")], 0).fillna(0)

# ==============================================================================
# 6. COMPONENTES SIDEBAR (FILTROS)
# ==============================================================================

st.sidebar.header("Filtros")

# Filtro de navegação estruturado em lista vertical padrão (um abaixo do outro)
visualizacao = st.sidebar.radio(
    "Visualização",
    ["Dashboard Completo", "Administrativo", "Financeiro", "Estratégico"]
)

# Filtros demográficos e estruturais das variáveis contratuais
unidade = st.sidebar.multiselect(
    "Unidade",
    sorted(df["UNIDADE BENEFICIADA"].dropna().unique())
)

categoria = st.sidebar.multiselect(
    "Categoria",
    sorted(df["CATEGORIA DO OBJETO"].dropna().unique())
)

situacao = st.sidebar.multiselect(
    "Situação",
    sorted(df["SITUAÇÃO DO CONTRATO"].dropna().unique())
)

contratada = st.sidebar.multiselect(
    "Contratada",
    sorted(df["CONTRATADA"].dropna().unique())
)

# Coleta e ordenação dos anos identificados na base para preenchimento do comparativo
anos_disponiveis = sorted(df["ANO"].dropna().unique())

# Lógica para cálculo automático dos índices padrão (2025 e 2026) das caixas de seleção
idx_2025 = anos_disponiveis.index(2025) if 2025 in anos_disponiveis else 0
idx_2026 = (
    anos_disponiveis.index(2026)
    if 2026 in anos_disponiveis
    else min(1, len(anos_disponiveis) - 1)
)

st.sidebar.divider()

# Atualização da legenda lateral para o escopo anual de análise
st.sidebar.subheader("Comparação por ano")

# Dropdowns para seleção dos períodos que alimentarão os gráficos comparativos
ano_1 = st.sidebar.selectbox("Ano 1", anos_disponiveis, index=idx_2025)
ano_2 = st.sidebar.selectbox("Ano 2", anos_disponiveis, index=idx_2026)

# ==============================================================================
# 7. APLICAÇÃO DOS FILTROS
# ==============================================================================

df_filtro = df.copy()

if unidade:
    df_filtro = df_filtro[df_filtro["UNIDADE BENEFICIADA"].isin(unidade)]

if category_filter := categoria:
    df_filtro = df_filtro[df_filtro["CATEGORIA DO OBJETO"].isin(category_filter)]

if situacao:
    df_filtro = df_filtro[df_filtro["SITUAÇÃO DO CONTRATO"].isin(situacao)]

if contratada:
    df_filtro = df_filtro[df_filtro["CONTRATADA"].isin(contratada)]

# ==============================================================================
# 8. CÁLCULO E EXIBIÇÃO DE KPIS
# ==============================================================================

# Agregações matemáticas baseadas no dataframe filtrado
valor_total = df_filtro["VALOR TOTAL"].sum()
valor_exec = df_filtro["VALOR EXECUTADO"].sum()
n_contratos = df_filtro.shape[0]
exec_media = df_filtro["% EXECUÇÃO"].mean()

# Agrupamento para identificação do fornecedor com maior volume de contratos
top_contratada = df_filtro.groupby("CONTRATADA").size().sort_values(ascending=False)
if len(top_contratada) > 0:
    top_contratada_nome = top_contratada.index[0]
else:
    top_contratada_nome = "-"

# Agrupamento para identificação do ano com maior recorrência de novos contratos
ano_lider = df_filtro.groupby("ANO").size().sort_values(ascending=False)
if len(ano_lider) > 0:
    ano_lider_nome = str(ano_lider.index[0])
else:
    ano_lider_nome = "-"

# Alocação das linhas de colunas Streamlit para posicionamento das métricas
k1, k2, k3 = st.columns(3)
k4, k5, k6 = st.columns(3)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">
        <span class="tooltip" title="Soma do valor total contratado após aplicação dos filtros">
        💰 Valor Total Contratado
        </span>
        </div>
        <div class="kpi-value">
        R$ {valor_total:,.2f}
        </div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">
        <span class="tooltip" title="Valor já executado ou liquidado dos contratos filtrados">
        📊 Valor Executado dos Contratos
        </span>
        </div>
        <div class="kpi-value">
        R$ {valor_exec:,.2f}
        </div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">
        <span class="tooltip" title="Quantidade total de contratos após aplicação dos filtros">
        📄 Total de Contratos
        </span>
        </div>
        <div class="kpi-value">
        {n_contratos}
        </div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">
        <span class="tooltip" title="Percentual médio entre valor executado e valor contratado">
        ⚙️ Execução Média
        </span>
        </div>
        <div class="kpi-value">
        {exec_media:.1f}%
        </div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">
        <span class="tooltip" title="Contratada com maior quantidade de contratos nos filtros atuais">
        🏢 Maior Contratada
        </span>
        </div>
        <div class="kpi-value" style="font-size:22px;">
        {top_contratada_nome}
        </div>
    </div>
    """, unsafe_allow_html=True)

with k6:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">
        <span class="tooltip" title="Ano com maior quantidade de contratos">
        📅 Ano com mais Contratos
        </span>
        </div>
        <div class="kpi-value">
        {ano_lider_nome}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ==============================================================================
# 9. SEÇÃO ADMINISTRATIVA
# ==============================================================================

# Validação do estado do radio button lateral para controle do fluxo de exibição operacional
mostrar_admin = (visualizacao == "Dashboard Completo" or visualizacao == "Administrativo")

if mostrar_admin:
    st.markdown(
        '<div class="section-title">📋 Eficiência Operacional</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-subtitle">Análise quantitativa dos contratos e sua distribuição administrativa.</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Quantidade de Contratos por Ano")
        contratos_ano = (
            df_filtro
            .groupby("ANO")
            .size()
            .reset_index(name="Quantidade")
            .sort_values("ANO")
        )
        fig = px.bar(
            contratos_ano,
            x="ANO",
            y="Quantidade",
            color="Quantidade",
            color_continuous_scale="Blues"
        )
        fig.update_layout(
            xaxis_title="Ano",
            yaxis_title="Quantidade",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader(f"Comparação {ano_1} x {ano_2}")
        comp = (
            df_filtro[df_filtro["ANO"].isin([ano_1, ano_2])]
            .groupby("ANO")
            .size()
            .reset_index(name="Quantidade")
        )
        comp["ANO"] = comp["ANO"].astype(str)
        fig = px.bar(
            comp.astype({"ANO": str}),
            x="ANO",
            y="Quantidade",
            color="ANO",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_xaxes(type="category")
        fig.update_layout(
            xaxis_title="Ano",
            yaxis_title="Contratos",
            xaxis=dict(type="category")
        )
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        st.subheader("Quantidade por Categoria")
        categoria_obj = (
            df_filtro
            .groupby("CATEGORIA DO OBJETO")
            .size()
            .reset_index(name="Quantidade")
            .sort_values("Quantidade", ascending=False)
        )
        fig = px.bar(
            categoria_obj,
            x="CATEGORIA DO OBJETO",
            y="Quantidade",
            color="Quantidade",
            color_continuous_scale="Teal"
        )
        fig.update_layout(
            xaxis_title="Categoria",
            yaxis_title="Contratos",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        st.subheader("Lei / Vigência")
        st.info("""
        Lei:
        Necessário criar coluna indicando
        Lei 8.666 ou Lei 14.133.
        """)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ==============================================================================
# 10. SEÇÃO FINANCEIRA
# ==============================================================================

# Validação do estado do radio button lateral para controle do fluxo de exibição de finanças
mostrar_fin = (visualizacao == "Dashboard Completo" or visualizacao == "Financeiro")

if mostrar_fin:
    st.markdown(
        '<div class="section-title">💰 Eficiência Financeira</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-subtitle">Comportamento financeiro e execução dos contratos.</div>',
        unsafe_allow_html=True
    )

    f1, f2 = st.columns(2)

    with f1:
        st.subheader("Valor Contratado por Ano")
        valor_ano = df_filtro.groupby("ANO")["VALOR TOTAL"].sum().reset_index()
        fig = px.bar(
            valor_ano,
            x="ANO",
            y="VALOR TOTAL",
            color="VALOR TOTAL",
            color_continuous_scale="Greens"
        )
        fig.update_layout(
            xaxis_title="Ano",
            yaxis_title="Valor (R$)",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with f2:
        st.subheader(f"Valor Contratado {ano_1} x {ano_2}")
        comp_valor = (
            df_filtro[df_filtro["ANO"].isin([ano_1, ano_2])]
            .groupby("ANO")["VALOR TOTAL"]
            .sum()
            .reset_index()
        )
        fig = px.bar(
            comp_valor.astype({"ANO": str}),
            x="ANO",
            y="VALOR TOTAL",
            color="ANO"
        )
        fig.update_xaxes(type="category")
        fig.update_xaxes(
            tickmode="array",
            tickvals=[ano_1, ano_2],
            ticktext=[str(ano_1), str(str(ano_1)), str(ano_2)]
        )
        st.plotly_chart(fig, use_container_width=True)

    f3, f4 = st.columns(2)

    with f3:
        st.subheader("Valor Executado por Ano")
        exec_ano = df_filtro.groupby("ANO")["VALOR EXECUTADO"].sum().reset_index()
        fig = px.line(
            exec_ano,
            x="ANO",
            y="VALOR EXECUTADO",
            markers=True
        )
        fig.update_layout(
            xaxis_title="Ano",
            yaxis_title="Executado (R$)"
        )
        st.plotly_chart(fig, use_container_width=True)

    with f4:
        st.subheader(f"Executado {ano_1} x {ano_2}")
        comp_exec = (
            df_filtro[df_filtro["ANO"].isin([ano_1, ano_2])]
            .groupby("ANO")["VALOR EXECUTADO"]
            .sum()
            .reset_index()
        )
        fig = px.bar(
            comp_exec.astype({"ANO": str}),
            x="ANO",
            y="VALOR EXECUTADO",
            color="ANO",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_xaxes(
            tickmode="array",
            tickvals=[ano_1, ano_2],
            ticktext=[str(ano_1), str(ano_2)]
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Valor por Categoria do Objeto")
    valor_cat = (
        df_filtro
        .groupby("CATEGORIA DO OBJETO")["VALOR TOTAL"]
        .sum()
        .reset_index()
        .sort_values("VALOR TOTAL", ascending=False)
    )
    fig = px.bar(
        valor_cat,
        x="CATEGORIA DO OBJETO",
        y="VALOR TOTAL",
        color="VALOR TOTAL",
        color_continuous_scale="Viridis"
    )
    fig.update_layout(
        xaxis_title="Categoria",
        yaxis_title="Valor (R$)",
        coloraxis_showscale=False
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ==============================================================================
# 11. SEÇÃO ESTRATÉGICA
# ==============================================================================

# Validação do estado do radio button lateral para controle do fluxo estratégico temporal
mostrar_est = (visualizacao == "Dashboard Completo" or visualizacao == "Estratégico")

if mostrar_est:
    st.markdown(
        '<div class="section-title">🎯 Direcionamento Estratégico</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-subtitle">Evolução temporal e comportamento dos contratos.</div>',
        unsafe_allow_html=True
    )

    e1, e2 = st.columns(2)

    with e1:
        st.subheader("Contratos Mês a Mês")
        mensal = (
            df_filtro
            .groupby(["ANO", "MÊS"])
            .size()
            .reset_index(name="Quantidade")
        )
        fig = px.line(
            mensal,
            x="MÊS",
            y="Quantidade",
            color="ANO",
            markers=True
        )
        fig.update_layout(
            xaxis=dict(
                tickmode="array",
                tickvals=list(meses.keys()),
                ticktext=list(meses.values())
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    with e2:
        st.subheader(f"Comparação Mensal {ano_1} x {ano_2}")
        comp_mensal = (
            df_filtro[df_filtro["ANO"].isin([ano_1, ano_2])]
            .groupby(["ANO", "MÊS"])
            .size()
            .reset_index(name="Quantidade")
        )
        fig = px.line(
            comp_mensal,
            x="MÊS",
            y="Quantidade",
            color="ANO",
            markers=True
        )
        fig.update_layout(
            xaxis=dict(
                tickmode="array",
                tickvals=list(meses.keys()),
                ticktext=list(meses.values())
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Comportamento Mensal por Categoria")
    cat_mes = (
        df_filtro
        .groupby(["MÊS", "CATEGORIA DO OBJETO"])
        .size()
        .reset_index(name="Quantidade")
    )
    fig = px.line(
        cat_mes,
        x="MÊS",
        y="Quantidade",
        color="CATEGORIA DO OBJETO",
        markers=True
    )
    fig.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=list(meses.keys()),
            ticktext=list(meses.values())
        )
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top 10 Contratadas")
    top = (
        df_filtro
        .groupby("CONTRATADA")
        .size()
        .reset_index(name="Quantidade")
        .sort_values("Quantidade", ascending=False)
        .head(10)
    )
    fig = px.bar(
        top,
        x="Quantidade",
        y="CONTRATADA",
        orientation="h",
        color="Quantidade",
        color_continuous_scale="Plasma"
    )
    fig.update_layout(
        xaxis_title="Contratos",
        yaxis_title="Contratada",
        coloraxis_showscale=False
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ==============================================================================
# 12. APRESENTAÇÃO E DOWNLOAD DA BASE
# ==============================================================================

st.markdown('<div class="section-title">📄 Dados</div>', unsafe_allow_html=True)

with st.expander("Visualizar dados filtrados"):
    st.dataframe(df_filtro, use_container_width=True)

# Conversão final da base processada/filtrada para string passível de exportação
csv = df_filtro.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Baixar dados filtrados",
    data=csv,
    file_name="contratos_filtrados.csv",
    mime="text/csv"
)