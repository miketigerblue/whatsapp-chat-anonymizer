# WhatsApp Chat Anonymizer

  

An open-source tool to anonymize WhatsApp chat exports by replacing personal names and other Personally Identifiable Information (PII) with tokens, while preserving the conversation's timeline and flow.

  

## Table of Contents

  

- [Introduction](#introduction)

- [Features](#features)

- [Prerequisites](#prerequisites)

- [Installation](#installation)

- [1. Clone the Repository](#1-clone-the-repository)

- [2. Set Up a Virtual Environment](#2-set-up-a-virtual-environment)

- [3. Install Dependencies](#3-install-dependencies)

- [Usage](#usage)

- [1. Prepare Your WhatsApp Chat Export](#1-prepare-your-whatsapp-chat-export)

- [2. Run the Anonymizer Script](#2-run-the-anonymizer-script)

- [3. Output](#3-output)

- [Customization](#customization)

- [Anonymizing Additional Entities](#anonymizing-additional-entities)

- [Adjusting Name Token Prefix](#adjusting-name-token-prefix)

- [Examples](#examples)

- [Contributing](#contributing)

- [License](#license)

- [Disclaimer](#disclaimer)

  

## Introduction

  

**WhatsApp Chat Anonymizer** is a Python script that processes WhatsApp chat exports (`.txt` files) and replaces personal names and other PII with anonymized tokens. This allows you to share or analyze chat data without exposing sensitive information.

  

## Features

  

-  **Anonymizes Personal Names**: Replaces names with consistent tokens (e.g., `[Person1]`, `[Name1]`).

-  **Retains Date and Time**: Keeps the original date and time to preserve the conversation timeline.

-  **Anonymizes Message Content**: Removes or replaces emails, phone numbers, and other PII within messages.

-  **Customizable**: Easily adjust which entities to anonymize or retain.

-  **Uses NLP**: Leverages [spaCy](https://spacy.io/) for accurate Named Entity Recognition (NER).

  

## Prerequisites

  

-  **Python 3.7 to 3.11**: Ensure you have a compatible Python version installed.

-  **pip**: Python package installer.

-  **git**: Version control system (optional, for cloning the repository).

  

## Installation

  

### 1. Clone the Repository

  

```

git clone https://github.com/tigerblue/whatsapp-chat-anonymizer.git

cd whatsapp-chat-anonymizer

```

  

## Introduction

  

WhatsApp Chat Anonymizer is a Python script that processes WhatsApp chat exports (.txt files) and replaces personal names and other PII with anonymized tokens. This allows you to share or analyze chat data without exposing sensitive information.

  

## Features

  

Anonymizes Personal Names: Replaces names with consistent tokens (e.g., [Person1], [Name1]).

Retains Date and Time: Keeps the original date and time to preserve the conversation timeline.

Anonymizes Message Content: Removes or replaces emails, phone numbers, and other PII within messages.

  

Customizable: Easily adjust which entities to anonymize or retain.

Uses NLP: Leverages spaCy for accurate Named Entity Recognition (NER).

  

## Prerequisites

  

Python 3.7 to 3.11: Ensure you have a compatible Python version installed.

pip: Python package installer.

git: Version control system (optional, for cloning the repository).

  
  

## Installation

  

1. Clone the Repository

  

```

git clone https://github.com/tigerblue/whatsapp-chat-anonymizer.git

cd whatsapp-chat-anonymizer

```

  

2. Set Up a Virtual Environment

  

Create a virtual environment to manage dependencies:

```

python3 -m venv venv

Activate the virtual environment:

```

  

On macOS/Linux:

  

`source venv/bin/activate`

  

On Windows (Command Prompt):

  

`venv\Scripts\activate`

  

3. Install Dependencies

  

Upgrade pip and install required packages:

  
  

`pip install --upgrade pip setuptools wheel`

`pip install -r requirements.txt`

  

Install spaCy's English language model:

  

`python -m spacy download en_core_web_sm`

  
  

## Usage

 
1. Prepare Your WhatsApp Chat Export


Export your WhatsApp chat to a .txt file:
 

Open the chat in WhatsApp.
  

Go to Options > More > Export Chat.

Choose Without Media to export text only.

Save the archive to your device, we'll need to unzip and look inside this for a _chat.txt file.

  

2. Run the Anonymizer Script

  

`python anonymize_whatsapp.py _chat.txt -o anonymized_chat.txt`

  

input_chat.txt: Path to your exported WhatsApp chat file.

  

-o anonymized_chat.txt: (Optional) Specify the output file name.

  

3. Output

  

The script will generate an anonymized chat file (anonymized_chat.txt by default) with personal names and other PII replaced with tokens.

  

## Customization

  

Anonymizing Additional Entities

  

You can extend the script to anonymize other entities such as locations, organizations, or dates within messages.

  

Example: Anonymize Locations

  

In anonymize_whatsapp.py, modify the anonymize_message function:

```

def anonymize_message(message):

doc = nlp(message)

entities = [(ent.text, ent.label_) for ent in doc.ents]

location_counter = 1

location_map = {}

for text, label in entities:

if label == 'GPE' and text not in location_map:

location_map[text] = f'[Location{location_counter}]'

location_counter += 1

for loc, token in location_map.items():

pattern = re.compile(r'\b{}\b'.format(re.escape(loc)))

message = pattern.sub(token, message)

# Existing anonymization code...

  

return message

```

  
  

## Adjusting Name Token Prefix

  

Change the prefix used for name tokens by modifying the sender_map in the anonymize_pii function:

  

`sender_map = {sender: f'[User{i+1}]' for i, sender in enumerate(df['sender'].unique())}`

**Examples**

  

**Original Message:**

  

[12/10/2023, 7:00 PM] Alice: Hey Bob, are you coming to the party on Saturday?

**Anonymized Output:**

  

[12/10/2023, 7:00 PM] [Person1]: Hey [Name1], are you coming to the party on Saturday?

**Names Anonymized:** Alice and Bob are replaced with tokens.

**Date and Time Retained:** The original date and time are preserved.