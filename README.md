# AI Inquiry Analyzer

A small Django demo application that demonstrates how unstructured customer manufacturing requests can be converted into structured data using an LLM.

The project was built as a learning project to explore Django, structured AI output, validation, persistence, and automated testing.

## What It Does

A customer submits an inquiry containing:

- Name
- Email
- Free-text request description

For example:

> I need 20 aluminium brackets, 3 mm thick and 200 x 100 mm, by January 10th, 2027

The application:

1. Validates and stores the original inquiry.
2. Sends only the description to an AI service.
3. Extracts structured manufacturing information.
4. Validates the AI output using Pydantic.
5. Stores the AI-generated analysis separately from the original inquiry.
6. Displays both the original request and extracted information on the inquiry detail page.

The extracted information includes:

- Material
- Quantity
- Thickness
- Width
- Height
- Deadline

If information is not present in the customer's request, the model is instructed to return `null` rather than guess.

---

## Tech Stack

- Python
- Django
- SQLite
- Pydantic
- OpenRouter
- Django TestCase
- `unittest.mock`

The application currently uses the OpenRouter-compatible API with:

```text
nvidia/nemotron-3-super-120b-a12b:free
```

---

## Architecture

The application separates HTTP handling, AI processing, validation, and persistence.

```text
Customer
   ↓
Django Form
   ↓
Inquiry
   ↓
AI Service
   ↓
OpenRouter / Qwen
   ↓
Structured JSON
   ↓
Pydantic Validation
   ↓
InquiryAnalysis
   ↓
Detail Page
```

The project is organized roughly as follows:

```text
inquiries/
├── services/
│   ├── ai.py
│   └── analysis.py
│
├── templates/
│   └── inquiries/
│
├── static/
│   └── inquiries/
│
├── forms.py
├── models.py
├── schemas.py
├── urls.py
├── views.py
└── tests.py
```

### Responsibilities

`views.py`  
Handles HTTP requests, forms, redirects, and rendering.

`models.py`  
Defines persistent application data.

`forms.py`  
Handles customer input and validation.

`schemas.py`  
Defines the expected structure of AI output using Pydantic.

`services/ai.py`  
Communicates with the LLM through OpenRouter.

`services/analysis.py`  
Handles AI analysis and maps validated output into the database.

---

## Data Model

The original customer request and the AI-generated result are intentionally stored separately.

```text
Inquiry
    1
    │
    │ One-to-One
    │
    1
InquiryAnalysis
```

### Inquiry

Stores the original customer data:

```text
customer_name
email
description
status
created_at
```

### InquiryAnalysis

Stores information extracted by the AI:

```text
material
quantity
thickness_mm
width_mm
height_mm
deadline
```

This separation keeps the customer's original request as the source of truth while treating AI output as derived data.

---

## AI Validation

The AI does not write directly to the database.

The response is constrained using a structured-output schema and is then validated again using Pydantic before being persisted.

```text
LLM response
    ↓
JSON Schema
    ↓
Pydantic validation
    ↓
Django model
    ↓
Database
```

Missing information is represented as `None`.

## Failure Handling

AI processing is intentionally independent from the original inquiry submission.

If the AI request fails because of:

- API errors
- provider errors
- malformed output
- validation failures
- network problems

the original `Inquiry` remains stored.

```text
Inquiry saved
     ↓
AI processing
   /       \
success    failure
  ↓           ↓
analysis    inquiry remains
saved       available for
            manual review
```

AI failures are logged and do not cause valid customer requests to be lost.

---

## Setup

Clone the repository:

```bash
git clone <repository-url>
cd <repository-directory>
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```text
OPENROUTER_API_KEY=your_api_key_here
```

Apply database migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/inquiries/
```

---

## Testing

Run the complete test suite with:

```bash
python manage.py test
```

The tests cover behavior including:

- Valid inquiry creation
- Invalid form submissions
- Inquiry detail pages
- 404 handling
- Successful AI analysis processing
- AI processing failures
- Preservation of the original inquiry when AI analysis fails

External AI calls are mocked during automated tests so the test suite does not depend on network access or OpenRouter availability.
