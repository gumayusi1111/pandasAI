"""
PandasAI to Pandas Converter

A web application that converts natural language queries to Pandas code
using PandasAI and DeepSeek models.
"""

from .app import app
from .core import generate_pandas_code

__all__ = ['app', 'generate_pandas_code']
