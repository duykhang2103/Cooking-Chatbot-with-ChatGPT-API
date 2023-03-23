# chatgpt

# Setup

Make sure you have python3 installed:

```
python3 --version
```

Create a virtual environment and install the dependencies:

### Windows:

```
python -m venv venv
venv\Scripts\activate.bat
pip install openai
pip install flask
pip install python-dotenv
pip install colorama
```

# Configuration

Copy `env.sample` to `.env` and add your OpenAI API key to the file.

```
OPENAI_API_KEY=<<YOUR_API_KEY>>
```

Edit `bot.py` and replace `<<PUT THE PROMPT HERE>>` with your prompt:


# Running

To run just do the following:

### Windows:

```
venv\Scripts\activate.bat
flask run
```

![image](https://user-images.githubusercontent.com/93172216/227234243-82e1e477-171a-42d7-a4f2-e2f374f4d982.png)
