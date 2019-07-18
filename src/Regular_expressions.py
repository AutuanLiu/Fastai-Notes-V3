import re

# 同时提取 月 日
regex = r"^([a-zA-Z]+) (\d+)$"    # 必须使用 raw string
if re.search(regex, "June 24"):
    match = re.search(regex, "June 24")

    print("Match at index %s, %s" % (match.start(), match.end()))

    #    match.group(0)，match.group()  全部提取信息
    #    match.group(1), match.group(2), ... 从左到右返回提取信息
    print("Full match: %s" % (match.group(0)))
    print("Month: %s" % (match.group(1)))
    print("Day: %s" % (match.group(2)))
else:
    print("The regex pattern does not match. :(")

regex = r"^[a-zA-Z]+ \d+$"
# 找出所有匹配信息
matches = re.findall(regex, "June 24, August 9, Dec 12")
for match in matches:
    print("Full match: %s" % (match))

# 提取月
regex = r"([a-zA-Z]+) \d+"
matches = re.findall(regex, "June 24, August 9, Dec 12")
for match in matches:
    print("Match month: %s" % (match))

regex = r"([a-zA-Z]+) \d+"
# 返回匹配的开始 结束位置
matches = re.finditer(regex, "June 24, August 9, Dec 12")
for match in matches:
    print("Match at index: %s, %s" % (match.start(), match.end()))

regex = r"([a-zA-Z]+) (\d+)"
regex1 = r"\2 of \1"

# 替换提取到的信息为新的模式
print(re.sub(regex, regex1, "June 24, August 9, Dec 12"))

regex = re.compile(r"(\w+) World")
result = regex.search("Hello World is the easiest")
if result:
    print(result.start(), result.end())

for result in regex.findall("Hello World, Bonjour World"):
    print(result)

print(regex.sub(r"\1 Earth", "Hello World"))
