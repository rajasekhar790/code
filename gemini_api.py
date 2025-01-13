import subprocess
import json

def get_gemini_response(prompt: str, api_key: str) -> str:
    """
    Sends a request to the Gemini API and returns the generated text.

    Args:
        prompt: The text prompt to send to the API.
        api_key: Your Gemini API key.

    Returns:
        The generated text from the API response, or an error message.
    """
    api_key = ''
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    try:
        # Use subprocess to execute the curl command
        process = subprocess.run(
            ["curl", "-s", "-X", "POST", "-H", "Content-Type: application/json", "-d", json.dumps(data), url],
            capture_output=True,
            text=True,
            check=True  # Raise an exception for non-zero exit codes
        )

        response_json = json.loads(process.stdout)

        # Extract the generated text from the response
        if "candidates" in response_json and response_json["candidates"]:
            generated_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
            return generated_text
        else:
            # Handle cases where the response doesn't contain the expected structure
            if "error" in response_json:
              return f"API Error: {response_json['error']['message']}"
            else:
              return "Error: Could not find generated text in API response."

    except subprocess.CalledProcessError as e:
        return f"Error executing curl command: {e.stderr}"
    except json.JSONDecodeError as e:
        return f"Error decoding JSON response: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

if __name__ == "__main__":
    api_key = "AIzaSyBjmn5UK3lpiwq7lbK767EoHxsan-Hu-kI"  # Replace with your actual API key
    prompt = "Generative AI job Market"  # You can change this to any prompt you want

    response = get_gemini_response(prompt, api_key)
    print(response)
