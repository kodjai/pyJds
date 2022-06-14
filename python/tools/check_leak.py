import argparse
import re
from typing import List


def read_log(fname):
    l_match = []
    with open(fname) as f:
        for s_line in f:
            if "cid_" in s_line:
                # print(s_line)
                l_match.append(s_line)

    return l_match


def extract_cid(logs: List[str]):
    for log in logs:
        m = re.findall(".*cid_ *(.*)", log)
        if m != None:
            print(m[0])
            # print(type(m[0]))


def check_cid(logs: List[str]):
    d_cid = {}
    for log in logs:
        m = re.findall(".*cid_\\((.*)\\)", log)
        # m = re.findall("/(?<=\\(]).*?(?=\\))/", log)
        if m != None:
            a = m[0]
            if a == "1644902040235607":
                x = 1
            if d_cid.get(m[0]) == None:
                d_cid[m[0]] = log
            else:
                d_cid.pop(m[0])

    for l in d_cid.values():
        print(l)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="memory leack check from log")
    parser.add_argument("filename", help="解析対象logファイル")
    # args = parser.parse_args()
    # l_has_cid = read_log(args.filename)
    l_has_cid = read_log("./aaa222.log")
    check_cid(l_has_cid)
