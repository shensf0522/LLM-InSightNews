import re

def parse_text(text):
    '''
    对大模型分析后的文本进行特定格式解析
    :param text:
    :return: 分析结果（字典）
    '''
    sections = re.split(r'(\[\w.*\]:|\n<\w.*>:)', text)
    result = {}
    current_key = "Category"
    result.setdefault(current_key, "")

    for section in sections:
        section = section.strip()
        if not section:
            continue
        if section.startswith('[') or section.startswith('<'):
            current_key = section[1:-2]
            result[current_key] = ''
        elif current_key:
            result[current_key] += section + '\n'
        else:
            # Handling sections that do not follow the "key: value" format
            if ':' in section:
                key, value = section.split(': ', 1)  # 初始为1
                result[key] = value
            else:
                print("the error section is:\n",section)
                result[current_key] = section.strip()
    return result

def parse_response_news(response_data: object) -> object:
    '''
    对于推荐新闻的处理结果进行解析
    :param response_data:
    :return: 获取到的候选新闻标题
    '''
    start_marker = "Recommend news:"
    end_marker = "Recommend news end"
    print(">>>>>>>>>>>>>>>>>>>>>>")
    print(response_data)
    print("<<<<<<<<<<<<<<<<<<<<<<<<")
    start_index = response_data.find(start_marker) + len(start_marker)
    end_index = response_data.find(end_marker)

    recommended_news_content = response_data[start_index:end_index].strip()
    print("获取分析的结果：\n",recommended_news_content)
    recommended_news_content = recommended_news_content.split('\n')
    print("推荐新闻内容：\n",recommended_news_content)

    # 将排序的内容中的非数字删除掉
    recommended_news_content = [re.sub(r'^[a-zA-Z]*(\d+)', lambda x: x.group(1), title) for title in recommended_news_content]
    # 对元素进行分割，并且按照索引，将小的序号放在前面
    sorted_titles = [title for _, title in sorted(enumerate(recommended_news_content), key=lambda x: int(x[1].split(":")[0]))]
    # 将排序的结果仅提取标题，用于进行和新闻id进行绑定
    cleaned_titles = [re.sub(r'：', ':', title) for title in sorted_titles]
    extracted_titles_only = [item.split(":")[1].strip() for item in cleaned_titles]
    # 去除掉重复的标题
    extracted_titles_only = list(set(extracted_titles_only))
    print("排序新闻内容：\n",extracted_titles_only)
    return extracted_titles_only

def parse_response_summary(data):
    start_index = data.find('[Summary]:')
    if start_index != -1:
        # 提取子字符串后的内容
        summary_content = data[start_index + len('[Summary]:'):].strip()
        return summary_content
    else:
        return "find failure!"