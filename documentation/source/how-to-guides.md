# How-to Guides

This section provides step-by-step instructions for common tasks with AIDocGen.

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Docker (optional, for containerized deployment)

### Local Development Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/eystraluc/AIDocGen.git
   cd AIDocGen
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Create a `.env` file with necessary configuration:
   ```env
   AZURE_STORAGE_CONNECTION_STRING=your_connection_string
   OPENAI_API_KEY=your_openai_key
   NEO4J_URI=your_neo4j_uri
   NEO4J_USERNAME=your_username
   NEO4J_PASSWORD=your_password
   ```

## Running the System

### Starting Individual Microservices

#### AI Layer
```bash
# Start the coordinator
python microservices/ai_layer/coordinator.py

# Start individual agents
python microservices/ai_layer/planning_agent.py
python microservices/ai_layer/generation_agent.py
python microservices/ai_layer/quality_agent.py
python microservices/ai_layer/query_agent.py
```

#### Input Integration Pipeline
```bash
# Start the main pipeline
python microservices/input_integration_pipeline/main.py
```

#### Transforming Pipeline
```bash
# Start the transforming pipeline
python microservices/transforming_pipeline/main.py
```

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Common Tasks

### Generating Documentation from a Repository

1. **Upload Repository**
   ```bash
   curl -X POST "http://localhost:8000/upload" \
        -F "repository=@/path/to/your/repo.zip"
   ```

2. **Start Processing**
   ```bash
   curl -X POST "http://localhost:8000/process" \
        -H "Content-Type: application/json" \
        -d '{"repo_id": "your_repo_id"}'
   ```

3. **Check Status**
   ```bash
   curl "http://localhost:8000/status/{repo_id}"
   ```

4. **Download Documentation**
   ```bash
   curl "http://localhost:8000/download/{repo_id}" -o documentation.zip
   ```

### Customizing Processing Pipeline

1. **Add Custom Component**
   - Create a new component in `microservices/transforming_pipeline/components/`
   - Implement the required interface
   - Register the component in `pipeline_extensions.json`

2. **Configure Anonymization**
   - Edit anonymization patterns in `components/anonimization/utils/patterns.py`
   - Adjust PII detection rules
   - Test with sample data

### Monitoring and Debugging

1. **View System Health**
   ```bash
   curl "http://localhost:8000/health"
   ```

2. **Check Service Status**
   ```bash
   # Individual service health
   curl "http://localhost:8001/status"  # AI Layer
   curl "http://localhost:8002/status"  # Input Pipeline
   curl "http://localhost:8003/status"  # Transform Pipeline
   ```

3. **Access Logs**
   ```bash
   # View application logs
   tail -f logs/aiDocGen.log
   
   # View specific service logs
   tail -f logs/ai_layer.log
   tail -f logs/input_pipeline.log
   tail -f logs/transform_pipeline.log
   ```

## Configuration

### Pipeline Configuration

Edit `microservices/transforming_pipeline/pipeline_extensions.json`:

```json
{
  "components": [
    {
      "name": "anonimization",
      "enabled": true,
      "config": {
        "detection_threshold": 0.8,
        "anonymization_method": "replacement"
      }
    },
    {
      "name": "cleaning_and_transformation",
      "enabled": true,
      "config": {
        "remove_comments": false,
        "standardize_formatting": true
      }
    }
  ]
}
```

### AI Model Configuration

Configure AI models in the respective agent files:

```python
# In planning_agent.py
MODEL_CONFIG = {
    "model": "gpt-4",
    "temperature": 0.3,
    "max_tokens": 2000
}
```

## Troubleshooting

### Common Issues

1. **Connection Errors**
   - Check that all required services are running
   - Verify environment variables are set correctly
   - Ensure network connectivity between services

2. **Processing Failures**
   - Check input data format and size
   - Review error logs for specific issues
   - Verify sufficient disk space and memory

3. **Quality Issues**
   - Adjust quality thresholds in quality_agent.py
   - Review and update processing rules
   - Validate input data quality

### Performance Optimization

1. **Scaling Services**
   - Use Docker Compose scaling: `docker-compose up -d --scale ai_layer=3`
   - Configure load balancing
   - Monitor resource usage

2. **Database Optimization**
   - Index frequently queried fields
   - Optimize Neo4j queries
   - Configure appropriate connection pools

3. **Storage Optimization**
   - Use appropriate blob storage tiers
   - Implement data lifecycle policies
   - Monitor storage usage and costs
