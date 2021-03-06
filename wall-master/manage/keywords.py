# -*- coding:utf-8 -*-
"""
    :基于DFA算法的敏感词检测
    :2022.4.12
    :数据集词库 keywords.txt
"""
import time
time1 = time.time()

# DFA算法
class DFAFilter():
    def __init__(self):
        self.keyword_chains = {}
        self.delimit = '\x00'

    def add(self, keyword):
        # keyword = keyword.lower()
        chars = keyword.strip()
        if not chars:
            return
        level = self.keyword_chains
        for i in range(len(chars)):
            if chars[i] in level:
                level = level[chars[i]]
            else:
                if not isinstance(level, dict):
                    break
                for j in range(i, len(chars)):
                    level[chars[j]] = {}
                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]
                last_level[last_char] = {self.delimit: 0}
                break
        if i == len(chars) - 1:
            level[self.delimit] = 0

    def parse(self, path):
        with open(path,encoding='utf-8') as f:
            for keyword in f:
                self.add(str(keyword).strip())

    def filter(self, message, repl="*"):
        message1 = message.lower()
        ret = []
        start = 0
        while start < len(message1):
            level = self.keyword_chains
            step_ins = 0
            for char in message1[start:]:
                if char in level:
                    step_ins += 1
                    if self.delimit not in level[char]:
                        level = level[char]
                    else:
                        ret.append(repl * step_ins)
                        start += step_ins - 1
                        break
                else:
                    ret.append(message[start])
                    break
            else:
                ret.append(message[start])
            start += 1

        return ''.join(ret)


# if __name__ == "__main__":
#     gfw = DFAFilter()
#     gfw.parse('keywords.txt')
#     text ="我日你奶奶"
#     result = gfw.filter(text)
#
#     print(text)
#     print(result)
#     time2 = time.time()
#     print('总共耗时：' + str(time2 - time1) + 's')
