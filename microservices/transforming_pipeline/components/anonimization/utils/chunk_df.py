def chunk_dataframe(df, chunk_size):
    """
    Yield successive chunks from a DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to chunk.
    chunk_size : int
        The number of rows per chunk.

    Yields
    ------
    pandas.DataFrame
        Chunks of the original DataFrame.
    """
    for i in range(0, len(df), chunk_size):
        yield df.iloc[i:i + chunk_size]