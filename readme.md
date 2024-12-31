# AI-Powered Voice Assistant

This is an AI-powered voice assistant application that uses the **OpenAI API** for generating responses and the **IBM Watson API** for speech-to-text (STT) and text-to-speech (TTS) capabilities. The application is built with Flask and can be deployed using Docker or AWS Elastic Beanstalk.

Live application: [AI-Powered Voice Assitant](http://flask-app-env.eba-emnvvbm6.us-east-2.elasticbeanstalk.com/)

## Features

- **Speech-to-Text (STT)**: Converts user speech to text using IBM Watson STT API.
- **Text-to-Speech (TTS)**: Converts AI-generated responses to speech using IBM Watson TTS API.
- **AI-Powered Responses**: Utilizes OpenAI API to process user inputs and provide intelligent responses.
- **Interactive UI**: A simple web interface to interact with the voice assistant.

## Technologies Used

- **Programming Language**: Python (Flask Framework)
- **APIs**: OpenAI, IBM Watson (STT & TTS)
- **Deployment**: Docker, AWS Elastic Beanstalk, GitHub Actions
- **Frontend**: HTML, CSS, JavaScript (static files located in the static folder)

## Getting Started

### Prerequisites

1. Python 3.12 or later
2. Docker (optional for containerization)
3. AWS CLI (for Elastic Beanstalk deployment)
4. GitHub Actions (for CI/CD)

### Environment Variables

Create a `.env` file in the root directory with the following keys:

```bash
OPENAI_API_KEY=<your_openai_api_key>
IBM_API_KEY_STT=<your_ibm_stt_api_key>
IBM_REGION_STT=<your_ibm_stt_region>
INSTANCE_STT=<your_ibm_stt_instance>
IBM_API_KEY_TTS=<your_ibm_tts_api_key>
IBM_REGION_TTS=<your_ibm_tts_region>
INSTANCE_TTS=<your_ibm_tts_instance>
```

## Setup and Installation

**1. Clone the Repository**

```bash
git clone https://github.com/sp-ho/ai_powered_voice_assistant.git
cd ai_powered_voice_assistant
```

**2. Install Dependencies**

Create a virtual environment and install the dependencies:

```bash
python -m venv my_env
source my_env/bin/activate  # On Windows: my_env\Scripts\activate
pip install -r requirements.txt
```

**3. Run Locally**

```bash
python application.py
```

Access the app at: http://localhost:8080


## Using Docker

**1. Build the Docker Image**

```bash
docker build -t flask-app .
```

**2. Run the Docker Container**

```bash
docker run -p 8080:8080 flask-app
```

Access the app at: http://localhost:8080


## Deployment to AWS Elastic Beanstalk

**1. Initialize Elastic Beanstalk**

```bash
eb init -p docker flask-app-env --region <your-region>
```

**2. Deploy the Application**

```bash
eb create flask-app-env
```

**3. Update Deployment**

For future updates:

```bash
eb deploy
```

## CI/CD with GitHub Actions

The project includes a GitHub Actions workflow for automating deployment to AWS Elastic Beanstalk whenever changes are pushed to the main branch.

**1. Create an IAM User for GitHub Actions**

- Go to the AWS Management Console and create an IAM user with programmatic access.
- Assign the AWSElasticBeanstalkFullAccess policy to the user.
- Save the Access Key ID and Secret Access Key.

**2. Add Secrets to GitHub**

- In your GitHub repository, go to Settings > Secrets and variables > Actions.
- Add the following secrets:
    - AWS_ACCESS_KEY_ID: Your IAM user’s access key ID.
    - AWS_SECRET_ACCESS_KEY: Your IAM user’s secret access key.
    - AWS_REGION: The region of your Elastic Beanstalk environment (e.g., us-east-2).
    - EB_ENV_NAME: The name of your Elastic Beanstalk environment (e.g., flask-app-env).

**3. GitHub Actions Workflow File**

The .github/workflows/deploy.yml file automates the deployment process:

```yaml
name: Deploy to Elastic Beanstalk

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install Elastic Beanstalk CLI
        run: |
          sudo apt-get update && sudo apt-get install -y unzip
          curl -Lo aws-cli.zip https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip
          unzip aws-cli.zip
          sudo ./aws/install
          curl -Lo eb.zip https://s3.amazonaws.com/elasticbeanstalk/cli/AWS-ElasticBeanstalk-CLI-3.20.1.zip
          unzip eb.zip -d ebcli
          sudo pip install ./ebcli

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_REGION }}

      - name: Deploy to Elastic Beanstalk
        run: |
          eb init -p docker ${{ secrets.EB_ENV_NAME }} --region ${{ secrets.AWS_REGION }} --interactive
          eb deploy
```

## Project Structure

```plaintext
ai_powered_voice_assistant/
├── app/
│   ├── static/           # Static files (CSS, JavaScript)
│   │   ├── style.css
│   │   └── script.js
│   ├── templates/        # HTML templates
│   │   └── index.html
│   ├── application.py    # Flask application
│   └── worker.py         # Helper functions for APIs
├── .dockerignore         # Files excluded from Docker build
├── .ebignore             # Files excluded from Elastic Beanstalk deployment
├── Dockerfile            # Docker configuration
├── requirements.txt      # Python dependencies
├── .github/workflows/    # GitHub Actions workflows
│   └── deploy.yml        # CI/CD workflow file
└── README.md             # Project documentation
```
