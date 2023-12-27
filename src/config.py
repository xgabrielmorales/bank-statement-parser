from pydantic import BaseModel


class BankStatementConfig(BaseModel):
    columns: dict[str, str]
    decimal_separator: str
    thousands_separator: str


BBVA_SAVINGS_ACCOUNT_COLOMBIA = BankStatementConfig(
    columns={
        "MOVIMIENTO": "UInt32",
        "FECHA_OPERACION": "str",
        "FECHA_VALOR": "str",
        "CONCEPTO": "str",
        "CARGOS": "float64",
        "ABONOS": "float64",
        "SALDO": "float64",
    },
    decimal_separator=".",
    thousands_separator=",",
)
