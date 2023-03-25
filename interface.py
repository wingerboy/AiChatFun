from chatgpt import ChatGPT, MessageGenerator
from paper import Paper


class PaperAssistant():

    def paper_summary_chatgpt(self, paper):
        prompt = MessageGenerator()
        openai_chatgpt = ChatGPT()
        # 第一步先用title，abs，和introduction进行总结。
        summary = openai_chatgpt.request(prompt.get_paper_summary_prompt(paper.fields, paper.query_text_summary))

        # 第二步总结方法：
        # TODO，由于有些文章的方法章节名是算法名，所以简单的通过关键词来筛选，很难获取，后面需要用其他的方案去优化。
        summary_method = openai_chatgpt.request(
            prompt.get_paper_method_prompt(paper.fields,
                                            f"<Summary> {summary}, " + paper.query_text_method))

        # 第三步总结全文，并打分：
        summary_method_cons = openai_chatgpt.request(
            prompt.get_paper_conclusion_prompt(paper.fields,
                                            f"<Summary> {summary}, \n\n<Method Summary> {summary_method}\n\n " + paper.query_text_conclusion))

        data = [summary, "\n", summary_method, "\n", summary_method_cons]
        return "\n".join(data)


if __name__ == "__main__":

    print(PaperAssistant().paper_summary_chatgpt(Paper(file_path='test.pdf')))
