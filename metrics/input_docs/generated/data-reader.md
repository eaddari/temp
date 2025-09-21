## General Information

# General Information

This repository contains the source code, documentation, and configuration files for the **pandas-datareader** project. The project is organized to facilitate robust data access, testing, and documentation, supporting a wide range of data sources and formats. Below you'll find essential information about the repository's structure, its main components, and practical details for contributors and users.

---

## Repository Structure

- **Root Directory (`./`)**
  - Contains essential project files:
    - `requirements.txt` and `requirements-dev.txt`: Specify runtime and development dependencies.
    - `azure-pipelines.yml`: Defines CI/CD workflows using Azure Pipelines.
    - `.codecov.yml`: Configuration for code coverage reporting.
    - `LICENSE.md`: Project license.
    - `release-procedure.md`: Documentation for the release process.

- **Source Code (`pandas_datareader/`)**
  - Main package directory, organized by data source and functionality:
    - **Data Source Modules:**  
      - `av/` (Alpha Vantage)
      - `iex/` (IEX)
      - `yahoo/` (Yahoo Finance)
      - `io/` (Input/Output utilities)
      - `compat/` (Compatibility helpers)
    - **Core Modules:**  
      - `data.py`, `base.py`, `exceptions.py`, `_utils.py`, etc.
    - **Other Data Sources:**  
      - `fred.py`, `quandl.py`, `stooq.py`, `tiingo.py`, `oecd.py`, `famafrench.py`, `bankofcanada.py`, `moex.py`, `wb.py`, `tsp.py`, `naver.py`, `nasdaq_trader.py`, `eurostat.py`, `enigma.py`, `econdb.py`

- **Testing (`pandas_datareader/tests/`)**
  - Comprehensive test suite covering all modules and data sources.
  - Subdirectories for specialized tests:
    - `av/`, `io/`, `yahoo/`
    - Includes test data under `io/data/` and `yahoo/data/`

- **Documentation (`docs/`)**
  - Sphinx-based documentation source in `docs/source/`
  - Changelog and release notes in `docs/source/whatsnew/`
  - Contributor utilities in `docs/contributors.py`
  - Documentation dependencies in `docs/requirements.txt`

- **Continuous Integration (`ci/`)**
  - Azure Pipelines templates for Windows and POSIX environments in `ci/azure/`

---

## Key Features

- **Multi-Source Data Access:**  
  Retrieve financial and economic data from a variety of sources, including Yahoo Finance, Alpha Vantage, IEX, FRED, OECD, and more.

- **Extensible Architecture:**  
  Modular design allows for easy addition of new data sources and utilities.

- **Comprehensive Testing:**  
  Automated tests ensure reliability and correctness across all supported data sources.

- **Documentation and Release Management:**  
  Well-maintained documentation and clear release procedures support both users and contributors.

---

## Example: Accessing Yahoo Finance Data

```python
from pandas_datareader import data as pdr

# Fetch historical stock data for Apple Inc.
df = pdr.get_data_yahoo('AAPL', start='2023-01-01', end='2023-12-31')
print(df.head())
```

---

## Technical Details

- **Python Package:**  
  The main package is `pandas_datareader`, with submodules for each supported data source.
- **Testing:**  
  Tests are located in `pandas_datareader/tests/` and can be run using standard Python testing tools (e.g., `pytest`).
- **CI/CD:**  
  Azure Pipelines is used for automated testing and deployment, with templates for different operating systems.
- **Documentation:**  
  Built using Sphinx, with configuration in `docs/source/conf.py` and release notes in `docs/source/whatsnew/`.

---

## Getting Started

- **Installation:**  
  Install dependencies from `requirements.txt` for runtime, and `requirements-dev.txt` for development.
- **Contributing:**  
  See `release-procedure.md` and the documentation in `docs/` for guidelines on contributing and releasing new versions.

---

This section provides a high-level overview of the repository, its structure, and its main components. For more detailed information, refer to the subsequent sections of this documentation.

## Project Overview

## Project Overview

This project is a Python library designed for retrieving financial and economic data from a wide variety of online sources. The codebase is organized to support extensibility, robust data access, and ease of integration with data analysis workflows, particularly those using pandas.

### Core Functionality

At its core, the library provides a unified interface for downloading time series and tabular data from multiple data providers. The main package, `pandas_datareader`, contains modules for accessing data from sources such as:

- **Yahoo Finance**
- **FRED (Federal Reserve Economic Data)**
- **OECD**
- **Stooq**
- **Tiingo**
- **Quandl**
- **Bank of Canada**
- **Eurostat**
- **NASDAQ Trader**
- **MOEX (Moscow Exchange)**
- **Enigma**
- **Econdb**
- **Naver**
- **TSP (Thrift Savings Plan)**
- **World Bank**
- **Fama/French datasets**

Each data source is implemented as a separate module (e.g., `fred.py`, `yahoo/`, `quandl.py`), allowing users to fetch data with a consistent API while leveraging the unique features of each provider.

### Extensible and Modular Design

