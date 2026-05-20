import streamlit as st
import plotly.express as px
import pandas as pd
import os

# ================= CONFIG =================
st.set_page_config(page_title="PROADMI - Contratos", page_icon="📊", layout="wide")

st.title("📊 PROADMI - Dashboard de Contratos")
st.markdown("Análise dos contratos da UPE")

# ================= LOAD =================

fl = st.file_uploader("📂 Upload da planilha", type=(["csv", "xlsx"]))

if fl is not None:
    df = pd.read_csv(fl)
else:
    os.chdir(r"C:\Users\johnn\Documents\GitHub\dashboard-streamlit-upe")
    df = pd.read_csv("PGC_Contratos_Limpos.csv")

# ================= TRATAMENTO LEVE =================

df["DATA DE INÍCIO"] = pd.to_datetime(df["DATA DE INÍCIO"], errors="coerce")
df["DATA DE TÉRMINO"] = pd.to_datetime(df["DATA DE TÉRMINO"], errors="coerce")

df["DURAÇÃO (DIAS)"] = (df["DATA DE TÉRMINO"] - df["DATA DE INÍCIO"]).dt.days
df["ANO"] = df["DATA DE INÍCIO"].dt.year

# % execução
df["% EXECUÇÃO"] = (df["VALOR EXECUTADO"] / df["VALOR TOTAL"]) * 100

# ================= FILTROS =================

st.sidebar.header("Filtros")

unidade = st.sidebar.multiselect("Unidade", df["UNIDADE BENEFICIADA"].unique())
categoria = st.sidebar.multiselect("Categoria", df["CATEGORIA DO OBJETO"].unique())
situacao = st.sidebar.multiselect("Situação", df["SITUAÇÃO DO CONTRATO"].unique())
contratada = st.sidebar.multiselect("Contratada", df["CONTRATADA"].unique())

df_filtro = df.copy()

if unidade:
    df_filtro = df_filtro[df_filtro["UNIDADE BENEFICIADA"].isin(unidade)]

if categoria:
    df_filtro = df_filtro[df_filtro["CATEGORIA DO OBJETO"].isin(categoria)]

if situacao:
    df_filtro = df_filtro[df_filtro["SITUAÇÃO DO CONTRATO"].isin(situacao)]

if contratada:
    df_filtro = df_filtro[df_filtro["CONTRATADA"].isin(contratada)]

# ================= KPIs =================

k1, k2, k3, k4 = st.columns(4)

k1.metric("💰 Valor Total", f"R$ {df_filtro['VALOR TOTAL'].sum():,.2f}")
k2.metric("📊 Executado", f"R$ {df_filtro['VALOR EXECUTADO'].sum():,.2f}")
k3.metric("📄 Nº Contratos", df_filtro.shape[0])
k4.metric("⚙️ Execução Média", f"{df_filtro['% EXECUÇÃO'].mean():.1f}%")

st.divider()

# ================= GRÁFICOS =================

col1, col2 = st.columns(2)

# 1️⃣ Valor por Categoria
with col1:
    st.subheader("📦 Valor por Categoria")

    cat = df_filtro.groupby("CATEGORIA DO OBJETO", as_index=False)["VALOR TOTAL"].sum()

    fig = px.bar(
        cat,
        x="CATEGORIA DO OBJETO",
        y="VALOR TOTAL",
        color="VALOR TOTAL",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig, use_container_width=True)

# 2️⃣ Distribuição por Situação
with col2:
    st.subheader("📌 Situação dos Contratos")

    # Filtrar valores inválidos
    df_situacao = df_filtro[
        (df_filtro["SITUAÇÃO DO CONTRATO"].notna()) &
        (df_filtro["SITUAÇÃO DO CONTRATO"].str.lower() != "nan") &
        (df_filtro["SITUAÇÃO DO CONTRATO"] != "Não informado")
    ]

    fig = px.pie(
        df_situacao,
        values="VALOR TOTAL",
        names="SITUAÇÃO DO CONTRATO",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    st.plotly_chart(fig, use_container_width=True)

# 3️⃣ Top Contratadas
st.subheader("🏢 Top 10 Contratadas")

top = (
    df_filtro.groupby("CONTRATADA", as_index=False)["VALOR TOTAL"]
    .sum()
    .sort_values(by="VALOR TOTAL", ascending=False)
    .head(10)
)

fig = px.bar(
    top,
    x="VALOR TOTAL",
    y="CONTRATADA",
    orientation="h",
    color="VALOR TOTAL",
    color_continuous_scale="Viridis"
)

st.plotly_chart(fig, use_container_width=True)

# 4️⃣ Valor por Unidade (Top 5)
st.subheader("🏫 Top 5 Unidades por Valor")

unit = (
    df_filtro.groupby("UNIDADE BENEFICIADA", as_index=False)["VALOR TOTAL"]
    .sum()
    .sort_values(by="VALOR TOTAL", ascending=False)
    .head(5)
)

fig = px.bar(
    unit,
    x="UNIDADE BENEFICIADA",
    y="VALOR TOTAL",
    color="VALOR TOTAL",
    color_continuous_scale="Teal"
)

st.plotly_chart(fig, use_container_width=True)

# 5️⃣ % de Execução por Categoria
st.subheader("⚙️ Execução Média por Categoria")

exec_cat = (
    df_filtro.groupby("CATEGORIA DO OBJETO", as_index=False)["% EXECUÇÃO"]
    .mean()
)

fig = px.bar(
    exec_cat,
    x="CATEGORIA DO OBJETO",
    y="% EXECUÇÃO",
    color="% EXECUÇÃO",
    color_continuous_scale="RdYlGn"
)

st.plotly_chart(fig, use_container_width=True)


# 6️⃣ Distribuição por Faixa de Valor
st.subheader("📊 Distribuição por Faixa de Valor")

# Criar faixas
bins = [0, 50000, 200000, 500000, 1000000, df_filtro["VALOR TOTAL"].max()]
labels = ["Até 50k", "50k-200k", "200k-500k", "500k-1M", "Acima de 1M"]

df_filtro["FAIXA VALOR"] = pd.cut(df_filtro["VALOR TOTAL"], bins=bins, labels=labels)

faixa = df_filtro["FAIXA VALOR"].value_counts().reset_index()
faixa.columns = ["Faixa", "Quantidade"]

fig = px.bar(
    faixa,
    x="Faixa",
    y="Quantidade",
    color="Quantidade",
    color_continuous_scale="Teal"
)

st.plotly_chart(fig, use_container_width=True)
# ================= TABELA =================

with st.expander("📄 Visualizar dados"):
    st.dataframe(df_filtro)

# ================= DOWNLOAD =================

csv = df_filtro.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Baixar dados filtrados",
    data=csv,
    file_name="contratos_filtrados.csv",
    mime="text/csv"
)