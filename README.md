Este projeto apresenta um dashboard desenvolvido em Python e Streamlit para visualização e análise de registros de temperatura provenientes de dispositivos IoT.
Os dados são processados, normalizados e exibidos em gráficos interativos para facilitar o acompanhamento de variações térmicas ao longo do tempo.

A aplicação roda tanto localmente quanto em ambiente containerizado via Docker, oferecendo portabilidade e reprodutibilidade.

🚀 Tecnologias Utilizadas

Python 3.11

Streamlit

Pandas

Plotly

Supabase Storage (opcional para obter o dataset)

Docker & Docker Compose

📂 Estrutura do Projeto

app.py — Dashboard em Streamlit

IOT-temp-updated.csv — Dataset atualizado com datas ajustadas para 2025

Dockerfile — Container da aplicação

docker-compose.yml — Orquestração do serviço

requirements.txt — Dependências do projeto

▶️ Como Executar o Projeto
1. Clonar o repositório
git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
cd SEU-REPOSITORIO

2. Rodar com Docker

Certifique-se de que o Docker está em execução.

docker compose up --build


Acesse o dashboard em:

👉 http://localhost:8501

3. Rodar sem Docker (opcional)

Instale as dependências:

pip install -r requirements.txt


Execute o Streamlit:

python -m streamlit run app.py

ou

python -m streamlit run app.py --server.port=8501 --server.address=0.0.0.0

📊 Dashboard (Exemplos de Telas)

<img width="1796" height="824" alt="image" src="https://github.com/user-attachments/assets/ca5293de-91a2-4ea7-9241-bfd41f8f0c7a" />

<img width="1852" height="639" alt="image" src="https://github.com/user-attachments/assets/ae538180-fc92-4c54-9b12-19115db603e0" />

<img width="1771" height="708" alt="image" src="https://github.com/user-attachments/assets/2d730752-4680-4cd2-9de0-5c34fcff1b85" />