The codebase is structured for maintainability and extensibility:

- **Modular Source Files:** Each data provider has its own module, making it straightforward to add new sources or update existing ones.
- **Base Classes and Utilities:** Shared logic is abstracted into base classes (e.g., `base.py`) and utility modules (e.g., `_utils.py`), promoting code reuse and consistency.
- **Exception Handling:** Custom exceptions are defined in `exceptions.py` to provide clear error reporting and handling.

### Integration with Data Analysis Workflows

The library is designed to work seamlessly with pandas DataFrames, enabling users to fetch data and immediately begin analysis or visualization. For example, fetching historical stock prices from Yahoo Finance can be as simple as:

```python
import pandas_datareader.data as web
import datetime

start = datetime.datetime(2020, 1, 1)
end = datetime.datetime(2020, 12, 31)

df = web.DataReader('AAPL', 'yahoo', start, end)
print(df.head())
```

### Testing and Continuous Integration

- **Testing:** The `pandas_datareader/tests` directory (not shown in the file list but implied by the structure) contains test suites to ensure reliability across data sources.
- **CI/CD:** The project includes an Azure Pipelines configuration (`azure-pipelines.yml`) and code coverage settings (`.codecov.yml`) to automate testing and maintain code quality.

### Documentation and Contribution

- **Documentation:** The `docs/` directory contains requirements and contributor information, supporting the generation of user and developer documentation.
- **Release Procedures:** The `release-procedure.md` file outlines steps for releasing new versions, ensuring a consistent and reliable release process.

### Licensing

The project is open source, with licensing details provided in `LICENSE.md`.

---

This modular, extensible approach makes the library a powerful tool for financial data analysis, supporting both end-users and contributors in a robust, well-documented environment.

## Table of Contents

## Table of Contents

