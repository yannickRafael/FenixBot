class Menu:
    def __init__(self, name, prompt, options):
        self.name = name
        self.prompt = prompt
        self.options = options
        self.range = []
        for i in range(0, len(options)):
            self.range.append(str(i+1))



    def print_prompt(self):
        text = self.prompt + ': \n'
        for i in range(0, len(self.options)):
            text = text + str(1 + i) + '. ' + self.options[i] + '\n'

        return text

    def select_data(self, message):
        try:
            i = int(message)
            if 1 <= i <= len(self.options):
                return self.options[i - 1]
            else:
                return 'Opção inválida'
        except:
            return 'Opção inválida'


    def get_name(self):
        return self.name


    def set_options(self, options):
        self.options = options
