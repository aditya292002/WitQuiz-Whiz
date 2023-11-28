
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
   $ python -m uvicorn main:app --reload
   ```

### Running on Docker

To run the application using Docker, follow these steps:

1. Pull the Docker image:
   ```bash
   $ docker pull aditya292002/witquiz-wiz:0.0.1.RELEASE
   ```

2. Run the Docker container:
   ```bash
   $ docker container run -p 8000:8000 aditya292002/witquiz-wiz:0.0.1.RELEASE
   ```

### Prerequisites

- It is recommended to run this on a virtual environment. Activate the venv and run the **requirements.sh** script to install the required version of Python libraries.
- An OPENAI API KEY is required to run the app.

### Installation

1. Clone the repo.
2. Follow the Getting Started steps to run the app.

## Usage

This project aims to enhance the learning experience by converting PDFs and website content into engaging multiple-choice questions effortlessly.

## LICENSE

[MIT LICENSE](LICENSE)
