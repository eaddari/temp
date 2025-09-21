import pytest
import pandas as pd
import asyncio
from components.md_to_txt.source.converter import FileConverter, md_to_text, rst_to_text

"""
Test suite for Markdown and reStructuredText to text conversion utilities.

These tests validate the conversion of .md and .rst files to HTML/text and the FileConverter class.
"""

@pytest.mark.asyncio
async def test_md_to_text_basic():
    """
    Test basic Markdown to HTML conversion.

    Asserts that the result contains expected HTML tags.
    """
    md = "# Titolo\nTesto **importante**."
    result = await md_to_text(md)
    assert "<h1>" in result and "<strong>" in result

@pytest.mark.asyncio
async def test_rst_to_text_basic():
    """
    Test basic reStructuredText to HTML conversion.

    Asserts that the result contains expected HTML tags.
    """
    rst = "Titolo\n====="
    result = await rst_to_text(rst)
    assert "<div" in result or "<section" in result

@pytest.mark.asyncio
async def test_file_converter_md():
    """
    Test FileConverter with Markdown input.

    Asserts that the conversion is successful for Markdown files.
    """
    df = pd.DataFrame({
        'name': ['file1.md', 'file2.md'],
        'content': ["# Uno", "## Due"]
    })
    converter = FileConverter(df, ['.md'])
    out_df = await converter.file_to_text()
    assert len(out_df) == 2
    assert all(out_df['content'].str.contains('<h'))

@pytest.mark.asyncio
async def test_file_converter_rst():
    """
    Test FileConverter with reStructuredText input.

    Asserts that the conversion is successful for reStructuredText files.
    """
    df = pd.DataFrame({
        'name': ['file1.rst', 'file2.rst'],
        'content': ["Titolo\n=====" , "Sottotitolo\n---------"]
    })
    converter = FileConverter(df, ['.rst'])
    out_df = await converter.file_to_text()
    assert len(out_df) == 2
    assert all(out_df['content'].str.contains('<div') | out_df['content'].str.contains('<section'))

@pytest.mark.asyncio
async def test_file_converter_empty():
    """
    Test FileConverter with empty DataFrame.

    Asserts that the result is an empty DataFrame when no input is provided.
    """
    df = pd.DataFrame({'name': [], 'content': []})
    converter = FileConverter(df, ['.md', '.rst'])
    out_df = await converter.file_to_text()
    assert out_df.empty
