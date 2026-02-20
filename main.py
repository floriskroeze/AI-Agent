import os
from dotenv import load_dotenv
from prompts.prompts import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key == None:
    raise RuntimeError("Gemini api key not found")

from google import genai
import argparse

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [genai.types.Content(role="user", parts=[genai.types.Part(text=args.user_prompt)])]
call = client.models.generate_content(model="gemini-2.5-flash", contents=messages, config=genai.types.GenerateContentConfig(system_instruction= system_prompt))

if call.usage_metadata == None:
    raise RuntimeError("No metadata in response")

def printResponse(response, user_prompt, isVerbose=False):
    if isVerbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(response.text)

printResponse(call, args.user_prompt, args.verbose)