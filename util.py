import datetime
from configparser import NoSectionError

from parse import findall


class GetWeek:
    def __init__(self):
        self.weekCycle = [None, "", "单", "双"]
        self.result = ""

    def addAbbreviate(self, cycle, begin, end):
        if type(self.result) == str and self.result != "":
            self.result += " "
        if begin == end:
            self.result += str(begin)
        else:
            self.result += self.weekCycle[cycle] + str(begin) + "-" + str(end)
        return self.result

    def mashalOdd(self, result, weekOccupy, From, start):

        if (start - From + 2) % 2 == 0:
            cycle = 3
        else:
            cycle = 2
        i = start + 2
        while i < len(weekOccupy):
            if weekOccupy[i] == "1":
                if weekOccupy[i + 1] == "1":
                    self.addAbbreviate(cycle, start - From + 2, i - 2 - From + 2)
                    return i
            else:
                if i - 2 == start:
                    cycle = 1
                self.addAbbreviate(cycle, start - From + 2, i - 2 - From + 2)
                return i + 1
            i += 2
        return i

    def mashalContinue(self, result, weekOccupy, From, start):
        cycle = 1
        i = start + 2
        while i < len(weekOccupy):
            if weekOccupy[i] == "1":
                if weekOccupy[i + 1] != "1":
                    self.addAbbreviate(cycle, start - From + 2, i - From + 2)
                    return i + 2
            else:
                self.addAbbreviate(cycle, start - From + 2, i - 1 - From + 2)
                return i + 1
            i += 2
        return i

    def repeatChar(self, str, length):
        if length <= 1:
            return str
        rs = ""
        k = 0
        while k < length:
            rs += str
            k += 1
        return rs

    def marshal(self, weekOccupy, From, startWeek, endWeek):
        self.result = ""
        if not weekOccupy:
            return ""

        initLength = len(weekOccupy)

        if From > 1:
            before = weekOccupy[0:From - 1]
            if before.find("1") != -1:
                weekOccupy = weekOccupy + before
        tmpOccupy = self.repeatChar("0", From + startWeek - 2)
        tmpOccupy += weekOccupy[From + startWeek - 2:From + endWeek - 1]
        tmpOccupy += self.repeatChar("0", initLength - len(weekOccupy))
        weekOccupy = tmpOccupy

        if endWeek > len(weekOccupy):
            endWeek = len(weekOccupy)

        if weekOccupy.find('1') == -1:
            return ""
        weekOccupy += "000"
        start = 0
        while weekOccupy[start] != "1":
            start += 1
        i = start + 1
        while i < len(weekOccupy):
            post = weekOccupy[start + 1]
            if post == '0':
                start = self.mashalOdd(self.result, weekOccupy, From, start)
            if post == '1':
                start = self.mashalContinue(self.result, weekOccupy, From, start)
            while start < len(weekOccupy) and weekOccupy[start] != "1":
                start += 1
            i = start
        return self.result


class Logger:
    def i(self, tag, content):
        date_string = str(datetime.datetime.today())[:16]
        print("{date}: INFO [{tag}] {content}".format(date=date_string, tag=tag, content=content))

    def e(self, tag, content):
        date_string = str(datetime.datetime.today())[:16]
        print("{date}: ERROR [{tag}] {content}".format(date=date_string, tag=tag, content=content))


def load_config(config_path='static/config.ini'):
    """load static/config.ini"""
    from configparser import ConfigParser
    conf = ConfigParser()
    try:
        conf.read(config_path)
        config_dict = {}
        for k, v in conf.items('UUIA-config'):
            config_dict.update({k: v})
        return config_dict
    except NoSectionError:
        raise FileNotFoundError("Please confirm static/config.ini")


def search_all(template: str, html: str):
    """Search the :class:`Element <Element>` (multiple times) for the given parse
    template.

    :param html: html_text
    :param template: The Parse template to use.
    """
    return [r for r in findall(template, html)]


def save_html(html_text):
    with open('testHTML/tmp.html', 'w') as fp:
        fp.write(html_text)
    print("output to current directory successfully!")
