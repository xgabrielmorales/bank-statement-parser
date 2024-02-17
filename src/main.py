from pathlib import Path

import pandas as pd
import tabula as tb
from config import BankStatementConfig, SavingAccountBBVAColombia


class BankStatementParser:
    def __init__(self, filename: str, bank_config: BankStatementConfig) -> None:
        self.bank_config = bank_config
        self.filename = Path(filename)

        self.input_path = Path(f"data/input/{self.filename}")
        self.output_path = Path(f"data/output/{self.filename.stem}")

    def is_valid(self) -> bool:
        """
        Validates if the supplied data is valid.

        Args:
            None

        Returns:
            bool: True if the data is valid, False otherwise.

        Raises:
            Exception: If the given file path does not exist.
            Exception: If the bank_config is not an instance of the BankStatementConfig class.
        """
        if hasattr(self, "_is_valid"):
            return self._is_valid

        if not self.input_path.exists():
            raise Exception("The given file path does not exist.")

        if not self.input_path.stat().st_size:
            raise Exception("The given file is empty.")

        if not isinstance(self.bank_config, BankStatementConfig):
            raise Exception(
                "The bank_config must be an instantiation of the BankStatementConfig class."
            )

        self._is_valid = True

        return self._is_valid

    def to_dataframe(self) -> pd.DataFrame:
        """
        Converts the bank statements from a PDF file to a pandas DataFrame.

        Args:
            None

        Returns:
            pd.DataFrame: The converted bank statements as a pandas DataFrame.

        Raises:
            Exception: If the `.is_valid()` method has not been called before calling this method.
            ValueError: If the given PDF file does not contain any bank statements.
        """
        if not getattr(self, "_is_valid", False):
            raise Exception("You must call the `.is_valid()` method first.")

        tables = tb.read_pdf(
            input_path=self.input_path,
            multiple_tables=False,
            pages="all",
            pandas_options={
                "decimal": self.bank_config.decimal_separator,
                "dtype": self.bank_config.columns,
                "names": list(self.bank_config.columns.keys()),
                "thousands": self.bank_config.thousands_separator,
            },
            silent=True,
            stream=True,
        )

        bank_statements = next(iter(tables), pd.DataFrame())

        if bank_statements.empty:
            raise ValueError("The given pdf does not contain bank statements.")

        return bank_statements

    def to_csv(self, decimal_separator: str = ";") -> None:
        """
        Converts the bank statements to a CSV file and saves it to the specified output path.

        Args:
            decimal_separator (str): The separator used in the CSV file (default is ";").

        Returns:
            None
        """
        EXTENSION = ".csv"
        filename = str(self.output_path) + EXTENSION

        bank_statements = self.to_dataframe()
        bank_statements.to_csv(path_or_buf=filename, sep=decimal_separator, index=False)

    def to_excel(self) -> None:
        """
        Converts the bank statements to an Excel file and saves it to the specified output path.

        Args:
            None

        Returns:
            None
        """
        EXTENSION = ".xlsx"
        filename = str(self.output_path) + EXTENSION

        bank_statements = self.to_dataframe()
        bank_statements.to_excel(excel_writer=filename, index=False)


def main() -> int:
    # The name of the file located in the ./data/input directory.
    filename = "savings_account.pdf"
    # The configuration of your bank statement.
    bank_config = SavingAccountBBVAColombia()

    parser = BankStatementParser(filename=filename, bank_config=bank_config)
    parser.is_valid()
    parser.to_csv()

    return 0


if __name__ == "__main__":
    main()
