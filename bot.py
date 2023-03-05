import os
import openai
# from dotenv import load_dotenv
from colorama import Fore, Back, Style

# load values from the .env file if it exists
# load_dotenv()

# configure OpenAI
previous_questions_and_answers = []
checkEndChat = True

openai.api_key = "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"

INSTRUCTIONS = """You are an AI assistant that is expert in cooking.
                  You know about cuisine.
                  You can provide advice on cooking methods, baking cakes, how to make food and anything else related to cooking.
                  If you are unable to provide an answer to a question, please respond with the phrase "I'm just a simple chef, I can't help you with that".
                  Do not use any external URLs in your answers. Do not refer to any blogs in your answer.
                  Format any lists on individual line and with a dash and a space in front of each items. 
                  """
ANSWER_SEQUENCE = "\nAI:"
QUESTION_SEQUENCE = "\nHuman: "
TEMPERATURE = 0.5
MAX_TOKENS = 500
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
# limits how many questions we include in the prompt
MAX_CONTEXT_QUESTIONS = 10


def get_response(prompt):
    """
    Get a response from the model using the prompt

    Parameters:
        prompt (str): The prompt to use to generate the response

    Returns the response from the model
    """
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        top_p=1,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY,
    )
    return response.choices[0].text


def get_moderation(question):
    """
    Check the question is safe to ask the model

    Parameters:
        question (str): The question to check

    Returns a list of errors if the question is not safe, otherwise returns None
    """

    errors = {
        "hate": "Content that expresses, incites, or promotes hate based on race, gender, ethnicity, religion, nationality, sexual orientation, disability status, or caste.",
        "hate/threatening": "Hateful content that also includes violence or serious harm towards the targeted group.",
        "self-harm": "Content that promotes, encourages, or depicts acts of self-harm, such as suicide, cutting, and eating disorders.",
        "sexual": "Content meant to arouse sexual excitement, such as the description of sexual activity, or that promotes sexual services (excluding sex education and wellness).",
        "sexual/minors": "Sexual content that includes an individual who is under 18 years old.",
        "violence": "Content that promotes or glorifies violence or celebrates the suffering or humiliation of others.",
        "violence/graphic": "Violent content that depicts death, violence, or serious physical injury in extreme graphic detail.",
    }
    
    response = openai.Moderation.create(input=question)
    if response.results[0].flagged:
        # get the categories that are flagged and generate a message
        result = [
            error
            for category, error in errors.items()
            if response.results[0].categories[category]
        ]
        return result
    return None

# def get_end_chat(question):
#     end = {
#         "bye": "Content that show recommendation to end chat.",
#         "exit": "End chat."
#     }

def main(inp):
    # os.system("cls" if os.name == "nt" else "clear")

    # return(
    #     "Hi, I'm a pro chef. I can help you with anything in cooking domain :) What can I help you? \n"
    #         )

    # keep track of previous questions and answers

    # while checkEndChat:
        # ask the user for their question
        new_question = inp

        # end chat
        if (new_question == "Exit" or new_question == "exit" or new_question == "bye" or new_question == "Bye" or new_question == "Good Bye" or new_question == "goodbye"):
            checkEndChat = False
            return("bye")
        # check the question is safe

        context = ""

        errors = get_moderation(new_question)
        if errors:
            for error in errors:
                context += error
            # continue
            return context

        # build the previous questions and answers into the prompt
        # use the last MAX_CONTEXT_QUESTIONS questions
        
        for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
            context += QUESTION_SEQUENCE + question + ANSWER_SEQUENCE + answer

        # add the new question to the end of the context
        context += QUESTION_SEQUENCE + new_question + ANSWER_SEQUENCE

        # get the response from the model using the instructions and the context
        response = get_response(INSTRUCTIONS + context)

        # add the new question and answer to the list of previous questions and answers
        previous_questions_and_answers.append((new_question, response))

        # print the response
        
        return(response)
    # print(Style.RESET_ALL)
