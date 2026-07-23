from openai import OpenAI
from config import OPENAI_KEY


client=OpenAI(
    api_key=OPENAI_KEY
)



def analyze(text):


    prompt=f"""

Analyzuj tento článek.

Vrať JSON:

{{
"summary":"",
"sentiment":"",
"relevance":0
}}

Sentiment:
positive
neutral
negative

Článek:

{text}

"""


    response=client.chat.completions.create(

        model="gpt-5.5-mini",

        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]

    )


    return response.choices[0].message.content
