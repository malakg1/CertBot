# CertBot

This project demonstrates how a team of AI agents can collaborate to detect certificates in Gmail, extract details, generate LinkedIn posts, and publish them automatically.

Built with LangGraph, PyTesseract, Selenium, and the Gmail API.

## Features

Gmail Agent → Uses Gmail API (via GCP) to detect new certificates.

OCR Agent → Extracts certificate text with PyTesseract.

Metadata Agent → Enriches details like program name, role, sponsors, and skills.

Post Generator Agent → Drafts a LinkedIn post.

Polish Agent → Adjusts tone, formatting, and phrasing.

Slack Preview Agent → Sends a draft preview to Slack.

Publisher Agent → Publishes the final post to LinkedIn via Selenium.

## Tech Stack

LangGraph
 – Orchestrating the multi-agent workflow

PyTesseract
 – Optical Character Recognition (OCR)

Selenium
 – Automating LinkedIn posting

Gmail API (via Google Cloud Platform) – Accessing certificates from Gmail

Slack API
 – Sending draft previews

Gemini model – Metadata enrichment

## Instructions
1. Clone the Repository
git clone https://github.com/your-username/ai-agents-linkedin-certificates.git
cd ai-agents-linkedin-certificates

2. Create & Activate Virtual Environment
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Configure Gmail API

Enable the Gmail API in your Google Cloud Console.

Download credentials.json and place it in the project root.

The first run will open a browser for OAuth authentication.

5. Configure Environment Variables

## Create a .env file:

SLACK_API_TOKEN=your_slack_token
GMAIL_CREDENTIALS=credentials.json
LINKEDIN_USERNAME=your_email
LINKEDIN_PASSWORD=your_password
