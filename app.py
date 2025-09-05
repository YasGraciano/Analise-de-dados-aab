import pandas as pd 
import streamlit as st
import plotly.express as px

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard de análise de Atividades",
    page_icon="📊",
    layout="wide",
)

# --- Carregamento dos dados ---
df = pd.read_csv("atividades.csv")

# --- Conteúdo Principal ---
st.title("Análise das atividades de Janeiro a Julho")
st.markdown(
    "Gráficos mostrando o total de participantes por mês nas atividades realizadas pela Casa de Cultura e Biblioteca Solidária, "
    "o número de atividades e eventos realizados, assim como as atividades extras desenvolvidas pela equipe."
)

# ==============================
# Função para formatar números no padrão brasileiro
# ==============================
def format_num(numero):
    return f"{numero:,.0f}".replace(",", ".")  # troca vírgula por ponto

# ==============================
# Gráfico 1 - Total de Participantes por Mês
# ==============================
st.markdown("---")  # linha separadora
st.subheader("Total de Participantes por Mês")

df_mes = df[df["Mês"].isin(["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho"])]
if not df_mes.empty:
    total_mes = df_mes.groupby('Mês')['Total Global participantes'].sum().reset_index()
    total_mes['Mês'] = pd.Categorical(total_mes['Mês'],
                                      categories=["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho"],
                                      ordered=True)
    total_mes = total_mes.sort_values('Mês').dropna()

    grafico_meses = px.bar(
        total_mes,
        x='Total Global participantes',
        y='Mês',
        orientation='h',
        title="Total de Participantes de Janeiro a Julho",
        labels={'Total Global participantes': 'Participantes', 'Mês': ''},
        color='Total Global participantes',
        color_continuous_scale='blues'
    )
    grafico_meses.update_layout(
        title_x=0.5,
        yaxis={'categoryorder':'array', 'categoryarray': ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho"]},
        coloraxis_showscale=False
    )
    st.plotly_chart(grafico_meses, use_container_width=True)

    total_participantes_mes = total_mes['Total Global participantes'].sum()
    st.markdown(f"<h4 style='background-color:#1e1e1e; color:#90caf9; padding:10px; border-radius:8px;'>"
                f"Total de Participantes (Jan-Jul): <strong>{format_num(total_participantes_mes)}</strong>"
                f"</h4>", unsafe_allow_html=True)

else:
    st.warning("Nenhum dado para exibir no gráfico de meses.")

# ==============================
# Gráfico 2 - Participantes por Categoria (Pizza)
# ==============================
st.markdown("---")  # linha separadora
st.subheader("Participantes por Eventos e Atividades Previstas")

df['Subprojeto_norm'] = df['Subprojeto'].astype(str).str.strip().str.lower()
df['Título_norm'] = df['Título'].astype(str).str.strip().str.lower()

def categoriza_linha(row):
    if row['Subprojeto_norm'] == "mostra colibri de artes 2025":
        return "Mostra Colibri de Artes"
    elif "clube de leitura" in row['Título_norm']:
        return "Clube de Leitura"
    elif "julina" in row['Título_norm']:
        return "Festa Julina da Comunidade"
    else:
        return None

df['Categoria'] = df.apply(categoriza_linha, axis=1)
df_grafico = df[df['Categoria'].notna()].copy()

if not df_grafico.empty:
    dados_categoria = df_grafico.groupby('Categoria', as_index=False)['Total Global participantes'].sum()
    dados_categoria = dados_categoria[dados_categoria['Categoria'].notna()]  # remove nulos

    grafico_pizza = px.pie(
        dados_categoria,
        names='Categoria',
        values='Total Global participantes',
        title="Participantes por Eventos e Atividades Previstas",
        color_discrete_sequence=px.colors.qualitative.Set2,
        hole=0.4
    )
    grafico_pizza.update_traces(textinfo='percent+label+value', textposition='inside')
    grafico_pizza.update_layout(title_x=0.5)
    st.plotly_chart(grafico_pizza, use_container_width=True)

    total_participantes_categoria = dados_categoria['Total Global participantes'].sum()
    st.markdown(f"<h4 style='background-color:#1e1e1e; color:#ffcc80; padding:10px; border-radius:8px;'>"
                f"Total de Participantes por Eventos e Atividades Previstas: <strong>{format_num(total_participantes_categoria)}</strong>"
                f"</h4>", unsafe_allow_html=True)

else:
    st.warning("Nenhum dado para exibir no gráfico de participantes por categoria.")

# ==============================
# Gráfico 3 - Atividades Extras (Pizza)
# ==============================
st.markdown("---")  # linha separadora
st.subheader("Atividades Extras")

projetos_extras = ["Conexão Comunitária", "Biblioteca Solidária", "Voluntariado"]
df_extras = df[df["Projeto"].isin(projetos_extras)].copy()

# Renomear "Voluntariado" para "Projeto Voluntariado"
df_extras.loc[df_extras["Projeto"] == "Voluntariado", "Projeto"] = "Projeto Voluntariado"

if not df_extras.empty:
    dados_extras = df_extras.groupby('Projeto', as_index=False)['Total Global participantes'].sum()
    dados_extras = dados_extras[dados_extras['Projeto'].notna()]  # remove nulos
    dados_extras.rename(columns={'Total Global participantes': 'Participantes'}, inplace=True)

    grafico_extras = px.pie(
        dados_extras,
        names='Projeto',
        values='Participantes',
        title='Participantes por Atividades Extras',
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    grafico_extras.update_traces(textinfo='percent+label+value', textposition='inside')
    grafico_extras.update_layout(title_x=0.5, legend=dict(orientation="v", x=1, y=0.5))
    st.plotly_chart(grafico_extras, use_container_width=True)

    total_participantes_extras = dados_extras['Participantes'].sum()
    st.markdown(f"<h4 style='background-color:#1e1e1e; color:#a5d6a7; padding:10px; border-radius:8px;'>"
                f"Total de Participantes nas Atividades Extras: <strong>{format_num(total_participantes_extras)}</strong>"
                f"</h4>", unsafe_allow_html=True)

else:
    st.warning("Nenhum dado encontrado para os projetos extras selecionados.")

# ==============================
# Observação Final
# ==============================
st.markdown("---")
st.markdown(
    """
    <div style="background-color:#1e1e1e; padding:15px; border-radius:10px; border:1px solid #424242">
        <h4 style="color:#ffb74d">📌 Observação</h4>
        <p>No mês de <strong>agosto</strong>, aconteceram <strong>3 atividades extras</strong>, 
        que somam <strong>96 participantes</strong>, totalizando até agosto <strong>496 participantes</strong> 
        nas atividades extras desenvolvidas pela equipe.</p>
    </div>
    """, unsafe_allow_html=True
)
