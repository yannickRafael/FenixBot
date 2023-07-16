
class Menu:

    def __init__(self, title, options, state):
        self.title = title
        self.options = options
        self.estado = state
        ans = []
        for i in range(0, len(options)):
            ans.append(str(i+1))
        self.range = ans

    def to_string(self):
        text = self.title+'\n'
        for i in range(0, len(self.options)):
            text = text + str(i+1)+'. '+self.options[i]+'\n'
        return text

    def getOption(self, selected):
        if selected in self.range:
            return self.options[selected]
        else:
            return 'invalid option'







