from chatgpt import ChatGPT, MessageGenerator


class PaperAssistant():

    def paper_summary_chatgpt(self, paper):
        prompt = MessageGenerator()
        openai_chatgpt = ChatGPT()
        summary = openai_chatgpt.request(prompt.get_paper_summary_prompt(paper.fields, paper.query_text_summary))

        summary_method = openai_chatgpt.request(
            prompt.get_paper_summary_prompt(paper.fields,
                                            f"<Summary> {summary}, " + paper.query_text_method))

        summary_method_cons = openai_chatgpt.request(
            prompt.get_paper_summary_prompt(paper.fields,
                                            f"<Summary> {summary}, \n\n<Method Summary> {summary_method}\n\n " + paper.query_text_conclusion))

        data = [summary, "\n"*4, summary_method, "\n"*4, summary_method_cons]
        return "\n".join(data)
