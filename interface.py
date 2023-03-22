import tenacity


class PaperAssistant():
    def __init__(self,
                 paper,
                 ):
        self.paper = paper

    def conclusion(self):
        # 第一步先用title，abs，和introduction进行总结。
        text = ''
        text += 'Title:' + self.paper.title
        text += 'Url:' + self.paper.url
        text += 'Abstrat:' + self.paper.abs
        text += 'Paper_info:' + self.paper.section_text_dict['paper_info']
        # intro
        text += list(self.paper.section_text_dict.values())[0]

        chat_summary_text = self.chat_summary(text=text)

        # 由于图像信息不重要，还经常报错，我把这段内容注释掉。
        #             # TODO 往md文档中插入论文里的像素最大的一张图片，这个方案可以弄的更加智能一些：
        #             first_image, ext = paper.get_image_path()
        #             if first_image is None or self.gitee_key == '':
        #                 pass
        #             else:
        #                 image_title = self.validateTitle(paper.title)
        #                 image_url = self.upload_gitee(image_path=first_image, image_name=image_title, ext=ext)
        #                 htmls.append("\n\n")
        #                 htmls.append("![Fig]("+image_url+")")
        #                 htmls.append("\n\n")
        # 第二步总结方法：
        # TODO，由于有些文章的方法章节名是算法名，所以简单的通过关键词来筛选，很难获取，后面需要用其他的方案去优化。
        method_key = ''
        for parse_key in self.paper.section_text_dict.keys():
            if 'method' in parse_key.lower() or 'approach' in parse_key.lower():
                method_key = parse_key
                break

        if method_key != '':
            text = ''
            method_text = ''
            summary_text = ''
            summary_text += "<summary>" + chat_summary_text
            # methods
            method_text += self.paper.section_text_dict[method_key]
            text = summary_text + "\n\n<Methods>:\n\n" + method_text
            chat_method_text = self.chat_method(text=text)
        else:
            chat_method_text = ''

        # 第三步总结全文，并打分：
        conclusion_key = ''
        for parse_key in self.paper.section_text_dict.keys():
            if 'conclu' in parse_key.lower():
                conclusion_key = parse_key
                break

        text = ''
        conclusion_text = ''
        summary_text = ''
        summary_text += "<summary>" + chat_summary_text + "\n <Method summary>:\n" + chat_method_text
        if conclusion_key != '':
            # conclusion
            conclusion_text += self.paper.section_text_dict[conclusion_key]
            text = summary_text + "\n\n<Conclusion>:\n\n" + conclusion_text
        else:
            text = summary_text
        chat_conclusion_text = self.chat_conclusion(text=text)

    @tenacity.retry(wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
                    stop=tenacity.stop_after_attempt(5),
                    reraise=True)
    def try_download_pdf(self, result, path, pdf_name):
        result.download_pdf(path, filename=pdf_name)

    def download_pdf(self, filter_results):
        # 先创建文件夹
        date_str = str(datetime.datetime.now())[:13].replace(' ', '-')
        key_word = str(self.key_word.replace(':', ' '))
        path = self.root_path + 'pdf_files/' + self.query.replace('au: ', '').replace('title: ', '').replace('ti: ',
                                                                                                             '').replace(
            ':', ' ')[:25] + '-' + date_str
        try:
            os.makedirs(path)
        except:
            pass
        print("All_paper:", len(filter_results))
        # 开始下载：
        paper_list = []
        for r_index, result in enumerate(filter_results):
            try:
                title_str = self.validateTitle(result.title)
                pdf_name = title_str + '.pdf'
                # result.download_pdf(path, filename=pdf_name)
                self.try_download_pdf(result, path, pdf_name)
                paper_path = os.path.join(path, pdf_name)
                print("paper_path:", paper_path)
                paper = Paper(path=paper_path,
                              url=result.entry_id,
                              title=result.title,
                              abs=result.summary.replace('-\n', '-').replace('\n', ' '),
                              authers=[str(aut) for aut in result.authors],
                              )
                # 下载完毕，开始解析：
                paper.parse_pdf()
                paper_list.append(paper)
            except Exception as e:
                print("download_error:", e)
                pass
        return paper_list