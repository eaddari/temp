import requests
from tenacity import retry, stop_after_attempt, wait_fixed


def handle_error(e, status_text, progress_bar=None):
    """
    Handles errors by logging them and displaying an error message.
    
    Args:
        e (Exception): The exception to handle.
        status_text (Streamlit status text object): The status text to update with the error message.
        progress_bar (Streamlit progress bar object, optional): The progress bar to clear if provided.
    """
    if isinstance(e, requests.exceptions.RequestException):
        status_text.error(f"Connection error: {str(e)}")
    elif isinstance(e, KeyError):
        status_text.error(f"Server response error: Missing key {str(e)}")
    else:
        status_text.error(f"Unexpected error: {str(e)}")
    
    if progress_bar:
        progress_bar.empty()

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def make_request(url, method="post", **kwargs):
    """
    Makes a request to the specified URL with retry logic.
    
    Args:
        url (str): The URL to make the request to.
        method (str): The HTTP method to use ('post' or 'get').
        **kwargs: Additional arguments to pass to the request.
    
    Returns:
        Response: The response object from the request.
    """
    if method == "post":
        return requests.post(url, **kwargs)
    elif method == "get":
        return requests.get(url, **kwargs)
