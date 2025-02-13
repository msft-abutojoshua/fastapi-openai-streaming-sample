from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import openai
import asyncio
import os
from dotenv import load_dotenv
 

# Azure OpenAI API Configuration
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
 
if not AZURE_OPENAI_ENDPOINT or not AZURE_OPENAI_KEY or not AZURE_OPENAI_DEPLOYMENT:
    raise ValueError("Missing environment variables for Azure OpenAI")

# FastAPI instance 
app = FastAPI()
 
# Set up OpenAI client
openai.api_type = "azure"
openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_key = AZURE_OPENAI_KEY
openai.api_version = "2023-03-15-preview"  # Update if needed
 
# Request model
class ChatRequest(BaseModel):
    messages: list  # List of messages in OpenAI format
    temperature: float = 0.7
    max_tokens: int = 500
 
async def stream_openai_response(messages, temperature, max_tokens):
    """
    Streams responses from Azure OpenAI ChatGPT.
    """
    try:
        response = openai.ChatCompletion.create(
            engine=AZURE_OPENAI_DEPLOYMENT,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,  # Enable streaming
        )
 
        # Iterate through stream and yield responses
        for chunk in response:
            if chunk and "choices" in chunk:
                content = chunk["choices"][0]["delta"].get("content", "")
                if content:
                    yield f"data: {content}\n\n"
                    await asyncio.sleep(0)  # Yield control to event loop
 
    except Exception as e:
        yield f"data: Error: {str(e)}\n\n"
 
@app.post("/chat-stream")
async def chat_stream(request: ChatRequest):
    """
    API endpoint for streaming responses from Azure OpenAI.
    """
    return StreamingResponse(
        stream_openai_response(request.messages, request.temperature, request.max_tokens),
        media_type="text/event-stream"
    )
 
# Run FastAPI server
if __name__ == "__main__":
    import uvicorn
uvicorn.run(app, host="0.0.0.0", port=8000)