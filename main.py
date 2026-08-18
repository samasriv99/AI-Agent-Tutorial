import os
import argparse
from dotenv import load_dotenv
from google import genai
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions,call_function
import json
import sys
def main()->None:
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("API Key is not found")
    


    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,)
    messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    for _ in range(20):
        final_response = generate_content(client,messages,args.verbose)
        try:
            if final_response:
                print(final_response)
                return
        except Exception as e:
            print(f"Error in generating content: {e}")
    print("No content could be generated in the given iterations")
    sys.exit(1)

def generate_content(client,messages,verbose:bool = False):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,)
    if not response.usage:
        raise RuntimeError("API response appears to be malformed")

    if verbose:
        print("Prompt tokens:", response.usage.prompt_tokens)
        print("Response tokens:", response.usage.completion_tokens)

    message = response.choices[0].message
    messages.append(message)

    if not message.tool_calls:
        return message.content

    for tool_call in message.tool_calls:
        if tool_call.type != "function":
            continue
        result_message = call_function(tool_call, verbose)
        if not result_message.get("content"):
            raise RuntimeError(f"Empty function response for {tool_call.function.name}")
        if verbose:
            print(f"-> {result_message['content']}")
        messages.append(result_message)
    return None
        

if __name__ == "__main__":
    main()

