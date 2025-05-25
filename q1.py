import httpx

# API endpoint
API_URL = "https://aiproxy.sanand.workers.dev/openai/v1/completions"  # Verify the correct endpoint

# Dummy API key
API_KEY = "dummy_api_key"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Request payload
DATA = {
    "model": "gpt-4o-mini",  # Ensure this is the correct model name
    "messages": [
        {"role": "system", "content": "Analyze the sentiment of the following text as GOOD, BAD, or NEUTRAL."},
        {"role": "user", "content": "n WNa8fyPgO4FGm 3C Djn0Vj2Za6fh  etiVemrm7a k  18"}
    ]
}

# Send POST request with error handling
async def send_request():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(API_URL, json=DATA, headers=HEADERS)
            response.raise_for_status()  # Check if the response was successful (status code 200-299)

            # Parse response
            result = response.json()
            print(result)
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Main function to run the request
import asyncio
asyncio.run(send_request())
