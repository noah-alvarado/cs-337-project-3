from ingredient import Ingredient
from common_data import task_tools

class Step:
    def __init__(self, raw_step=None, recipe_ingredients=None):
        if recipe_ingredients is None:
            recipe_ingredients = []

        self.recipe_ingredients = recipe_ingredients

        self.raw = raw_step
        self.tools = []
        self.methods = []
        self.ingredients = []
        self.current_time_string = ''
        self.time_in_minutes = 0

        # fill data members
        self._parse_ingredients()
        self._parse_tools()
        self._parse_methods()
        self._parse_time()

    def _parse_time(self):
        self.raw = self.raw.replace('more minutes', 'minutes')

        bad_chars = ['(', ')', ',']
        raw_clean = self.raw
        for char in bad_chars:
            raw_clean = raw_clean.replace(char, '')

        step_words = raw_clean.split()
        for index, word in enumerate(step_words):
            if Ingredient.is_number(word) and index < len(step_words) - 1:
                if step_words[index + 1] == 'hour' or step_words[index + 1] == 'hours':
                    self.current_time_string = word + ' ' + step_words[index + 1]
                    self.time_in_minutes = float(word) * 60
                elif step_words[index + 1] == 'minutes':
                    self.current_time_string += ' ' + word + ' ' + step_words[index + 1]
                    self.time_in_minutes += float(word)
                elif step_words[index + 1] == 'seconds':
                    self.current_time_string += ' ' + word + ' ' + step_words[index + 1]
                    self.time_in_minutes += float(word) / 60
                self.current_time_string = self.current_time_string.strip()

    def _parse_ingredients(self):
        bad_chars = ['(', ')', ',']
        raw_clean = self.raw.lower()
        for char in bad_chars:
            raw_clean = raw_clean.replace(char, '')

        for ingredient in self.recipe_ingredients:
            if ingredient.name in raw_clean:
                if ingredient.name not in self.ingredients:
                    self.ingredients.append(ingredient.name)

    def _parse_tools(self):
        for word, tools in task_tools.items():
            if word in self.raw.lower():
                if word == "cover":
                    for cover_type in tools:
                        if cover_type in self.raw.lower():
                            self.tools.append(cover_type)
                else:
                    for tool in tools:
                        if tool not in self.tools:
                            self.tools.append(tool)

    def _parse_methods(self):
        for word, tools in task_tools.items():
            if word in self.raw.lower() and word not in self.methods:
                self.methods.append(word)
