# Project Data Structure and Code Reference

---

## Table of Contents

1. [Introduction](#introduction)
2. [Project Overview](#project-overview)
   - [Folder Structure](#folder-structure)
   - [Key Files](#key-files)
   - [Example: Importing an Endpoint](#example-importing-an-endpoint)
   - [Summary](#summary)
3. [Class and Inheritance Structure](#class-and-inheritance-structure)
   - [Overview](#overview)
   - [Class List](#class-list)
   - [Inheritance](#inheritance)
   - [Decorators](#decorators)
   - [File Organization](#file-organization)
   - [Summary Table](#summary-table)
4. [Functions and Methods Reference](#functions-and-methods-reference)
   - [Standalone Functions](#standalone-functions)
   - [Classes and Methods](#classes-and-methods)
   - [Usage Notes](#usage-notes)
5. [Code Relationships and Call Graph](#code-relationships-and-call-graph)
   - [Overview](#overview-1)
   - [Method-to-Method Calls](#method-to-method-calls)
   - [Method-to-Function Calls](#method-to-function-calls)
   - [Visual Call Graph](#visual-call-graph)
   - [Key Insights for Developers](#key-insights-for-developers)
   - [Recommendations](#recommendations)
6. [Folder and File Containment](#folder-and-file-containment)
   - [Overview](#overview-2)
   - [Data Model](#data-model)
   - [Containment Hierarchy](#containment-hierarchy)
   - [Example Queries](#example-queries)
   - [Practical Usage](#practical-usage)
   - [Summary](#summary-1)
7. [Usage Examples](#usage-examples)
   - [Mocking Azure Blob Storage Clients for Testing](#1-mocking-azure-blob-storage-clients-for-testing)
   - [Chunking Data](#2-chunking-data)
   - [Azure Retry Decorator](#3-azure-retry-decorator)
   - [Sanitizing Container Names](#4-sanitizing-container-names)
   - [Path Validation for Uploads](#5-path-validation-for-uploads)
   - [Uploading a Repository to Azure Blob Storage](#6-uploading-a-repository-to-azure-blob-storage)
   - [Uploading a Single File](#7-uploading-a-single-file)
   - [Data Cleaning Utilities](#8-data-cleaning-utilities)
   - [Summary](#summary-2)
8. [Conclusion](#conclusion)

---

## Introduction

This document serves as a comprehensive technical reference for the **Input Integration Pipeline** microservice project. It is designed to help developers, maintainers, and contributors quickly understand the organization, architecture, and usage patterns of the codebase. The guide covers the project structure, class and function references, code relationships, data model, and practical usage examples.

---

## Project Overview

This section provides a high-level overview of the folder and file structure for the **Input Integration Pipeline** microservice. Understanding the organization of the codebase will help developers quickly locate relevant modules, endpoints, utilities, and tests.

### Folder Structure

The project is organized into a hierarchy of folders, each serving a specific purpose within the microservice architecture. Below is a breakdown of the main directories:

```
microservices/
└── input_integration_pipeline/
    └── source/
        ├── fetch_repo_from_blob/
        │   ├── endpoints/
        │   ├── source/
        │   ├── tests/
        │   └── utilities/
        └── repo_downloader/
            ├── endpoints/
            ├── source/
            └── tests/
```

#### Folder Descriptions

- **fetch_repo_from_blob/**
  - `endpoints/`: API endpoint definitions for the fetch_repo_from_blob service.
  - `source/`: Core logic and data schemas.
  - `tests/`: Unit and integration tests.
  - `utilities/`: Utility functions and helpers.

- **repo_downloader/**
  - `endpoints/`: API endpoint definitions for the repo_downloader service.
  - `source/`: Core logic and initialization files.
  - `tests/`: Test suite for the repo_downloader component.

---

### Key Files

#### fetch_repo_from_blob

- `endpoints/api.py`: API endpoints for fetch_repo_from_blob.
- `main.py`: Entry point for the microservice.
- `source/schemas.py`: Data models and schemas for request/response validation.
- `tests/test_fetch_repo_from_blob.py`: Test cases for logic and endpoints.
- `utilities/chunk_rows.py`: Utility for chunking data rows.
- `utilities/retry.py`: Retry logic for robust error handling.

#### repo_downloader

- `endpoints/status.py`: Status-related API endpoints.
- `main.py`: Entry point for the microservice.
- `source/__init__.py`: Marks the source directory as a Python package.
- `tests/__init__.py`: Marks the tests directory as a Python package.

---

### Example: Importing an Endpoint

To use an endpoint from the fetch_repo_from_blob service:

```python
from fetch_repo_from_blob.endpoints.api import some_endpoint_function
```

To utilize a utility function:

```python
from fetch_repo_from_blob.utilities.retry import retry_function
```

---

### Summary

This structure separates concerns clearly between API endpoints, business logic, utilities, and tests, making the codebase maintainable and scalable. Each microservice component is self-contained, facilitating independent development and testing.

For more detailed information on each module or to contribute, refer to the respective README files or in-code documentation within each directory.

---

## Class and Inheritance Structure

### Overview

All data model classes are defined in a single file:

```
microservices/input_integration_pipeline/source/fetch_repo_from_blob/source/schemas.py
```

Each class represents a specific request or response schema used throughout the microservice. All classes inherit from a common base, ensuring consistency and leveraging shared validation and serialization logic.

### Class List

- `BlobRequest`
- `BlobToParquetRequest`
- `BlobDownloadResponse`
- `ContainerRequest`
- `ContainerDownloadRequest`
- `FilesByTypeRequest`
- `ContainerToParquetRequest`
- `ContainerAccessResponse`
- `ContainerDownloadResponse`
- `FilesByTypeResponse`

#### Example Class Definition

```python
from pydantic import BaseModel

class BlobRequest(BaseModel):
    # Define fields here
    pass
```

### Inheritance

All classes inherit directly from `BaseModel`, provided by [Pydantic](https://docs.pydantic.dev/), which offers:

- Data validation on instantiation
- Automatic serialization/deserialization
- Type hints and editor support

**Inheritance Diagram:**

```
BaseModel
   ├── BlobRequest
   ├── BlobToParquetRequest
   ├── BlobDownloadResponse
   ├── ContainerRequest
   ├── ContainerDownloadRequest
   ├── FilesByTypeRequest
   ├── ContainerToParquetRequest
   ├── ContainerAccessResponse
   ├── ContainerDownloadResponse
   └── FilesByTypeResponse
```

### Decorators

No class decorators are used in any of the defined classes. All logic is contained within the class bodies themselves or inherited from `BaseModel`.

### File Organization

All schema classes are centralized in:

```
microservices/input_integration_pipeline/source/fetch_repo_from_blob/source/schemas.py
```

This organization simplifies maintenance and discoverability.

### Summary Table

| Class Name                  | Inherits From | Decorators | Defined In                                                      |
|-----------------------------|---------------|------------|-----------------------------------------------------------------|
| BlobRequest                 | BaseModel     | None       | microservices/input_integration_pipeline/source/fetch_repo_from_blob/source/schemas.py |
| BlobToParquetRequest        | BaseModel     | None       | microservices/input_integration_pipeline/source/fetch_repo_from_blob/source/schemas.py |
| BlobDownloadResponse        | BaseModel     | None       | microservices/input_integration_pipeline/source/fetch_repo_from_blob/source/schemas.py |
| ContainerRequest            | BaseModel     | None       | microservices/input_integration_pipeline/source/fetch_repo_from_blob/source/schemas.py |
| ContainerDownloadRequest    | BaseModel     | None       | microservices/input_integration_pipeline/source/fetch_repo_from_blob/source/schemas.py |
| FilesByTypeRequest          | BaseModel     | None       | microservices/input_integration_pipeline/source/fetch_repo_from_blob/source/schemas.py |
| ContainerToParquetRequest   | BaseModel     | None       | microservices/input_integration_pipeline/source/fetch_repo_from_blob/source/schemas.py |
| ContainerAccessResponse     | BaseModel     | None       | microservices/input_integration_pipeline/source/fetch_repo_from_blob/source/schemas.py |
| ContainerDownloadResponse   | BaseModel     | None       | microservices/input_integration_pipeline/source/fetch_repo_from_blob/source/schemas.py |
| FilesByTypeResponse         | BaseModel     | None       | microservices/input_integration_pipeline/source/fetch_repo_from_blob/source/schemas.py |

---

**In summary:**  
All schema classes are Pydantic models, defined in a single file, with no decorators and a flat inheritance structure. This design promotes clarity, maintainability, and consistency across the microservice’s data handling components.

---

## Functions and Methods Reference

This section provides a comprehensive reference for all standalone functions and class methods defined in the codebase. Each entry includes the function or method name, its signature, and any decorators applied.

---

### Standalone Functions

#### `test_fetch_repo_from_blob.py`

- **`mock_blob_client()`**
  - **Signature:** `()`
  - **Decorators:** `@pytest_asyncio.fixture`
  - **Description:** Provides a mock blob client for use in asynchronous pytest tests.

- **`mock_container_client_fixture()`**
  - **Signature:** `()`
  - **Decorators:** `@pytest_asyncio.fixture`
  - **Description:** Supplies a mock container client as a fixture for tests.

- **`list_blobs()`**
  - **Signature:** `()`
  - **Decorators:** None
  - **Description:** Lists blobs (implementation details in test context).

- **`get_blob_client(name)`**
  - **Signature:** `(name)`
  - **Decorators:** None
  - **Description:** Returns a blob client for the given blob name.

- **`patch_blob_service_client(monkeypatch, mock_container_client_fixture)`**
  - **Signature:** `(monkeypatch, mock_container_client_fixture)`
  - **Decorators:** `@pytest.fixture(autouse=True)`
  - **Description:** Automatically patches the blob service client for all tests in the module.

#### `chunk_rows.py`

- **`chunk_rows(rows, chunk_size)`**
  - **Signature:** `(rows, chunk_size)`
  - **Decorators:** None
  - **Description:** Splits an iterable of rows into chunks of a specified size.

#### `retry.py`

- **`azure_retry(function)`**
  - **Signature:** `(function)`
  - **Decorators:** None
  - **Description:** Decorator to add retry logic to Azure-related functions.

#### `status.py`

- **`get_status()`**
  - **Signature:** `()`
  - **Decorators:** `@router.get('/status', summary='Check the status of the API.')`
  - **Description:** Endpoint handler to check the status of the API.

#### `helpers.py`

- **`sanitize_container_name(name)`**
  - **Signature:** `(name)`
  - **Decorators:** None
  - **Description:** Sanitizes a container name to comply with Azure naming rules.

- **`is_path_allowed(relative_path)`**
  - **Signature:** `(relative_path)`
  - **Decorators:** None
  - **Description:** Checks if a given relative path is allowed for upload.

---

### Classes and Methods

#### `AsyncBlobIterator`

- **`__aiter__(self)`**
  - **Signature:** `(self)`
  - **Description:** Asynchronous iterator protocol implementation.

#### `RepoUploader`

- **`__init__(self, blob_manager)`**
- **`upload_repository(self, repo_path, max_workers=8)`**
- **`_speed_up_upload(self, container_client, files, max_workers)`**
- **`upload_single_file(self, container_client, full_path, relative_path)`**

#### `TextCleaner`

- **`__init__(self, df)`**
- **`__remove_extra_whitespace(self, text)`**
- **`__remove_special_characters(self, text)`**
- **`__normalize_punctuation(self, text)`**
- **`__remove_urls(self, text)`**

---

### Usage Notes

- **Decorators** such as `@pytest.fixture`, `@pytest_asyncio.fixture`, and FastAPI's `@router.get` are used for testing and API integration.
- **Private methods** (with double underscores) are for internal use.
- **Chunking and retry utilities** support robust and scalable data processing.

---

## Code Relationships and Call Graph

### Overview

This section analyzes the relationships between methods and functions, focusing on which methods invoke others. This helps developers understand the flow of execution and dependencies.

---

### Method-to-Method Calls

#### **RepoUploader**

- `upload_repository` calls `_speed_up_upload`

#### **TextCleaner**

- `clean_text` calls:
  - `__remove_extra_whitespace`
  - `__remove_special_characters`
  - `__normalize_punctuation`
  - `__remove_urls`
  - `__remove_emails`
  - `__fix_encoding_issues`
  - `__lowercase_text`
  - `__remove_short_lines`
- `get_txt_files` calls `clean_text`

---

### Method-to-Function Calls

#### **RepoUploader**

- `upload_single_file` calls `get_blob_client`

#### **ManageTransforming**

- `__run` calls `cleaner`

---

### Visual Call Graph

```
RepoUploader
├── upload_repository
│   └── _speed_up_upload
└── upload_single_file
    └── get_blob_client (function)

TextCleaner
├── get_txt_files
│   └── clean_text
│       ├── __remove_extra_whitespace
│       ├── __remove_special_characters
│       ├── __normalize_punctuation
│       ├── __remove_urls
│       ├── __remove_emails
│       ├── __fix_encoding_issues
│       ├── __lowercase_text
│       └── __remove_short_lines

ManageTransforming
└── __run
    └── cleaner (function)
```

---

### Key Insights for Developers

- **TextCleaner**’s `clean_text` is central, orchestrating several helpers.
- **RepoUploader** delegates upload logic and uses external functions.
- **ManageTransforming** relies on an external `cleaner` function, indicating modularity.

---

### Recommendations

- Review callees when modifying methods to understand downstream effects.
- Mock called methods/functions in tests to isolate behavior.
- Use this call graph for onboarding or refactoring.

---

## Folder and File Containment

### Overview

This section describes the hierarchical organization of folders and files within the data model, using a graph-based approach.

### Data Model

- **Folder**: Represents a directory, with a `path` property.
- **File**: Represents a file, with a `path` property.
- **CONTAINS** relationship: 
  - Folder CONTAINS Folder (subfolder)
  - Folder CONTAINS File (file in folder)

### Containment Hierarchy

Allows traversal from parent folders to subfolders and files, supporting:

- Directory tree visualization
- Recursive operations (e.g., listing all files)
- Organizational/access control policies

### Example Queries

#### 1. List All Subfolders of a Folder

```cypher
MATCH (parent:Folder)-[:CONTAINS]->(child:Folder)
RETURN parent.path AS ParentFolder, child.path AS Subfolder
```

#### 2. List All Files in a Folder

```cypher
MATCH (folder:Folder)-[:CONTAINS]->(file:File)
RETURN folder.path AS Folder, file.path AS File
```

#### 3. Traverse the Full Containment Hierarchy

```cypher
MATCH (root:Folder {path: '/your/folder/path'})-[:CONTAINS*]->(file:File)
RETURN file.path
```

### Practical Usage

- **Navigation:** Build file explorers.
- **Batch Operations:** Copy, move, or delete folder trees.
- **Access Control:** Apply permissions based on containment.

### Summary

The containment model provides a clear, flexible way to represent and query the file system hierarchy. By leveraging `CONTAINS` relationships and `path` properties, developers can efficiently access, manage, and visualize the structure.

---

## Usage Examples

This section provides practical code snippets for key functions and methods.

---

### 1. Mocking Azure Blob Storage Clients for Testing

#### `mock_blob_client`

```python
from unittest.mock import AsyncMock

def mock_blob_client():
    mock = AsyncMock()
    mock.download_blob.return_value.readall.return_value = b"test content"
    return mock
```

#### `mock_container_client_fixture`

```python
from unittest.mock import MagicMock, AsyncMock

def mock_container_client_fixture():
    mock = MagicMock()
    mock.get_container_properties = AsyncMock(return_value={})

    class AsyncBlobIterator:
        def __aiter__(self):
            async def gen():
                blob_mock = MagicMock()
                blob_mock.name = "test_blob.txt"
                yield blob_mock
            return gen()

    def list_blobs(*args, **kwargs):
        return AsyncBlobIterator()
    mock.list_blobs = list_blobs

    def get_blob_client(name):
        blob_client_mock = AsyncMock()
        blob_client_mock.download_blob.return_value.readall.return_value = b"test content"
        blob_client_mock.download_blob.return_value = AsyncMock()
        blob_client_mock.download_blob.return_value.readall.return_value = b"test content"
        return blob_client_mock
    mock.get_blob_client.side_effect = get_blob_client

    return mock
```

#### Patching Blob Service Client

```python
def patch_blob_service_client(monkeypatch, mock_container_client_fixture):
    from source import container_services, blob_services
    monkeypatch.setattr(
        container_services, "blob_service_client",
        MagicMock(get_container_client=MagicMock(return_value=mock_container_client_fixture))
    )
    monkeypatch.setattr(
        blob_services, "blob_service_client",
        MagicMock(get_container_client=MagicMock(return_value=mock_container_client_fixture))
    )
```

---

### 2. Chunking Data

#### `chunk_rows`

```python
def chunk_rows(rows, chunk_size):
    for i in range(0, len(rows), chunk_size):
        yield rows[i:i + chunk_size]
```

**Usage:**

```python
rows = [1, 2, 3, 4, 5, 6, 7]
for chunk in chunk_rows(rows, 3):
    print(chunk)
# Output:
# [1, 2, 3]
# [4, 5, 6]
# [7]
```

---

### 3. Azure Retry Decorator

#### `azure_retry`

```python
import functools
from tenacity import AsyncRetrying, stop_after_attempt, wait_exponential, retry_if_exception_type
from azure.core.exceptions import AzureError

def azure_retry(function):
    @functools.wraps(function)
    async def wrapper(*args, **kwargs):
        async for attempt in AsyncRetrying(
            stop=stop_after_attempt(5),
            wait=wait_exponential(multiplier=1, min=2, max=10),
            retry=retry_if_exception_type(AzureError)
        ):
            with attempt:
                return await function(*args, **kwargs)
    return wrapper
```

**Usage:**

```python
@azure_retry
async def upload_blob(...):
    pass
```

---

### 4. Sanitizing Container Names

#### `sanitize_container_name`

```python
import re

def sanitize_container_name(name: str) -> str:
    name = re.sub(r'[^a-z0-9-]', '-', name.lower())
    name = re.sub(r'-{2,}', '-', name)
    name = name.strip('-')
    name = name[:63].strip('-')
    return name
```

**Usage:**

```python
container_name = sanitize_container_name("My_Repo/Name!")
print(container_name)  # Output: "my-repo-name"
```

---

### 5. Path Validation for Uploads

#### `is_path_allowed`

```python
import os

EXCLUDED_DIRS = {...}
ALLOWED_EXTENSIONS = {...}

def is_path_allowed(relative_path: str) -> bool:
    parts = relative_path.split("/")
    if any(part in EXCLUDED_DIRS for part in parts):
        return False
    _, ext = os.path.splitext(relative_path)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        return False
    return True
```

**Usage:**

```python
if is_path_allowed("src/main.py"):
    # Proceed with upload
    pass
```

---

### 6. Uploading a Repository to Azure Blob Storage

#### `upload_repository` (Method)

```python
def upload_repository(self, repo_path: str, max_workers: int = 8) -> Tuple[str, bool]:
    container_name = sanitize_container_name(os.path.basename(os.path.normpath(repo_path)))
    container_client, created = self.blob_manager.ensure_container_exists(container_name)
    files = []
    for root, _, filenames in os.walk(repo_path):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            relative_path = os.path.relpath(full_path, repo_path).replace("\\", "/")
            if not is_path_allowed(relative_path):
                continue
            files.append((full_path, relative_path))
    existing_blobs = self.blob_manager.get_blob_name_set(container_name)
    local_paths = {rel for _, rel in files}
    to_delete = existing_blobs - local_paths
    for blob_name in to_delete:
        container_client.delete_blob(blob_name)
    self._speed_up_upload(container_client, files, max_workers)
    return container_name, created
```

**Usage:**

```python
manager = RepositoryUploader(blob_manager)
container_name, created = manager.upload_repository("/path/to/local/repo")
print(f"Uploaded to container: {container_name}, Created: {created}")
```

---

### 7. Uploading a Single File

#### `upload_single_file` (Method)

```python
def upload_single_file(self, container_client, full_path: str, relative_path: str):
    blob_client = container_client.get_blob_client(relative_path)
    with open(full_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
```

---

### 8. Data Cleaning Utilities

#### Remove Extra Whitespace

```python
def __remove_extra_whitespace(self, text: str) -> str:
    # Removes multiple spaces, tabs, and excessive newlines
    ...
```

#### Remove Special Characters

```python
def __remove_special_characters(self, text: str) -> str:
    # Removes unnecessary special characters, keeping only basic punctuation and HTML tags
    ...
```

#### Normalize Punctuation

```python
def __normalize_punctuation(self, text: str) -> str:
    # Normalizes spacing around punctuation
    ...
```

#### Remove URLs

```python
def __remove_urls(self, text: str) -> str:
    # Removes http/https and www URLs from text
    ...
```

**Usage:**

```python
cleaned = self.__remove_extra_whitespace("Hello   world!\n\nThis is   a test.")
print(cleaned)  # Output: "Hello world!\nThis is a test."
```

---

### Summary

This section covered the most important usage patterns for the codebase, including mocking Azure services, chunking data, validating and sanitizing inputs, and uploading files to Azure Blob Storage. For further details on specific functions or methods, refer to the full API documentation or source code.

---

## Conclusion

The **Input Integration Pipeline** microservice codebase is organized for clarity, modularity, and scalability. Key insights include:

- **Separation of Concerns:** Clear distinction between endpoints, business logic, utilities, and tests.
- **Consistent Data Modeling:** All schemas use Pydantic models, centralized for easy maintenance.
- **Robust Utilities:** Utilities for chunking, retry logic, and input validation support reliable and scalable operations.
- **Testability:** Extensive use of mocking and fixtures enables thorough testing.
- **Navigable Structure:** The folder and file containment model, along with clear call graphs, makes the codebase approachable for new contributors.

By following the patterns and references in this document, developers can efficiently navigate, extend, and maintain the project. For further details, consult the in-code documentation and module-level README files.

---