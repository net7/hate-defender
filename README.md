# Hate Defender Plugin for Cheshire Cat

This plugin protects your Cheshire Cat instance by detecting and blocking hate speech in user messages. It leverages Hugging Face transformers for state-of-the-art text classification.

## Features

- Detects hate speech in incoming user messages.
- Blocks messages identified as hate speech with a configurable score threshold.
- Customizable response message for blocked content.
- Allows you to choose any compatible text classification model from the Hugging Face Hub.

## How it works

The plugin uses a `fast_reply` hook with high priority. It intercepts every user message before the Cat starts processing it.
It uses a text classification pipeline from the `transformers` library to analyze the message. If the model classifies the message as "HATE" with a confidence score above the configured threshold, the plugin stops the regular workflow and sends a predefined message to the user.

## Configuration

You can configure the plugin from the Cheshire Cat's admin panel under the "Plugins" section.

1.  **Model**: Insert the name of a text classification model from the Hugging Face Hub.
    - Default: `IMSyPP/hate_speech_en`

2.  **Hate Labels (comma-separated)**: A comma-separated list of labels from your chosen model that should be considered hate speech. The check is case-insensitive. To find the correct labels, check the `config.json` file or the model card on the model's Hugging Face page.
    - Default: `LABEL_2, LABEL_3`

3.  **Threshold**: Set a confidence threshold for the hate speech detection, from 0.0 to 1.0. A higher value makes the detection stricter.
    - Default: `0.7`

4.  **Output Message**: The message to be sent to the user when hate speech is detected.
    - Default: `I can't answer, this message contains hate speech.`

The plugin is activated automatically when loaded in the Cheshire Cat.

## Installation

1.  Go to the plugins page in your Cat's admin dashboard.
2.  Search for "Hate Defender" and install it.
3.  Activate the plugin and configure it as needed.