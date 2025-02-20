# Desafio Técnico DIT - Secretária Municipal de Saúde do Rio
<div align='center'>
 <img src="https://github.com/herianc/dit-smt-rio/blob/main/images/header.png?raw=true">
</div>

## 💭 Sobre
Este repositório contém o projeto desenvolvido para o desafio técnico da Diretoria de Inovação e Tecnologia da Secretaria Municipal de Saúde do Rio, referente à vaga de Engenheiro de Dados Júnior. O desafio envolve a captura, a cada minuto, de dados dos ônibus do BRT por meio de uma API em tempo real. Os dados são então armazenados em um arquivo CSV e posteriormente inseridos em um banco de dados PostgreSQL. Além disso, é necessário criar uma tabela contendo o código, a localização e a velocidade dos ônibus.

## 📃 Documentação do Projeto
- [Documentação](https://github.com/herianc/dit-smt-rio/wiki)

## 🧰 Principais bibliotecas e frameworks utilizados

- Requests (Extração via API)
- Pandas  (Manipulação)
- Pandera (Validação )
- DBT (Transformação)
- Prefect 0.15.9 (Orquestração de Workflows)
  
## 🖥️ Requisitos 
- Python 3.9
- Docker

## ⬇️ Instalação

Clone o repositório.
```bash
git clone https://github.com/herianc/dit-smt-rio.git
```

Instale o gerenciador de pacotes uv:

```bash
cd dit-smt-rio
pip install uv
```
Ative o ambiente virtual:

```bash
uv venv .venv --python 3.9
source .venv/bin/activate
```
Instale as dependências do projeto:

```bash
uv add pyproject.toml
```

Ainda na pasta raiz do projeto, suba o container com a imagem do PostgreSQL:

```bash
docker compose up -d
```

O diretório `init-sql` contém um script para criação da tabela onde serão armazenado os dados extraídos durante pipeline.

Defina as variáveis de ambiente utilizadas neste projeto. 

```bash
export DB_USER=postgres
export DB_PASSWORD=datario2025
```

## ⚙️ Configuração Self-host Prefect

Inicie o servidor local.
```bash
prefect backend server
prefect server start -d --no-hasura-port --no-graphql-port --postgres-port '5433'
```
Crie o projeto e registre os flows.
```bash
cd pipelines
prefect create project 'DIT: BRT GPS'
prefect register --project 'DIT: BRT GPS' -p .
```
Ative o agente local.
```bash
prefect agent local start -f
```
Os fluxos em execução podem ser monitorados em `localhost:8080`.

### Exemplo de execução

<div align=center>
 <img src="https://github.com/herianc/dit-smt-rio/blob/main/images/printscreen.png?raw=true">
</div>

# 📑 Entendendo os fluxos

## Captura

O fluxo de captura ocorre de maneira sequencial e é executado a cada minuto. Primeiramente, os dados brutos são capturados pela API e convertidos para um DataFrame do pandas. Em seguida, são salvos em formato CSV. Após essa etapa, realiza-se um tratamento simples, que inclui a conversão do atributo datahora e a adição da data e horário de captura. Antes do carregamento no banco de dados, os dados passam por uma validação de tipos utilizando a biblioteca Pandera. Por fim, os dados são inseridos na base de dados.


<div align=center>
 <img src="https://github.com/herianc/datario/blob/main/images/mermaid_diagram.png?raw=true" width="222" height="440">
</div>


## Materialização

Este fluxo contém apenas uma tarefa: Materializar a tabela com um filtro dos registros que estão com ignição ativa e pertencem a uma linha, ou seja, ônibus que integram o BRT, além de pegar os resultados mais recentes (. 

## Liberação de espaço de armazenamento

Este fluxo também contém apenas uma tarefa, que é liberar espaço de armazenamento mensalmente. Sua execução é ocorre de forma mensal tendo em vista possíveis auditorias nos dados e também para backup da tabela dos dados extraídos.
