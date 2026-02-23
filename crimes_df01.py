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
    initial_sidebar_state="collapsed"  # Mobile-first: sidebar recolhida
)

# ---------------------------------------------------
# CSS CUSTOMIZADO PROFISSIONAL & MOBILE-FIRST
# ---------------------------------------------------
st.markdown("""
<style>
    /* Reset e Fontes */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    /* Cores do tema */
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
    
    /* Layout responsivo base */
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
    
    /* Header premium */
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
    
    /* Grid de KPIs responsivo */
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
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid var(--border);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
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
    
    /* Cards de gráficos */
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
    
    /* Filtros estilizados */
    .filter-section {
        background: var(--card);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid var(--border);
    }
    
    /* Pills modernos */
    div[data-testid="stPills"] {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    
    div[data-testid="stPills"] button {
        border-radius: 8px !important;
        border: 1px solid var(--border) !important;
        background: var(--bg) !important;
        color: var(--text) !important;
        font-weight: 500 !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s !important;
    }
    
    div[data-testid="stPills"] button[aria-pressed="true"] {
        background: var(--primary) !important;
        color: white !important;
        border-color: var(--primary) !important;
        box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.2);
    }
    
    /* Botões de ação */
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
    
    /* Expander moderno */
    .streamlit-expanderHeader {
        background: var(--bg) !important;
        border-radius: 12px !important;
        border: 1px solid var(--border) !important;
        font-weight: 600 !important;
        color: var(--primary) !important;
    }
    
    /* Tabela estilizada */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid var(--border) !important;
    }
    
    /* Footer */
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
    
    /* Mobile optimizations */
    @media (max-width: 640px) {
        .kpi-container {
            grid-template-columns: 1fr;
        }
        
        .chart-card {
            padding: 1rem;
        }
        
        .dashboard-header {
            padding: 1rem;
        }
        
        /* Melhorar touch targets */
        div[data-testid="stPills"] button {
            padding: 0.75rem 1rem !important;
            min-height: 44px;
        }
        
        .stButton button {
            min-height: 48px;
        }
    }
    
    /* Animações sutis */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .kpi-card, .chart-card {
        animation: fadeIn 0.5s ease-out forwards;
    }
    
    /* Scrollbar estilizada */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-muted);
    }
    
    /* Esconder elementos desnecessários no mobile */
    @media (max-width: 768px) {
        [data-testid="stSidebarNav"] { display: none; }
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# CARREGAMENTO DOS DADOS COM CACHE OTIMIZADO
# ---------------------------------------------------
@st.cache_data(ttl=3600, show_spinner="Carregando dados...")
def carregar_dados():
    try:
        df = pd.read_csv("base_criminalidade_tratada.csv")
        
        # Validação de colunas essenciais
        colunas_necessarias = ['Tipo_Crime', 'Ano', 'Quantidade', 'Regiao']
        for col in colunas_necessarias:
            if col not in df.columns:
                st.error(f"Coluna '{col}' não encontrada no dataset")
                return pd.DataFrame()
        
        # Classificação otimizada
        def classificar(crime):
            c = str(crime).upper()
            if any(x in c for x in ['HOMICÍDIO', 'LATROCÍNIO', 'MORTE', 'FEMINICÍDIO']):
                return 'Crimes Contra a Vida'
            if 'ROUBO' in c:
                return 'Roubos'
            if 'FURTO' in c:
                return 'Furtos'
            if any(x in c for x in ['TRÁFICO', 'DROGA', 'ENTORPECENTE']):
                return 'Drogas'
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
# SIDEBAR COLAPSÁVEL (MOBILE-FRIENDLY)
# ---------------------------------------------------
with st.sidebar:
    st.markdown("### 🎛️ Painel de Controle")
    
    # Toggle para mobile
    st.markdown("""
    <style>
    @media (max-width: 768px) {
        [data-testid="stSidebar"] {
            width: 100% !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Anos com seleção inteligente
    anos_disponiveis = sorted(df["Ano"].unique(), reverse=True)
    anos_selecionados = st.pills(
        "📅 Anos de Análise",
        options=anos_disponiveis,
        selection_mode="multi",
        default=[anos_disponiveis[0]] if anos_disponiveis else [],
        help="Selecione um ou mais anos para análise"
    )
    
    if not anos_selecionados:
        anos_selecionados = [max(anos_disponiveis)]
    
    st.divider()
    
    # Categorias de crime agrupadas (mais eficiente)
    categorias = st.pills(
        "📊 Categorias Criminais",
        options=sorted(df["Categoria"].unique()),
        selection_mode="multi",
        default=sorted(df["Categoria"].unique()),
        help="Filtrar por categoria de crime"
    )
    
    # Expander para tipos específicos (economia de espaço)
    with st.expander("🔍 Tipos Específicos de Crime"):
        crimes_filtrados = df[df["Categoria"].isin(categorias)]["Tipo_Crime"].unique()
        crimes_selecionados = st.multiselect(
            "Selecione os tipos",
            options=sorted(crimes_filtrados),
            default=sorted(crimes_filtrados),
            placeholder="Todos selecionados..."
        )
    
    st.divider()
    
    # Filtro de região com busca
    regioes_disponiveis = sorted(df["Regiao"].dropna().unique())
    regioes = st.multiselect(
        "📍 Regiões Administrativas",
        options=regioes_disponiveis,
        placeholder="Todas as regiões...",
        help="Deixe vazio para todas as regiões"
    )
    
    # Botão de reset
    if st.button("🔄 Resetar Filtros", use_container_width=True):
        st.rerun()

# ---------------------------------------------------
# FILTRAGEM INTELIGENTE
# ---------------------------------------------------
# Filtra por categoria primeiro, depois por tipo específico se selecionado
mask_categoria = df["Categoria"].isin(categorias) if categorias else pd.Series([True] * len(df))
df_categorizado = df[mask_categoria]

if 'crimes_selecionados' in locals() and crimes_selecionados:
    df_categorizado = df_categorizado[df_categorizado["Tipo_Crime"].isin(crimes_selecionados)]

df_filtro = df_categorizado[
    (df_categorizado["Ano"].isin(anos_selecionados))
]

if regioes:
    df_filtro = df_filtro[df_filtro["Regiao"].isin(regioes)]

# ---------------------------------------------------
# HEADER PRINCIPAL
# ---------------------------------------------------
anos_texto = " • ".join(map(str, sorted(anos_selecionados)))
st.markdown(f"""
<div class="dashboard-header">
    <h1>🚔 Análise Criminal do DF</h1>
    <div class="subtitle">Dados de referência: 2015–{max(anos_disponiveis)} | Período selecionado: {anos_texto}</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# KPIs COM LAYOUT RESPONSIVO
# ---------------------------------------------------
total_periodo = int(df_filtro["Quantidade"].sum())
regioes_afetadas = df_filtro["Regiao"].nunique()
media_anual = total_periodo / len(anos_selecionados) if anos_selecionados else 0

# Cálculo de variação ano a ano
variacao = 0
tendencia = "neutral"
if len(anos_selecionados) >= 2:
    anos_ord = sorted(anos_selecionados)
    totais_por_ano = df_filtro.groupby("Ano")["Quantidade"].sum()
    if len(totais_por_ano) >= 2:
        ultimo = totais_por_ano[anos_ord[-1]]
        penultimo = totais_por_ano[anos_ord[-2]]
        variacao = ((ultimo - penultimo) / penultimo * 100) if penultimo else 0
        tendencia = "positive" if variacao < 0 else "negative"  # Negativo é bom (queda no crime)

# HTML para KPIs
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="kpi-card {'positive' if total_periodo == 0 else 'neutral'}">
        <div class="kpi-label">Total de Ocorrências</div>
        <div class="kpi-value">{total_periodo:,}</div>
        <div class="kpi-delta">No período selecionado</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    delta_class = "positive" if variacao < 0 else "negative" if variacao > 0 else "neutral"
    delta_icon = "↓" if variacao < 0 else "↑" if variacao > 0 else "→"
    st.markdown(f"""
    <div class="kpi-card {delta_class}">
        <div class="kpi-label">Variação Anual</div>
        <div class="kpi-value">{abs(variacao):.1f}%</div>
        <div class="kpi-delta {delta_class}">{delta_icon} vs ano anterior</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card neutral">
        <div class="kpi-label">Cobertura Territorial</div>
        <div class="kpi-value">{regioes_afetadas}</div>
        <div class="kpi-delta">Regiões monitoradas</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# GRID DE GRÁFICOS RESPONSIVO
# ---------------------------------------------------
col_left, col_right = st.columns([2, 1], gap="large")

with col_left:
    # Ranking Territorial
    st.markdown("""
    <div class="chart-card">
        <div class="chart-header">
            <div class="chart-title">🏆 Ranking de Incidência Criminal</div>
        </div>
    """, unsafe_allow_html=True)
    
    ranking = df_filtro.groupby("Regiao")["Quantidade"].sum().reset_index()
    ranking = ranking[ranking["Regiao"].notna()].sort_values("Quantidade", ascending=True).tail(15)
    
    fig_rank = px.bar(
        ranking,
        x="Quantidade",
        y="Regiao",
        orientation="h",
        color="Quantidade",
        color_continuous_scale="Reds",
        text="Quantidade",
        height=500
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
    # Distribuição por Categoria
    st.markdown("""
    <div class="chart-card">
        <div class="chart-header">
            <div class="chart-title">🎯 Distribuição por Categoria</div>
        </div>
    """, unsafe_allow_html=True)
    
    df_cat = df_filtro.groupby("Categoria")["Quantidade"].sum().reset_index()
    
    fig_pie = px.pie(
        df_cat,
        values="Quantidade",
        names="Categoria",
        hole=0.6,
        color_discrete_sequence=px.colors.sequential.Reds_r
    )
    
    fig_pie.update_traces(
        textposition='inside',
        textinfo='percent+label',
        insidetextorientation='radial',
        pull=[0.02] * len(df_cat)
    )
    
    fig_pie.update_layout(
        showlegend=False,
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif"),
        annotations=[dict(text='Total<br>{}'.format(total_periodo), x=0.5, y=0.5, font_size=16, showarrow=False)]
    )
    
    st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# TENDÊNCIA TEMPORAL (LARGURA TOTAL)
# ---------------------------------------------------
st.markdown("""
<div class="chart-card">
    <div class="chart-header">
        <div class="chart-title">📈 Evolução Temporal</div>
    </div>
""", unsafe_allow_html=True)

serie_temporal = df_categorizado.groupby(["Ano", "Categoria"])["Quantidade"].sum().reset_index()

fig_line = px.line(
    serie_temporal,
    x="Ano",
    y="Quantidade",
    color="Categoria",
    markers=True,
    line_shape="spline",
    color_discrete_sequence=px.colors.qualitative.Set1
)

fig_line.update_traces(line_width=3, marker_size=8)
fig_line.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=10, r=10, t=10, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis_title="",
    yaxis_title="Quantidade de Ocorrências",
    font=dict(family="Inter, sans-serif"),
    hovermode="x unified"
)

st.plotly_chart(fig_line, use_container_width=True, config={'displayModeBar': False})
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# HEATMAP E PARETO (COLUNAS)
# ---------------------------------------------------
col_heat, col_pareto = st.columns(2)

with col_heat:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-header">
            <div class="chart-title">🔥 Intensidade por Região e Ano</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Top 10 regiões para melhor visualização
    top_regioes = df_filtro.groupby("Regiao")["Quantidade"].sum().nlargest(10).index
    df_heat = df_filtro[df_filtro["Regiao"].isin(top_regioes)]
    
    pivot = df_heat.pivot_table(
        values="Quantidade", 
        index="Regiao", 
        columns="Ano", 
        aggfunc="sum", 
        fill_value=0
    )
    
    fig_heat = px.imshow(
        pivot,
        aspect="auto",
        color_continuous_scale="Reds",
        labels=dict(color="Ocorrências"),
        height=400
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
            <div class="chart-title">📊 Concentração Criminal (Pareto)</div>
        </div>
    """, unsafe_allow_html=True)
    
    pareto = df_filtro.groupby("Regiao")["Quantidade"].sum().sort_values(ascending=False).head(15)
    pareto_acum = (pareto.cumsum() / pareto.sum() * 100).round(1)
    
    fig_pareto = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig_pareto.add_trace(
        go.Bar(x=pareto.index, y=pareto.values, name="Quantidade", marker_color="#dc2626"),
        secondary_y=False
    )
    
    fig_pareto.add_trace(
        go.Scatter(x=pareto.index, y=pareto_acum.values, name="% Acumulado", 
                  mode='lines+markers', line=dict(color="#0f172a", width=3)),
        secondary_y=True
    )
    
    fig_pareto.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        font=dict(family="Inter, sans-serif"),
        height=400
    )
    
    fig_pareto.update_yaxes(title_text="Quantidade", secondary_y=False)
    fig_pareto.update_yaxes(title_text="% Acumulado", range=[0, 105], secondary_y=True)
    fig_pareto.update_xaxes(tickangle=45)
    
    st.plotly_chart(fig_pareto, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# TABELA ANALÍTICA COLAPSÁVEL
# ---------------------------------------------------
with st.expander("📋 Dados Detalhados (Clique para expandir)"):
    # Resumo estatístico
    col_stats1, col_stats2, col_stats3 = st.columns(3)
    with col_stats1:
        st.metric("Média por Região", f"{df_filtro.groupby('Regiao')['Quantidade'].sum().mean():.0f}")
    with col_stats2:
        st.metric("Mediana", f"{df_filtro['Quantidade'].median():.0f}")
    with col_stats3:
        st.metric("Desvio Padrão", f"{df_filtro['Quantidade'].std():.0f}")
    
    st.dataframe(
        df_filtro.sort_values("Quantidade", ascending=False),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Quantidade": st.column_config.NumberColumn("Qtd", help="Quantidade de ocorrências"),
            "Ano": st.column_config.NumberColumn("Ano", format="%d"),
            "Regiao": "Região Administrativa",
            "Tipo_Crime": "Tipo de Crime",
            "Categoria": "Categoria"
        }
    )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("""
<div class="footer-info">
    <span>📌</span>
    <div>
        <strong>Fonte:</strong> Portal da Transparência do Governo do Distrito Federal<br>
        <small>Última atualização: {} | Dados sujeitos a revisão</small>
    </div>
</div>
""".format(pd.Timestamp.now().strftime("%d/%m/%Y")), unsafe_allow_html=True)
