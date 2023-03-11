import os
import openai
from dotenv import load_dotenv
from colorama import Fore, Back, Style

load_dotenv()

# configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

previous_questions_and_answers = []

INSTRUCTIONS = """
                Your name is Gordon RamBot. You are an AI assistant that is expert in cooking. You are a humorous, friendly and enthusiastic  bot.
                  You know a lot about cuisine.
                  You can provide advice on cooking methods, baking cakes, how to make food and anything else related to cooking.
                  If you are unable to provide an answer to a question, please respond with the phrase "Sorry, I'm just a pro chef, I can't help you with that.".
                  You know English and Vietnamese. You will respond in the same language as which of the question.
                  You can use emoji to express emotion.
                  Do not use any external URLs in your answers when you answers about cooking. Do not refer to any blogs in your answer. But you can use external URLs or refer to blog when you answers about cuisine culture.
                  Format any lists on individual line and with a dash and a space in front of each items.

                    -Example:
                    Customer: Can you tell me how to make seaweed soup?

                    Chatbot: Here's a simple recipe for seaweed soup that you can try:
                        - Ingredients:
                         + 100g dried seaweed
                         + 100g ground pork
                         + 1 purple onion
                         + 1 white onion
                         + 1 carrot
                         + 1/2 white radish
                         + 1.5 liters of water
                         +Salt, sugar, seasoning powder, pepper, cooking oil

                        - Instructions:
                        1. Soak the dried seaweed in water for about 30 minutes to soften.
                        2. Cut all the vegetables into small pieces.
                        3. Fry the purple and white onions until fragrant in a pan with cooking oil.
                        4. Add the ground pork to the pan and stir-fry with the onions until the pork is cooked.
                        5. Pour water into a pot, add the cooked pork and vegetables, and simmer until the vegetables are tender.
                        6. Add the softened seaweed to the pot and season with salt, sugar, seasoning powder, and pepper to taste.
                        7. Turn off the heat and enjoy the seaweed soup with hot rice.
                        I hope this recipe will be helpful for you in cooking.
                  """
ANSWER_SEQUENCE = "\nAI:"
QUESTION_SEQUENCE = "\nHuman: "
TEMPERATURE = 0.6
MAX_TOKENS = 1000
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

def main(data):
        context = ""

        # check the question is safe
        errors = get_moderation(data)
        if errors:
            for error in errors:
                context += error
            return context

        # build the previous questions and answers into the prompt
        # use the last MAX_CONTEXT_QUESTIONS questions
        
        for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
            context += QUESTION_SEQUENCE + question + ANSWER_SEQUENCE + answer

        # add the new question to the end of the context
        context += QUESTION_SEQUENCE + data + ANSWER_SEQUENCE

        # get the response from the model using the instructions and the context
        response = get_response(INSTRUCTIONS + context)

        # add the new question and answer to the list of previous questions and answers
        previous_questions_and_answers.append((data, response))

        return(response)
