import os
from openai import OpenAI
from inquiries.schemas import AnalysisResult
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
base_url="https://openrouter.ai/api/v1",
api_key= os.environ["OPENROUTER_API_KEY"],
)

def analyze_inquiry(description: str) -> AnalysisResult:
    response = client.chat.completions.create(
        model= "nvidia/nemotron-3-super-120b-a12b:free",
        messages= [
            {
                "role": "system",
                "content": (
                    "Extract manufacturing information from the customer inquiry. "
                    "Only extract information explicitly provided by the customer. "
                    "Do not guess missing information. "
                    "Use null for any information that is not provided."
                ),
            },
            {
                "role": "user",
                "content": (
                    description
                )
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "inquiry_analysis",
                "strict": True,
                "schema": AnalysisResult.model_json_schema(),
            },
        },
    )


    raw_result = response.choices[0].message.content

    return AnalysisResult.model_validate_json(raw_result)