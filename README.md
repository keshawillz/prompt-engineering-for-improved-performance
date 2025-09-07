# Prompt Engineering for Improved Performance
This repository contains the Python code examples from the Pluralsight course **Prompt Engineering for Improved Performance**.

![Prompt Engineering for Improved Performance](https://github.com/keshawillz/prompt-engineering-for-improved-performance/blob/main/course_image.png)

In the course, you'll:
- Learn how to analyze model performance and identify areas for improvement
- Understand how to design prompts that improve model performance and inference time
- Learn how to optimize prompts for specific use cases and applications
- Gain hands-on experience with prompt engineering for improved model performance
- Understand the latest research and advancements in prompt engineering for generative AI

## Requirements
- Python 3.9+
- An [OpenAI API key](https://platform.openai.com/account/api-keys)

## Setup

1. **Clone this repo** (or download the files).
2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate   # macOS/Linux
    venv\Scripts\activate      # Windows
    ```
3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4. **Set your OpenAI API key or place in .env file**:
    ```bash
    export OPENAI_API_KEY="your_api_key"      # macOS/Linux
    setx OPENAI_API_KEY "your_api_key"        # Windows PowerShell
    ```

## Running the Examples

Run the main demo script to see all lessons in action:

```bash
python lesson.py

