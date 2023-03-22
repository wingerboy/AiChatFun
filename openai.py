import openai
from logging import log


class OpenAi:
    def __init__(self,
                 model,
                 prompt,
                 max_tokens,
                 temperature=0.9,
                 frequency_penalty=0,
                 presence_penalty=0):
        self.model = model
        self.prompt = prompt
        self.tokens = max_tokens
        self.temperature = temperature
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self._set_message()

    def __call__(self):
        response = openai.ChatCompletion.create(
            model=self.model,
            # prompt需要用英语替换，少占用token。
            messages=self.messages,
        )
        result = ''
        for choice in response.choices:
            result += choice.message.content
        log.info(f"summary_result:{result}", )
        log.info(f"prompt_token_used: {response.usage.prompt_tokens}, "
                 f"completion_token_used:, {response.usage.completion_tokens}, "
                 f"total_token_used:, {response.usage.total_tokens}")
        log.info(f"response_time: {response.response_ms / 1000.0}s")
        return result

    def _set_message(self):
        self.messages = {
                            "model": "text-davinci-003",
                            "prompt": self.prompt,
                            "max_tokens": self.tokens,
                            "temperature": self.temperature,
                            "frequency_penalty": self.frequency_penalty,
                            "presence_penalty": self.presence_penalty
                        }


class PaperSummMessage():
    def __init__(self,
                 key_word,
                 language
                 ):
        self.key_word = key_word
        self.language = language
        self.messages = [
                {"role": "system",
                 "content": "You are a reviewer in the field of [" + self.key_word + "] and you need to critically review this article"},
                # chatgpt 角色
                {"role": "assistant",
                 "content": "This is the <summary> and <conclusion> part of an English literature, where <summary> you have already summarized, but <conclusion> part, I need your help to summarize the following questions:" + clip_text},
                # 背景知识，可以参考OpenReview的审稿流程
                {"role": "user", "content": """                 
                             8. Make the following summary.Be sure to use {} answers (proper nouns need to be marked in English).
                                - (1):What is the significance of this piece of work?
                                - (2):Summarize the strengths and weaknesses of this article in three dimensions: innovation point, performance, and workload.                   
                                .......
                             Follow the format of the output later: 
                             8. Conclusion: \n\n
                                - (1):xxx;\n                     
                                - (2):Innovation point: xxx; Performance: xxx; Workload: xxx;\n                      
            
                             Be sure to use {} answers (proper nouns need to be marked in English), statements as concise and academic as possible, do not repeat the content of the previous <summary>, the value of the use of the original numbers, be sure to strictly follow the format, the corresponding content output to xxx, in accordance with \n line feed, ....... means fill in according to the actual requirements, if not, you can not write.                 
                             """.format(self.language, self.language)}
                ]

