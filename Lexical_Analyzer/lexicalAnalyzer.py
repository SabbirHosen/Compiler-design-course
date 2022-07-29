import re
# regular expression patterns for identify tokens
token_pattern = r'''
(?P<identifier_or_keywords>[a-zA-Z_][a-zA-Z0-9_]*)
|(?P<multi_line_comment>/\*(.*?)\*/)
|(?P<single_line_comment>//(.*?)\n)
|(?P<number>[0-9.]+)
|(?P<punctuation>[\.\;\,\:])
|(?P<parenthesis>[{}\(\)\[\]])
|(?P<operator>[+-/\*%])
|(?P<newline>\n)
|(?P<whitespace>\s+)
|(?P<header>\<(.*?)\>)
|(?P<equals>[=])
|(?P<logical_operator>[\!\>\<\&\|])
|(?P<slash>[/])
|(?P<string>"(.*?)")
|(?P<predecessor>[#])
'''

token_re = re.compile(token_pattern, re.VERBOSE)


class TokenizerException(Exception): pass


def tokenize(text):
    token_list = []
    pos = 0
    while True:
        m = token_re.match(text, pos)
        if not m: break
        pos = m.end()
        tokname = m.lastgroup
        tokvalue = m.group(tokname)
        token_list.append((tokname, tokvalue))
    if pos != len(text):
        raise TokenizerException('tokenizer stopped at pos %r of %r character is %r' % (
            pos, len(text), text[pos]))
    else:
        return token_list


result = {
    'identifier': [],
    'keywords': [],
    'predecessor': [],
    'integer': [],
    'float': [],
    'parenthesis': [],
    'operator': [],
    'logical_operator': [],
    'string': [],
    'header': [],
    'comment': [],
    'punctuation': [],
    'extras': []
}
keyword_list = ['alignas', 'decltype', 'namespace', 'struct', 'alignof', 'default', 'new', 'switch', 'and', 'delete',
                'noexcept', 'template', 'and_eq', 'do', 'not', 'this', 'asm', 'double', 'not_eq', 'thread_local',
                'auto', 'dynamic_cast', 'nullptr', 'throw', 'bitand', 'else', 'operator', 'true', 'bitor', 'enum', 'or',
                'try', 'bool', 'explicit', 'or_eq', 'typedef', 'break', 'export', 'private', 'typeid', 'case', 'extern',
                'protected', 'typename', 'catch', 'false', 'public', 'union', 'char', 'float', 'register', 'unsigned',
                'char16_t', 'for', 'reinterpret_cast', 'using', 'char32_t', 'friend', 'return', 'virtual', 'class',
                'goto', 'short', 'void', 'compl', 'if', 'signed', 'volatile', 'const', 'inline', 'sizeof', 'wchar_t',
                'constexpr', 'int', 'static', 'while', 'const_cast', 'long', 'static_assert', 'xor', 'continue',
                'mutable', 'static_cast', 'xor_eq']


def identify_token(token_list):
    # it will identify token class and append to the corrosponding class
    i = 0
    while i < len(token_list):
        if token_list[i][0] == 'identifier_or_keywords':
            if token_list[i][1] in keyword_list:
                if token_list[i][1] not in result['keywords']:
                    result['keywords'].append(token_list[i][1])
            else:
                if token_list[i][1] not in result['identifier']:
                    result['identifier'].append(token_list[i][1])
        elif token_list[i][0] == 'operator':
            if token_list[i][1] == '-' and token_list[i + 1][0] == 'number':
                temp = token_list[i + 1][1]
                if temp.isdigit():
                    temp1 = token_list[i][1] + token_list[i + 1][1]
                    if temp1 not in result['integer']:
                        result['integer'].append(temp1)
                elif temp.replace('.', '', 1).isdigit() and temp.count('.') < 2:
                    temp1 = token_list[i][1] + token_list[i + 1][1]
                    if temp1 not in result['float']:
                        result['float'].append(temp1)
                i += 1
            else:
                if token_list[i][1] not in result['operator']:
                    result['operator'].append(token_list[i][1])
        elif token_list[i][0] == 'logical_operator' or token_list[i][0] == 'equals':
            if token_list[i][0] == 'logical_operator' and (
                    token_list[i + 1][0] == 'logical_operator' or token_list[i + 1][0] == 'equals'):
                temp = token_list[i][1] + token_list[i + 1][1]
                if temp not in result['logical_operator']:
                    result['logical_operator'].append(temp)
                    i += 1
            elif token_list[i][0] == 'equals' and token_list[i + 1][0] == 'equals':
                temp = token_list[i][1] + token_list[i + 1][1]
                if temp not in result['logical_operator']:
                    result['logical_operator'].append(temp)
                    i += 1
            elif token_list[i][0] == 'equals':
                if token_list[i][1] not in result['logical_operator']:
                    result['logical_operator'].append(token_list[i][1])
            elif token_list[i][0] == 'logical_operator':
                if token_list[i][1] not in result['logical_operator']:
                    result['logical_operator'].append(token_list[i][1])
        elif token_list[i][0] == 'predecessor':
            if token_list[i][1] not in result['predecessor']:
                result['predecessor'].append(token_list[i][1])
        elif token_list[i][0] == 'number':
            temp = token_list[i][1]
            if temp.isdigit():
                if temp not in result['integer']:
                    result['integer'].append(temp)
            elif temp.replace('.', '', 1).isdigit() and temp.count('.') < 2:
                if temp not in result['float']:
                    result['float'].append(temp)
        elif token_list[i][0] == 'parenthesis':
            if token_list[i][1] not in result['parenthesis']:
                result['parenthesis'].append(token_list[i][1])
        elif token_list[i][0] == 'string':
            if token_list[i][1] not in result['string']:
                result['string'].append(token_list[i][1])
        elif token_list[i][0] == 'header':
            if token_list[i][1] not in result['header']:
                result['header'].append(token_list[i][1])
        elif token_list[i][0] == 'multi_line_comment' or token_list[i][0] == 'single_line_comment':
            if token_list[i][1] not in result['comment']:
                result['comment'].append(token_list[i][1])
        elif token_list[i][0] == 'punctuation':
            if token_list[i][1] not in result['punctuation']:
                result['punctuation'].append(token_list[i][1])
        else:
            if token_list[i][1] not in result['extras']:
                result['extras'].append(token_list[i][1])

        i += 1


if __name__ == '__main__':
    # read code from the text file
    with open('text1.text', 'r') as file:
        text = file.read()
    # inline input option
    stuff = r'''#include<stdio.h>
        #define mx -100 int include
        int main() {
        a = b + c- a *4 /0;
        a == &&b|| >c <=d !=
       printf("Hello, World!");
       [start]
       /*dcomment*/
       //scomment
       return -0.5;
    }
    '''
    # calling tokenization function and return a list of tokens
    token_list = tokenize(text)
    # this function identify the tokens basis on there class
    identify_token(token_list)
    # print the results
    keys_list = result.keys()
    for key in keys_list:
        print(f'{key}({len(result[key])}):{result[key]}')
    # print(result.keys())
