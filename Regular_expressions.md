# 正则表达式

- [正则表达式](#%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F)
  - [基本内容](#%E5%9F%BA%E6%9C%AC%E5%86%85%E5%AE%B9)
  - [总结](#%E6%80%BB%E7%BB%93)
  - [Python3 的正则表达式](#python3-%E7%9A%84%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F)
    - [示例](#%E7%A4%BA%E4%BE%8B)
  - [参考文献](#%E5%8F%82%E8%80%83%E6%96%87%E7%8C%AE)

## 基本内容

正则表达式在从文本（如代码，日志文件，电子表格甚至文档）中提取信息时非常有用。使用正则表达式时首先要认识到的是，所有内容本质上都是一个字符，
我们通过编写模式以匹配特定的字符序列。 大多数模式使用普通的 ASCII 码，包括字母，数字，标点符号和键盘上的其他符号，如 `%$@!`，但是 unicode 字符也可用于匹配任何类型的国际文本。

1. `\d` 可用于代替 0 到 9 之间的任何数字。前面的斜杠将其与普通的 d 字符区分开来。` \d\d\d` 匹配任意三位数字。`\D` 可用于代替除了数字的任意字符。

2. 字符 `.` 可以匹配任何单个字符（字母，数字，空格，一切）。 您可能会注意到这实际上会覆盖句点字符的匹配，因此为了专门匹配句点，您需要使用斜杠 `\.` 来转义。

```bash
...\.  # 表示任意三个符号后面是一个 . 如 abd. 125.
```

3. 使用正则表达式匹配特定字符，方法是在**方括号**内定义它们。例如，模式 `[abc]` 只匹配单个 a，b 或 c 字母而不是其他内容。`[cmf]an` 表示第一个字母为 [c, m, f] 中的一个，
后两个字母是 an, 即匹配 can, mam, fan。

4. 使用方括号 `[]` 和 `^`(hat) 排除特定字符。例如，模式 `[^abc]` 将匹配**除**字母 a，b 或 c 之外的任何单个字符。`[^b]og` 表示不包含 bog。

5. 通过在**方括号**中使用**短划线**表示字符范围，来匹配连续字符列表中的字符。例如，模式 `[0-6]` 只匹配从 0 到 6 的任何单个数字字符，而不是其他任何字符。
同样，`[^n-p]` 只匹配除字母 n 到 p 之外的任何单个字符。

6. 多个字符范围也可以在**同一组括号**中使用，也可以与单个字符一起使用。一个例子是 `\w` ，它相当于字符范围 `[A-Za-z0-9_]`，通常用于匹配英文文本中的字符。

7. 使用**花括号**表示法指定我们想要的每个字符的重复次数。例如，`a{3}` 将恰好匹配 a 字符三次。某些正则表达式引擎甚至允许您为此重复指定一个**范围**，使得 `a{1,3}` 将匹配 a 字符不超过3次，但不得少于一次。
`[wxy]{5}` 表示匹配 5 次重复字符，每个字符可以是 w，x 或 y；`.{2,6}`表示匹配任意一个字符 2 到 6 次。

8. 正则表达式中的一个强大概念是能够**匹配任意数量**的字符。使用 `*` 表示有至少 0 个字符，使用 `+` 表示有至少 1 个字符。如 `\d*` 表示至少有 0 个数字（有可能没有数字），`\d+` 表示至少有 1 个数字。
`a+` 表示一个或者更多的 a，`[abc]+` 表示一个或者更多的 a，或 b 或 c，`.*` 表示 0 个或者多个任意字符。

9. `?` 用于代表**可选的**，允许匹配**前面**一个*字符或组中*的*零个或一个*字符。如 `ab?c` 表示匹配字符串 abc 或者 ac。使用 `\?` 表示真正的 `?`。

10. `\s` 表示任意的**空格**（空格 whitesapce，换行 `\n` 回车 `\r`）。`\d\.\s+abc` 可以表示 1. abc  2.        abc [示例](https://regexone.com/lesson/whitespaces?)

11. 尽可能地编写特定的正则表达式，以确保在匹配真实世界文本时不会出现误报。所以，通常使用 `^` 表示匹配输入字符串的开始位置（这和 `[^]` 含义是不同的），使用 `$` 表示匹配输入字符串的结束位置。`Mission:successful$` 表示以 Mission 开头，以 successful 结束。

12. 正则表达式不仅可以匹配文本，还可以提取信息以便进一步处理。这是通过定义**字符组 group**并使用特殊括号 `(and)` 来完成的。括号内的任何**子模式**将组合成一个组 group 进行匹配。 实际上，这可以用于从各种数据中提取电话号码或电子邮件等信息。
`^(IMG\d+\.png)$` 表示以 IMG 开头，中间是一个或多个数字，以 .png 结尾，提取整个文件名。而 `^(IMG\d+)\.png$` 只提取 . 之前的信息。

13. **Nested groups**: `^(IMG(\d+))\.png$` 不仅提取文件名，同时提取图片编号。内部嵌套的 group 模式是为了提取数字信息。嵌套组在模式中从左向右读取，第一个捕获的结果是第一个括号组的内容。**分别提取**

14. **全部提取**：`(\d+)x(\d+)` 提取分辨率的长度和宽度（1920x768）-> 1920 768[示例](https://regexone.com/lesson/more_groups)

15. 使用 `|` 表示逻辑或，如 `(milk|bread|juice)` 表示 milk，bread，juice 中的一种。

16. `\S` 表示任意非空格字符，`\W` 表示任意非字母字符，`\b` 匹配边界，`\1`, `\2` 用于引用通过组 group 捕获的内容， `\2-\1` 表示互换捕获内容的位置。

## 总结

|符号|含义|
|---|---|
|`\d`|用于代替 0 到 9 之间的任何数字|
|`.`|可以匹配任何单个字符|
|`[]`|匹配特定字符|
|`[^]`|排除特定字符|
|`[a-c]`|匹配特定字符范围|
|`[^n-p]`|排除特定字符范围|
|`{3}`|字符的重复次数|
|`{3,6}`|字符的重复次数的范围|
|`*`|至少 0 个字符|
|`+`|至少 1 个字符|
|`?`|代表可选的|
|`\s`|任意的空格|
|`^`|匹配输入字符串的开始位置|
|`$`|匹配输入字符串的结束位置|
|`()`|组匹配策略, 提取信息|
|`管道操作符`|逻辑或|
|`\S`|任意非空格字符|
|`\W`|任意非字母字符|
|`\b`|匹配边界|
|`\1`, `\2`|引用通过组 group 捕获的内容|
|`\2-\1`|互换捕获内容的位置|




## Python3 的正则表达式

Python3 使用 `re` 库开实现正则表达式。要求使用 raw strings （普通字符串 "ab*"，raw字符串 r"ab*"）。raw string 不解释字符串中出现的转移符号 '\'。

`re.search()` 方法返回 None 表示未匹配成功或者 re.MatchObject 对象存储匹配内容。

```python
matchObject = re.search(pattern, input_str, flags=0)
matchList = re.findall(pattern, input_str, flags=0)
matchList = re.finditer(pattern, input_str, flags=0)
replacedString = re.sub(pattern, replacement_pattern, input_str, count, flags=0)
```


### 示例

```python
import re
# Lets use a regular expression to match a date string. Ignore
# the output since we are just testing if the regex matches.
regex = r"([a-zA-Z]+) (\d+)"
if re.search(regex, "June 24"):
    # Indeed, the expression "([a-zA-Z]+) (\d+)" matches the date string

    # If we want, we can use the MatchObject's start() and end() methods
    # to retrieve where the pattern matches in the input string, and the
    # group() method to get all the matches and captured groups.
    match = re.search(regex, "June 24")

    # This will print [0, 7), since it matches at the beginning and end of the
    # string
    print("Match at index %s, %s" % (match.start(), match.end()))

    # The groups contain the matched values.  In particular:
    #    match.group(0) always returns the fully matched string
    #    match.group(1), match.group(2), ... will return the capture
    #            groups in order from left to right in the input string
    #    match.group() is equivalent to match.group(0)

    print("Full match: %s" % (match.group(0)))
    print("Month: %s" % (match.group(1)))
    print("Day: %s" % (match.group(2)))
else:
    # If re.search() does not match, then None is returned
    print("The regex pattern does not match. :(")
```

## 参考文献
1. [RegexOne - Learn Regular Expressions - Lesson 1: An Introduction, and the ABCs](https://regexone.com/)
2. [RegexOne - Learn Regular Expressions - Python](https://regexone.com/references/python)
