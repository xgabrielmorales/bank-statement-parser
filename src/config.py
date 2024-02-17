class BankStatementConfig:
    columns: dict[str, str]
    decimal_separator: str
    thousands_separator: str


class SavingAccountBBVAColombia(BankStatementConfig):
    columns = {
        "MOVIMIENTO": "UInt32",
        "FECHA_OPERACION": "str",
        "FECHA_VALOR": "str",
        "CONCEPTO": "str",
        "CARGOS": "float64",
        "ABONOS": "float64",
        "SALDO": "float64",
    }
    decimal_separator = "."
    thousands_separator = ","
