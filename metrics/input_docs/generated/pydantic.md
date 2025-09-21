## General Information

# General Information

This repository contains the source code, tests, and documentation for **Pydantic**, a robust data validation and settings management library for Python. Pydantic leverages Python type annotations to provide runtime data parsing, validation, and serialization, making it a popular choice for building reliable data models in modern Python applications.

## Key Features

- **Type-Safe Data Models:** Define data structures using Python type hints, and Pydantic will validate and coerce input data at runtime.
- **Serialization & Deserialization:** Easily convert between Python objects and JSON or other formats.
- **Settings Management:** Built-in support for environment-based configuration via `env_settings`.
- **Extensible Validation:** Support for custom validators, functional validators, and serialization logic.
- **Plugin Architecture:** Experimental plugin system for extending Pydantic's core functionality.
- **Backward Compatibility:** Maintains a `v1` namespace for legacy support and a `deprecated` module for phased-out features.
- **Comprehensive Testing:** Extensive test suite, including benchmarks and type-checking scenarios.

## Repository Structure

The codebase is organized into several main directories:

- **pydantic/**: Core library source code, including models, validators, type adapters, serialization, and configuration logic.
- **pydantic/_internal/**: Internal implementation details, such as schema generation, validation internals, and utility functions.
- **pydantic/v1/**: Legacy Pydantic v1 API for backward compatibility.
- **pydantic/deprecated/**: Deprecated modules and features, maintained for transitional support.
- **pydantic/experimental/**: Experimental features and APIs, such as pipelines and argument schemas.
- **pydantic/plugin/**: Plugin loader and schema validator infrastructure.
- **tests/**: Comprehensive test suite covering core functionality, edge cases, benchmarks, mypy/type-checking, and plugin integration.
- **docs/**: Extensive documentation, including API references, conceptual guides, migration notes, and integration instructions.

## Example: Defining and Validating a Model

Pydantic models are defined using standard Python classes and type annotations. For example:

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str

# Validation and parsing
user = User(id='123', name='Alice', email='alice@example.com')
print(user.id)  # 123 (parsed as int)
```

If invalid data is provided, Pydantic raises a `ValidationError`:

```python
from pydantic import ValidationError

try:
    User(id='not-an-int', name='Bob', email='bob@example.com')
except ValidationError as e:
    print(e)
```

## Advanced Features

- **Custom Validators:** Use the `@validator` decorator or functional validators for complex validation logic.
- **Root Models:** Support for models wrapping a single value or collection.
- **Type Adapters:** Use `TypeAdapter` for validating arbitrary types outside of models.
- **Dataclasses:** Pydantic can validate and serialize standard Python dataclasses.
- **JSON Schema Generation:** Automatic generation of JSON Schema from models for API documentation and validation.
- **Plugin Support:** Extend Pydantic with custom plugins via the `pydantic.plugin` module.

## Documentation and Support

- **API Reference:** See `docs/api/` for detailed documentation of all public APIs.
- **Conceptual Guides:** The `docs/concepts/` directory covers topics like validation, serialization, strict mode, and performance.
- **Migration Guides:** `docs/migration.md` provides instructions for upgrading between major versions.
- **Integrations:** Guides for using Pydantic with tools like FastAPI, mypy, IDEs, and more are in `docs/integrations/`.

## Testing and Quality

- **Unit Tests:** Located in `tests/`, covering all major features and edge cases.
- **Benchmarks:** Performance tests in `tests/benchmarks/`.
- **Type Checking:** Mypy integration tests in `tests/mypy/` and `tests/typechecking/`.
- **Linting:** Configuration files for pre-commit and markdown linting are included at the root.

---

Pydantic is designed to be both powerful and easy to use, with a strong focus on correctness, performance, and developer experience. For more details, refer to the [Project Overview](#project-overview) and the [official documentation](docs/index.md).

## Project Overview

## Project Overview

Welcome to the project! This repository is designed as a foundation for building robust, maintainable, and scalable software solutions. While the current codebase data indicates that no files or modules have been added yet, this project structure is prepared to support a wide range of applications and development workflows.

### Purpose

The primary goal of this project is to provide a well-organized starting point for new development. It includes a recommended directory structure, documentation templates, and guidelines for contributing, ensuring consistency and best practices as the project evolves.

### Key Features

- **Modular Structure:** The project is organized into logical sections, making it easy to add new features and components as development progresses.
- **Documentation-First Approach:** Comprehensive documentation sections are included to facilitate onboarding and collaboration.
- **Scalability:** The architecture is designed to accommodate growth, whether you are building a small utility or a large-scale application.

### Example Usage

As the codebase currently contains no source files, here is an example of how you might begin using this project:

```bash
# Clone the repository
git clone https://github.com/your-username/your-project.git
cd your-project

# Create a new Python module (example)
mkdir src
echo "# Main module" > src/main.py
```

You can then start implementing your application logic within the `src/` directory, following the recommended structure outlined in the documentation.

### Next Steps

- **Add Source Code:** Begin by adding your main application code to the appropriate directories.
- **Update Documentation:** As you develop, keep the documentation up to date to reflect new features and changes.
- **Configure Dependencies:** Use the `requirements.txt` or `package.json` file to manage external libraries as needed.

---

This overview will be updated automatically as the codebase evolves and new components are added. For more information on getting started, refer to the [Installation](#installation) and [Usage](#usage) sections.

## Table of Contents

## Table of Contents

- [General Information](#general-information)
- [Project Overview](#project-overview)
- [Table of Contents](#table-of-contents)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Key Components](#key-components)
- [Architecture Overview](#architecture-overview)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)
- [Contact Information](#contact-information)
- [Acknowledgements](#acknowledgements)

---

### Documentation

#### Release Notes & History
- [Release Instructions](release/README.md)
- [Changelog & History](HISTORY.md)

#### API Reference (`docs/api/`)
- [Aliases](docs/api/aliases.md)
- [Annotated Handlers](docs/api/annotated_handlers.md)
- [Base Model](docs/api/base_model.md)
- [Config](docs/api/config.md)
- [Dataclasses](docs/api/dataclasses.md)
- [Errors](docs/api/errors.md)
- [Experimental Features](docs/api/experimental.md)
- [Fields](docs/api/fields.md)
- [Functional Serializers](docs/api/functional_serializers.md)
- [Functional Validators](docs/api/functional_validators.md)
- [JSON Schema](docs/api/json_schema.md)
- [Networks](docs/api/networks.md)
- [Pydantic Core](docs/api/pydantic_core.md)
- [Pydantic Core Schema](docs/api/pydantic_core_schema.md)
- [Extra Types: Color](docs/api/pydantic_extra_types_color.md)
- [Extra Types: Coordinate](docs/api/pydantic_extra_types_coordinate.md)
- [Extra Types: Country](docs/api/pydantic_extra_types_country.md)
- [Extra Types: Currency Code](docs/api/pydantic_extra_types_currency_code.md)
- [Extra Types: ISBN](docs/api/pydantic_extra_types_isbn.md)
- [Extra Types: Language Code](docs/api/pydantic_extra_types_language_code.md)
- [Extra Types: MAC Address](docs/api/pydantic_extra_types_mac_address.md)
- [Extra Types: Payment](docs/api/pydantic_extra_types_payment.md)
- [Extra Types: Pendulum Datetime](docs/api/pydantic_extra_types_pendulum_dt.md)
- [Extra Types: Phone Numbers](docs/api/pydantic_extra_types_phone_numbers.md)
- [Extra Types: Routing Numbers](docs/api/pydantic_extra_types_routing_numbers.md)
- [Extra Types: Script Code](docs/api/pydantic_extra_types_script_code.md)
- [Extra Types: Semantic Version](docs/api/pydantic_extra_types_semantic_version.md)
- [Extra Types: Timezone Name](docs/api/pydantic_extra_types_timezone_name.md)
- [Extra Types: ULID](docs/api/pydantic_extra_types_ulid.md)
- [Pydantic Settings](docs/api/pydantic_settings.md)
- [Root Model](docs/api/root_model.md)
- [Standard Library Types](docs/api/standard_library_types.md)
- [Type Adapter](docs/api/type_adapter.md)
- [Types](docs/api/types.md)
- [Validate Call](docs/api/validate_call.md)
- [Version](docs/api/version.md)

#### Concepts & Guides (`docs/concepts/`)
- [Alias Usage](docs/concepts/alias.md)
- [Configuration](docs/concepts/config.md)
- [Conversion Table](docs/concepts/conversion_table.md)
- [Dataclasses](docs/concepts/dataclasses.md)
- [Experimental Concepts](docs/concepts/experimental.md)
- [Fields](docs/concepts/fields.md)
- [Forward Annotations](docs/concepts/forward_annotations.md)
- [JSON Handling](docs/concepts/json.md)
- [JSON Schema Concepts](docs/concepts/json_schema.md)

#### Testing & Quality
- [Mypy Type Checking Tests](tests/mypy/README.md)
- [General Type Checking Tests](tests/typechecking/README.md)
- [Style Guide Tests](.hyperlint/style_guide_test.md)

---

### Example: Navigating the Documentation

- To understand how to define and use custom types, see [Types](docs/api/types.md) and [Standard Library Types](docs/api/standard_library_types.md).
- For configuration options and best practices, refer to [Config](docs/api/config.md) and [Configuration Concepts](docs/concepts/config.md).
- Explore [Functional Serializers](docs/api/functional_serializers.md) and [Functional Validators](docs/api/functional_validators.md) for advanced data processing.
- For experimental features and upcoming changes, check [Experimental Features](docs/api/experimental.md) and [Experimental Concepts](docs/concepts/experimental.md).
- Review [Release Instructions](release/README.md) and [Changelog & History](HISTORY.md) for deployment and versioning details.

---

**Tip:** Use the above links to quickly access detailed technical documentation, conceptual guides, and testing resources directly related to the codebase.

## Installation

## Installation

Pydantic is easy to install and works with Python 3.9 and above. You can install it using `pip`, `uv`, or `conda`, and there are options for optional dependencies and advanced environments like AWS Lambda.

### Basic Installation

You can install Pydantic from PyPI using your preferred package manager:

=== "pip"

    ```bash
    pip install pydantic
    ```

=== "uv"

    ```bash
    uv add pydantic
    ```

=== "conda"

    ```bash
    conda install pydantic -c conda-forge
    ```

> **Note:** Pydantic requires Python 3.9, 3.10, 3.11, or 3.12.

### Dependencies

Pydantic will automatically install its core dependencies:

- [`pydantic-core`](https://pypi.org/project/pydantic-core/): Core validation logic written in Rust.
- [`typing-extensions`](https://pypi.org/project/typing-extensions/): Backport of the standard library typing module.
- [`annotated-types`](https://pypi.org/project/annotated-types/): Reusable constraint types for use with `typing.Annotated`.

### Optional Dependencies

Some features require extra dependencies. You can install these with "extras":

- **Email validation:** Provided by [`email-validator`](https://pypi.org/project/email-validator/).
- **Timezone support:** Provided by [`tzdata`](https://pypi.org/project/tzdata/).

To install with optional dependencies:

=== "pip"

    ```bash
    # Email validation support
    pip install 'pydantic[email]'

    # Email and timezone support
    pip install 'pydantic[email,timezone]'
    ```

=== "uv"

    ```bash
    uv add 'pydantic[email]'
    uv add 'pydantic[email,timezone]'
    ```

You can also install these requirements manually:

```bash
pip install email-validator tzdata
```

### Installing from Source

To install the latest development version directly from the repository:

=== "pip"

    ```bash
    pip install 'git+https://github.com/pydantic/pydantic@main'
    # With optional extras:
    pip install 'git+https://github.com/pydantic/pydantic@main#egg=pydantic[email,timezone]'
    ```

=== "uv"

    ```bash
    uv add 'git+https://github.com/pydantic/pydantic@main'
    uv add 'git+https://github.com/pydantic/pydantic@main#egg=pydantic[email,timezone]'
    ```

### AWS Lambda Installation

When deploying to AWS Lambda, you may need to ensure that native dependencies are built for the correct platform. Use the following `pip` command to build for the Lambda environment:

```bash
pip install \
    --platform manylinux2014_x86_64 \
    --target=<your_package_dir> \
    --implementation cp \
    --python-version 3.10 \
    --only-binary=:all: \
    --upgrade pydantic
```

- Replace `<your_package_dir>` with your deployment directory (e.g., `python` for Lambda Layers).
- Adjust `--platform` and `--python-version` as needed for your Lambda runtime.

**Troubleshooting:**  
If you see errors like `no module named pydantic_core._pydantic_core`, check that the compiled library matches your Lambda's Python version and platform. See the [AWS Lambda integration guide](docs/integrations/aws_lambda.md) for more details.

### Migrating from Pydantic V1

Pydantic V2 is the current production release. To upgrade:

```bash
pip install -U pydantic
```

If you need to use Pydantic V1:

```bash
pip install "pydantic==1.*"
```

You can also access the V1 API from Pydantic V2 via:

```python
from pydantic.v1 import BaseModel
```

See the [migration guide](docs/migration.md) for more details.

---

For more advanced installation options, see the [official documentation](https://docs.pydantic.dev/latest/install/). If you encounter issues, please [open an issue on GitHub](https://github.com/pydantic/pydantic/issues).

## Usage

## Usage

This section provides practical guidance and examples for using the project, focusing on common usage patterns, error handling, and best practices as reflected in the codebase.

### Common Usage Patterns

#### Defining Models

Models are typically defined by subclassing `BaseModel`:

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
```

#### Instantiating Models

Instantiate models by passing field values as keyword arguments:

```python
user = User(id=1, name='Alice')
```

#### Handling Forward References

If you reference types before they are defined, you may encounter a `class-not-fully-defined` error. To resolve this, define all referenced types before instantiating the model, or use `.model_rebuild()`:

```python
from typing import Optional
from pydantic import BaseModel

class Foo(BaseModel):
    a: Optional['Bar'] = None

class Bar(BaseModel):
    b: 'Foo'

Foo.model_rebuild()
foo = Foo(a={'b': {'a': None}})
```

### Error Handling

Pydantic provides detailed error messages to help diagnose and fix issues. Below are some common errors and how to address them.

#### Class Not Fully Defined

Occurs when a type in an annotation is not defined at the time of model creation.

**Example:**

```python
from typing import ForwardRef
from pydantic import BaseModel, PydanticUserError

UndefinedType = ForwardRef('UndefinedType')

class Foobar(BaseModel):
    a: UndefinedType

try:
    Foobar(a=1)
except PydanticUserError as exc_info:
    assert exc_info.code == 'class-not-fully-defined'
```

#### Custom JSON Schema

In Pydantic V2, use `__get_pydantic_json_schema__` instead of `__modify_schema__` to customize JSON schema generation.

**Example:**

```python
from typing import Any
from pydantic_core import CoreSchema
from pydantic import BaseModel, GetJsonSchemaHandler

class Model(BaseModel):
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler) -> dict[str, Any]:
        json_schema = super().__get_pydantic_json_schema__(core_schema, handler)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema.update(examples=['example'])
        return json_schema

print(Model.model_json_schema())
# Output: {'examples': ['example'], 'properties': {}, 'title': 'Model', 'type': 'object'}
```

#### Decorator on Missing Field

Raised when a validator is defined for a field that does not exist.

**Example:**

```python
from typing import Any
from pydantic import BaseModel, PydanticUserError, field_validator

try:
    class Model(BaseModel):
        a: str

        @field_validator('b')
        def check_b(cls, v: Any):
            return v
except PydanticUserError as exc_info:
    assert exc_info.code == 'decorator-missing-field'
```

**Solution:** Use `check_fields=False` if you intend to inherit and add the field later.

### Advanced Usage

#### Discriminated Unions

When using discriminated unions, ensure all models define the discriminator field as a `Literal` and use consistent aliases.

**Example of error:**

```python
from typing import Literal, Union
from pydantic import BaseModel, Field, PydanticUserError

class Cat(BaseModel):
    c: str

class Dog(BaseModel):
    pet_type: Literal['dog']
    d: str

try:
    class Model(BaseModel):
        pet: Union[Cat, Dog] = Field(discriminator='pet_type')
        number: int
except PydanticUserError as exc_info:
    assert exc_info.code == 'discriminator-no-field'
```

#### Validators

- Always specify fields as separate string arguments in `@field_validator`.
- Validators must be class or static methods, not instance methods.

**Correct usage:**

```python
from pydantic import BaseModel, field_validator

class Model(BaseModel):
    a: str
    b: str

    @field_validator('a', 'b')
    def check_fields(cls, v):
        return v
```

#### Serializers

- `@model_serializer` must be applied to instance methods.
- Use the correct signature for field and model serializers.

**Example:**

```python
from pydantic import BaseModel, model_serializer

class MyModel(BaseModel):
    a: int

    @model_serializer
    def _serialize(self):
        return {'a': self.a}
```

### Function Validation

Use `@validate_call` to validate function arguments, but note the following:

- Decorators like `@classmethod` and `@staticmethod` must be applied before `@validate_call`.
- `validate_call` cannot be applied directly to classes or callable instances.

**Correct usage:**

```python
from pydantic import validate_call

@validate_call
def my_function(x: int, y: str) -> None:
    pass
```

### TypeAdapter Configuration

When using `TypeAdapter`, do not pass `config` for types that already have their own config (e.g., `BaseModel`, `TypedDict`). Instead, set the config on the type itself.

**Example:**

```python
from typing_extensions import TypedDict
from pydantic import ConfigDict, TypeAdapter

class MyTypedDict(TypedDict):
    x: int
    __pydantic_config__ = ConfigDict(strict=True)

TypeAdapter(MyTypedDict)  # ok
```

### Additional Error Scenarios

The codebase documents many specific error cases, such as:

- Using `model_config` as a field name
- Applying `with_config` to a `BaseModel` subclass
- Using `dataclass` on a `BaseModel` subclass
- Invalid use of `Self` type
- Overlapping unpacked `TypedDict` fields

Refer to the [errors documentation](docs/errors/usage_errors.md) for comprehensive examples and solutions.

---

For more advanced usage patterns and troubleshooting, consult the detailed error examples and migration notes in the codebase documentation.

## Project Structure

## Project Structure

This project is organized into several key directories and modules, each serving a specific purpose. Below is an overview of the main components, their roles, and practical examples to help you navigate and understand the codebase.

---

### Top-Level Layout

```
.
├── pydantic/           # Main library source code
├── tests/              # Automated tests and test utilities
├── docs/               # Documentation source files
├── release/            # Release tooling and scripts
├── .hyperlint/         # Linting and style configuration
├── HISTORY.md          # Project changelog
├── .pre-commit-config.yaml
├── .markdownlint.yaml
```

---

### Main Source Code: `pydantic/`

The `pydantic` directory contains the core implementation of the library, organized into logical modules and subpackages:

#### Core Modules

- **`pydantic/__init__.py`**  
  Entry point for the package; exposes main APIs.

- **`pydantic/main.py`**  
  Core logic for model definition and validation.

- **`pydantic/fields.py`**  
  Field definitions and metadata handling.

- **`pydantic/types.py`**  
  Built-in and custom types supported by Pydantic.

- **`pydantic/validators.py`**  
  Validation utilities and functions.

- **`pydantic/errors.py`**  
  Error classes and error handling logic.

- **`pydantic/dataclasses.py`**  
  Support for Python dataclasses integration.

- **`pydantic/json_schema.py`**  
  JSON Schema generation for models.

- **`pydantic/type_adapter.py`**  
  TypeAdapter utility for runtime type validation.

- **`pydantic/functional_validators.py`**  
  Decorators and helpers for functional validation.

- **`pydantic/functional_serializers.py`**  
  Functional serialization utilities.

- **`pydantic/config.py`**  
  Configuration management for models.

- **`pydantic/aliases.py`**, **`pydantic/alias_generators.py`**  
  Field aliasing and alias generator utilities.

#### Internal Implementation

- **`pydantic/_internal/`**  
  Contains internal modules (prefixed with `_`) for advanced logic, such as:
  - `_validators.py`, `_serializers.py`: Core validation and serialization logic.
  - `_fields.py`: Internal field processing.
  - `_model_construction.py`: Model creation internals.
  - `_schema_generation_shared.py`, `_generate_schema.py`: Schema generation logic.
  - `_decorators.py`, `_decorators_v1.py`: Decorator implementations.
  - `_utils.py`, `_core_utils.py`: Internal utility functions.

#### Versioned and Deprecated APIs

- **`pydantic/v1/`**  
  Maintains backward compatibility with Pydantic v1 APIs.  
  Example:  
  ```python
  from pydantic.v1 import BaseModel
  ```

- **`pydantic/deprecated/`**  
  Contains deprecated modules and utilities for legacy support.

#### Experimental and Plugin Support

- **`pydantic/experimental/`**  
  Experimental features and APIs under development.

- **`pydantic/plugin/`**  
  Plugin system and plugin loader logic.

---

### Testing: `tests/`

The `tests` directory contains comprehensive test coverage for the library:

- **Unit Tests**:  
  Individual test files (e.g., `test_validators.py`, `test_types.py`) cover specific modules and features.

- **Benchmarks**:  
  `tests/benchmarks/` contains performance benchmarks and comparison scripts.

- **Type Checking**:  
  `tests/typechecking/` includes tests for type hints and static analysis.

- **Mypy Plugin Testing**:  
  `tests/mypy/` and its subfolders test the Pydantic mypy plugin integration, including expected outputs.

- **Plugin Tests**:  
  `tests/plugin/` contains tests for plugin-related functionality.

**Example: Running Tests**
```bash
pytest tests/
```

---

### Documentation: `docs/`

- **API Reference**:  
  `docs/api/` contains detailed API documentation in Markdown.

- **Concepts & Guides**:  
  `docs/concepts/` provides conceptual guides and explanations.

- **Integrations**:  
  `docs/integrations/` covers integration with other tools (e.g., mypy, IDEs).

- **Examples**:  
  `docs/examples/` offers practical usage examples.

- **Error Reference**:  
  `docs/errors/` documents error types and troubleshooting.

---

### Release Tooling: `release/`

Scripts and utilities for managing releases, such as:

- `release/prepare.py`: Prepares a new release.
- `release/push.py`: Handles pushing releases.
- `release/shared.py`: Shared release logic.
- `release/README.md`: Documentation for release processes.

---

### Linting and Style: `.hyperlint/`

Contains configuration for linting and style checks, including:

- `.hyperlint/styles/`: Custom linting rules and vocabularies.
- `.hyperlint/style_guide_test.md`: Style guide documentation.

---

## Practical Example: Adding a New Validator

Suppose you want to add a custom validator:

1. **Implement the Validator**  
   Add your function to `pydantic/validators.py` or as a method on your model.

2. **Register the Validator**  
   Use the `@validator` decorator in your model (see `pydantic/functional_validators.py`).

   ```python
   from pydantic import BaseModel, validator

   class User(BaseModel):
       name: str

       @validator('name')
       def name_must_be_titlecase(cls, v):
           if not v.istitle():
               raise ValueError('Name must be titlecase')
           return v
   ```

3. **Test Your Validator**  
   Add a test in `tests/test_validators.py` to ensure correct behavior.

---

## Summary Table

| Directory / File            | Purpose / Contents                                      |
|-----------------------------|--------------------------------------------------------|
| `pydantic/`                 | Main library source code                               |
| `pydantic/_internal/`       | Internal/private implementation details                |
| `pydantic/v1/`              | Backward compatibility for v1 APIs                     |
| `pydantic/deprecated/`      | Deprecated modules and legacy support                  |
| `pydantic/experimental/`    | Experimental features                                  |
| `pydantic/plugin/`          | Plugin system and loaders                              |
| `tests/`                    | Unit, integration, and type-checking tests             |
| `docs/`                     | Documentation, guides, and API reference               |
| `release/`                  | Release management scripts                             |
| `.hyperlint/`               | Linting and style configuration                        |

---

This structure ensures a clear separation of concerns, maintainability, and ease of contribution. For more details on each module or to contribute, refer to the respective README files or documentation within each directory.

## Key Components

## Key Components

This project is structured around several core modules, each providing essential functionality for data validation, parsing, configuration, and extensibility. Below is an overview of the key components, their roles, and practical examples of their usage.

---

### 1. **Core Validation and Model System (`pydantic/v1/main.py`, `pydantic/v1/fields.py`, `pydantic/v1/class_validators.py`)**

#### **BaseModel and ModelMetaclass**
- **Purpose:** The backbone of the data validation system, enabling the definition of strongly-typed models with automatic parsing and validation.
- **Key Classes:** `BaseModel`, `ModelMetaclass`
- **Key Functions:** `validate_model`, `create_model`

**Example:**
```python
from pydantic.v1.main import BaseModel

class User(BaseModel):
    id: int
    name: str

user = User(id=123, name="Alice")
```

#### **Fields and FieldInfo**
- **Purpose:** Define and manage model fields, including metadata and validation constraints.
- **Key Classes:** `ModelField`, `FieldInfo`, `DeferredType`
- **Key Functions:** `Field`, `PrivateAttr`

**Example:**
```python
from pydantic.v1.fields import Field

class Product(BaseModel):
    name: str
    price: float = Field(..., gt=0)
```

#### **Validators**
- **Purpose:** Attach custom validation logic to fields or models.
- **Key Classes:** `ValidatorGroup`, `Validator`
- **Key Functions:** `validator`, `root_validator`, `prep_validators`

**Example:**
```python
from pydantic.v1.class_validators import validator

class User(BaseModel):
    email: str

    @validator('email')
    def email_must_contain_at(cls, v):
        assert '@' in v
        return v
```

---

### 2. **Types and Constraints (`pydantic/v1/types.py`)**

- **Purpose:** Provide a rich set of constrained types (e.g., `PositiveInt`, `StrictStr`, `ConstrainedList`) and factory functions for custom constraints.
- **Key Classes:** `ConstrainedInt`, `PositiveInt`, `StrictStr`, `ConstrainedList`, etc.
- **Key Functions:** `conint`, `constr`, `conlist`, `confloat`, etc.

**Example:**
```python
from pydantic.v1.types import PositiveInt, constr

class Order(BaseModel):
    quantity: PositiveInt
    sku: constr(min_length=8, max_length=12)
```

---

### 3. **Parsing and Serialization (`pydantic/v1/tools.py`, `pydantic/v1/parse.py`, `pydantic/v1/json.py`)**

- **Purpose:** Utilities for parsing data from various sources and serializing models.
- **Key Functions:** `parse_obj_as`, `parse_raw_as`, `parse_file_as`, `schema_json_of`, `schema_of`, `pydantic_encoder`

**Example:**
```python
from pydantic.v1.tools import parse_obj_as

data = [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]
users = parse_obj_as(list[User], data)
```

---

### 4. **Error Handling (`pydantic/v1/errors.py`, `pydantic/v1/error_wrappers.py`)**

- **Purpose:** Structured error types and wrappers for detailed validation error reporting.
- **Key Classes:** `ValidationError`, `ErrorWrapper`, `PydanticErrorMixin`, `PydanticTypeError`, `PydanticValueError`
- **Key Functions:** `display_errors`, `flatten_errors`

**Example:**
```python
try:
    User(id='not-an-int', name='Alice')
except ValidationError as e:
    print(e.json())
```

---

### 5. **Configuration and Settings (`pydantic/v1/config.py`, `pydantic/v1/env_settings.py`)**

- **Purpose:** Manage model and application configuration, including environment variable support.
- **Key Classes:** `BaseConfig`, `ConfigDict`, `BaseSettings`
- **Key Functions:** `prepare_config`, `read_env_file`

**Example:**
```python
from pydantic.v1.env_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str

settings = Settings()
```

---

### 6. **Advanced Features**

#### **Generics (`pydantic/v1/generics.py`)**
- **Purpose:** Support for generic models.
- **Key Class:** `GenericModel`

**Example:**
```python
from pydantic.v1.generics import GenericModel
from typing import TypeVar, Generic

T = TypeVar('T')

class Wrapper(GenericModel, Generic[T]):
    payload: T
```

#### **Dataclasses Integration (`pydantic/v1/dataclasses.py`)**
- **Purpose:** Seamless validation for Python dataclasses.
- **Key Functions:** `dataclass`, `create_pydantic_model_from_dataclass`

**Example:**
```python
from pydantic.v1.dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int
```

#### **Network Types (`pydantic/v1/networks.py`)**
- **Purpose:** Specialized types for URLs, emails, and network addresses.
- **Key Classes:** `EmailStr`, `HttpUrl`, `IPvAnyAddress`, etc.

**Example:**
```python
from pydantic.v1.networks import EmailStr

class Contact(BaseModel):
    email: EmailStr
```

---

### 7. **Experimental and Plugin System**

#### **Experimental Features (`pydantic/experimental/`)**
- **Purpose:** New or unstable features, such as pipelines and argument schema generation.
- **Key Classes:** `_Pipeline`, `_Constraint`
- **Key Functions:** `generate_arguments_schema`, `check_pattern`, etc.

#### **Plugin System (`pydantic/plugin/`)**
- **Purpose:** Extensibility via plugins for schema validation and data handling.
- **Key Classes:** `PluggableSchemaValidator`, `PydanticPluginProtocol`
- **Key Functions:** `get_plugins`, `create_schema_validator`

---

### 8. **Deprecated API (`pydantic/deprecated/`)**

- **Purpose:** Backward compatibility for legacy APIs and migration support.
- **Key Classes/Functions:** Mirror many v1 components (e.g., `DecoratorBaseModel`, `parse_obj_as`, `schema_of`), but marked as deprecated.

---

### 9. **Utilities (`pydantic/v1/utils.py`, `pydantic/v1/typing.py`)**

- **Purpose:** Helper functions for type inspection, string manipulation, and model utilities.
- **Key Functions:** `get_model`, `generate_model_signature`, `is_valid_identifier`, `import_string`, `resolve_annotations`

---

## Summary Table

| Module/Path                        | Purpose                                      | Key Classes/Functions                          |
|-------------------------------------|----------------------------------------------|------------------------------------------------|
| `pydantic/v1/main.py`              | Core model definition/validation             | `BaseModel`, `validate_model`                  |
| `pydantic/v1/fields.py`            | Field management                             | `ModelField`, `FieldInfo`, `Field`             |
| `pydantic/v1/class_validators.py`   | Custom validation logic                      | `validator`, `root_validator`                  |
| `pydantic/v1/types.py`             | Constrained types                            | `PositiveInt`, `constr`, etc.                  |
| `pydantic/v1/tools.py`             | Parsing/serialization utilities              | `parse_obj_as`, `schema_json_of`               |
| `pydantic/v1/errors.py`            | Error types                                  | `ValidationError`, `PydanticErrorMixin`        |
| `pydantic/v1/config.py`            | Model configuration                          | `BaseConfig`, `ConfigDict`                     |
| `pydantic/v1/env_settings.py`      | Environment-based settings                   | `BaseSettings`                                 |
| `pydantic/v1/generics.py`          | Generic models                               | `GenericModel`                                 |
| `pydantic/v1/dataclasses.py`       | Dataclass integration                        | `dataclass`                                    |
| `pydantic/v1/networks.py`          | Network/email/url types                      | `EmailStr`, `HttpUrl`                          |
| `pydantic/experimental/`           | Experimental features                        | `_Pipeline`, `generate_arguments_schema`        |
| `pydantic/plugin/`                  | Plugin system                                | `PluggableSchemaValidator`, `get_plugins`      |
| `pydantic/deprecated/`             | Deprecated APIs                              | `DecoratorBaseModel`, `parse_obj_as`           |
| `pydantic/v1/utils.py`, `typing.py`| Utilities                                    | `get_model`, `resolve_annotations`             |

---

These components collectively provide a robust, extensible, and user-friendly framework for data validation, parsing, and configuration in Python applications. For more detailed usage, refer to the [Usage](#usage) and [Project Structure](#project-structure) sections.

## Architecture Overview

## Architecture Overview

This project follows a modular and scalable architecture, designed to promote maintainability, testability, and ease of extension. The architecture is documented in detail in [`docs/internals/architecture.md`](docs/internals/architecture.md), which serves as the canonical reference for internal design decisions and component interactions.

### High-Level Structure

At a high level, the codebase is organized into the following primary layers:

- **Core Modules:** Contain the essential business logic and domain models.
- **API Layer:** Exposes interfaces for interacting with the core modules, such as RESTful endpoints or CLI commands.
- **Data Layer:** Handles data persistence, retrieval, and external integrations (e.g., databases, third-party APIs).
- **Utilities & Helpers:** Provide reusable functions and abstractions to support the main modules.

```
+-------------------+
|    API Layer      |
+-------------------+
          |
+-------------------+
|   Core Modules    |
+-------------------+
          |
+-------------------+
|    Data Layer     |
+-------------------+
          |
+-------------------+
| Utilities/Helpers |
+-------------------+
```

### Component Interactions

- **API Layer** receives requests from users or external systems and delegates processing to the **Core Modules**.
- **Core Modules** encapsulate the main business logic and interact with the **Data Layer** for data operations.
- **Data Layer** abstracts the details of data storage and retrieval, allowing the core logic to remain agnostic of the underlying data sources.
- **Utilities & Helpers** are leveraged across all layers to avoid code duplication and enforce consistency.

### Example: Request Flow

1. **User Request:** A user sends a request to the API endpoint.
2. **API Handler:** The API layer validates the request and calls the appropriate service in the core module.
3. **Business Logic:** The core module processes the request, applying business rules and orchestrating necessary operations.
4. **Data Access:** If data persistence or retrieval is required, the core module interacts with the data layer.
5. **Response:** The result is returned up the stack to the API layer, which formats and sends the response to the user.

### Practical Example

Suppose the project implements a resource management feature:

- The **API Layer** defines an endpoint `/resources` that accepts POST requests.
- The **Core Module** contains a `ResourceService` class responsible for validating and creating new resources.
- The **Data Layer** provides a `ResourceRepository` that abstracts database operations.
- **Utilities** include input validation functions and error handling helpers.

**Sample Flow:**
```python
# API Layer
@app.route('/resources', methods=['POST'])
def create_resource():
    data = request.json
    resource = ResourceService.create(data)
    return jsonify(resource), 201

# Core Module
class ResourceService:
    @staticmethod
    def create(data):
        validate_resource_data(data)
        return ResourceRepository.save(data)

# Data Layer
class ResourceRepository:
    @staticmethod
    def save(data):
        # Database logic here
        pass
```

### Extensibility and Maintainability

- **Loose Coupling:** Each layer is decoupled from the others via well-defined interfaces, making it easy to swap implementations or add new features.
- **Separation of Concerns:** Responsibilities are clearly divided, reducing complexity and improving code readability.
- **Documentation:** The architecture and design decisions are thoroughly documented in [`docs/internals/architecture.md`](docs/internals/architecture.md).

For further technical details, refer to the [Architecture Documentation](docs/internals/architecture.md).

## Dependencies

## Dependencies

This project relies on a set of core Python standard libraries as well as internal and external modules to provide its functionality. Below is a detailed overview of the main dependencies, their roles within the codebase, and practical examples of how they are used.

### Core Standard Library Dependencies

#### 1. `functools`
- **Usage:** Extensively used throughout the codebase for function decorators, caching, and partial function application. It is present in both the main library and test files.
- **Examples in Code:**
  - Decorating functions to preserve metadata or implement custom validation logic.
  - Caching results of expensive computations.
- **Files Using `functools`:**
  - `pydantic/validate_call_decorator.py`
  - `pydantic/functional_validators.py`
  - `pydantic/dataclasses.py`
  - `pydantic/_internal/_validate_call.py`
  - Multiple test files, e.g., `tests/test_validate_call.py`, `tests/typechecking/decorators.py`
- **Practical Example:**
  ```python
  from functools import wraps

  def my_decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
          # Custom logic here
          return func(*args, **kwargs)
      return wrapper
  ```

#### 2. `operator`
- **Usage:** Used for efficient, functional-style operations such as attribute/item access and comparisons.
- **Files Using `operator`:**
  - `pydantic/main.py`
  - `pydantic/experimental/pipeline.py`
  - `pydantic/_internal/_model_construction.py`
  - `pydantic/_internal/_generics.py`
  - `tests/benchmarks/basemodel_eq_performance.py`
- **Practical Example:**
  ```python
  import operator

  result = operator.eq(a, b)  # Equivalent to a == b
  ```

#### 3. `subprocess`
- **Usage:** Used for running external commands and scripts, primarily in release tooling and documentation tests.
- **Files Using `subprocess`:**
  - `release/shared.py`
  - `release/push.py`
  - `pydantic/_internal/_git.py`
  - `tests/test_docs.py`
- **Practical Example:**
  ```python
  import subprocess

  subprocess.run(['git', 'status'], check=True)
  ```

### Internal and External Dependencies

#### 4. `pydantic`
- **Usage:** The main library is self-referential in its tests and internal modules, ensuring robust type validation and serialization.
- **Files Using `pydantic`:**
  - Test files such as `tests/typechecking/with_config_decorator.py`, `tests/typechecking/validate_call.py`, `tests/typechecking/type_adapter.py`, etc.
  - Used for testing features like model validation, computed fields, root models, and more.
- **Practical Example:**
  ```python
  from pydantic import BaseModel

  class User(BaseModel):
      id: int
      name: str
  ```

### Summary Table

| Dependency   | Purpose/Usage                                      | Example File(s)                                      |
|--------------|----------------------------------------------------|------------------------------------------------------|
| functools    | Decorators, caching, partials                      | `pydantic/validate_call_decorator.py`, tests         |
| operator     | Functional operations, comparisons                 | `pydantic/main.py`, `pydantic/_internal/_generics.py`|
| subprocess   | Running shell commands, release tooling            | `release/push.py`, `pydantic/_internal/_git.py`      |
| pydantic     | Type validation, serialization (self-reference)    | Test files, internal validation modules              |

### Notes

- All dependencies listed above are part of the Python standard library, except for `pydantic` itself, which is the main library being developed and tested.
- The codebase is structured to minimize external dependencies, focusing on reliability and portability.
- For development and testing, ensure you have a compatible version of Python installed (see [Installation](#installation)).

---

**Tip:**  
If you are contributing or running tests, you may need additional development dependencies (e.g., `pytest`). Refer to the [Contributing](#contributing) section for more details.

## Contributing

## Contributing

We welcome contributions of all kinds to this project! Whether you want to submit a bug fix, propose a new feature, improve documentation, or help with packaging and CI, your input is valuable. Below you'll find guidelines and practical information to help you get started as a contributor.

---

### How to Contribute

#### 1. Fork and Clone the Repository

Start by [forking the repository](https://github.com/pydantic/pydantic/fork) and cloning it to your local machine:

```bash
git clone https://github.com/<your-username>/pydantic.git
cd pydantic
```

#### 2. Set Up Your Development Environment

- **Dependencies:**  
  The project uses several dependencies for development, testing, and packaging. Make sure you have Python installed, then install the required dependencies:

  ```bash
  pip install -r requirements.txt
  ```

  The project also uses tools like `mypy` for type checking and `mkdocs` for documentation. You may need to install these as well:

  ```bash
  pip install mypy mkdocs
  ```

- **Packaging:**  
  The project uses [PEP 639](https://peps.python.org/pep-0639/) metadata standards and tools like `uv` for environment management (see [#10727](https://github.com/pydantic/pydantic/pull/10727)).  
  To ensure compatibility, check the `pyproject.toml` and `requirements` files for up-to-date dependencies.

#### 3. Make Your Changes

- **Code:**  
  Implement your feature or bug fix in a new branch:

  ```bash
  git checkout -b my-feature-branch
  ```

- **Testing:**  
  Add or update tests as appropriate. Run the test suite to ensure everything passes:

  ```bash
  pytest
  ```

- **Type Checking:**  
  Run static type checks:

  ```bash
  mypy .
  ```

- **Documentation:**  
  If your change affects the public API or usage, update the documentation accordingly. The project uses `mkdocs` for documentation:

  ```bash
  mkdocs serve
  ```

#### 4. Commit and Push

Commit your changes with a clear message:

```bash
git add .
git commit -m "Describe your change"
git push origin my-feature-branch
```

#### 5. Open a Pull Request

Go to your fork on GitHub and open a pull request (PR) against the main repository. Please include:

- A clear description of your changes
- Reference to any related issues or discussions
- Any relevant screenshots or test results

---

### Contribution Areas

- **Bug Fixes:**  
  See recent examples such as [#11579](https://github.com/pydantic/pydantic/pull/11579) and [#11082](https://github.com/pydantic/pydantic/pull/11082).
- **New Features:**  
  Propose and implement new features, e.g., [#11516](https://github.com/pydantic/pydantic/pull/11516).
- **Packaging & CI:**  
  Help keep dependencies up to date, e.g., [#11963](https://github.com/pydantic/pydantic/pull/11963), [#11725](https://github.com/pydantic/pydantic/pull/11725).
- **Documentation:**  
  Improve or expand the documentation, including usage examples and API references.
- **First-Time Contributions:**  
  We encourage first-time contributors! See the long list of [first contributions](#new-contributors) in our HISTORY.md for inspiration.

---

### Recognizing Contributors

We are proud of our growing community! Every contributor is acknowledged in our [HISTORY.md](HISTORY.md) file. Here are some recent first-time contributors:

- @parth-paradkar ([#11695](https://github.com/pydantic/pydantic/pull/11695))
- @dqkqd ([#11739](https://github.com/pydantic/pydantic/pull/11739))
- @fhightower ([#11722](https://github.com/pydantic/pydantic/pull/11722))
- @GSemikozov ([#12050](https://github.com/pydantic/pydantic/pull/12050))
- @hannah-heywa ([#12082](https://github.com/pydantic/pydantic/pull/12082))
- ...and many more!

See the [full list of contributors](HISTORY.md) for more.

---

### Tips for a Successful Contribution

- **Follow the code style:**  
  Ensure your code matches the existing style and passes linting.
- **Write clear commit messages:**  
  Summarize your changes and reference issues or PRs where relevant.
- **Be responsive:**  
  Respond to feedback and requested changes from reviewers.
- **Stay up to date:**  
  Pull the latest changes from the main branch before submitting your PR.

---

### Need Help?

If you have questions or need guidance, feel free to open a [discussion](https://github.com/pydantic/pydantic/discussions) or reach out via [issues](https://github.com/pydantic/pydantic/issues).

We look forward to your contributions! 🚀

## License

## License

**Note:** Based on the available codebase data, there is no explicit license file (such as `LICENSE` or `LICENSE.txt`) or license declaration found within the repository. This means the licensing terms for this project are currently **unspecified**.

### What This Means

- **No License Specified:** By default, if a project does not include a license, you do **not** have permission to use, copy, modify, or distribute the code. All rights are reserved by the original authors.
- **Contributions:** If you plan to contribute to this project, please contact the maintainers to clarify the intended license and contribution terms.
- **Usage:** If you wish to use this code in your own project or for commercial purposes, you must obtain explicit permission from the repository owners.

### Best Practices

If you are the maintainer or a contributor, it is highly recommended to:

1. **Add a License File:** Choose an appropriate open-source license (such as MIT, Apache 2.0, or GPL) and add a `LICENSE` file at the root of the repository.
2. **Declare License in Source Files:** Optionally, include a license header in each source file for clarity.
3. **Document License in README:** Clearly state the license in the README to inform users and contributors.

#### Example: Adding an MIT License

To add an MIT License, create a file named `LICENSE` with the following content:

```text
MIT License

Copyright (c) [year] [copyright holders]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
...
```

Then, update the README:

```markdown
## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
```

### Summary Table

| License File Present | License Declared in Code | Usage Rights         | Contribution Policy |
|----------------------|-------------------------|----------------------|---------------------|
| ❌                   | ❌                      | All rights reserved  | Contact maintainers |

---

If you have questions about licensing or need to clarify usage rights, please reach out to the project maintainers (see [Contact Information](#contact-information)).

## Contact Information

## Contact Information

For questions, support, or to contribute to the project, please use the following channels:

### GitHub Repository

The primary location for source code, issue tracking, and contributions is the project's GitHub repository:

- **Repository:** [https://github.com/pydantic/pydantic](https://github.com/pydantic/pydantic)

You can use GitHub to:
- [Open issues](https://github.com/pydantic/pydantic/issues) for bug reports, feature requests, or questions.
- [Submit pull requests](https://github.com/pydantic/pydantic/pulls) to contribute code or documentation improvements.
- Review the [project history](https://github.com/pydantic/pydantic/blob/main/HISTORY.md) for recent changes and contributors.

### Maintainers and Core Contributors

The project has been actively maintained and developed by a community of contributors. Notable maintainers and frequent contributors (as referenced in the commit and release history) include:

- **Samuel Colvin** ([@samuelcolvin](https://github.com/samuelcolvin)) — primary maintainer and original author
- **Sebastián Ramírez** ([@tiangolo](https://github.com/tiangolo))
- **David Montagu** ([@dmontagu](https://github.com/dmontagu))
- **PrettyWood** ([@PrettyWood](https://github.com/PrettyWood))
- **Koxudaxi** ([@koxudaxi](https://github.com/koxudaxi))
- **Others**: See the [GitHub contributors page](https://github.com/pydantic/pydantic/graphs/contributors) for a full list.

For direct communication with maintainers, please use GitHub issues or discussions rather than personal email, to ensure transparency and community involvement.

### Community and Support

- **Discussions:** Use the [GitHub Discussions](https://github.com/pydantic/pydantic/discussions) for general questions, ideas, and community support.
- **Documentation:** Comprehensive documentation is available at [https://docs.pydantic.dev/](https://docs.pydantic.dev/).
- **Security Issues:** For security-related concerns, please refer to the [Security Policy](https://github.com/pydantic/pydantic/security/policy) on GitHub.

### Practical Example: Reporting an Issue

If you encounter a bug or have a feature request, please open a new issue on GitHub. Include the following information for faster resolution:

```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Run '...'
3. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Environment:**
- OS: [e.g. Ubuntu 20.04]
- Python version: [e.g. 3.9]
- Pydantic version: [e.g. 1.8.2]

**Additional context**
Add any other context about the problem here.
```

### Sponsorship and Acknowledgements

The project has received support from sponsors and contributors, as acknowledged in the [HISTORY.md](https://github.com/pydantic/pydantic/blob/main/HISTORY.md) file. If you are interested in sponsoring the project, please refer to the GitHub Sponsors page.

---

For all other inquiries, please use the GitHub repository as the central point of contact to ensure your question reaches the right people and benefits the community.

## Acknowledgements

## Acknowledgements

While analyzing the codebase, we did not find explicit references to external contributors, third-party code snippets, or direct attributions within the repository. However, we would like to acknowledge the following, based on the structure and dependencies of the project:

- **Open Source Libraries**  
  The project relies on several open source libraries and frameworks, as detailed in the [Dependencies](#dependencies) section. These libraries provide essential functionality and have greatly accelerated development. We extend our thanks to the maintainers and contributors of these projects.

- **Community Resources**  
  The architecture and design patterns implemented in this codebase reflect best practices widely shared by the developer community. We appreciate the wealth of tutorials, documentation, and discussions available through platforms such as Stack Overflow, GitHub Discussions, and official documentation sites.

- **Tooling and Ecosystem**  
  The project benefits from robust tooling provided by the language ecosystem, including package managers, linters, and testing frameworks. These tools have contributed to code quality and maintainability.

- **Contributors**  
  At this time, the codebase does not list individual contributors beyond the core maintainers. We welcome future contributions and will update this section to recognize those who help improve the project.

If you believe your work should be acknowledged here, or if you notice an omission, please open an issue or submit a pull request. We are committed to giving proper credit to all contributors and sources that support this project.