CREATE TABLE IF NOT EXISTS brt_report (
    id BIGSERIAL PRIMARY KEY,
    codigo VARCHAR(20), 
    placa VARCHAR(10), 
    linha VARCHAR(10),
    latitude FLOAT,
    longitude FLOAT,
    datahora TIMESTAMP,
    velocidade FLOAT,
    sentido VARCHAR(5),
    direcao VARCHAR(10),
    trajeto VARCHAR(100),
    hodometro FLOAT,
    ignicao BOOLEAN
);