# API Reference

This section provides comprehensive reference documentation for all AIDocGen components.

## Overview

The AIDocGen reference documentation is organized by microservice components. Each section includes:

- **API endpoints** with request/response schemas
- **Function signatures** and parameters
- **Class definitions** and methods
- **Configuration options** and environment variables
- **Error codes** and troubleshooting information

## Quick Navigation

### AI Layer Components

- **[Coordinator](reference/ai_layer/coordinator.md)** - Central orchestration service
- **[Planning Agent](reference/ai_layer/planning_agent.md)** - Analysis and planning logic
- **[Generation Agent](reference/ai_layer/generation_agent.md)** - Documentation generation
- **[Quality Agent](reference/ai_layer/quality_agent.md)** - Quality assurance and validation
- **[Query Agent](reference/ai_layer/query_agent.md)** - Information retrieval and search
- **[Utils](reference/ai_layer/utils/tools.md)** - Shared utilities and tools

### Input Integration Pipeline

- **[Main Pipeline](reference/input_integration_pipeline/main.md)** - Core pipeline orchestration
- **[Repository Management](reference/input_integration_pipeline/source/repo_downloader/source/github_cloner.md)** - Git repository handling
- **[Blob Storage](reference/input_integration_pipeline/source/fetch_repo_from_blob/source/blob_services.md)** - Azure Blob Storage integration
- **[File Upload](reference/input_integration_pipeline/source/upload_repo_on_blob/src/services/uploader.md)** - File upload services

### Transforming Pipeline

- **[Pipeline Core](reference/transforming_pipeline/main.md)** - Main transformation orchestrator
- **[Anonymization](reference/transforming_pipeline/components/anonimization/index.md)** - PII detection and removal
- **[Cleaning & Transformation](reference/transforming_pipeline/components/cleaning_and_transformation/README.md)** - Code standardization
- **[Format Conversion](reference/transforming_pipeline/components/md_to_txt/main.md)** - File format conversions
- **[Python Processing](reference/transforming_pipeline/components/python_to_text_conversion/llm_explainer/source/python_explainer.md)** - Python-specific transformations
- **[Enrichment](reference/transforming_pipeline/components/enrichment/README.md)** - Metadata and context addition

## API Endpoints

### Core System APIs

#### Health Check
```
GET /health
```
Returns the overall system health status.

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "ai_layer": "healthy",
    "input_pipeline": "healthy",
    "transform_pipeline": "healthy"
  },
  "timestamp": "2023-09-10T12:00:00Z"
}
```

#### System Information
```
GET /info
```
Returns system information and version details.

### Documentation Generation

#### Generate Documentation
```
POST /generate
```
Initiates documentation generation for a given repository.

**Request Body:**
```json
{
  "repository_url": "https://github.com/user/repo.git",
  "branch": "main",
  "options": {
    "include_tests": true,
    "anonymize_pii": true,
    "output_format": "markdown"
  }
}
```

**Response:**
```json
{
  "job_id": "uuid-12345",
  "status": "processing",
  "estimated_completion": "2023-09-10T12:30:00Z"
}
```

#### Check Generation Status
```
GET /generate/{job_id}/status
```
Returns the current status of a documentation generation job.

#### Download Generated Documentation
```
GET /generate/{job_id}/download
```
Downloads the generated documentation as a zip file.

## Configuration Reference

### Environment Variables

#### AI Layer Configuration
```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=4000

# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password

# Service Configuration
AI_LAYER_HOST=0.0.0.0
AI_LAYER_PORT=8001
```

#### Storage Configuration
```env
# Azure Blob Storage
AZURE_STORAGE_CONNECTION_STRING=your_connection_string
AZURE_CONTAINER_NAME=aiDocGen-storage

# Local Storage (fallback)
LOCAL_STORAGE_PATH=/app/data
MAX_FILE_SIZE_MB=100
```

#### Pipeline Configuration
```env
# Processing Configuration
MAX_CONCURRENT_JOBS=5
PROCESSING_TIMEOUT_MINUTES=30
CLEANUP_INTERVAL_HOURS=24

