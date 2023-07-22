import sys
sys.path.append("../FlagData")
import flagdata
from flagdata.cleaner.text_cleaner import DataCleaner
import json
import os
import yaml

def load_filter_words(file_path):
    with open(file_path, "r") as file:
        filter_words = set(word.strip() for word in file)
    return filter_words


def contains_filter_words(sentence, filter_words):
    for word in filter_words:
        if word in sentence:
            return True
    return False
def read_config(config_path: str):
    with open(config_path, "r", encoding="utf8") as fr:
        return yaml.safe_load(fr)

if __name__ == "__main__":
    #This is the first step, to clean the raw txt data from webpages or books
    #cleaner = DataCleaner("cleaner.yaml")
    #cleaner.clean() #To use flagdata

    #This is the second step, to merge the each cleanedContent in jsonl file into one
    config = read_config("cleaner.yaml")
    merge_src_path = config["basic"].get("output")

    filter_file_path = "filter_out.txt"
    # 加载过滤词列表
    filter_words = load_filter_words(filter_file_path)
    cleaned_contents = ""
    id_prefix = "warehouse-0-"
    i = 0
    with open("traindata_merge.jsonl", "w", encoding="utf-8") as fw:

        for merge_src_file in os.listdir(merge_src_path):
            full_path = os.path.join(merge_src_path, merge_src_file)
            with open(full_path, "r", encoding="utf-8") as f:
                i = i+1
                print(merge_src_file)
                data_list = {}
                data_list["title"] = ""
                data_list["id"] = ""
                data_list["meta"] = {}
                data_list["text"] = ""
                cleaned_contents = ""
                for line in f:
                    data = json.loads(line)
                    cleaned_content = data.get("cleanedContent", "")
                    # 检查输入句子是否包含过滤词
                    if len(cleaned_content) == 0:
                        continue
                    if not contains_filter_words(cleaned_content, filter_words):
                        cleaned_contents = cleaned_contents + cleaned_content + "\n"
                    else:
                        print("to filter out: ", cleaned_content)
            data_list["id"] = id_prefix + str(i)
            data_list["text"] = cleaned_contents
            print(cleaned_contents)
            json.dump(data_list, fw, ensure_ascii=False)
            fw.write("\n")





