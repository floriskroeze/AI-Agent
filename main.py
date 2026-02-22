import os
from dotenv import load_dotenv
from prompts.prompts import system_prompt
from google import genai
import argparse
from functions.call_function import available_functions, call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key == None:
        raise RuntimeError("Gemini api key not found")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [genai.types.Content(role="user", parts=[genai.types.Part(text=args.user_prompt)])]
    
    for _ in range(20):
        call = call_model(client, messages)

        if call.candidates:
            for candidate in call.candidates:
                messages.append(candidate.content)

        if call.usage_metadata == None:
            raise RuntimeError("No metadata in response")
        
        if call.function_calls:
            function_responses = []
            for function_call in call.function_calls:
                function_responses.append(handle_function_call(function_call, args.verbose))
                
        else:
            print_response(call, args.user_prompt, args.verbose)
            break
        
        messages.append(genai.types.Content(role="user", parts=function_responses))
    
    print("Too many calls")
    exit(0)

def call_model(client, messages):
    return client.models.generate_content(model="gemini-2.5-flash", contents=messages, config=genai.types.GenerateContentConfig(system_instruction= system_prompt,temperature=0, tools=[available_functions]))

def print_response(response, user_prompt, isVerbose=False):
    if isVerbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Final response: \n{response.text}")

def handle_function_call(function_call, verbose):
    function_call_result = call_function(function_call)

    if not len(function_call_result.parts):
        raise Exception("Error: No function parts")
    
    if not function_call_result.parts[0].function_response:
        raise Exception("Error: No function result")

    if not function_call_result.parts[0].function_response.response:
        raise Exception("Error: No response on function response")
    
    if verbose:
        print(f"-> {function_call_result.parts[0].function_response.response}")

    return function_call_result.parts[0]

main() 