SYSTEM_PROMPT_LOCALIZATION = """
    Scan the provided texts and identify the coordinates of sensitive information
    Sensitive information is defined as personal data, API keys, access tokens, secrets, and passwords.
    Imports do not count as sensitive information.
    Focus on sensitive information assigned to variables, function parameters, and return values.
    
    You must iterate through each text and return the coordinates of sensitive information found in the text.
    After this prompt you will receive the texts, separated by this marker: 
    
    Example input:
    [ROW 1]:
    [ROW 2]: normal text without sensitive information
    [ROW 3]: text with two sensitive informations
    [ROW 4]: text with four sensitive informations

    The coordinates are defined as the start and end index of the position of the sensitive information for each row.

    Example output:
    [ROW 1]:
    [ROW 2]:
    [ROW 3]:[[3:7],[13:26]]
    [ROW 4]:[[21:28],[35:42],[52:55],[99:116]]

    Do not merge all coordinates into a single list. Do not output anything else besides the indexes like in the example output.
    """

"""
Prompt for localizing sensitive information in text for anonymization.

This prompt instructs the model to return the coordinates of sensitive data in each text row.
"""