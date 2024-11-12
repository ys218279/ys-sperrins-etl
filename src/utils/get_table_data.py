import pandas as pd

def get_table_data(table: str, row_id: int, connection) -> pd.DataFrame:
    """extracts data for the given table name for all rows with id > row id

    Args:
        table (str): name of the table to query.
        row_id (int): row from which to collect data (exclusive)
        connection: ??????

    Returns:
        df (dataframe): a pandas dataframe containing the new data

    Raises:
    """
    pass