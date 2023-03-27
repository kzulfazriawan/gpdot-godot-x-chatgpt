import sys
import openai
import re


class App:
    sc_key: str = ""
    result: str

    def ask(self, m):
        openai.api_key = self.sc_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a chatbot"},
                {"role": "user", "content": m},
            ]
        )

        for item in response.choices:
            self.result = item.message.content

    @staticmethod
    def converterBBCode(s):
        links = {}
        codes = []

        def gather_link(m):
            links[m.group(1)] = m.group(2);
            return ""

        def replace_link(m):
            return "[url=%s]%s[/url]" % (links[m.group(2) or m.group(1)], m.group(1))

        def gather_code(m):
            codes.append(m.group(3));
            return "[code=%d]" % len(codes)

        def replace_code(m):
            return "%s" % codes[int(m.group(1)) - 1]

        def translate(p="%s", g=1):
            def inline(m):
                s = m.group(g)
                s = re.sub(r"(`+)(\s*)(.*?)\2\1", gather_code, s)
                s = re.sub(r"\[(.*?)\]\[(.*?)\]", replace_link, s)
                s = re.sub(r"\[(.*?)\]\((.*?)\)", "[url=\\2]\\1[/url]", s)
                s = re.sub(r"<(https?:\S+)>", "[url=\\1]\\1[/url]", s)
                s = re.sub(r"\B([*_]{2})\b(.+?)\1\B", "[b]\\2[/b]", s)
                s = re.sub(r"\B([*_])\b(.+?)\1\B", "[i]\\2[/i]", s)
                return p % s

            return inline

        s = re.sub(r"(?m)^\[(.*?)]:\s*(\S+).*$", gather_link, s)
        s = re.sub(r"(?m)^    (.*)$", "~[code]\\1[/code]", s)
        s = re.sub(r"(?m)^(\S.*)\n=+\s*$", translate("~[size=200][b]%s[/b][/size]"), s)
        s = re.sub(r"(?m)^(\S.*)\n-+\s*$", translate("~[size=100][b]%s[/b][/size]"), s)
        s = re.sub(r"(?m)^#\s+(.*?)\s*#*$", translate("~[size=200][b]%s[/b][/size]"), s)
        s = re.sub(r"(?m)^##\s+(.*?)\s*#*$", translate("~[size=100][b]%s[/b][/size]"), s)
        s = re.sub(r"(?m)^###\s+(.*?)\s*#*$", translate("~[b]%s[/b]"), s)
        s = re.sub(r"(?m)^> (.*)$", translate("~[quote]%s[/quote]"), s)
        s = re.sub(r"(?m)^[-+*]\s+(.*)$", translate("~[list]\n[*]%s\n[/list]"), s)
        s = re.sub(r"(?m)^\d+\.\s+(.*)$", translate("~[list=1]\n[*]%s\n[/list]"), s)
        s = re.sub(r"(?m)^((?!~).*)$", translate(), s)
        s = re.sub(r"(?m)^~\[", "[", s)
        s = re.sub(r"\[/code]\n\[code(=.*?)?]", "\n", s)
        s = re.sub(r"\[/quote]\n\[quote]", "\n", s)
        s = re.sub(r"\[/list]\n\[list(=1)?]\n", "", s)
        s = re.sub(r"(?m)\[code=(\d+)]", replace_code, s)

        return s


if __name__ == "__main__":
    app = App()
    app.ask(" ".join(sys.argv[1:]) if len(sys.argv) > 2 else sys.argv[1])
    sys.stdout.write(App.converterBBCode(app.result))
