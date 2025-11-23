import os
from typing import Optional

import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client

# ------------------------------
# Configuração da página
# ------------------------------
st.set_page_config(
    page_title="IoT Temperature Monitoring Dashboard",
    page_icon="🌡️",
    layout="wide",
)

# ------------------------------
# Configuração do Supabase (opcional)
# ------------------------------
SUPABASE_URL = os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_ANON_KEY = os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")

if SUPABASE_URL and SUPABASE_ANON_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
else:
    supabase = None


# ------------------------------
# Função para carregar dados
# ------------------------------
def carregar_dados() -> Optional[pd.DataFrame]:
    df = None

    # 1) Tenta baixar do Supabase, se configurado
    if supabase is not None:
        try:
            data = supabase.storage.from_("tempiot").download("IOT-temp.csv")
            with open("IOT-temp.csv", "wb") as f:
                f.write(data)
            df = pd.read_csv("IOT-temp.csv")
        except Exception as e:
            st.warning(
                f"Não foi possível baixar do Supabase ({e}). "
                "Tentando usar o arquivo local 'IOT-temp.csv'..."
            )
            df = None
    else:
        st.info(
            "Variáveis do Supabase não configuradas. "
            "Usando o arquivo local 'IOT-temp.csv'."
        )

    # 2) Se não conseguiu via Supabase, tenta ler o CSV local
    if df is None:
        try:
            df = pd.read_csv("IOT-temp.csv")
        except Exception as e:
            st.error(f"Erro ao carregar dados locais: {e}")
            return None

    # 3) Tratamento dos dados
    df["noted_date"] = pd.to_datetime(
        df["noted_date"],
        format="%Y-%m-%d %H:%M:%S",
        errors="coerce",
    )

    # Deslocar a série temporal para começar hoje
    first_date = df["noted_date"].min()
    if pd.notna(first_date):
        first_date_norm = first_date.normalize()
        today = pd.Timestamp.today().normalize()
        delta = today - first_date_norm
        if delta.days > 0:
            df["noted_date"] = df["noted_date"] + delta

    # Renomear coluna se necessário
    if "room_id/id" in df.columns:
        df.rename(columns={"room_id/id": "room_id"}, inplace=True)

    # Ajustes finais
    df["temp"] = pd.to_numeric(df["temp"], errors="coerce")
    df = df.dropna(subset=["noted_date", "temp"])
    df = df.sort_values("noted_date").reset_index(drop=True)

    return df


# ------------------------------
# Carrega os dados
# ------------------------------
df = carregar_dados()

if df is None or df.empty:
    st.warning("Nenhum dado disponível para exibição no momento.")
    st.stop()

# ------------------------------
# Dashboard
# ------------------------------
st.title("Dashboard de Monitoramento de Temperaturas IoT")

# Resumo de dados
st.header("Resumo de Dados")
col1, col2, col3, col4 = st.columns(4)

media_temp = df["temp"].mean()
temp_max = df["temp"].max()
temp_min = df["temp"].min()
total_leituras = len(df)

with col1:
    st.metric(label="Média de Temperatura", value=f"{media_temp:.1f} °C")
with col2:
    st.metric(label="Temperatura Máxima", value=f"{temp_max:.1f} °C")
with col3:
    st.metric(label="Temperatura Mínima", value=f"{temp_min:.1f} °C")
with col4:
    st.metric(label="Total de Leituras", value=total_leituras)

# Gráfico: temperatura ao longo do tempo
fig1 = px.line(
    df,
    x="noted_date",
    y="temp",
    title="Temperatura ao Longo do Tempo",
    markers=True,
)
st.plotly_chart(fig1, use_container_width=True)

# Gráfico: contagem de leituras por hora
df["hour"] = df["noted_date"].dt.hour
contagem_hora = df.groupby("hour").size().reset_index(name="contagem")

fig2 = px.bar(
    contagem_hora,
    x="hour",
    y="contagem",
    title="Contagem de Leituras por Hora",
)
st.plotly_chart(fig2, use_container_width=True)

# Gráfico: temperaturas máximas e mínimas por dia
df["date"] = df["noted_date"].dt.date
agregados = (
    df.groupby("date")
    .agg({"temp": ["max", "min"]})
    .reset_index()
)
agregados.columns = ["date", "temp_max", "temp_min"]

fig3 = px.line(
    agregados,
    x="date",
    y=["temp_max", "temp_min"],
    title="Temperaturas Máximas e Mínimas por Dia",
)
st.plotly_chart(fig3, use_container_width=True)

# Rodapé
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.8em;'>"
    "IoT Temperature Monitoring Dashboard."
    "</div>",
    unsafe_allow_html=True,
)
