# Export-Grok-Advanced
By scraping the API to obtain the entire Response object, we can not only get complete conversation data, but the Response object even contains the web page content that Grok searches in the background.

## Project Vision
Since the founding of Elon Musk's XAI Grok, Musk's team has been pursuing a data monopoly, preventing many users from accessing their own data. This project aims to break Elon Musk's data monopoly.

## Introduce
This tool, written in Python, provides a dialogue capture tool and a dialogue visualization tool. "Export.py" is the dialogue capture tool, which saves the captured dialogues to a folder. Each dialogue is an independent file, with the filename being the dialogue title. All data is saved, including the web page content retrieved by Grok. "visual.py" is the visualization tool. After the dialogues are downloaded, you need to click the button to open the directory where the dialogues are stored. The sidebar will then load all the dialogues. When you click, the dialogue content will be displayed on the right, showing not only all the dialogues but also the web pages searched by Grok.

## How to use
Enter your cookies in the cookies3 field. Cookies can be obtained from Chrome's developer tools.
