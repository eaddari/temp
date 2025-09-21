import time
from random import uniform

def retry_with_backoff(func, max_retries=5, backoff_factor=2):
    """
    Retry a function with exponential backoff.

    Parameters
    ----------
    func : callable
        The function to retry.
    max_retries : int, optional
        Maximum number of retries (default is 5).
    backoff_factor : int, optional
        Backoff multiplier (default is 2).

    Returns
    -------
    Any
        The result of the function if successful.

    Raises
    ------
    Exception
        The last exception if all retries fail.
    """
    for attempt in range(max_retries):
        try:
            return func()
        except (httpx.ConnectTimeout, APITimeoutError) as e:
            if attempt < max_retries - 1:
                wait_time = backoff_factor ** attempt
                print(f"Retrying in {wait_time} seconds due to: {e}")
                time.sleep(wait_time)
            else:
                raise