# Quality Settings
MIN_DOCUMENTATION_COVERAGE=0.8
QUALITY_THRESHOLD=0.75
```

### Configuration Files

#### Pipeline Extensions
Location: `microservices/transforming_pipeline/pipeline_extensions.json`

```json
{
  "version": "1.0",
  "components": [
    {
      "name": "anonimization",
      "enabled": true,
      "priority": 1,
      "config": {
        "detection_models": ["spacy_pii", "azure_text_analytics"],
        "anonymization_strategy": "replacement",
        "preserve_structure": true
      }
    },
    {
      "name": "cleaning_and_transformation",
      "enabled": true,
      "priority": 2,
      "config": {
        "remove_empty_lines": false,
        "standardize_indentation": true,
        "preserve_comments": true
      }
    }
  ]
}
```

## Error Codes

### HTTP Status Codes

| Code | Description | Common Causes |
|------|-------------|---------------|
| 200  | Success | Request completed successfully |
| 202  | Accepted | Request accepted for processing |
| 400  | Bad Request | Invalid request parameters |
| 401  | Unauthorized | Missing or invalid authentication |
| 403  | Forbidden | Insufficient permissions |
| 404  | Not Found | Resource not found |
| 409  | Conflict | Resource already exists |
| 422  | Unprocessable Entity | Invalid data format |
| 429  | Too Many Requests | Rate limit exceeded |
| 500  | Internal Server Error | System error |
| 503  | Service Unavailable | Service temporarily unavailable |

### Application Error Codes

| Code | Category | Description |
|------|----------|-------------|
| DOC001 | Generation | Invalid repository URL |
| DOC002 | Generation | Repository access denied |
| DOC003 | Generation | Unsupported file format |
| DOC004 | Generation | Processing timeout |
| DOC005 | Generation | Insufficient disk space |
| AI001 | AI Layer | Model API unavailable |
| AI002 | AI Layer | Token limit exceeded |
| AI003 | AI Layer | Invalid model response |
| STOR001 | Storage | Storage quota exceeded |
| STOR002 | Storage | File upload failed |
| STOR003 | Storage | Storage service unavailable |

## SDK and Client Libraries

### Python SDK

```python
from aiDocGen import AIDocGenClient

# Initialize client
client = AIDocGenClient(
    api_key="your_api_key",
    base_url="https://api.aiDocGen.com"
)

# Generate documentation
job = client.generate_documentation(
    repository_url="https://github.com/user/repo.git",
    options={
        "include_tests": True,
        "anonymize_pii": True
    }
)

# Wait for completion
result = client.wait_for_completion(job.id)

# Download documentation
client.download_documentation(job.id, "output.zip")
```

### REST Client Examples

#### cURL
```bash
# Generate documentation
curl -X POST "https://api.aiDocGen.com/generate" \
  -H "Authorization: Bearer your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "repository_url": "https://github.com/user/repo.git",
    "options": {
      "include_tests": true,
      "anonymize_pii": true
    }
  }'
```

#### JavaScript
```javascript
const response = await fetch('https://api.aiDocGen.com/generate', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer your_api_key',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    repository_url: 'https://github.com/user/repo.git',
    options: {
      include_tests: true,
      anonymize_pii: true
    }
  })
});

const job = await response.json();
```

## Performance and Limits

### Rate Limits

| Endpoint | Limit | Window |
|----------|-------|---------|
| `/generate` | 10 requests | per hour |
| `/status` | 100 requests | per minute |
| `/download` | 50 requests | per hour |
| All others | 1000 requests | per hour |

### Processing Limits

- **Maximum repository size**: 1GB
- **Maximum processing time**: 2 hours
- **Concurrent jobs per user**: 5
- **File count limit**: 10,000 files
- **Maximum file size**: 50MB per file

### Performance Metrics

- **Average processing time**: 5-15 minutes for typical repositories
- **Supported languages**: Python, JavaScript, TypeScript, Java, C#, Go, Rust
- **Documentation coverage**: Typically 85-95% for well-structured code
- **Quality score**: Average 8.5/10 on human evaluation scale

For detailed implementation information, please refer to the specific component documentation in the [reference section](reference.md).
