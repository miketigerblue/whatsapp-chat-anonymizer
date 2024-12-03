#!/usr/bin/env python3
import re
import argparse
import pandas as pd
import spacy

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

def parse_chat(file_content):
    """
    Parse WhatsApp chat text into a pandas DataFrame.
    """
    pattern = re.compile(
        r'^\[(?P<date>\d{1,2}/\d{1,2}/\d{2,4}), (?P<time>\d{1,2}:\d{2}(?::\d{2})?(?:\s?[AP]M)?)\] (?P<sender>.*?): (?P<message>.*)',
        re.MULTILINE
    )
    data = pattern.findall(file_content)
    df = pd.DataFrame(data, columns=['date', 'time', 'sender', 'message'])
    return df

def anonymize_pii(df):
    """
    Anonymize PII in the DataFrame while retaining date and time.
    """
    # Retain date and time by not modifying df['date'] and df['time']
    
    # Map senders to consistent tokens
    sender_map = {sender: f'[Person{i+1}]' for i, sender in enumerate(df['sender'].unique())}
    df['sender'] = df['sender'].map(sender_map)
    
    # Anonymize message content
    df['message'] = df['message'].apply(anonymize_message)
    
    return df

def anonymize_message(message):
    """
    Anonymize PII in a single message.
    """
    doc = nlp(message)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    # Create mappings for names and other entities
    name_counter = 1
    name_map = {}
    
    for text, label in entities:
        if label == 'PERSON' and text not in name_map:
            name_map[text] = f'[Name{name_counter}]'
            name_counter += 1
        
        # You can add more entity types to anonymize if needed
        # For example, to anonymize locations:
        # if label == 'GPE' and text not in location_map:
        #     location_map[text] = f'[Location{location_counter}]'
        #     location_counter += 1
    
    for name, token in name_map.items():
        pattern = re.compile(r'\b{}\b'.format(re.escape(name)))
        message = pattern.sub(token, message)
    
    # Anonymize emails and phone numbers
    message = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', '[EMAIL]', message)
    message = re.sub(r'\b\d{10,}\b', '[PHONE_NUMBER]', message)
    
    return message

def reconstruct_chat(df):
    """
    Reconstruct chat text from the DataFrame.
    """
    chat_lines = df.apply(lambda row: f'[{row["date"]}, {row["time"]}] {row["sender"]}: {row["message"]}', axis=1)
    return '\n'.join(chat_lines)

def main():
    parser = argparse.ArgumentParser(description='Anonymize WhatsApp chat data.')
    parser.add_argument('input_file', help='Path to the WhatsApp .txt file.')
    parser.add_argument('-o', '--output_file', default='anonymized_chat.txt', help='Output file name.')
    args = parser.parse_args()
    
    # Read input file
    with open(args.input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse, anonymize, and reconstruct chat
    df = parse_chat(content)
    df = anonymize_pii(df)
    anonymized_chat = reconstruct_chat(df)
    
    # Write to output file
    with open(args.output_file, 'w', encoding='utf-8') as f:
        f.write(anonymized_chat)
    
    print(f'Anonymized chat saved to {args.output_file}')

if __name__ == '__main__':
    main()
