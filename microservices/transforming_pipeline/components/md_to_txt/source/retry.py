import asyncio
import logging

"""
Async retry utilities for file conversion and processing.

Provides retry logic for async functions and safe conversion wrappers.
"""

async def retry_async(func, *args, retries=3, delay=0.5, **kwargs):
    """
    Retry an async function with a delay between attempts.

    Parameters
    ----------
    func : callable
        The async function to retry.
    *args
        Positional arguments for the function.
    retries : int, optional
        Maximum number of retries (default is 3).
    delay : float, optional
        Delay in seconds between retries (default is 0.5).
    **kwargs
        Keyword arguments for the function.

    Returns
    -------
    Any
        The result of the function if successful.

    Raises
    ------
    Exception
        The last exception if all retries fail.
    """
    for attempt in range(retries):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            if attempt < retries - 1:
                await asyncio.sleep(delay)
            else:
                logging.error(f"Function failed after {retries} attempts: {e}")
                raise

async def safe_convert(func, text, retries=3, delay=0.5):
    """
    Safely convert text using a function with retry logic.

    Parameters
    ----------
    func : callable
        The async function to use for conversion.
    text : str
        The text to convert.
    retries : int, optional
        Maximum number of retries (default is 3).
    delay : float, optional
        Delay in seconds between retries (default is 0.5).

    Returns
    -------
    str
        The converted text, or the original text if conversion fails.
    """
    try:
        return await retry_async(func, text, retries=retries, delay=delay)
    except Exception:
        return text