import os
from openai import OpenAI

os.environ["HTTP_PROXY"]
os.environ["HTTPS_PROXY"]
API_KEY = os.getenv("API_KEY")
os.environ["OPENAI_API_KEY"] = API_KEY

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

completion = client.chat.completions.create(
    # extra_headers={
    #     "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional. Site URL for rankings on openrouter.ai.
    #     "X-Title": "<YOUR_SITE_NAME>",  # Optional. Site title for rankings on openrouter.ai.
    # },
    extra_body={},
    model="meta-llama/llama-3.3-8b-instruct:free",
    messages=[{"role": "user", "content": "What is the meaning of life?"}],
)
print(completion.choices[0].message.content)
