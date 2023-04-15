import os
import json
import openai

TOKEN = ''

class Copilot:

    def clear_text(self, text):
        a = text.replace("\n", " ")
        b = a.split()
        c = " ".join(b)

        return c

    def get_answer(self, question):
        prompt = question
        
        openai.api_key = TOKEN
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=512,
            temperature=0.5,
        )

        json_object = response

        # Convert the JSON object to a JSON string
        json_string = json.dumps(json_object)

        # Parse the JSON string using json.loads()
        parsed_json = json.loads(json_string)

        text = parsed_json['choices'][0]['text']
        cleared_text = self.clear_text(text)
        
        return cleared_text

    def gpt_3(self, question):
        prompt = question
        messages = []
        messages.append({"role": "user", "content": prompt})

        openai.api_key = TOKEN
        completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                n=2,
                )
        
        chat_response = completion.choices[0].message.content
        lst = [chat_response.split("\n")]
        # cleared_text = self.clear_text(chat_response)

        return completion

    def get_image(self, question):
        prompt = question

        openai.api_key = TOKEN
        completion = openai.Image.create(
                prompt=prompt,
                n=2,
                size="256x256",
                )

        return completion['data'][0]


# a = Copilot()

# print(a.gpt_3("flip a coin"))
