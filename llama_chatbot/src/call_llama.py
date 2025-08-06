import requests
import json

def call_llama(model, prompt, stream=False):
    url = "http://localhost:11434/v1/chat/completions"
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": stream
    }

    json_data = json.dumps(data)
    response = requests.post(url, data=json_data, headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}"
    

if __name__ == "__main__":
    model_name = "gemma3:1b"
    prompt_text = "Hello, how are you?"

    response = call_llama(model_name, prompt_text)

    clean_response = str(response).encode('ascii', errors='ignore').decode()
    print(clean_response)