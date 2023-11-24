
# WitQuiz-Whiz

WitQuiz Whiz: Convert PDFs and website content into engaging multiple-choice questions effortlessly.

## Table of Contents

- [About](#about)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## About

This project aims to enhance the learning experience by converting PDFs and website content into engaging multiple-choice questions effortlessly.

## Getting Started

1. Run the bash script **requirements.sh**:
   ```bash
   $ pip install -r requirements.txt
   ```

2. Add your **OPENAI_API_KEY** to **constants.py**.

3. Generate an assistant using OPENAI; visit [OpenAI Assistants Overview](https://platform.openai.com/docs/assistants/overview) for more details.

4. Add your assistant_id to **openai_handler.py**.

5. Run the FastAPI server:
   ```bash
   $ uvicorn main:app --reload
   ```

### Prerequisites

- It is recommended to run this on a virtual environment. Activate the venv and run the **requirements.sh** script to install the required version of Python libraries.
- An OPENAI API KEY is required to run the app.

### Installation

1. Clone the repo.
2. Follow the Getting Started steps to run the app.

## Usage

This project aims to enhance the learning experience by converting PDFs and website content into engaging multiple-choice questions effortlessly.

