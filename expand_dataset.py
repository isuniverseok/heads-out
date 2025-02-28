import requests
import json

prompt = ("Generate a list of 100 unique travel destinations in JSON format. Each entry should have:\n"
          "- City\n"
          "- Country\n"
          "- Two clues\n"
          "- Two fun facts\n"
          "- Two trivia facts\n"
          "Return the data in a structured JSON format:\n"
          "[\n"
          "  {\n"
          "    \"city\": \"Example City\",\n"
          "    \"country\": \"Example Country\",\n"
          "    \"clues\": [\"Clue 1\", \"Clue 2\"],\n"
          "    \"fun_fact\": [\"Fact 1\", \"Fact 2\"],\n"
          "    \"trivia\": [\"Trivia 1\", \"Trivia 2\"]\n"
          "  },\n"
          "  ...\n"
          "]"
          "DO NOT print your reasoning response, instead strictly start your response with the required JSON format.")

url = "https://router.huggingface.co/sambanova/v1/chat/completions"
headers = {
    "Authorization": "Bearer khudki_api_key",  # Replace with your actual API key
    "Content-Type": "application/json"
}

data = {
    "model": "Meta-Llama-3.2-3B-Instruct",
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ],
    "max_tokens": 2000,
    "stream": False
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    try:
        response_json = response.json()

        # Extract generated JSON text
        if "choices" in response_json and len(response_json["choices"]) > 0:
            generated_text = response_json["choices"][0]["message"]["content"]

            # Save response as raw JSON text (without parsing)
            with open("extended_data.json", "w") as json_file:
                json.dump({"generated_text" : generated_text}, json_file, indent=4)

            print("Data saved successfully to extended_data.json")

        else:
            print("Unexpected API response format")

    except Exception as e:
        print(f"Error processing response: {e}")

else:
    print(f"API Error: {response.status_code}, {response.text}")
