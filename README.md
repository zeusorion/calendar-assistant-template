# Calendar Assistant with Few-Shot Prompting

This project is a Python-based assistant that uses OpenAI's API to extract calendar tasks and translate them into structured cron expressions.

## 📦 Project Structure

- `main.py` — Python script to run the assistant
- `text_to_cron_input.json` — Input test cases
- `cron-input-samples.json` — Few-shot examples to guide the model
- `output.json` — Sample output (for reference)
- `requirements.txt` — Dependencies list

## ⚙️ Setup Instructions

1️⃣ Clone this repository or use it as a GitHub template.

2️⃣ Install dependencies:

```
pip install -r requirements.txt
```

3️⃣ Set your OpenAI API key (you can export it as an environment variable):

```
export OPENAI_API_KEY=your_openai_key_here
```

4️⃣ Run the script:

```
python main.py
```

The script will send input examples through the OpenAI API, apply few-shot prompting, and print structured results.

## 🚀 Notes

- Make sure you have Python 3.8+ installed.
- You can modify `text_to_cron_input.json` with your own phrases to test.
- Review `cron-input-samples.json` to adjust or expand few-shot examples.

Enjoy experimenting!
