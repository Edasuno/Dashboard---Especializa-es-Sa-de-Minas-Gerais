import streamlit as st 
import matplotlib.pyplot as plt 
import seaborn as sbn
import pandas as pd 
import plotly.express as px


#Data

df = pd.read_csv("/data/newdata.csv")

totalmed = df.shape[0]

avgprice = round(df["price"].mean(), 2)

telemedicine_count = df[df["telemedicine"] == 1].shape[0]

city_counts = df["city1"].value_counts().head(5) 

spec_count = df["specialization"].value_counts().head(5)

#Media de preço por cidade 
city_price_avg = df.groupby("city1")["price"].mean().reset_index()
city_price_avg.columns = ["Cidade", "Média de Preço"]

# Arredondar os valores para 2 casas decimais
city_price_avg["Média de Preço"] = city_price_avg["Média de Preço"].round(2)

#Ordenado mais caro para mais barato
city_price_avg = city_price_avg.sort_values(by="Média de Preço", ascending=False)


#Data view


st.set_page_config(layout="wide")

st.title("Especializações Saúde - (MG)")


col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <div style="display: flex; align-items: center;">
            <i class="fas fa-user-md" style="font-size: 2rem; margin-right: 10px;"></i>
            <div style="font-weight: bold; font-size: 1.5rem;">Total de especialistas</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style='background-color:#4CB5F5; padding:20px; border-radius:10px; font-weight: bold; font-size: 1.5rem; display: flex; align-items: center; justify-content: center;'>
            <i class="fas fa-users" style="font-size: 2rem; margin-right: 10px;"></i> {totalmed}
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <div style="display: flex; align-items: center;">
            <i class="fas fa-dollar-sign" style="font-size: 2rem; margin-right: 10px;"></i>
            <div style="font-weight: bold; font-size: 1.5rem;">Média de preços</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style='background-color:#D32D41; padding:20px; border-radius:10px; font-weight: bold; font-size: 1.5rem; display: flex; align-items: center; justify-content: center;'>
            <i class="fas fa-money-bill-wave" style="font-size: 2rem; margin-right: 10px;"></i> {avgprice}
        </div>
    """, unsafe_allow_html=True)


with col3:
    st.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <div style="display: flex; align-items: center;">
            <i class="fas fa-video" style="font-size: 1.5rem; margin-right: 10px;"></i>
            <div style="font-weight: bold; font-size: 1.5rem;">Atendimento com Telemedicina</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style='background-color:#6AB187; padding:20px; border-radius:10px; font-weight: bold; font-size: 1.5rem; display: flex; align-items: center; justify-content: center;'>
            <i class="fas fa-laptop" style="font-size: 2rem; margin-right: 10px;"></i> {telemedicine_count}
        </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)



#Gráficos e estatiticas 

#Grafico cidades
fig, ax = plt.subplots()
colors = ["#0091D5", "#B3C100", "#fca311", "#7209b7", "#ff595e"]  # Cores 
wedges, texts, autotexts = ax.pie(city_counts, labels=city_counts.index, autopct="%1.1f%%", 
                                   startangle=90, colors=colors, textprops={'fontsize': 6.5})  # Fonte menor
ax.set_title("Cidades com mais especialistas", fontsize=14, fontweight="bold")

fig.patch.set_facecolor('#f3f3f3')


col1, col2 = st.columns([1.5, 2])  #proporção das colunas

with col1:
    st.pyplot(fig) 

with col2:
    st.markdown("<div style='font-weight: bold; font-size: 1.5rem;'>Cidades com mais Especialistas</div>", unsafe_allow_html=True)
    st.markdown("<ol style='font-size: 1.2rem; padding-left: 20px;'>" +
                "".join([f"<li><strong>{city}</strong>: {count} Profissionais</li>" for city, count in city_counts.items()]) +
                "</ol>", unsafe_allow_html=True)
    
    st.markdown ("<div style='font-weight: bold; font-size: 1.5rem; padding-top: 50px; '>Ranking de Especializações</div>", unsafe_allow_html=True)

    st.markdown("<ol style='font-size: 1.2rem; padding-left: 20px;'>" +
                "".join([f"<li><strong>{spec}</strong>: {count} Profissionais</li>" for spec, count in spec_count.items()]) +
                "</ol>", unsafe_allow_html=True)
    
st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)


#Gráfico de barras horizontal
fig = px.bar(city_price_avg, 
             x="Média de Preço", 
             y="Cidade", 
             orientation="h", 
             title="Cidades Mais Caras e Mais Baratas",
             text="Média de Preço", 
             color="Média de Preço", 
             color_continuous_scale=px.colors.sequential.Viridis)

# config para não ter distorções
fig.update_xaxes(range=[0, city_price_avg["Média de Preço"].max() + 100])

fig.update_layout(
    plot_bgcolor="#f9f9f9",  
    paper_bgcolor="#f9f9f9",
    font=dict(size=14),
)

# Mostrar gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)



st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)


#Conclusão 
# Para os icones dos botões a biblioteca de ícones FontAwesome
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">', unsafe_allow_html=True)

st.markdown(
    """
    <div style="display: flex; justify-content: center; gap: 20px; margin-top: 20px;">
        <a href="data/newdata.csv" download="newdata.csv" 
           style="text-decoration: none; background-color: #4CAF50; color: white; padding: 12px 20px; border-radius: 5px; font-size: 1.2rem; font-weight: bold; display: flex; align-items: center; gap: 10px;">
            <i class="fa fa-database"></i> Baixar Dataset
        </a>
        <a href="http://www.linkedin.com/in/edson-assun%C3%A7%C3%A3o-4438a2350" target="_blank" rel="noopener noreferrer"
           style="text-decoration: none; background-color: #0077b5; color: white; padding: 12px 20px; border-radius: 5px; font-size: 1.2rem; font-weight: bold; display: flex; align-items: center; gap: 10px;">
            <i class="fa fa-linkedin-square"></i> Meu LinkedIn
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
