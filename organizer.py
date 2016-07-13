from html.parser import HTMLParser

try:
    f = open(r"C:\Users\Arvind\Documents\GitHub\industryo\templates\base.html")
    print(f)
finally:
    f.close()

with open(r"C:\Users\Arvind\Documents\GitHub\industryo\templates\base.html") as f:
    data = f.read().replace('\n', '')


class MyHTMLParser(HTMLParser):
    """docstring for MyHTMLParser"""
    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name == 'class':
                print(value, 'in', tag)

    # def handle_endtag(self, tag):
    #     print("Encountered an end tag :", tag)

    # def handle_data(self, data):
    #     print("Encountered some data  :", data)


parser = MyHTMLParser()
parser.feed(data)
