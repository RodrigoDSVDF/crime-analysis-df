import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ---------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ---------------------------------------------------
st.set_page_config(
    page_title="Painel Criminalidade DF",
    page_icon="🚔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------
# CSS CUSTOMIZADO PROFISSIONAL & MOBILE-FIRST
# ---------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        -webkit-font-smoothing: antialiased;
    }
    
    :root {
        --primary: #0f172a;
        --primary-light: #1e293b;
        --accent: #dc2626;
        --accent-light: #ef4444;
        --success: #059669;
        --warning: #d97706;
        --bg: #f8fafc;
        --card: #ffffff;
        --text: #1e293b;
        --text-muted: #64748b;
        --border: #e2e8f0;
    }
    
    .main .block-container {
        padding: 1rem;
        max-width: 100%;
    }
    
    @media (min-width: 768px) {
        .main .block-container {
            padding: 2rem;
            max-width: 95%;
        }
    }
    
    .dashboard-header {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 40px -10px rgba(15, 23, 42, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .dashboard-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(220, 38, 38, 0.2) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    .dashboard-header h1 {
        color: white !important;
        font-size: clamp(1.5rem, 5vw, 2.5rem);
        font-weight: 800;
        margin: 0;
        border: none;
        padding: 0;
        position: relative;
        z-index: 1;
    }
    
    .dashboard-header .subtitle {
        color: rgba(255,255,255,0.8);
        font-size: 0.95rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .kpi-card {
        background: var(--card);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid var(--border);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: var(--accent);
    }
    
    .kpi-card.positive::before { background: var(--success); }
    .kpi-card.negative::before { background: var(--accent); }
    .kpi-card.neutral::before { background: var(--warning); }
    
    .kpi-label {
        font-size: 0.875rem;
        color: var(--text-muted);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    .kpi-value {
        font-size: clamp(1.5rem, 4vw, 2.25rem);
        font-weight: 800;
        color: var(--text);
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    
    .kpi-delta {
        font-size: 0.875rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        background: rgba(220, 38, 38, 0.1);
        color: var(--accent);
    }
    
    .kpi-delta.positive {
        background: rgba(5, 150, 105, 0.1);
        color: var(--success);
    }
    
    .chart-card {
        background: var(--card);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid var(--border);
        margin-bottom: 1.5rem;
    }
    
    .chart-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    
    .chart-title {
        font-size: 1.125rem;
        font-weight: 700;
        color: var(--primary);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .filter-section {
        background: var(--card);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid var(--border);
    }
    
    /* Estilo específico para pills de categoria */
    div[data-testid="stPills"] {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    
    div[data-testid="stPills"] button {
        border-radius: 8px !important;
        border: 2px solid var(--border) !important;
        background: var(--bg) !important;
        color: var(--text) !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.2rem !important;
        transition: all 0.2s !important;
        font-size: 0.9rem !important;
    }
    
    div[data-testid="stPills"] button[aria-pressed="true"] {
        background: var(--primary) !important;
        color: white !important;
        border-color: var(--primary) !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.3);
        transform: scale(1.05);
    }
    
    div[data-testid="stPills"] button:hover {
        border-color: var(--accent) !important;
        transform: translateY(-2px);
    }
    
    .stButton button {
        background: var(--primary) !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
        width: 100%;
    }
    
    .stButton button:hover {
        background: var(--accent) !important;
        transform: translateY(-2px);
        box-shadow: 0 10px 20px -5px rgba(220, 38, 38, 0.3);
    }
    
    .streamlit-expanderHeader {
        background: var(--bg) !important;
        border-radius: 12px !important;
        border: 1px solid var(--border) !important;
        font-weight: 600 !important;
        color: var(--primary) !important;
    }
    
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid var(--border) !important;
    }
    
    .footer-info {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-top: 2rem;
        border-left: 4px solid var(--primary);
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 0.9rem;
        color: var(--text-muted);
    }
    
    @media (max-width: 640px) {
        .kpi-container { grid-template-columns: 1fr; }
        .chart-card { padding: 1rem; }
        .dashboard-header { padding: 1rem; }
        
        div[data-testid="stPills"] button {
            padding: 0.75rem 1rem !important;
            min-height: 44px;
            font-size: 0.85rem !important;
        }
        
        .stButton button { min-height: 48px; }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .kpi-card, .chart-card {
        animation: fadeIn 0.5s ease-out forwards;
    }
    
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }
    
    @media (max-width: 768px) {
        [data-testid="stSidebarNav"] { display: none; }
    }
    
    /* Badge de contador */
    .category-counter {
        background: var(--accent);
        color: white;
        border-radius: 12px;
        padding: 0.2rem 0.6rem;
        font-size: 0.75rem;
        font-weight: 700;
        margin-left: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# CARREGAMENTO DOS DADOS
# ---------------------------------------------------
@st.cache_data(ttl=3600, show_spinner="Carregando dados...")
def carregar_dados():
    try:
        df = pd.read_csv("base_criminalidade_tratada.csv")
        
        colunas_necessarias = ['Tipo_Crime', 'Ano', 'Quantidade', 'Regiao']
        for col in colunas_necessarias:
            if col not in df.columns:
                st.error(f"Coluna '{col}' não encontrada no dataset")
                return pd.DataFrame()
        
        # Classificação expandida e precisa
        def classificar(crime):
            c = str(crime).upper().strip()
            
            # Crimes contra a vida (prioridade máxima)
            if any(x in c for x in ['HOMICÍDIO', 'LATROCÍNIO', 'MORTE', 'FEMINICÍDIO', 'INFANTICÍDIO', 'ASSASSINATO']):
                return 'Crimes Contra a Vida'
            
            # Roubos (várias modalidades)
            elif any(x in c for x in ['ROUBO', 'ASSALTO']) and 'FURTO' not in c:
                if any(x in c for x in ['BANCO', 'CAIXA ELETRÔNICO', 'INSTITUIÇÃO FINANCEIRA']):
                    return 'Roubos a Bancos'
                elif any(x in c for x in ['VEÍCULO', 'CARRO', 'MOTO', 'CAMINHÃO', 'AUTOMÓVEL', 'CARGA']):
                    return 'Roubos de Veículos'
                elif any(x in c for x in ['RESIDÊNCIA', 'CASA', 'APARTAMENTO', 'DOMICÍLIO']):
                    return 'Roubos a Residências'
                elif any(x in c for x in ['COMÉRCIO', 'ESTABELECIMENTO', 'LOJA']):
                    return 'Roubos a Comércio'
                elif any(x in c for x in ['COLETIVO', 'ÔNIBUS', 'METRÔ', 'TRANSPORTE']):
                    return 'Roubos em Transporte'
                elif any(x in c for x in ['PESSOA', 'PEDESTRE', 'TRanseunte']):
                    return 'Roubos a Pessoas'
                else:
                    return 'Outros Roubos'
            
            # Furtos (várias modalidades)
            elif 'FURTO' in c:
                if any(x in c for x in ['VEÍCULO', 'CARRO', 'MOTO', 'CAMINHÃO']):
                    return 'Furtos de Veículos'
                elif any(x in c for x in ['RESIDÊNCIA', 'CASA', 'APARTAMENTO']):
                    return 'Furtos a Residências'
                elif any(x in c for x in ['COMÉRCIO', 'ESTABELECIMENTO', 'LOJA']):
                    return 'Furtos a Comércio'
                else:
                    return 'Outros Furtos'
            
            # Drogas
            elif any(x in c for x in ['TRÁFICO', 'DROGA', 'ENTORPECENTE', 'NARCÓTICO', 'MACONHA', 'COCAÍNA']):
                return 'Tráfico de Drogas'
            
            # Violência doméstica e sexual
            elif any(x in c for x in ['VIOLÊNCIA DOMÉSTICA', 'LESÃO CORPORAL', 'AMEAÇA', 'ESTUPRO', 'ABUSO SEXUAL']):
                return 'Violência Doméstica/Sexual'
            
            # Crimes patrimoniais
            elif any(x in c for x in ['EXTORSÃO', 'SEQUESTRO', 'CÁRCERE', 'ESTELIONATO', 'FRAUDE']):
                return 'Crimes Patrimoniais'
            
            # Armas e munições
            elif any(x in c for x in ['ARMA', 'MUNIÇÃO', 'PORTE ILEGAL', 'POSSE DE ARMA']):
                return 'Posse/Porte de Armas'
            
            # Danos e vandalismo
            elif any(x in c for x in ['DANO', 'VANDALISMO', 'DEPREDAÇÃO']):
                return 'Danos/Vandalismo'
            
            # Outros crimes específicos
            elif any(x in c for x in ['FALSIDADE', 'DOCUMENTO', 'MOEDA FALSA']):
                return 'Falsificação'
            
            elif any(x in c for x in ['CONTRA A ORDEM', 'DESACATO', 'DESOBEDIÊNCIA', 'RESISTÊNCIA']):
                return 'Crimes contra a Ordem Pública'
            
            else:
                return 'Outros Crimes'
        
        df["Categoria"] = df["Tipo_Crime"].apply(classificar)
        
        # Limpeza de dados
        df = df.dropna(subset=['Quantidade', 'Ano'])
        df['Quantidade'] = pd.to_numeric(df['Quantidade'], errors='coerce').fillna(0)
        df['Ano'] = pd.to_numeric(df['Ano'], errors='coerce').astype(int)
        
        return df
        
    except FileNotFoundError:
        st.error("Arquivo 'base_criminalidade_tratada.csv' não encontrado!")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()

df = carregar_dados()

if df.empty:
    st.stop()

# ---------------------------------------------------
# SIDEBAR COM TODAS AS CATEGORIAS
# ---------------------------------------------------
with st.sidebar:
    st.markdown("### 🎛️ Painel de Controle")
    
    # Obtém todas as categorias únicas presentes nos dados
    todas_categorias = sorted(df["Categoria"].unique())
    
    st.markdown("**📊 Categorias Criminais Disponíveis:**")
    st.caption(f"Total: {len(todas_categorias)} categorias")
    
    # Pills com TODAS as categorias disponíveis no dataset
    categorias_selecionadas = st.pills(
        "Selecione as categorias para análise:",
        options=todas_categorias,
        selection_mode="multi",
        default=todas_categorias,  # Todas selecionadas por padrão
        help="Desmarque para filtrar categorias específicas"
    )
    
    # Se nenhuma categoria selecionada, usa todas
    if not categorias_selecionadas:
        categorias_selecionadas = todas_categorias
        st.warning("⚠️ Selecione pelo menos uma categoria. Usando todas por padrão.")
    
    # Mostra contagem por categoria
    with st.expander("📈 Resumo por Categoria"):
        resumo_cat = df[df["Categoria"].isin(categorias_selecionadas)].groupby("Categoria")["Quantidade"].sum().sort_values(ascending=False)
        for cat, qtd in resumo_cat.items():
            st.write(f"**{cat}:** {qtd:,} ocorrências")
    
    st.divider()
    
    # Filtro de anos
    anos_disponiveis = sorted(df["Ano"].unique(), reverse=True)
    anos_selecionados = st.pills(
        "📅 Anos",
        options=anos_disponiveis,
        selection_mode="multi",
        default=[anos_disponiveis[0]] if anos_disponiveis else [],
        help="Selecione um ou mais anos"
    )
    
    if not anos_selecionados:
        anos_selecionados = [max(anos_disponiveis)]
    
    st.divider()
    
    # Filtro de região
    regioes_disponiveis = sorted(df["Regiao"].dropna().unique())
    regioes = st.multiselect(
        "📍 Regiões",
        options=regioes_disponiveis,
        placeholder="Todas as regiões...",
        help="Deixe vazio para todas"
    )
    
    if st.button("🔄 Resetar Filtros", use_container_width=True):
        st.rerun()

# ---------------------------------------------------
# FILTRAGEM DOS DADOS
# ---------------------------------------------------
df_filtrado = df[
    (df["Categoria"].isin(categorias_selecionadas)) &
    (df["Ano"].isin(anos_selecionados))
]

if regioes:
    df_filtrado = df_filtrado[df_filtrado["Regiao"].isin(regioes)]

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
anos_texto = " • ".join(map(str, sorted(anos_selecionados)))
categorias_texto = f"{len(categorias_selecionadas)} categorias selecionadas"

st.markdown(f"""
<div class="dashboard-header">
    <h1>🚔 Análise Criminal do DF</h1>
    <div class="subtitle">{categorias_texto} | Período: {anos_texto}</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# KPIs
# ---------------------------------------------------
total_periodo = int(df_filtrado["Quantidade"].sum())
regioes_afetadas = df_filtrado["Regiao"].nunique()

# Variação ano a ano
variacao = 0
tendencia = "neutral"
if len(anos_selecionados) >= 2:
    anos_ord = sorted(anos_selecionados)
    totais_por_ano = df_filtrado.groupby("Ano")["Quantidade"].sum()
    if len(totais_por_ano) >= 2:
        ultimo = totais_por_ano[anos_ord[-1]]
        penultimo = totais_por_ano[anos_ord[-2]]
        variacao = ((ultimo - penultimo) / penultimo * 100) if penultimo else 0
        tendencia = "positive" if variacao < 0 else "negative"

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="kpi-card neutral">
        <div class="kpi-label">Total de Ocorrências</div>
        <div class="kpi-value">{total_periodo:,}</div>
        <div class="kpi-delta">{len(categorias_selecionadas)} categorias ativas</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    delta_class = "positive" if variacao < 0 else "negative" if variacao > 0 else "neutral"
    delta_icon = "↓" if variacao < 0 else "↑" if variacao > 0 else "→"
    st.markdown(f"""
    <div class="kpi-card {delta_class}">
        <div class="kpi-label">Variação Anual</div>
        <div class="kpi-value">{abs(variacao):.1f}%</div>
        <div class="kpi-delta {delta_class}">{delta_icon} vs anterior</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card neutral">
        <div class="kpi-label">Cobertura Territorial</div>
        <div class="kpi-value">{regioes_afetadas}</div>
        <div class="kpi-delta">Regiões</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# GRÁFICOS PRINCIPAIS
# ---------------------------------------------------
col_left, col_right = st.columns([2, 1], gap="large")

with col_left:
    # Ranking Territorial
    st.markdown("""
    <div class="chart-card">
        <div class="chart-header">
            <div class="chart-title">🏆 Top Regiões - Todas Categorias</div>
        </div>
    """, unsafe_allow_html=True)
    
    ranking = df_filtrado.groupby("Regiao")["Quantidade"].sum().reset_index()
    ranking = ranking[ranking["Regiao"].notna()].sort_values("Quantidade", ascending=True).tail(12)
    
    fig_rank = px.bar(
        ranking,
        x="Quantidade",
        y="Regiao",
        orientation="h",
        color="Quantidade",
        color_continuous_scale="Reds",
        text="Quantidade",
        height=450
    )
    
    fig_rank.update_traces(
        textposition='outside',
        texttemplate='%{text:,.0f}',
        marker_line_width=0
    )
    
    fig_rank.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=10, b=10),
        coloraxis_showscale=False,
        xaxis_title="",
        yaxis_title="",
        font=dict(family="Inter, sans-serif")
    )
    
    st.plotly_chart(fig_rank, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    # GRÁFICO DE PIZZA COM TODAS AS CATEGORIAS SELECIONADAS
    st.markdown(f"""
    <div class="chart-card">
        <div class="chart-header">
            <div class="chart-title">🎯 Distribuição por Categoria</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Agrupa por categoria mantendo todas as selecionadas
    df_pizza = df_filtrado.groupby("Categoria")["Quantidade"].sum().reset_index()
    
    # Garante que todas as categorias selecionadas apareçam (mesmo com valor 0)
    todas_cats_df = pd.DataFrame({"Categoria": categorias_selecionadas})
    df_pizza = todas_cats_df.merge(df_pizza, on="Categoria", how="left").fillna(0)
    df_pizza = df_pizza[df_pizza["Quantidade"] > 0]  # Remove apenas as realmente zeradas
    
    # Cores distintas para cada categoria
    cores_categorias = px.colors.qualitative.Bold + px.colors.qualitative.Vivid
    
    fig_pie = px.pie(
        df_pizza,
        values="Quantidade",
        names="Categoria",
        hole=0.55,
        color="Categoria",
        color_discrete_sequence=cores_categorias
    )
    
    fig_pie.update_traces(
        textposition='inside',
        textinfo='percent+label',
        insidetextorientation='radial',
        pull=[0.02 if qtd == df_pizza["Quantidade"].max() else 0 for qtd in df_pizza["Quantidade"]],
        marker=dict(line=dict(color='white', width=2)),
        rotation=90
    )
    
    fig_pie.update_layout(
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
            font=dict(size=10),
            traceorder='normal'
        ),
        margin=dict(l=10, r=120, t=30, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif"),
        annotations=[dict(
            text=f'<b>{total_periodo:,}</b><br>Total',
            x=0.5, y=0.5,
            font_size=14,
            showarrow=False,
            font=dict(family="Inter, sans-serif", color="#0f172a")
        )]
    )
    
    st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# ANÁLISE TEMPORAL POR CATEGORIA
# ---------------------------------------------------
st.markdown("""
<div class="chart-card">
    <div class="chart-header">
        <div class="chart-title">📈 Evolução Temporal por Categoria</div>
    </div>
""", unsafe_allow_html=True)

# Série temporal mantendo todas as categorias selecionadas
serie_temporal = df[
    (df["Categoria"].isin(categorias_selecionadas)) &
    (df["Ano"].isin(anos_disponiveis))
].groupby(["Ano", "Categoria"])["Quantidade"].sum().reset_index()

# Pivot para garantir que todas as categorias apareçam na legenda
pivot_temporal = serie_temporal.pivot(index="Ano", columns="Categoria", values="Quantidade").fillna(0)
pivot_temporal = pivot_temporal.reset_index().melt(id_vars=["Ano"], var_name="Categoria", value_name="Quantidade")

fig_line = px.line(
    pivot_temporal,
    x="Ano",
    y="Quantidade",
    color="Categoria",
    markers=True,
    line_shape="spline",
    color_discrete_sequence=cores_categorias
)

fig_line.update_traces(line_width=3, marker_size=10, opacity=0.9)
fig_line.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=10, r=10, t=10, b=10),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(size=10),
        traceorder='normal'
    ),
    xaxis_title="",
    yaxis_title="Quantidade",
    font=dict(family="Inter, sans-serif"),
    hovermode="x unified",
    height=450
)

st.plotly_chart(fig_line, use_container_width=True, config={'displayModeBar': False})
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# GRID INFERIOR: HEATMAP E PARETO
# ---------------------------------------------------
col_heat, col_pareto = st.columns(2)

with col_heat:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-header">
            <div class="chart-title">🔥 Mapa de Calor: Região x Ano</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Top regiões das categorias selecionadas
    top_regioes = df_filtrado.groupby("Regiao")["Quantidade"].sum().nlargest(8).index
    df_heat = df_filtrado[df_filtrado["Regiao"].isin(top_regioes)]
    
    pivot_heat = df_heat.pivot_table(
        values="Quantidade", 
        index="Regiao", 
        columns="Ano", 
        aggfunc="sum", 
        fill_value=0
    )
    
    fig_heat = px.imshow(
        pivot_heat,
        aspect="auto",
        color_continuous_scale="Reds",
        labels=dict(color="Ocorrências"),
        height=400,
        text_auto=True
    )
    
    fig_heat.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif")
    )
    
    st.plotly_chart(fig_heat, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

with col_pareto:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-header">
            <div class="chart-title">📊 Lei de Pareto (80/20)</div>
        </div>
    """, unsafe_allow_html=True)
    
    pareto = df_filtrado.groupby("Regiao")["Quantidade"].sum().sort_values(ascending=False).head(12)
    pareto_acum = (pareto.cumsum() / pareto.sum() * 100).round(1)
    
    fig_pareto = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig_pareto.add_trace(
        go.Bar(
            x=pareto.index, 
            y=pareto.values, 
            name="Quantidade", 
            marker_color="#dc2626",
            opacity=0.8
        ),
        secondary_y=False
    )
    
    fig_pareto.add_trace(
        go.Scatter(
            x=pareto.index, 
            y=pareto_acum.values, 
            name="% Acumulado", 
            mode='lines+markers', 
            line=dict(color="#0f172a", width=3),
            marker=dict(size=8)
        ),
        secondary_y=True
    )
    
    # Linha de referência 80%
    fig_pareto.add_hline(y=80, line_dash="dash", line_color="green", 
                        annotation_text="80%", secondary_y=True)
    
    fig_pareto.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        font=dict(family="Inter, sans-serif"),
        height=400,
        xaxis_tickangle=-45
    )
    
    fig_pareto.update_yaxes(title_text="Quantidade", secondary_y=False)
    fig_pareto.update_yaxes(title_text="% Acumulado", range=[0, 105], secondary_y=True)
    
    st.plotly_chart(fig_pareto, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# TABELA DETALHADA
# ---------------------------------------------------
with st.expander("📋 Dados Completos por Categoria e Região"):
    
    # Resumo estatístico por categoria
    st.subheader("Resumo Estatístico")
    stats_cols = st.columns(len(categorias_selecionadas)) if len(categorias_selecionadas) <= 4 else st.columns(4)
    
    resumo_stats = df_filtrado.groupby("Categoria")["Quantidade"].agg(['sum', 'mean', 'count'])
    
    for idx, (cat, row) in enumerate(resumo_stats.iterrows()):
        col_idx = idx % 4
        with stats_cols[col_idx]:
            st.metric(
                label=cat[:20] + "..." if len(cat) > 20 else cat,
                value=f"{int(row['sum']):,}",
                delta=f"{int(row['count'])} tipos"
            )
    
    st.divider()
    
    # Tabela detalhada
    st.dataframe(
        df_filtrado.sort_values(["Categoria", "Quantidade"], ascending=[True, False]),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Quantidade": st.column_config.NumberColumn("Qtd", format="%d"),
            "Ano": st.column_config.NumberColumn("Ano", format="%d"),
            "Regiao": "Região",
            "Tipo_Crime": "Tipo Específico",
            "Categoria": st.column_config.Column("Categoria", width="medium")
        }
    )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown(f"""
<div class="footer-info">
    <span>📌</span>
    <div>
        <strong>Fonte:</strong> Portal da Transparência do Governo do Distrito Federal<br>
        <small>Analisando {len(categorias_selecionadas)} categorias criminais | Atualizado: {pd.Timestamp.now().strftime("%d/%m/%Y %H:%M")}</small>
    </div>
</div>
""", unsafe_allow_html=True)
