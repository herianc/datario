import pandera as pa
from pandera.typing import Series

class BrtReport(pa.DataFrameModel):
    codigo : Series[str]
    placa : Series[str] = pa.Field(nullable=True)
    linha : Series[str] = pa.Field(nullable=False)
    latitude : Series[float] = pa.Field(nullable=False)
    longitude : Series[float] = pa.Field(nullable=False)
    direcao: Series[str] = pa.Field(nullable=True)
    datahora: Series[pa.DateTime] = pa.Field(nullable=False)
    velocidade : Series[float] = pa.Field(nullable=True)
    sentido : Series[str] = pa.Field(nullable=True)
    trajeto : Series[str] = pa.Field(nullable=True)
    hodometro : Series[float] = pa.Field(nullable=True)
    ignicao : Series[bool] = pa.Field(nullable=True)
    
    class Config:
        strict = True
        coerce = True