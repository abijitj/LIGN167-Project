# LIGN 167 LLM Application Project

## How to run: 
- First, please paste your Open-AI API key into a `.env` file in the root directory of the project. It should look like this. 

```py
OPENAI_API_KEY="[insert key here]"
```

- Install all the python dependencies: `pip install -r requirements.txt`. You may also choose to install these within a virtual environment for best practice. 

- Run the streamlit frontend: `streamlit run pdf_reader.py`

- To run the chrome extension: 
  - First, start the Flask backend server: `python backend.py`
  - Two, open Google Chrome and go to your extension manager (type `chrome://extensions/` in the search bar). Then click on "Load unpacked" on the top left and select the "chrome-extension" folder that is in this directory. Finally, activate this extension. 
  - Now, you should be able to go the media gallery of any UCSD class on Canvas to see the extension work. 

## Disclaimer:

- The code is a mixture of that written by our group members and that created using ChatGPT and Colab. This is noted in the code itself.

- `manifest.json` was also created using ChatGPT but comments aren't included in the JSON.

- The raw transcript example is downloaded from UCSD Professor Jason Fleischer's public YouTube lecture on ML for Cogs 118A: https://www.youtube.com/watch?v=Z1jwmbABdFA
