# AI Movie Production Agent 🎬

An AI-powered multi-agent movie production system that transforms a movie idea into a structured movie concept using specialized AI agents for screenplay development, casting recommendations, and final proposal generation.

## Overview

The system uses a team of AI agents to:

- Develop a screenplay outline
- Generate main character descriptions
- Create a three-act story structure
- Suggest plot twists and key scenes
- Recommend actors for major roles
- Use web search to research relevant actor information
- Produce a structured movie concept and final proposal

## Architecture

The application consists of three main components.

### ScriptWriter Agent

**Model: OpenRouter**

Uses an OpenRouter-hosted language model to:

- Develop the screenplay outline
- Create character descriptions
- Define key plot points
- Structure the story into three acts
- Suggest plot twists and memorable scenes

### CastingDirector Agent

**Model: OpenRouter + SerpAPI**

Uses an OpenRouter-hosted language model and SerpAPI to:

- Analyze the movie concept and main characters
- Suggest suitable actors for major roles
- Search the web for relevant actor information
- Explain the reasoning behind casting recommendations
- Distinguish researched information from unverified suggestions

### MovieProducer Team

**Model: Google Gemini**

Coordinates the ScriptWriter and CastingDirector agents and combines their outputs into a coherent movie proposal, including the story synopsis, character descriptions, plot structure, and casting recommendations.

## Tech Stack

- Python
- Streamlit
- Agno
- OpenRouter API
- Google Gemini API
- SerpAPI

## Features

- Multi-agent AI workflow
- LLM-powered screenplay development
- AI-assisted casting recommendations
- Web search integration
- Genre selection
- Target audience selection
- Adjustable movie runtime
- Structured movie proposal generation
- Downloadable movie proposal in Markdown format

## API Keys

The application requires API keys from the following providers:

- **OpenRouter:** For the ScriptWriter and CastingDirector agents
- **Google Gemini:** For the MovieProducer team
- **SerpAPI:** For web search and actor research

Free model availability and API usage limits depend on each provider's current plan.

## Installation

Clone the repository or navigate to the project directory.

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

Start the Streamlit application using:

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to access the application.

## Project Goal

The goal of this project is to demonstrate how multiple AI agents can collaborate on a creative production task by combining screenplay development, casting research, and AI-driven coordination into a single application.
