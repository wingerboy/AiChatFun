import openai
import tiktoken
from logger import log
from config import conf


class ChatGPT:
    def __init__(self,
                 model="gpt-3.5-turbo",
                 temperature=0.9,
                 frequency_penalty=0,
                 presence_penalty=0):
        self.model = model
        self.temperature = temperature
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty

    def request(self, messages):
        openai.api_key = ''
        response = openai.ChatCompletion.create(
            model=self.model,
            # prompt需要用英语替换，少占用token。
            messages=messages,
        )
        result = ''
        for choice in response.choices:
            result += choice.message.content
        log.info(f"response_time: {response.response_ms / 1000.0}s, "
                 f"prompt_token_used: {response.usage.prompt_tokens}, "
                 f"completion_token_used:, {response.usage.completion_tokens}, "
                 f"total_token_used:, {response.usage.total_tokens}")
        return result


class MessageGenerator:
    def __init__(self):
        self.encoding = tiktoken.get_encoding("gpt2")

    def get_paper_summary_prompt(self, fields, query_text):
        summary_prompt_token = 1000
        text_token = len(self.encoding.encode(query_text))
        clip_text_index = int(len(query_text) * (conf.openai_max_tokens - summary_prompt_token) / text_token)
        clip_text = query_text[:clip_text_index]

        prompt = [
            {"role": "system", "content": "You are a researcher in the field of [" + '/'.join(
                fields) + "] who is good at summarizing papers using concise statements"},
            {"role": "assistant",
             "content": "This is the title, author, link, abstract and introduction of an English document. I need your help to read and summarize the following questions: " + clip_text},
            {"role": "user", "content": f"""                 
                     1. Mark the title of the paper (with Chinese translation)
                     2. list all the authors' names (use English)
                     3. mark the first author's affiliation (output {conf.output_language} translation only)                 
                     4. mark the keywords of this article (use English)
                     5. link to the paper, Github code link (if available, fill in Github:None if not)
                     6. summarize according to the following four points.Be sure to use {conf.output_language} answers (proper nouns need to be marked in English)
                        - (1):What is the research background of this article?
                        - (2):What are the past methods? What are the problems with them? Is the approach well motivated?
                        - (3):What is the research methodology proposed in this paper?
                        - (4):On what task and what performance is achieved by the methods in this paper? Can the performance support their goals?
                     Follow the format of the output that follows:                  
                     1. Title: xxx\n\n
                     2. Authors: xxx\n\n
                     3. Affiliation: xxx\n\n                 
                     4. Keywords: xxx\n\n   
                     5. Urls: xxx or xxx , xxx \n\n      
                     6. Summary: \n\n
                        - (1):xxx;\n 
                        - (2):xxx;\n 
                        - (3):xxx;\n  
                        - (4):xxx.\n\n     

                     Be sure to use {conf.language} answers (proper nouns need to be marked in English), statements as concise and academic as possible, do not have too much repetitive information, numerical values using the original numbers, be sure to strictly follow the format, the corresponding content output to xxx, in accordance with \n line feed.                 
                     """},
        ]
        return prompt

    def get_paper_method_prompt(self, fields, query_text):
        summary_prompt_token = 1000
        text_token = len(self.encoding.encode(query_text))
        clip_text_index = int(len(query_text) * (conf.openai_max_tokens - summary_prompt_token) / text_token)
        clip_text = query_text[:clip_text_index]

        prompt = [
            {"role": "system", "content": "You are a researcher in the field of [" + '/'.join(
                fields) + "] who is good at summarizing papers using concise statements"},  # chatgpt 角色
            {"role": "assistant",
             "content": "This is the <summary> and <Method> part of an English document, where <summary> you have summarized, but the <Methods> part, I need your help to read and summarize the following questions." + clip_text},
            # 背景知识
            {"role": "user", "content": f"""                 
                     7. Describe in detail the methodological idea of this article. Be sure to use {conf.output_language} answers (proper nouns need to be marked in English). For example, its steps are.
                        - (1):...
                        - (2):...
                        - (3):...
                        - .......
                     Follow the format of the output that follows: 
                     7. Methods: \n\n
                        - (1):xxx;\n 
                        - (2):xxx;\n 
                        - (3):xxx;\n  
                        ....... \n\n     

                     Be sure to use {conf.output_language} answers (proper nouns need to be marked in English), statements as concise and academic as possible, do not repeat the content of the previous <summary>, the value of the use of the original numbers, be sure to strictly follow the format, the corresponding content output to xxx, in accordance with \n line feed, ....... means fill in according to the actual requirements, if not, you can not write.                 
                     """},
        ]
        return prompt

    def get_paper_conclusion_prompt(self, fields, query_text):
        summary_prompt_token = 1000
        text_token = len(self.encoding.encode(query_text))
        clip_text_index = int(len(query_text) * (conf.openai_max_tokens - summary_prompt_token) / text_token)
        clip_text = query_text[:clip_text_index]

        prompt = [
            {"role": "system",
             "content": "You are a reviewer in the field of [" + '/'.join(
                 fields) + "] and you need to critically review this article"},
            # chatgpt 角色
            {"role": "assistant",
             "content": "This is the <summary> and <conclusion> part of an English literature, where <summary> you have already summarized, but <conclusion> part, I need your help to summarize the following questions:" + clip_text},
            # 背景知识，可以参考OpenReview的审稿流程
            {"role": "user", "content": f"""                 
             8. Make the following summary.Be sure to use {conf.output_language} answers (proper nouns need to be marked in English).
                - (1):What is the significance of this piece of work?
                - (2):Summarize the strengths and weaknesses of this article in three dimensions: innovation point, performance, and workload.                   
                .......
             Follow the format of the output later: 
             8. Conclusion: \n\n
                - (1):xxx;\n                     
                - (2):Innovation point: xxx; Performance: xxx; Workload: xxx;\n                      

             Be sure to use {conf.output_language} answers (proper nouns need to be marked in English), statements as concise and academic as possible, do not repeat the content of the previous <summary>, the value of the use of the original numbers, be sure to strictly follow the format, the corresponding content output to xxx, in accordance with \n line feed, ....... means fill in according to the actual requirements, if not, you can not write.                 
             """}
        ]
        return prompt



