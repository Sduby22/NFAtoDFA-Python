

str = ''
with open('./data.in', encoding='utf8') as f:
    for x in next(f).split():
        print(x)
