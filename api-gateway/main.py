import os
import httpx
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import StreamingResponse

app = FastAPI()

API_SECRET_KEY = os.getenv("API_SECRET_KEY")
OLLAMA_URL = os.getenv("OLLAMA_URL")

@app.post("/api/generate")
async def generate_response(request: Request):
    # Check the API Key from the request header.
    auth_header = request.headers.get("X-API-Key")
    if not auth_header or auth_header != API_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )

    # Get the request body.
    request_body = await request.json()

    # Add stream=true to get a streaming response.
    request_body["stream"] = True

    try:
        # Forward the request to the Ollama service.
        async def generate_stream():
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST",
                    f"{OLLAMA_URL}/api/generate",
                    json=request_body,
                    headers={"Content-Type": "application/json"},
                    timeout=None # Ensure there is no timeout when processing large models.
                ) as response:
                    response.raise_for_status()
                    async for chunk in response.aiter_bytes():
                        yield chunk

        return StreamingResponse(generate_stream(), media_type="application/x-ndjson")

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Ollama API returned an error: {e.response.text}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
