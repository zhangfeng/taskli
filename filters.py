import re

dot_re = re.compile(r"\s*\. (.+)")

def dot_cmd(line):
    m = dot_re.match(line)
    if m:
        return 'add ' + m[1]
    return line


