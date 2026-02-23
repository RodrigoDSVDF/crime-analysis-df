import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ---------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA E CSS CUSTOMIZADO
# ---------------------------------------------------
st.set_page_config(page_title="Painel Analítico Criminalidade DF", layout="wide")

# Injeta CSS personalizado
st.markdown("""
<style>
    /* Fonte principal */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Cabeçalhos */
    h1 {
        color: #0a2b4e;
        font-weight: 700;
        margin-bottom: 1rem;
        border-left: 5px solid #e53e3e;
        padding-left: 1rem;
    }
    h2, h3 {
        color: #1e3a6f;
    }
    
    /* Sidebar */
    .css-1d391kg, .css-12oz5g7 {
        background-color: #f8fafc;
    }
    .sidebar .sidebar-content {
        background-color: #f8fafc;
    }
    
    /* KPIs - cartões */
    div.css-1r6slb0.e1tzin5v2 {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    div.css-1r6slb0.e1tzin5v2:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 18px rgba(0,0,0,0.1);
    }
    
    /* Métricas dentro dos cartões */
    div.css-1xarl3l.e16fv1kl3 {
        background-color: transparent;
    }
    
    /* Gráficos */
    .stPlotlyChart {
        background-color: white;
        border-radius: 12px;
        padding: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    /* Títulos das seções */
    .stSubheader {
        color: #0a2b4e;
        font-weight: 600;
        font-size: 1.3rem;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #eef2f6;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Divisor */
    hr {
        margin: 25px 0px;
        border: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, #ccc, transparent);
    }
    
    /* Pills (filtros) */
    div[data-testid="stPills"] button {
        border-radius: 20px;
        margin-right: 5px;
        margin-bottom: 5px;
        border: 1px solid #d1d5db;
        background-color: white;
        color: #1f2937;
    }
    div[data-testid="stPills"] button[aria-pressed="true"] {
        background-color: #1e3a6f;
        color: white;
        border-color: #1e3a6f;
    }
    
    /* Multiselect (regiões) */
    div[data-baseweb="select"] {
        border-radius: 8px;
    }
    
    /* Botão limpar filtros */
    .stButton button {
        background-color: #1e3a6f;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 16px;
        font-weight: 600;
        transition: background-color 0.2s;
    }
    .stButton button:hover {
        background-color: #0a2b4e;
        color: white;
    }
    
    /* Estilo para a fonte dos dados */
    .fonte-dados {
        text-align: center;
        color: #4a5568;
        font-size: 0.9rem;
        margin-top: 20px;
        margin-bottom: 10px;
        padding: 10px;
        background-color: #edf2f7;
        border-radius: 8px;
        border-left: 5px solid #1e3a6f;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# CARREGAMENTO DOS DADOS
# ---------------------------------------------------
@st.cache_data
def carregar_dados():
    df = pd.read_csv("base_criminalidade_tratada.csv")

    def classificar(crime):
        c = str(crime).upper()
        if any(x in c for x in ['HOMICÍDIO', 'LATROCÍNIO', 'MORTE']):
            return 'Vida'
        if 'ROUBO' in c:
            return 'Roubo'
        if 'FURTO' in c:
            return 'Furto'
        return 'Outros'

    df["Categoria"] = df["Tipo_Crime"].apply(classificar)
    return df

df = carregar_dados()

# ---------------------------------------------------
# SIDEBAR — FILTROS COMPACTOS (ESTILO "V")
# ---------------------------------------------------
st.sidebar.header("🔍 Filtros")

# Anos - usando pills para seleção múltipla visual
anos_disponiveis = sorted(df["Ano"].unique())
anos_selecionados = st.sidebar.pills(
    "📅 Anos",
    options=anos_disponiveis,
    selection_mode="multi",
    default=[max(anos_disponiveis)]
)

# Tipos de crime - também com pills
crimes_disponiveis = sorted(df["Tipo_Crime"].unique())
crimes_selecionados = st.sidebar.pills(
    "🔫 Tipos de Crime",
    options=crimes_disponiveis,
    selection_mode="multi",
    default=crimes_disponiveis
)

# Regiões - multiselect tradicional, mas compacto
regioes = st.sidebar.multiselect(
    "📍 Regiões (opcional)",
    options=sorted(df["Regiao"].unique()),
    placeholder="Selecione..."
)

# Botão para limpar filtros
if st.sidebar.button("🔄 Limpar Filtros"):
    st.rerun()

# Fallback para versões antigas do Streamlit (sem pills)
# anos_selecionados = st.sidebar.multiselect("Anos", anos_disponiveis, default=[max(anos_disponiveis)])
# crimes_selecionados = st.sidebar.multiselect("Tipos de Crime", crimes_disponiveis, default=crimes_disponiveis)

# ---------------------------------------------------
# FILTRAGEM
# ---------------------------------------------------
df_filtro = df[
    (df["Ano"].isin(anos_selecionados)) &
    (df["Tipo_Crime"].isin(crimes_selecionados))
]

if regioes:
    df_filtro = df_filtro[df_filtro["Regiao"].isin(regioes)]

# ---------------------------------------------------
# TÍTULO DINÂMICO
# ---------------------------------------------------
texto_anos = ", ".join(map(str, sorted(anos_selecionados)))
st.title(f"📊 Análise de Crimes no DF : dados de ref 2015   — {texto_anos}")

# ---------------------------------------------------
# KPIs
# ---------------------------------------------------
total_periodo = df_filtro["Quantidade"].sum()
regioes_afetadas = df_filtro["Regiao"].nunique()

ano_ref = max(anos_selecionados) if anos_selecionados else None
if ano_ref and ano_ref - 1 in df["Ano"].unique():
    ano_anterior = ano_ref - 1
    total_atual = df[df["Ano"] == ano_ref]["Quantidade"].sum()
    total_passado = df[df["Ano"] == ano_anterior]["Quantidade"].sum()
    variacao = ((total_atual - total_passado) / total_passado * 100) if total_passado else 0
else:
    variacao = 0

k1, k2, k3 = st.columns(3)
with k1:
    st.metric("Total no Período", f"{total_periodo:,.0f}".replace(",", "."))
with k2:
    st.metric(f"Variação {ano_ref} vs {ano_anterior if 'ano_anterior' in locals() else 'anterior'}", f"{variacao:.2f}%")
with k3:
    st.metric("Regiões Impactadas", regioes_afetadas)

st.divider()

# ---------------------------------------------------
# RANKING TERRITORIAL
# ---------------------------------------------------
ranking = df_filtro.groupby("Regiao")["Quantidade"].sum().reset_index()
ranking = ranking[ranking["Regiao"].notna() & (ranking["Regiao"].astype(str).str.strip() != "")]
ranking = ranking.sort_values("Quantidade", ascending=False).head(20)

fig_rank = px.bar(
    ranking,
    x="Quantidade",
    y="Regiao",
    orientation="h",
    color="Quantidade",
    color_continuous_scale="Reds",
    title="Regiões com Maior Incidência",
    text="Regiao"
)

fig_rank.update_layout(
    yaxis={'categoryorder': 'total descending'},
    margin=dict(l=200)
)
st.plotly_chart(fig_rank, use_container_width=True)

# ---------------------------------------------------
# TENDÊNCIA TEMPORAL
# ---------------------------------------------------
st.subheader("📈 Tendência Temporal")

serie = df[
    (df["Ano"].isin(anos_selecionados)) &
    (df["Tipo_Crime"].isin(crimes_selecionados))
].groupby("Ano")["Quantidade"].sum().reset_index()

serie["Media_Movel"] = serie["Quantidade"].rolling(3, min_periods=1).mean()

fig_trend = px.line(
    serie,
    x="Ano",
    y=["Quantidade", "Media_Movel"],
    markers=True
)
st.plotly_chart(fig_trend, use_container_width=True)

# ---------------------------------------------------
# HEATMAP
# ---------------------------------------------------
st.subheader("🔥 Mapa de Calor Região x Ano")

pivot_data = df[df["Tipo_Crime"].isin(crimes_selecionados)]
pivot = pivot_data.pivot_table(values="Quantidade", index="Regiao", columns="Ano", aggfunc="sum", fill_value=0)

fig_heat = px.imshow(pivot, aspect="auto", color_continuous_scale="Reds", 
                     labels=dict(x="Ano", y="Região", color="Quantidade"))
st.plotly_chart(fig_heat, use_container_width=True)

# ---------------------------------------------------
# PARETO
# ---------------------------------------------------
st.subheader("🎯 Concentração Criminal (Pareto)")

pareto = df_filtro.groupby("Regiao")["Quantidade"].sum().sort_values(ascending=False)
pareto_acum = pareto.cumsum() / pareto.sum() * 100

fig_pareto = px.bar(x=pareto.index, y=pareto.values, labels={'x':'Região', 'y':'Quantidade'})
fig_pareto.add_scatter(x=pareto.index, y=pareto_acum, mode='lines+markers', name='% Acumulado', yaxis='y2')

fig_pareto.update_layout(
    yaxis2=dict(title='Percentual Acumulado', overlaying='y', side='right', range=[0, 110])
)
st.plotly_chart(fig_pareto, use_container_width=True)

# ---------------------------------------------------
# DISTRIBUIÇÃO POR TIPO DE CRIME (DETALHADA)
# ---------------------------------------------------
st.subheader("🥧 Distribuição por Tipo de Crime")

df_tipo = df_filtro.groupby("Tipo_Crime", as_index=False)["Quantidade"].sum()

# Opcional: limitar a N maiores e agrupar o resto como "Outros"
# N = 10
# df_tipo = df_tipo.sort_values("Quantidade", ascending=False)
# if len(df_tipo) > N:
#     outros = pd.DataFrame({
#         "Tipo_Crime": ["Outros"],
#         "Quantidade": [df_tipo.iloc[N:]["Quantidade"].sum()]
#     })
#     df_tipo = pd.concat([df_tipo.head(N), outros], ignore_index=True)

fig_cat = px.pie(
    df_tipo,
    values="Quantidade",
    names="Tipo_Crime",
    hole=0.5,
    title="Participação por Tipo de Crime"
)
st.plotly_chart(fig_cat, use_container_width=True)

# ---------------------------------------------------
# FONTE DOS DADOS
# ---------------------------------------------------
st.markdown("""
<div class="fonte-dados">
    <strong>📌 Fonte dos dados:</strong> Portal da Transparência do Governo do Distrito Federal (dados de 2015 em diante)
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TABELA ANALÍTICA
# ---------------------------------------------------
with st.expander("📋 Visualizar Dados Detalhados"):
    st.dataframe(df_filtro.sort_values("Quantidade", ascending=False), use_container_width=True)
