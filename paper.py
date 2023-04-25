import fitz
import re
import tiktoken
from PIL import Image
from config import conf
from logger import log


class Paper(object):
    def __init__(self,
                 download_url='',
                 file_path='',
                 key_words=['machine Learning', 'artificial intelligence']):
        self.paper_section_set = ["Abstract", 'Introduction', 'Related Work', 'Background',
                                "Preliminary", "Problem Formulation",'Methods', 'Methodology',
                                "Method", 'Approach', 'Approaches', "Materials and Methods",
                                "Experiment Settings", "Experiment", "Experimental Results",
                                "Evaluation", "Experiments","Results", 'Findings', 'Data Analysis',
                                "Discussion", "Results and Discussion", "Conclusion",'References',
                                'Supplementary Overview', 'Keywords', 'Key Words']
        self.paper_file = ''
        if file_path == '':
            self.paper_file = self.download_from_url(download_url)
        else:
            self.paper_file = file_path
        self.msg = {'ret': 0, 'msg': []}
        self.paper_pdf = fitz.open(self.paper_file)
        self.paper_url = download_url
        self.fields = key_words
        self.paper_sections = []
        self.paper_title = self._extract_title()
        self.paper_chapters = self._extract_chapters()

        self.paper_section2text = self._extract_section_dict()
        self.paper_section2text.update({'Title': self.paper_title})
        self.paper_images = None
        self.paper_author = []
        self.paper_institution = []
        self.paper_abstract = ''
        self.paper_introduction = ''
        self.paper_method = ''
        self.paper_conclusion = ''
        self.paper_related_work = ''
        self._paper_chapters_alignment()
        self.query_text_summary = self._get_query_summary()
        self.query_text_method = self._get_query_method()
        self.query_text_conclusion = self._get_query_conclusion()
        log.debug(f"paper_title: {self.paper_title},\n "
                f"paper_chapters: {self.paper_chapters},\n "
                f"paper_section2text: {self.paper_section2text.keys()},\n ")
        self.paper_pdf.close()

    def _extract_title(self):
        max_font_size = 0  # 初始化最大字体大小为0
        max_font_sizes = [0]
        abstract_font_size = 0
        for page_index, page in enumerate(self.paper_pdf):  # 遍历每一页
            text = page.get_text("dict")  # 获取页面上的文本信息
            blocks = text["blocks"]  # 获取文本块列表
            for block in blocks:  # 遍历每个文本块
                if block["type"] == 0 and len(block['lines']):  # 如果是文字类型
                    if len(block["lines"][0]["spans"]):
                        font_size = block["lines"][0]["spans"][0]["size"]  # 获取第一行第一段文字的字体大小
                        if block["lines"][0]["spans"][0]["text"] == 'Abstract':
                            abstract_font_size = font_size
                        max_font_sizes.append(font_size)
                        if font_size > max_font_size:  # 如果字体大小大于当前最大值
                            max_font_size = font_size  # 更新最大值
        max_font_sizes.sort()
        cur_title = ''
        for page_index, page in enumerate(self.paper_pdf):  # 遍历每一页
            text = page.get_text("dict")  # 获取页面上的文本信息
            blocks = text["blocks"]  # 获取文本块列表
            for block in blocks:  # 遍历每个文本块
                if block["type"] == 0 and len(block['lines']):  # 如果是文字类型
                    if len(block["lines"][0]["spans"]):
                        cur_string = block["lines"][0]["spans"][0]["text"]  # 更新最大值对应的字符串
                        font_size = block["lines"][0]["spans"][0]["size"]  # 获取第一行第一段文字的字体大小
                        if font_size == abstract_font_size:
                            for word in self.paper_section_set:
                                if cur_string.lower().find(word.lower()) < 0:
                                    continue
                                if cur_string[cur_string.lower().find(word.lower()):].lower() == word.lower():
                                    self.paper_sections.append(word)
                        if abs(font_size - max_font_sizes[-1]) < 0.3 or abs(font_size - max_font_sizes[-2]) < 0.3:
                            if len(cur_string) > 4 and "arXiv" not in cur_string:
                                if cur_title == '':
                                    cur_title += cur_string
                                else:
                                    cur_title += ' ' + cur_string
        title = cur_title.replace('\n', ' ')
        return title

    def _paper_chapters_alignment(self,):
        result = ''
        has_method = False
        unknow_sec = []
        for sec in self.paper_chapters:
            if 'abstract' in sec.lower():
                self.paper_abstract = self.paper_section2text[sec]
            if 'introduction' in sec.lower():
                self.paper_introduction = self.paper_section2text[sec]
            if 'related work' in sec.lower():
                self.paper_related_work = self.paper_section2text[sec]
            if 'method' in sec.lower() or 'methodology' in sec.lower() or 'approach' in sec.lower():
                has_method = False
                self.paper_method = self.paper_section2text[sec]
            if 'conclusion' in sec.lower():
                self.paper_conclusion = self.paper_section2text[sec]
            if 'result' in sec.lower() or 'discuss' in sec.lower():
                result = self.paper_section2text[sec]

            sec_tmp = re.sub(r'^(I{1,3}|IV|V|VI{1,3}|IIX|IX|X)+|\.', '', re.sub(r'\d+|\.', '', sec)).strip().title()
            if sec_tmp not in self.paper_section_set:
                unknow_sec.append(sec)

        if len(unknow_sec) > 0 and len(self.paper_method) < 10:
            self.paper_method = '\n'.join([self.paper_section2text[s] for s in unknow_sec])
        
        self.paper_conclusion = result + '\n' + self.paper_conclusion

        if len(self.paper_abstract) < 10:
            self.msg['msg'].append("can't extract abstract! ")  
        if len(self.paper_introduction) < 10:
            self.msg['msg'].append("can't extract paper introduction! ")   
        if len(self.paper_related_work) < 10:
            self.msg['msg'].append("can't extract paper related work! ")  
        if len(self.paper_method) < 10:
            self.msg['msg'].append("can't extract paper method! ")  
        if len(self.paper_conclusion) < 10:
            self.msg['msg'].append("can't extract paper conclusion! ")         

    def _extract_section_dict(self):
        section_dict = {}
        text = ""
        for page in self.paper_pdf:
            text += page.get_text()
        text = text.replace("\n", " ")
        for ind in range(len(self.paper_chapters)):
            if ind < len(self.paper_chapters)-1:
                section_dict[self.paper_chapters[ind]] = text[text.find(self.paper_chapters[ind]):text.find(self.paper_chapters[ind+1])]
            else:
                section_dict[self.paper_chapters[ind]] = text[text.find(self.paper_chapters[ind]):]
        
        # print("section_dict list extract from paper: ", section_dict.keys())
        return section_dict

    def _extract_chapters(self, ):
        h1_examples = 'INTRODUCTION'
        h1_list = []
        digit_num = [str(d + 1) for d in range(10)]
        roman_num = ["I", "II", 'III', "IV", "V", "VI", "VII", "VIII", "IIX", "IX", "X"]
        intro_h1 = ''
        intro_font = ''
        intro_font_size = 0
        has_intro = False
        for page_index, page in enumerate(self.paper_pdf):  # 遍历每一页
            text = page.get_text("dict")  # 获取页面上的文本信息
            blocks = text["blocks"]  # 获取文本块列表
            # 寻找INTRODUCTION
            for block in blocks:  # 遍历每个文本块
                if block["type"] == 0 and len(block['lines']):  # 如果是文字类型
                    if len(block["lines"][0]["spans"]):
                        block_text = ' '.join([l["spans"][0]["text"] for l in block["lines"]])
                        for line in block["lines"]:
                            line_text = line["spans"][0]["text"]
                            line_font = line["spans"][0]["font"]
                            line_font_size = line["spans"][0]["size"]
                            if h1_examples == line_text.upper():
                                intro_font = line_font
                                intro_font_size = line_font_size
                                has_intro = True
                            if has_intro:break
                        if has_intro:break
            if has_intro:break
        if intro_font_size == 0:
            self.msg['ret'] = -1
            self.msg['msg'].append("can't find introduction !")
            return []
        # print(intro_font, intro_font_size)
        # 遍历寻找和inrtoduction相同字体和大小的标题
        for page_index, page in enumerate(self.paper_pdf):  # 遍历每一页
            text = page.get_text("dict")  # 获取页面上的文本信息
            blocks = text["blocks"]  # 获取文本块列表
            for block in blocks:  # 遍历每个文本块
                if block["type"] == 0 and len(block['lines']):  # 如果是文字类型
                    if len(block["lines"][0]["spans"]) > 0: 
                        h1_text = ' '.join([l["spans"][0]["text"] for l in block["lines"] if (len(l["spans"]) > 0 and l["spans"][0]["font"]==intro_font and l["spans"][0]["size"]==intro_font_size)])
                        if len(h1_text) > 0:
                            h1_list.append(h1_text)

        # print(h1_list)
        # 清除一些脏数据
        intro_h1 = [h for h in h1_list if h1_examples in h.upper()][0]   
        pattern = ''
        if re.match(r'^\d\. {0,2}[A-Z].*$', intro_h1):
            pattern = r'^\d\. {0,2}[A-Z].*$'
        elif re.match(r'^\d  {0,2}[A-Z].*$', intro_h1):
            pattern = r'^\d  {0,2}[A-Z].*$'
        elif re.match(r'^(I{1,3}|IV|V|VI{1,3}|IIX|IX|X)\. {0, 2}[A-Z].*$', intro_h1):
            pattern = r'^(I{1,3}|IV|V|VI{1,3}|IIX|IX|X)\. {0, 2}[A-Z].*$'
        elif re.match(r'^(I{1,3}|IV|V|VI{1,3}|IIX|IX|X) {1, 2}[A-Z].*$', intro_h1):
            pattern = r'^(I{1,3}|IV|V|VI{1,3}|IIX|IX|X) {1, 2}[A-Z].*$'
        else:
            self.msg['ret'] = -1
            self.msg['msg'].append("Can't match string pattern !")
            return []

        h1_list_new = []
        for h in h1_list:
            if 'abstract' in h.lower():
                h1_list_new.append(h)
            elif 'keywords' in h.lower() or 'key words' in h.lower():
                h1_list_new.append(h)
            elif 'acknowledgments' in h.lower():
                h1_list_new.append(h)       
            elif 'references' in h.lower():
                h1_list_new.append(h)
            elif re.match(pattern, h) is not None:
                h1_list_new.append(h)
            else:
                continue

        if 'abstract' not in ' '.join(h1_list_new).lower():
            h1_list_new.insert(0, 'Abstract')

        log.info(f"h1 list extract from paper: {h1_list_new}")
        # print("h1 list extract from paper: ", h1_list_new)
        return h1_list_new

    '''
    def _extract_chapters(self, ):
        digit_num = [str(d + 1) for d in range(10)]
        roman_num = ["I", "II", 'III', "IV", "V", "VI", "VII", "VIII", "IIX", "IX", "X"]
        text_list = [page.get_text() for page in self.paper_pdf]
        all_text = ''
        for text in text_list:
            all_text += text
        # # 创建一个空列表，用于存储章节名称
        chapter_names = []
        for line in all_text.split('\n'):
            line_list = line.split(' ')
            if '.' in line:
                point_split_list = line.split('.')
                space_split_list = line.split(' ')
                if 1 < len(space_split_list) < 5:
                    if 1 < len(point_split_list) < 5 and (
                            point_split_list[0] in roman_num or point_split_list[0] in digit_num):
                        chapter_names.append(line)

        return chapter_names

    '''
        
    '''
    def _extract_section_dict(self):
        """
            获取PDF文件中每个页面的文本信息，并将文本信息按照章节组织成字典返回。

            Returns:
                section_dict (dict): 每个章节的文本信息字典，key为章节名，value为章节文本。
        """
        text = ''
        text_list = []
        section_dict = {}
        section_page_dict = self._section_page_index()

        # 再处理其他章节：
        text_list = [page.get_text() for page in self.paper_pdf]
        for sec_index, sec_name in enumerate(section_page_dict):
            print(sec_index, sec_name, section_page_dict[sec_name])
            # 直接考虑后面的内容：
            start_page = section_page_dict[sec_name]
            if sec_index < len(list(section_page_dict.keys())) - 1:
                end_page = section_page_dict[list(section_page_dict.keys())[sec_index + 1]]
            else:
                end_page = len(text_list)
            cur_sec_text = ''
            if end_page - start_page == 0:
                if sec_index < len(list(section_page_dict.keys())) - 1:
                    next_sec = list(section_page_dict.keys())[sec_index + 1]
                    if text_list[start_page].find(sec_name) == -1:
                        start_i = text_list[start_page].find(sec_name.upper())
                    else:
                        start_i = text_list[start_page].find(sec_name)
                    if text_list[start_page].find(next_sec) == -1:
                        end_i = text_list[start_page].find(next_sec.upper())
                    else:
                        end_i = text_list[start_page].find(next_sec)
                    cur_sec_text += text_list[start_page][start_i:end_i]
            else:
                for page_i in range(start_page, end_page):
                    if page_i == start_page:
                        if text_list[start_page].find(sec_name) == -1:
                            start_i = text_list[start_page].find(sec_name.upper())
                        else:
                            start_i = text_list[start_page].find(sec_name)
                        cur_sec_text += text_list[page_i][start_i:]
                    elif page_i < end_page:
                        cur_sec_text += text_list[page_i]
                    elif page_i == end_page:
                        if sec_index < len(list(section_page_dict.keys())) - 1:
                            next_sec = list(section_page_dict.keys())[sec_index + 1]
                            if text_list[start_page].find(next_sec) == -1:
                                end_i = text_list[start_page].find(next_sec.upper())
                            else:
                                end_i = text_list[start_page].find(next_sec)
                            cur_sec_text += text_list[page_i][:end_i]
            section_dict[sec_name] = cur_sec_text.replace('-\n', '').replace('\n', ' ')
        return section_dict

    def _section_page_index(self):
        # 初始化一个字典来存储找到的章节和它们在文档中出现的页码
        section_page_dict = {}
        # 遍历每一页文档
        for page_index, page in enumerate(self.paper_pdf):
            # 获取当前页面的文本内容
            cur_text = page.get_text()
            # 遍历需要寻找的章节名称列表
            for section_name in self.paper_section_set:
                # 将章节名称转换成大写形式
                section_name_upper = section_name.upper()
                # 如果当前页面包含"Abstract"这个关键词
                if "Abstract" == section_name and section_name in cur_text:
                    # 将"Abstract"和它所在的页码加入字典中
                    section_page_dict[section_name] = page_index
                # 如果当前页面包含章节名称，则将章节名称和它所在的页码加入字典中
                else:
                    if section_name + '\n' in cur_text:
                        section_page_dict[section_name] = page_index
                    elif section_name_upper + '\n' in cur_text:
                        section_page_dict[section_name] = page_index
        # 返回所有找到的章节名称及它们在文档中出现的页码
        return section_page_dict

    '''

    def _get_query_summary(self):
        '''
        通过论文的
        :return:
        '''
        text = ''
        text += 'Title:' + self.paper_title
        text += 'Url:' + self.paper_url
        text += 'Abstrat:' + self.paper_abstract
        text += 'Introduction:' + self.paper_introduction
        return text

    def _get_query_method(self):
        '''
        通过论文的
        :return:
        '''

        method_text = "\n\n<Methods>:\n\n" + self.paper_conclusion
        return method_text

    def _get_query_conclusion(self):
        '''
        通过论文的
        :return:
        '''

        text = "\n\n<Conclusion>:\n\n" + self.paper_conclusion
        return text

    def download_from_url(self, url, target_name="test.pdf"):
        import requests

        """ 根据论文id将论文下载到本地

        Parameters
        -----------
        paper_id: str
            论文id
        file_name: Optional[str]
            本地文件名，如果为空则用论文id做文件名

        Returns
        -------
        result: Optional[str]
            论文下载结果。成功则返回本地文件路径，失败则返回None
        """
        # paper_url = "https://arxiv.org/pdf/2303.12060.pdf"

        res = requests.get(url=url)
        if res.status_code == 200:
            with open(target_name, "wb") as f:
                f.write(res.content)
                return target_name
        return None


# class ArxivPaper(Paper):
#     '''
#     输入：路径
#     输出：论文内容
#     '''
#     def __init__(self,
#                  url,
#                  path=None):
#         file_path = ''
#         if not path:
#             file_path = self.download_from_url(url)
#         else:
#             file_path = path
#         # assert self.file_path is None, "path is null"
#         super(Paper, self).__init__(file_path)     # 遍历当前页面所有图片

    



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--file', default='', required=False)    # 位置参数
    parser.add_argument('--url', default='', required=False)  # 可选参数

    args = parser.parse_args()

    paper = None
    if args.file == '' and args.url == '':
        print("please input param! ")
        Paper(file_path="/Users/wingerliu/Downloads/github/test/1909.03184.pdf")
    elif args.file == '':
        paper = Paper(download_url=args.url)
    else:
        paper = Paper(file_path=args.file)
    
    print(">>>>>Title: ", paper.paper_title)
    print(">>>>>Paper Chapters: ", paper.paper_chapters)
    print(">>>>>Paper keys: ", paper.paper_section2text.keys())
    print(">>>>>Paper msg: ", paper.msg)

    print(">>>>>Paper abstract: ", paper.paper_abstract)

    