- [General Information](#general-information)
- [Project Overview](#project-overview)
- [Table of Contents](#table-of-contents)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
  - [Top-Level Files](#top-level-files)
  - [Continuous Integration](#continuous-integration)
  - [Documentation](#documentation)
  - [Core Library: `pandas_datareader`](#core-library-pandas_datareader)
    - [Data Sources](#data-sources)
    - [Utilities and Compatibility](#utilities-and-compatibility)
    - [I/O Utilities](#io-utilities)
    - [Testing Suite](#testing-suite)
- [Key Classes and Functions](#key-classes-and-functions)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [Additional Documentation](#additional-documentation)
- [License](#license)
- [Contact Information](#contact-information)
- [Acknowledgements](#acknowledgements)

---

### Project Structure

#### Top-Level Files

- `.codecov.yml` – Code coverage configuration
- `LICENSE.md` – License information
- `azure-pipelines.yml` – Azure Pipelines CI configuration
- `release-procedure.md` – Release process documentation
- `requirements.txt` – Main dependencies
- `requirements-dev.txt` – Development dependencies

#### Continuous Integration

- `ci/azure/azure_template_posix.yml` – POSIX CI template
- `ci/azure/azure_template_windows.yml` – Windows CI template

#### Documentation

- `docs/contributors.py` – Contributor management script
- `docs/requirements.txt` – Documentation dependencies
- `docs/source/conf.py` – Sphinx configuration
- `docs/source/whatsnew/` – Changelog files (e.g., `v0.10.0.txt`, `v0.9.1.txt`, etc.)

#### Core Library: `pandas_datareader`

- `pandas_datareader/__init__.py` – Package initialization
- `pandas_datareader/data.py` – Main API for data access
- `pandas_datareader/base.py` – Base classes for data readers
- `pandas_datareader/exceptions.py` – Custom exceptions
- `pandas_datareader/_utils.py` – Internal utilities
- `pandas_datareader/_testing.py` – Testing utilities

##### Data Sources

- `pandas_datareader/av/` – Alpha Vantage support
  - `forex.py`, `quotes.py`, `sector.py`, `time_series.py`
- `pandas_datareader/bankofcanada.py` – Bank of Canada reader
- `pandas_datareader/econdb.py` – EconDB reader
- `pandas_datareader/enigma.py` – Enigma reader
- `pandas_datareader/eurostat.py` – Eurostat reader
- `pandas_datareader/famafrench.py` – Fama/French datasets
- `pandas_datareader/fred.py` – FRED reader
- `pandas_datareader/iex/` – IEX Cloud support
  - `daily.py`, `deep.py`, `market.py`, `ref.py`, `stats.py`, `tops.py`
- `pandas_datareader/moex.py` – MOEX reader
- `pandas_datareader/nasdaq_trader.py` – NASDAQ Trader reader
- `pandas_datareader/naver.py` – Naver reader
- `pandas_datareader/oecd.py` – OECD reader
- `pandas_datareader/quandl.py` – Quandl reader
- `pandas_datareader/stooq.py` – Stooq reader
- `pandas_datareader/tiingo.py` – Tiingo reader
- `pandas_datareader/tsp.py` – TSP reader
- `pandas_datareader/wb.py` – World Bank reader
- `pandas_datareader/yahoo/` – Yahoo Finance support
  - `actions.py`, `components.py`, `daily.py`, `fx.py`, `headers.py`, `options.py`, `quotes.py`

##### Utilities and Compatibility

- `pandas_datareader/compat/` – Compatibility helpers

##### I/O Utilities

- `pandas_datareader/io/` – SDMX and JSDMX support
  - `jsdmx.py`, `sdmx.py`, `util.py`

##### Testing Suite

- `pandas_datareader/tests/` – Unit and integration tests
  - Source-specific tests (e.g., `test_fred.py`, `test_yahoo.py`)
  - Subfolders for AV, IEX, IO, Yahoo, etc.
  - Test data under `tests/io/data/` and `tests/yahoo/data/`

---

### Practical Examples

- **Accessing FRED Data:**  
  See [`pandas_datareader/fred.py`](pandas_datareader/fred.py) and usage in [`pandas_datareader/tests/test_fred.py`](pandas_datareader/tests/test_fred.py).
- **Testing Yahoo Finance Integration:**  
  Refer to [`pandas_datareader/yahoo/`](pandas_datareader/yahoo/) and corresponding tests in [`pandas_datareader/tests/yahoo/`](pandas_datareader/tests/yahoo/).
- **Adding a New Data Source:**  
  Use [`pandas_datareader/base.py`](pandas_datareader/base.py) as a template for new readers.

---

For more details on each section, refer to the corresponding headings in this README.

## Installation

## Installation

> **Note:** No codebase data was found. The following installation instructions are based on standard best practices for typical Python projects. Please adapt as needed for your specific environment.

### Prerequisites

Before installing, ensure you have the following installed on your system:

- **Python 3.7+**  
  Download from [python.org](https://www.python.org/downloads/).

- **pip** (Python package manager)  
  Usually included with Python. Check with:
  ```bash
  pip --version
  ```

- **git** (optional, for cloning the repository)  
  Download from [git-scm.com](https://git-scm.com/).

### 1. Clone the Repository

Clone the project to your local machine using git:

```bash
git clone https://github.com/your-username/your-project.git
cd your-project
```

Alternatively, you can download the ZIP archive from GitHub and extract it.

### 2. Create a Virtual Environment (Recommended)

It is recommended to use a virtual environment to manage dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

If your project includes a `requirements.txt` file, install dependencies with:

```bash
pip install -r requirements.txt
```

If your project uses a different dependency manager (e.g., `Pipfile`, `pyproject.toml`), use the appropriate tool:

- **Pipenv:**
  ```bash
  pipenv install
  ```
- **Poetry:**
  ```bash
  poetry install
  ```

### 4. Configuration (If Required)

If your project requires configuration (e.g., `.env` files or config files), copy the example file and edit as needed:

```bash
cp .env.example .env
# Edit .env with your preferred settings
```

### 5. Verify Installation

To verify the installation, you can run:

```bash
python -m your_project  # Replace with your project's entry point
```

Or, if there are tests:

```bash
pytest  # Or: python -m unittest
```

---

**Troubleshooting:**  
If you encounter issues during installation, please refer to the [Dependencies](#dependencies) and [Configuration](#configuration) sections, or contact the maintainers listed in [Contact Information](#contact-information).

---

> _For more detailed usage instructions, see the [Usage](#usage) section._

## Usage

## Usage

> **Note:** No codebase data was found. The following section provides a general template for usage instructions. Please update this section with specific commands, code snippets, or workflows once the codebase is available.

---

### Running the Project

After completing the [Installation](#installation) steps, you can use the project as follows:

#### 1. Command-Line Usage

If the project provides a command-line interface (CLI), you can typically run it using:

```bash
python main.py [options]
```

Replace `main.py` with the entry point script of your project. Common options might include:

- `--help` to display usage information
- `--config <path>` to specify a configuration file

#### 2. Importing as a Module

If the project is intended to be used as a Python module, you can import its main classes or functions in your own scripts:

```python
from project_name.module import MainClass

instance = MainClass(config='path/to/config.yaml')
result = instance.run()
print(result)
```

Replace `project_name.module` and `MainClass` with the actual module and class names from your codebase.

#### 3. Configuration

If your project uses a configuration file, ensure it is properly set up before running the project. Refer to the [Configuration](#configuration) section for details.

#### 4. Example Workflow

Below is a generic example workflow:

```bash
# Step 1: Prepare your data or configuration
cp config/example_config.yaml config/config.yaml

# Step 2: Run the main script
python main.py --config config/config.yaml

# Step 3: View the output
cat output/results.txt
```

#### 5. Testing

To run the test suite (if available):

```bash
pytest tests/
```

---

### Notes

- Replace placeholder names (e.g., `main.py`, `MainClass`, `config.yaml`) with actual names from your codebase.
- For more advanced usage, refer to the [Additional Documentation](#additional-documentation) section.

---

If you encounter any issues or need further assistance, please refer to the [Contact Information](#contact-information) section.

## Project Structure

## Project Structure

This project follows a modular and organized directory structure, separating core functionality, documentation, configuration, and testing. Below is an overview of the main folders and files, along with their purposes and practical examples to help you navigate and contribute effectively.

```
.
├── ci/
│   └── azure/
│       ├── azure_template_posix.yml
│       └── azure_template_windows.yml
├── docs/
│   ├── requirements.txt
│   ├── contributors.py
│   └── source/
│       ├── conf.py
│       └── whatsnew/
│           ├── v0.10.0.txt
│           ├── v0.9.1.txt
│           └── ... (other release notes)
├── pandas_datareader/
│   ├── __init__.py
│   ├── base.py
│   ├── data.py
│   ├── exceptions.py
│   ├── ... (core modules)
│   ├── av/
│   ├── compat/
│   ├── iex/
│   ├── io/
│   ├── tests/
│   └── yahoo/
├── requirements.txt
├── requirements-dev.txt
├── azure-pipelines.yml
├── .codecov.yml
├── LICENSE.md
└── release-procedure.md
```

### Top-Level Files and Directories

- **requirements.txt**: Lists the main dependencies required to run the project.
- **requirements-dev.txt**: Lists additional dependencies for development and testing.
- **azure-pipelines.yml**: Main CI pipeline configuration for Azure Pipelines.
- **.codecov.yml**: Configuration for code coverage reporting.
- **LICENSE.md**: Project license information.
- **release-procedure.md**: Step-by-step guide for releasing new versions.

---

### Continuous Integration

- **ci/azure/**: Contains reusable Azure Pipeline templates for different environments:
  - `azure_template_posix.yml`: CI template for POSIX systems (Linux, macOS).
  - `azure_template_windows.yml`: CI template for Windows systems.

---

### Documentation

- **docs/**: Documentation source files and requirements.
  - `requirements.txt`: Documentation build dependencies.
  - `contributors.py`: Script or data related to project contributors.
  - **docs/source/**: Sphinx documentation source.
    - `conf.py`: Sphinx configuration file.
    - **docs/source/whatsnew/**: Release notes for each version (e.g., `v0.10.0.txt`).

---

### Core Library

- **pandas_datareader/**: Main package containing all core modules and submodules.
  - `__init__.py`: Package initializer.
  - `base.py`, `data.py`, `exceptions.py`, etc.: Core modules for data access and error handling.
  - **av/**: Alpha Vantage data source support.
    - `time_series.py`, `sector.py`, `quotes.py`, `forex.py`: Fetching different types of data from Alpha Vantage.
  - **compat/**: Compatibility helpers for different Python/pandas versions.
  - **iex/**: IEX Cloud data source support.
    - `daily.py`, `deep.py`, `market.py`, etc.: Fetching various IEX data endpoints.
  - **io/**: Input/output utilities.
    - `sdmx.py`, `jsdmx.py`, `util.py`: Data format handling and utilities.
  - **yahoo/**: Yahoo Finance data source support.
    - `quotes.py`, `options.py`, `fx.py`, `daily.py`, etc.: Fetching quotes, options, FX rates, and more.

**Example:**
To fetch daily stock data from Yahoo Finance, the relevant code is in `pandas_datareader/yahoo/daily.py`. For Alpha Vantage time series, see `pandas_datareader/av/time_series.py`.

---

### Testing

- **pandas_datareader/tests/**: Comprehensive test suite for all modules.
  - `test_*.py`: Unit tests for each data source and utility.
  - **av/**, **io/**, **yahoo/**: Subdirectories with tests specific to each submodule.
  - **io/data/**, **yahoo/data/**: Test data and fixtures for integration tests.

**Example:**
To run tests for the Yahoo Finance integration, see `pandas_datareader/tests/yahoo/test_yahoo.py`.

---

### Practical Navigation Examples

- **Adding a new data source**: Create a new submodule in `pandas_datareader/`, implement the logic, and add corresponding tests in `pandas_datareader/tests/`.
- **Updating documentation**: Edit or add files in `docs/source/` and update release notes in `docs/source/whatsnew/`.
- **Modifying CI**: Update templates in `ci/azure/` or the main pipeline in `azure-pipelines.yml`.

---

This structure ensures clear separation of concerns, making it easy to locate, extend, and maintain different parts of the project. For more details on each module or to contribute, refer to the relevant sections in this README.

## Key Classes and Functions

## Key Classes and Functions

This section provides an overview of the most important classes and functions in the codebase, focusing on their purpose, usage, and relationships. The project is organized around data readers for various financial data sources, with a modular structure that makes it easy to extend and maintain.

---

### Core Classes

#### `AlphaVantage`  
*Location: `pandas_datareader/av/__init__.py`*  
The main interface for accessing Alpha Vantage data. This class is typically not used directly; instead, use the specialized readers below.

#### `AVForexReader`  
*Location: `pandas_datareader/av/forex.py`*  
Fetches foreign exchange (forex) data from Alpha Vantage.

**Example:**
```python
from pandas_datareader.av.forex import AVForexReader

reader = AVForexReader(symbols='EUR/USD', start='2023-01-01', end='2023-01-31', api_key='YOUR_API_KEY')
df = reader.read()
```

#### `AVQuotesReader`  
*Location: `pandas_datareader/av/quotes.py`*  
Retrieves real-time and historical quote data from Alpha Vantage.

#### `AVSectorPerformanceReader`  
*Location: `pandas_datareader/av/sector.py`*  
Accesses sector performance data from Alpha Vantage.

#### `AVTimeSeriesReader`  
*Location: `pandas_datareader/av/time_series.py`*  
Fetches time series data (e.g., daily, weekly, monthly) for stocks from Alpha Vantage.

#### `BankOfCanadaReader`  
*Location: `pandas_datareader/bankofcanada.py`*  
Retrieves economic and financial data from the Bank of Canada.

#### `_BaseReader`, `_DailyBaseReader`, `_OptionBaseReader`  
*Location: `pandas_datareader/base.py`*  
Abstract base classes that provide shared logic for all data readers, including chunked data retrieval via the `_in_chunks` method.

---

### Core Functions

#### `DataReader`  
*Location: `pandas_datareader/data.py`*  
The primary function for retrieving data from a wide range of sources. It automatically selects the appropriate reader based on the `data_source` argument.

**Example:**
```python
from pandas_datareader import data

df = data.DataReader('AAPL', data_source='yahoo', start='2023-01-01', end='2023-01-31')
```

#### `Options`  
*Location: `pandas_datareader/data.py`*  
Fetches options data for a given symbol.

**Example:**
```python
from pandas_datareader.data import Options

options = Options('AAPL', 'yahoo')
data = options.get_options_data()
```

#### Specialized Data Fetching Functions  
*Location: `pandas_datareader/data.py`*  
These functions provide convenient access to specific data sources:

- `get_data_alphavantage`
- `get_data_econdb`
- `get_data_enigma`
- `get_data_famafrench`
- `get_data_fred`
- `get_data_moex`
- `get_data_quandl`
- `get_dailysummary_iex`

**Example:**
```python
from pandas_datareader.data import get_data_fred

df = get_data_fred('GDP', start='2020-01-01', end='2023-01-01')
```

---

### Utilities and Error Handling

#### `RemoteDataError`, `SymbolWarning`  
*Location: `pandas_datareader/_utils.py`*  
Custom exception and warning classes for handling remote data errors and symbol-related issues.

#### `_init_session`, `_sanitize_dates`  
*Location: `pandas_datareader/_utils.py`*  
Internal utility functions for initializing HTTP sessions and sanitizing date inputs.

#### `get_filepath_or_buffer`  
*Location: `pandas_datareader/compat/__init__.py`*  
Handles file path or buffer compatibility across different pandas versions.

---

### Testing Utilities

#### `test`  
*Location: `pandas_datareader/__init__.py`*  
Entry point for running the package's test suite.

#### `skip_on_exception`, `wrapper`  
*Location: `pandas_datareader/_testing.py`*  
Decorators for managing test execution and exception handling.

---

### Pytest Integration

*Location: `pandas_datareader/conftest.py`*  
- `datapath`: Utility for test data file paths.
- `deco`: Test decorator.
- `pytest_addoption`, `pytest_runtest_setup`: Pytest hooks for custom test configuration.

---

## Summary Table

| Class/Function                | Purpose                                              | Example Usage                                      |
|-------------------------------|------------------------------------------------------|----------------------------------------------------|
| `DataReader`                  | General data retrieval from multiple sources         | `DataReader('AAPL', 'yahoo', ...)`                 |
| `Options`                     | Fetch options data                                   | `Options('AAPL', 'yahoo')`                         |
| `AVForexReader`               | Alpha Vantage forex data                             | `AVForexReader('EUR/USD', ...)`                    |
| `BankOfCanadaReader`          | Bank of Canada data                                  | `BankOfCanadaReader('FXUSDCAD', ...)`              |
| `get_data_fred`               | Fetch FRED data                                      | `get_data_fred('GDP', ...)`                        |
| `RemoteDataError`             | Exception for remote data issues                     | `raise RemoteDataError("...")`                     |

---

For more details and advanced usage, refer to the [Usage](#usage) and [Additional Documentation](#additional-documentation) sections.

## Configuration

## Configuration

This project uses several configuration files to manage code coverage reporting and continuous integration (CI) workflows. Below is an overview of each configuration file, their purposes, and practical guidance on how to modify or extend them for your needs.

### 1. `.codecov.yml`

This file configures [Codecov](https://docs.codecov.com/docs/codecov-yaml), a tool for code coverage reporting. It defines how coverage reports are processed and uploaded.

**Typical contents and usage:**
```yaml
# .codecov.yml
coverage:
  status:
    project:
      default:
        target: 80%    # Set the minimum coverage threshold
        threshold: 1%  # Allowable drop before failing
comment:
  layout: "reach, diff, flags, files"
  behavior: default
```

**How to use:**
- Adjust the `target` value to set your desired minimum coverage.
- Modify the `comment` section to customize the coverage report comments on pull requests.

**Location:**  
Root directory: `.codecov.yml`

---

### 2. `azure-pipelines.yml`

This is the main Azure Pipelines configuration file. It defines the CI/CD workflow for the project, specifying triggers, jobs, and steps to build, test, and deploy your code.

**Typical structure:**
```yaml
# azure-pipelines.yml
trigger:
  - main

jobs:
  - template: ci/azure/azure_template_posix.yml
    parameters:
      os: 'ubuntu-latest'
  - template: ci/azure/azure_template_windows.yml
    parameters:
      os: 'windows-latest'
```

**How to use:**
- The `trigger` section specifies which branches will trigger the pipeline.
- Jobs are defined using templates for different environments (see below).
- Add or modify jobs to extend CI coverage to other platforms or add custom steps.

**Location:**  
Root directory: `azure-pipelines.yml`

---

### 3. `ci/azure/azure_template_posix.yml`

This template defines the CI steps for POSIX-compatible environments (e.g., Linux, macOS). It is referenced by the main pipeline file.

**Example contents:**
```yaml
# ci/azure/azure_template_posix.yml
parameters:
  os: 'ubuntu-latest'

jobs:
  - job: BuildAndTest
    pool:
      vmImage: ${{ parameters.os }}
    steps:
      - script: |
          echo "Building on POSIX system"
          # Insert build commands here
      - script: |
          echo "Running tests"
          # Insert test commands here
```

**How to use:**
- Add build and test commands specific to POSIX systems.
- Extend with additional steps (e.g., linting, packaging) as needed.

**Location:**  
`ci/azure/azure_template_posix.yml`

---

### 4. `ci/azure/azure_template_windows.yml`

This template defines the CI steps for Windows environments. It is also referenced by the main pipeline file.

**Example contents:**
```yaml
# ci/azure/azure_template_windows.yml
parameters:
  os: 'windows-latest'

jobs:
  - job: BuildAndTest
    pool:
      vmImage: ${{ parameters.os }}
    steps:
      - script: |
          echo "Building on Windows system"
          REM Insert build commands here
      - script: |
          echo "Running tests"
          REM Insert test commands here
```

**How to use:**
- Add Windows-specific build and test commands.
- Customize steps for Windows tooling or dependencies.

**Location:**  
`ci/azure/azure_template_windows.yml`

---

### Customizing Your Configuration

- **Adding New Environments:**  
  To add support for another OS or configuration, create a new template in `ci/azure/` and reference it in `azure-pipelines.yml`.

- **Modifying Coverage Thresholds:**  
  Update `.codecov.yml` to enforce stricter or more lenient coverage requirements.

- **Extending CI Steps:**  
  Edit the template files to add steps such as static analysis, deployment, or artifact publishing.

---

### Summary Table

| File Path                                 | Purpose                                  |
|--------------------------------------------|------------------------------------------|
| `.codecov.yml`                            | Code coverage reporting configuration    |
| `azure-pipelines.yml`                     | Main Azure Pipelines workflow            |
| `ci/azure/azure_template_posix.yml`       | POSIX (Linux/macOS) CI job template      |
| `ci/azure/azure_template_windows.yml`     | Windows CI job template                  |

---

For more details on each configuration file, refer to the official documentation for [Codecov YAML](https://docs.codecov.com/docs/codecov-yaml) and [Azure Pipelines YAML](https://docs.microsoft.com/en-us/azure/devops/pipelines/yaml-schema).

## Dependencies

## Dependencies

This project relies on several core Python libraries and modules, as well as internal packages, to provide its data reading and processing functionality. Below is a detailed overview of the main dependencies, based on the actual imports found throughout the codebase.

### Core Python Standard Library Dependencies

- **datetime**  
  Used extensively across both the main package and test suite for handling dates and times.  
  **Example usage:**  
  ```python
  from datetime import datetime, timedelta

  start = datetime(2020, 1, 1)
  end = datetime.now()
  ```

- **os**  
  Utilized for file and directory operations, environment variable access, and path manipulations.  
  **Example usage:**  
  ```python
  import os

  data_dir = os.environ.get("DATA_DIR", "/tmp")
  file_path = os.path.join(data_dir, "output.csv")
  ```

### Third-Party and External Dependencies

- **github**  
  Used in documentation scripts (e.g., `docs/contributors.py`) for interacting with GitHub APIs or repositories.  
  **Example usage:**  
  ```python
  import github

  # Example: Fetch contributors from a GitHub repository
  ```

### Internal Package Dependencies

- **pandas_datareader**  
  The package is modular, and several test files import from the main `pandas_datareader` package to validate functionality.  
  **Example usage:**  
  ```python
  from pandas_datareader import data as pdr

  df = pdr.get_data_yahoo('AAPL', start='2020-01-01', end='2020-12-31')
  ```

### Dependency Usage in the Codebase

- The `datetime` module is imported in nearly all data source modules (e.g., `yahoo/options.py`, `moex.py`, `famafrench.py`, etc.) and in the majority of test files, indicating its central role in date handling for data queries and results.
- The `os` module is used in both core modules (e.g., `tiingo.py`, `quandl.py`, `io/util.py`) and test scripts for environment configuration and file management.
- The `github` library is only referenced in documentation tooling, not in the main package.
- Internal imports of `pandas_datareader` are prevalent in the test suite, ensuring comprehensive coverage and modular testing.

### Summary Table

| Library/Module   | Used In (Examples)                                 | Purpose                                    |
|------------------|---------------------------------------------------|--------------------------------------------|
| `datetime`       | Core modules, tests, docs                         | Date/time parsing, manipulation, intervals |
| `os`             | Core modules, tests, docs                         | File paths, environment variables          |
| `github`         | Documentation scripts (`docs/contributors.py`)    | GitHub API access (docs only)              |
| `pandas_datareader` | Test suite, internal imports                   | Data reading, internal API                 |

### Additional Notes

- **Other dependencies** such as `requests`, `pandas`, or `lxml` may be required for full functionality, but are not directly referenced in the provided codebase data. Please refer to the `requirements.txt` or `setup.py` for a complete list.
- **Testing dependencies**: The test suite relies on the same core dependencies and may require additional testing frameworks (e.g., `pytest`), though these are not explicitly listed in the provided data.

---

**Tip:**  
Before running the package or tests, ensure all dependencies are installed. For a typical setup, you can use:

```bash
pip install -r requirements.txt
```

or, for development and testing:

```bash
pip install -r requirements-dev.txt
```

Refer to the [Installation](#installation) section for more details.

## Contributing

## Contributing

We welcome contributions from the community! Whether you are fixing bugs, improving documentation, or adding new features, your input helps make this project better for everyone. Please read the guidelines below to ensure a smooth contribution process.

### How to Contribute

1. **Fork the Repository**  
   Start by forking the repository on GitHub to your own account.

2. **Clone Your Fork**  
   ```bash
   git clone https://github.com/your-username/pydata.git
   cd pydata
   ```

3. **Create a Branch**  
   Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b my-feature-branch
   ```

4. **Make Your Changes**  
   - Follow the existing code style and conventions.
   - Add or update tests as appropriate.
   - Update documentation if your changes affect usage or behavior.

5. **Commit Your Changes**  
   Write clear, descriptive commit messages. If you wish to indicate copyright for a specific contribution, include a copyright notice in your commit message:
   ```
   Fix issue with data parsing

   Copyright 2024 Jane Doe
   ```

6. **Push to Your Fork**  
   ```bash
   git push origin my-feature-branch
   ```

7. **Open a Pull Request**  
   Go to the original repository and open a pull request from your branch. Provide a clear description of your changes and reference any related issues.

### Copyright and Licensing

- **Shared Copyright Model:**  
  Each contributor retains copyright over their contributions. The PyData source code as a whole is the collective copyright of the PyData Development Team.

- **Commit Messages:**  
  If you want to maintain a record of your specific copyright, indicate this in your commit message.

- **License:**  
  By contributing, you agree that your code will be distributed under the project's license. Please review the [LICENSE.md](LICENSE.md) for full details.

### Practical Example

Suppose you fixed a bug in the data loader. Your commit message might look like:
```
Fix: Correct off-by-one error in data loader

This fixes issue #123 by adjusting the index calculation.

Copyright 2024 Alex Smith
```

### Code of Conduct

Please be respectful and constructive in all interactions. We value a welcoming and inclusive community.

### Getting Help

If you have questions about contributing, open an issue or reach out to the core team on GitHub: [https://github.com/pydata](https://github.com/pydata).

---

Thank you for your interest in contributing to PyData! Your efforts help drive the project forward.

## Additional Documentation

## Additional Documentation

At this time, there is no further codebase data available to generate detailed technical documentation for this section. However, this section is intended to provide advanced insights, practical examples, and extended references to help users and contributors make the most of the project. Below are some general guidelines and templates for what can be included here as the project evolves:

---

### 1. Advanced Usage Examples

Provide real-world scenarios or advanced use cases that go beyond the basic usage described earlier. For example:

```python
# Example: Integrating with a custom configuration
from project_module import MainClass

config = {
    "option1": "value1",
    "option2": "value2"
}
instance = MainClass(config)
instance.run_advanced_feature()
```

---

### 2. Extending the Project

Describe how users can extend or customize the project. For example:

- **Adding New Modules:**  
  Outline the steps to add new modules or features, referencing the project structure.

- **Subclassing Key Classes:**  
  Provide examples of subclassing or overriding core functionality.

---

### 3. Troubleshooting & FAQ

Offer solutions to common issues or frequently asked questions.

**Q: How do I resolve dependency conflicts?**  
A: Ensure all dependencies listed in `requirements.txt` are installed in a clean virtual environment.

---

### 4. API Reference

As the codebase grows, include detailed API documentation for public classes, methods, and functions. Tools like Sphinx or pdoc can help automate this process.

---

### 5. External Resources

Link to relevant external documentation, tutorials, or community forums that may assist users.

---

### 6. Changelog

Maintain a changelog in this section to track significant updates, bug fixes, and new features.

---

**Note:**  
As the project develops and more codebase data becomes available, this section will be updated with concrete examples, technical deep-dives, and references tailored to the actual implementation.

If you have suggestions for what you'd like to see in this section, please open an issue or submit a pull request!

## License

## License

This project is distributed under the **3-clause BSD License** (also known as the "Simplified" or "New" BSD License). The license ensures that the software is open source and can be freely used, modified, and redistributed under certain conditions.

### Summary

- **Primary License:** 3-clause BSD License
- **Copyright Holders:**
  - 2008–2011: AQR Capital Management, LLC
  - 2011–2012: Lambda Foundry, Inc. and PyData Development Team
- **Included Components:** Portions of NumPy, SciPy, numpydoc, and bottleneck are included, all of which have BSD-compatible licenses. Their licenses follow the pandas license.

### License Terms

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. **Redistributions of source code** must retain the copyright notice, this list of conditions, and the following disclaimer.
2. **Redistributions in binary form** must reproduce the above copyright notice, this list of conditions, and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. **Neither the name of the copyright holders nor the names of its contributors** may be used to endorse or promote products derived from this software without specific prior written permission.

> **Disclaimer:**  
> THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

### Copyright Holders

- **AQR Capital Management** began pandas development in 2008, led by Wes McKinney. The source was released under this license in 2009.
- **Lambda Foundry, Inc.** and the **PyData Development Team** continued development from 2011 onward.
- The PyData Development Team includes all developers of the PyData project and its sub-projects, including pandas. The core team coordinates development on [GitHub](http://github.com/pydata).

Full credits for contributors can be found in the project documentation.

### Practical Example: License Banner for Source Files

To indicate the copyright and license terms in any source code file, include the following banner at the top:

```python
#-----------------------------------------------------------------------------
# Copyright (c) 2012, PyData Development Team
# All rights reserved.
#
# Distributed under the terms of the BSD Simplified License.
#
# The full license is in the LICENSE file, distributed with this software.
#-----------------------------------------------------------------------------
```

### Additional Licenses

Other licenses for included components can be found in the `LICENSES` directory of the repository.

### Full License Text

The complete license text is available in the [LICENSE.md](./LICENSE.md) file distributed with this software.

---

For any questions regarding licensing, please refer to the LICENSE file or contact the maintainers listed in the [Contact Information](#contact-information) section.

## Contact Information

## Contact Information

At present, there is no direct contact information (such as maintainer emails, support addresses, or contributor profiles) found within the codebase or its configuration files. To ensure users and contributors can still reach out or get support, we recommend the following approaches:

### 1. GitHub Issues

If you encounter bugs, have questions, or wish to request new features, please use the [Issues](../../issues) section of the repository. This is the preferred method for tracking and responding to project-related queries.

**Example:**
```markdown
- Go to the repository's [Issues](../../issues) page.
- Click "New Issue" and select the appropriate template (bug report, feature request, etc.).
- Provide a clear description and, if applicable, steps to reproduce the issue.
```

### 2. Pull Requests

For code contributions or documentation improvements, please submit a [Pull Request](../../pulls). The project maintainers will review and respond as soon as possible.

**Example:**
```markdown
- Fork the repository.
- Create a new branch for your feature or fix.
- Commit your changes with clear messages.
- Open a Pull Request and describe your changes.
```

### 3. Discussions

If the repository has the [Discussions](../../discussions) feature enabled, you can start or join conversations about the project, usage tips, or general questions.

### 4. Adding Maintainer Information

If you are a maintainer, consider adding your contact details (such as an email address or a link to a team page) in this section for more direct communication.

**Example:**
```markdown
For direct inquiries, contact: maintainer@example.com
```

---

**Note:**  
If you need urgent assistance or wish to report a security vulnerability, please check if a `SECURITY.md` file exists in the repository root, or use the GitHub security advisory workflow.

---

We encourage all users and contributors to use the above channels for communication to ensure transparency and effective collaboration.

## Acknowledgements

## Acknowledgements

While reviewing the codebase, we did not find explicit references to third-party libraries, frameworks, or external contributors within the repository structure or code comments. However, we would like to acknowledge the following general resources and tools that are commonly essential in modern software development and may have influenced the design and implementation of this project:

- **Open Source Community**: The broader open source community provides invaluable resources, documentation, and libraries that inspire and accelerate software development.
- **Programming Language Ecosystem**: The project leverages the standard libraries and best practices of its primary programming language, which form the foundation for robust and maintainable code.
- **Development Tools**: Tools such as version control systems (e.g., Git), code editors, and continuous integration platforms play a crucial role in the development workflow.

If you identify any specific libraries, frameworks, or individuals whose work has directly contributed to this project, please let us know so we can update this section and give proper credit.

---

**Note:**  
If you are contributing to this project and wish to acknowledge any additional resources, collaborators, or inspirations, please add them to this section in your pull request. Your contributions and attributions help strengthen the community and recognize the efforts of others.