# Created using Copilot

with open('raw_transcript.txt', 'r') as file:
    transcript_text = file.readlines()
    print(' '.join([line[13:] for line in transcript_text]))