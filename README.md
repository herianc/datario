# Desafio Técnico DIT - Secretária Municipal de Saúde do Rio

Este repositório armazena o projeto feito durante o desafio técnico da DIT - SMS para a vaga de Engenheiro de Dados Junior. 

## Principais bibliotecas e frameworks utilizados

- Requests (Extração via API)
- Pandas  (Manipulação)
- Pandera (Validação )
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

O diretório `init-sql` contém um script para criação da tabela onde será armazenado os dados extraídos durante pipeline.

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

<img src="https://github.com/herianc/datario/blob/main/images/image1.png?raw=true" width="800" height="480">

# Entendendo os fluxos

## Captura

O fluxo de captura ocorre de maneira sequencial e é executado a cada minuto. Primeiramente, os dados brutos são capturados pela API e convertidos para um DataFrame do pandas. Em seguida, são salvos em formato CSV. Após essa etapa, realiza-se um tratamento simples, que inclui a conversão do atributo datahora e a adição da data e horário de captura. Antes do carregamento no banco de dados, os dados passam por uma validação de tipos utilizando a biblioteca Pandera. Por fim, os dados são inseridos na base de dados.


<div align=center>
 <img src="https://github.com/herianc/datario/blob/main/images/mermaid_diagram.png?raw=true" width="222" height="440">
</div>


## Materialização

Este fluxo contém apenas uma tarefa: Materializar a tabela com um filtro dos registros que estão com ignição ativa e pertencem a uma linha, ou seja, ônibus que integram o BRT, além de pegar os resultados mais recentes (. 

## Liberação de espaço de armazenamento

Este fluxo também contém apenas uma tarefa, que é liberar espaço de armazenamento mensalmente. Sua execução é ocorre de forma mensal tendo em vista possíveis auditorias nos dados e também para backup da tabela dos dados extraídos.
