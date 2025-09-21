# AIDocGen Documentation

Welcome to AIDocGen, an intelligent documentation generation system that leverages AI to automatically create comprehensive documentation from your codebase.

## Overview

AIDocGen is a sophisticated microservices-based system designed to transform code repositories into well-structured, readable documentation. The system combines multiple AI agents and processing pipelines to analyze, clean, transform, and generate high-quality documentation.

## Key Features

- **Intelligent Code Analysis**: AI-powered analysis of code structure and dependencies
- **Multi-format Support**: Support for Python, Jupyter notebooks, Markdown, and more
- **Automated Documentation**: Generate documentation automatically from codebases
- **Data Anonymization**: Built-in PII detection and anonymization capabilities
- **Scalable Architecture**: Microservices-based design for high scalability
- **Quality Assurance**: Built-in quality checks and validation

## Architecture

AIDocGen is built on a microservices architecture with three main components:

### AI Layer
The core intelligence layer that handles:
- **Coordinator**: Orchestrates the documentation generation process
- **Planning Agent**: Analyzes and plans the documentation structure
- **Generation Agent**: Creates the actual documentation content
- **Quality Agent**: Ensures documentation quality and consistency
- **Query Agent**: Handles information retrieval and queries

### Input Integration Pipeline
Handles data ingestion and preparation:
- Repository downloading and cloning
- File upload and blob storage management
- Data validation and initial processing

### Transforming Pipeline
Processes and transforms the raw data:
- **Anonymization**: PII detection and removal
- **Cleaning & Transformation**: Code cleaning and standardization
- **Format Conversion**: Convert between different file formats (MD to TXT, Python to text)
- **Enrichment**: Add metadata and context
- **Standardization**: Ensure consistent formatting

## Getting Started

1. **Installation**: Set up the development environment
2. **Configuration**: Configure the microservices
3. **Usage**: Start generating documentation from your codebase

For detailed instructions, see the [How-to Guides](how-to-guides.md) section.

## Documentation Structure

- **[How-to Guides](how-to-guides.md)**: Step-by-step instructions for common tasks
- **[Explanation](explanation.md)**: Detailed explanations of concepts and architecture
- **[Reference](reference.md)**: Complete API reference and code documentation

## Support

For questions, issues, or contributions, please refer to the project repository.
