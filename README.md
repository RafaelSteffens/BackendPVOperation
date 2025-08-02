# BackendPVOperation# 🚀 Projeto Backend – Usinas de Energia

Este projeto foi desenvolvido em **Python + Flask** com integração ao **MongoDB**, para fornecer uma **API REST** que consulta e processa informações sobre empreendimentos de geração de energia elétrica.

---

## 📌 Objetivo

- Ler dados de um **CSV** com informações de usinas.
- Armazenar os dados em um banco **MongoDB**.
- Expor uma **API REST** para consulta estruturada.
- Permitir **filtros** e **estatísticas agregadas** de forma eficiente.

---

## 🛠️ Funcionalidades

### 🔹 Endpoint `/usinas`
- **Listar empreendimentos** com paginação.
- Filtros disponíveis:
  - Estado → `SigUF`
  - Município → `NomMunicipio`
  - Distribuidora → `SigAgente`
  - Nome do Titular → `NomTitularEmpreendimento`

### 🔹 Endpoint `/estatisticas`
- Potência total (`MdaPotenciaInstaladaKW`) por **Estado (SigUF)**.
- Potência total (`MdaPotenciaInstaladaKW`) por **Distribuidora (SigAgente)**.

---

## 📂 Estrutura do Projeto

📦 backend-usinas
┣ 📂 app
┃ ┣ 📂 controllers
┃ ┣ 📂 models
┃ ┣ 📂 services
┃ ┣ 📜 __init__.py
┃ ┣ 📜 config.py
┃ ┣ 📜 extensions.py
┣ 📜 requirements.txt
┣ 📜 README.md
┣ 📜 run.py



## ⚙️ Requisitos

- Python **3.11+**
- MongoDB 
- Dependências do projeto (instaladas via `requirements.txt`)

---

## 📥 Instalação

1️⃣ **Clonar o repositório**
```bash
git clone https://github.com/RafaelSteffens/BackendPVOperation.git
cd backend-usinas

2️⃣ Criar ambiente virtual
python -m venv venv

3️⃣ Ativar o ambiente virtual
Windows:
venv\Scripts\activate

Linux/Mac:
source venv/bin/activate

4️⃣ Instalar dependências
pip install -r requirements.txt

🗄️ Configuração do MongoDB
1️⃣ Instalar o MongoDB Community
👉 Download Oficial

2️⃣ Iniciar o servidor MongoDB
mongod

3️⃣ Acessar o shell do Mongo
mongosh

4️⃣ Criar banco e coleção
use bdaneel
db.createCollection("empreendimentosGD")


▶️ Executando o Projeto
python main.py


A API estará disponível em:
👉 http://127.0.0.1:5000/


🌐 Exemplos de Requisições
Listar usinas (com filtros e paginação)
curl "http://localhost:5000/api/usinas?page=1&limit=20&SigUF=SP"

Estatísticas por Estado e Distribuidora
curl "http://localhost:5000/api/estatisticas"

📊 Boas Práticas Implementadas
Organização modular em Flask Blueprints.

Uso do Flask-CORS para permitir acesso externo.

Manipulação de grandes volumes de dados com Pandas.

Validação e tipagem de dados com Pydantic.

Integração com MongoDB utilizando PyMongo.

Paginação e filtros para eficiência em consultas.


👨‍💻 Autor
Projeto desenvolvido por Rafael Steffens
📩 Contato: 48 99177 1777 | E-mail rafaelfsteffens@gmail.com

