Este repositório armazena o projeto feito durante o desafio técnico da DIT - SMS. 

# Principais bibliotecas e frameworks utilizados

- Requests (Extração via API)
- Pandas  (Manipulação)
- Pandera (Validação dos dados)
- DBT (Transformação)
- Prefect 0.15.9 (Orquestração de workflows)
## Requisitos 
- Python 3.9
- Docker

## Instalação

Clone o repositório:
```bash
git clone https://github.com/herianc/datario.git
```

Entre no diretório do projeto, crie um ambiente virtual e baixe as dependências:

Exemplo em sistemas Unix:
```bash
cd datario
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

 Ainda na pasta raiz do projeto, suba um container com a imagem do Postgres.

```bash
docker compose up -d
```

O diretório `init-sql` contém um script para criação da tabela onde será armazenado os dados extraídos pelo pipeline.

Definindo as variáveis de ambiente utilizadas neste projeto. 

```bash
export DB_USER=postgres
export DB_PASSWORD=datario2025
```
# Iniciando os fluxos
## Captura
Para iniciar o fluxo, basta entrar no diretório `pipelines` e executar :

```bash
prefect -p run.py -n 'DIT: BRT GPS - Captura' -s
```


## Materialização

```bash
prefect -p run.py -n 'DIT: BRT GPS - Materialização' -s
```


### Exemplo de execução

<img src="vasco.png" width="200" height="100">
![/home/herian/Code/datario/image.png](file:///home/herian/Code/datario/image.png)


# Entendendo os fluxos

## Captura

O fluxo de captura é simples e ocorre de maneira sequencial. Começa capturando os dados brutos na API, em seguida é feita a estruturação do JSON recebido para o formato DataFrame do pandas. Logo após, é feito o salvamento dos dados no formato CSV. Adiante é feita um simples tratamento (transformação do atributo datahora e também adição da data e horário de captura) antes de serem carregados no banco de dados, é feita uma validação utilizando a biblioteca Pandera (validação de tipos). Por fim, é feito o carregamento dos dados na base de dados. Este fluxo é executado a cada 1 minuto.



<img src="vasco.png" width="200" height="100">


## Materialização

Este fluxo contém apenas uma tarefa: Materializar a tabela com os registros mais recentes e filtrar os registros que estão com a ignição ativa e pertencem a uma linha. 


