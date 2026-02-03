# REST API Documentation

The TiT Guild App exposes REST API endpoints for easy data scraping and integration.

## Running the Application

**Local Development:**

Start the application with API support:

```bash
streamlit run gt_guild_app/app.py --server.port 8503
```

The Streamlit UI will be available at `http://localhost:8503` and API endpoints at the same domain with `/api/*` paths.

**Streamlit Cloud Note:**

⚠️ The Starlette API integration may not be fully supported on Streamlit Cloud yet as it requires Streamlit 1.53+ features that are still being rolled out. If the API endpoints return "You need to enable JavaScript to run this app", this indicates the feature is not yet available in your deployment environment.

For production API access on Streamlit Cloud, consider:
- Running a separate FastAPI service
- Using Streamlit's built-in caching and session state for data access
- Deploying the API portion separately on a platform like Railway, Render, or Fly.io

## API Endpoints

### Health Check

**GET** `/api/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "TiT Guild App API"
}
```

---

### List All Goods

**GET** `/api/goods`

Get a list of all unique goods across all companies.

**Response:**
```json
{
  "status": "success",
  "data": {
    "goods": ["Adhesive", "Aluminum", "Berries", ...],
    "count": 150
  }
}
```

---

### List All Companies

**GET** `/api/companies`

Get a summary of all companies.

**Response:**
```json
{
  "status": "success",
  "data": {
    "companies": [
      {
        "name": "Company Name",
        "industry": "Industry Type",
        "professions": ["Prof1", "Prof2"],
        "timezone": "UTC +00:00",
        "goods_count": 25
      }
    ],
    "count": 10
  }
}
```

---

### Get Good Details

**GET** `/api/good/{good_name}`

Get pricing details for a specific good across all companies.

**Parameters:**
- `good_name` (path): Name of the good (e.g., "Adhesive")

**Response:**
```json
{
  "status": "success",
  "query": {
    "good": "Adhesive"
  },
  "data": {
    "results": [
      {
        "company": "Company Name",
        "good": "Adhesive",
        "planet_produced": "Kentaurus 2",
        "guildees_pay": 100,
        "live_exc_price": 120,
        "live_avg_price": 115,
        "guild_max": 110,
        "guild_min": 95,
        "discount_percent": 10,
        "discount_fixed": 5,
        "timezone": "UTC +00:00",
        "professions": ["Prof1"]
      }
    ],
    "count": 5,
    "cheapest": {
      "company": "Best Company",
      "guildees_pay": 95
    }
  }
}
```

Results are sorted by `guildees_pay` (cheapest first).

---

### Get Company Details

**GET** `/api/company/{company_name}`

Get full details for a specific company.

**Parameters:**
- `company_name` (path): Name of the company

**Response:**
```json
{
  "status": "success",
  "query": {
    "company": "Company Name"
  },
  "data": {
    "name": "Company Name",
    "industry": "Industry Type",
    "professions": ["Prof1", "Prof2"],
    "timezone": "UTC +00:00",
    "local_time": "2025-01-01 12:00:00",
    "goods": [
      {
        "produced_goods": "Adhesive",
        "planet_produced": "Kentaurus 2",
        "guildees_pay": 100,
        "live_exc_price": 120,
        "live_avg_price": 115,
        "guild_max": 110,
        "guild_min": 95,
        "discount_percent": 10,
        "discount_fixed": 5
      }
    ]
  }
}
```

---

### Get All Data

**GET** `/api/all`

Get the complete dataset with all companies and their goods.

**Response:**
```json
{
  "status": "success",
  "data": {
    "companies": [
      {
        "name": "Company Name",
        "industry": "Industry Type",
        "professions": ["Prof1"],
        "timezone": "UTC +00:00",
        "local_time": "2025-01-01 12:00:00",
        "goods": [...]
      }
    ],
    "count": 10
  }
}
```

## Error Responses

All endpoints may return error responses:

```json
{
  "status": "error",
  "message": "Error description"
}
```

HTTP status codes:
- `400`: Bad Request (missing parameters)
- `404`: Not Found (resource doesn't exist)
- `500`: Internal Server Error

## Implementation

The API is implemented using Streamlit 1.53+'s built-in Starlette integration:

```python
from streamlit.starlette import App
from starlette.routing import Route
from starlette.responses import JSONResponse

app = App(
    "app.py",
    routes=[
        Route("/api/health", api_health),
        Route("/api/goods", api_goods_list),
        # ... more routes
    ],
)
```

This allows the same application to serve both the Streamlit UI and REST API endpoints.

## Usage Examples

### Python

```python
import requests

# Get health status
response = requests.get("http://localhost:8503/api/health")
print(response.json())

# Find cheapest adhesive
response = requests.get("http://localhost:8503/api/good/Adhesive")
data = response.json()
cheapest = data['data']['cheapest']
print(f"Cheapest at {cheapest['company']}: {cheapest['guildees_pay']}")
```

### cURL

```bash
# Health check
curl http://localhost:8503/api/health

# Get all goods
curl http://localhost:8503/api/goods

# Get adhesive pricing
curl http://localhost:8503/api/good/Adhesive

# Get company details
curl http://localhost:8503/api/company/SomeCompany
```

### JavaScript

```javascript
// Fetch all companies
fetch('http://localhost:8503/api/companies')
  .then(response => response.json())
  .then(data => {
    console.log(`Found ${data.data.count} companies`);
    data.data.companies.forEach(company => {
      console.log(`${company.name} - ${company.goods_count} goods`);
    });
  });
```
