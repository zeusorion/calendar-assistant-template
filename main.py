import os
import json
import requests
from datetime import datetime, timezone

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') or 'your_openai_key'
ENDPOINT = 'https://api.openai.com/v1/chat/completions'
HEADERS = {
    'Authorization': f'Bearer {OPENAI_API_KEY}',
    'Content-Type': 'application/json'
}

def get_payload(user_input, examples):
    current_time = datetime.now(timezone.utc).isoformat()
    few_shot_messages = []
    for ex in examples['examples']:
        few_shot_messages.append({'role': 'user', 'content': ex['question']})
        few_shot_messages.append({'role': 'assistant', 'content': json.dumps(ex['response'])})

    return {
        'model': 'gpt-4o',
        'messages': [
            {'role': 'system', 'content': (
                "You are a helpful assistant that extracts calendar tasks and schedules from user messages. "
                "You will return a JSON object with 'task', 'frequency', and 'cronExpression'. If startDate or endDate "
                "is mentioned, include them as ISO UTC strings. Follow these few-shot examples carefully."
            )},
            *few_shot_messages,
            {'role': 'user', 'content': user_input}
        ],
        'temperature': 0
    }

def main():
    with open('text_to_cron_input.json') as f:
        input_tests = json.load(f)
    with open('cron-input-samples.json') as f:
        examples = json.load(f)

    output_results = []

    for item in input_tests:
        payload = get_payload(item['text'], examples)
        try:
            response = requests.post(ENDPOINT, headers=HEADERS, json=payload)
            response.raise_for_status()
            result_json = response.json()

            # Safely extract the relevant part from the response
            result_content = next(
                (choice['message']['content'] for choice in result_json.get('choices', []) if 'message' in choice),
                "{}"
            )

            # Convert string to JSON (if it's a string)
            try:
                result_data = json.loads(result_content)
            except json.JSONDecodeError:
                result_data = {"raw_content": result_content}

            output_entry = {
                "prompt": item['text'],
                "results": result_data
            }
            output_results.append(output_entry)
            print(f"Processed: {item['text']}")

        except Exception as e:
            print(f"Error processing '{item['text']}': {e}")
            output_results.append({
                "prompt": item['text'],
                "results": {"error": str(e)}
            })

    # Write all results to output.json
    with open('output.json', 'w') as out_f:
        json.dump(output_results, out_f, indent=2)
    print("All results written to output.json")

if __name__ == '__main__':
    main()
