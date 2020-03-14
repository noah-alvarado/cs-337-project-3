import random

from ingredient import Ingredient
from step import Step
from webscraper import parse_recipe
from common_data import meat_to_veg, meat_types, veg_to_meat, veg_types, oily_ingredients, mexican_conversions, italian_conversions, less_healthy_conversions, healthy_conversions, mexican_spices, italian_spices, meat_additions, vegan_to_meat


class Recipe:
    def __init__(self, url):
        self.ingredients = []
        self.tools = []
        self.prep_methods = []
        self.step_methods = []
        self.steps = []

        raw_recipe = parse_recipe(url)
        raw_ingredients = raw_recipe['ingredients']
        raw_directions = raw_recipe['directions']
        self.recipe_name = raw_recipe['name']

        for ingredient in raw_ingredients:
            try:
                processed_ingredient = Ingredient(ingredient)
            except ValueError:
                continue
            self.ingredients.append(processed_ingredient)
            for tool in processed_ingredient.tools:
                if tool not in self.tools:
                    self.tools.append(tool)
            for method in processed_ingredient.methods:
                if method not in self.prep_methods:
                    self.prep_methods.append(method)

        for direction in raw_directions:
            for sentence in direction.split('.'):
                sentence = sentence.strip()
                if len(sentence) > 0:
                    processed_step = Step(sentence, self.ingredients)
                    self.steps.append(processed_step)
                    for tool in processed_step.tools:
                        if tool not in self.tools:
                            self.tools.append(tool)
                    for method in processed_step.methods:
                        if method not in self.step_methods:
                            self.step_methods.append(method)

    def __str__(self):
        print_str = '\nHere is the recipe:\n\t' + self.recipe_name + '\n\n\tIngredients:\n'
        for ingredient in self.ingredients:
            if ingredient.quantity_is_set and isinstance(ingredient.quantity, float):
                if ingredient.measure == 'item':
                    description = '\t\t' + str(ingredient.quantity) + ' '
                else:
                    description = '\t\t' + str(ingredient.quantity) + ' ' + ingredient.measure
                    if ingredient.quantity > 1:
                        description += 's '
                    else:
                        description += ' '
            else:
                description = '\t\t'
            remove_comma = False
            for prep in ingredient.preparations:
                if prep not in ingredient.descriptors:
                    description += prep + ', '
                    remove_comma = True
            if remove_comma:
                description = description[0:len(description) - 2] + ' '
            remove_comma = False
            for descriptor in ingredient.descriptors:
                remove_comma = True
                description += descriptor + ', '
            if remove_comma:
                description = description[0:len(description) - 2] + ' '
            description += ingredient.name
            if ingredient.to_taste and ingredient.quantity_is_set:
                description += ' (or to taste)'
            elif ingredient.to_taste:
                description += ' (to taste)'
            print_str += description + '\n'

        print_str += '\n\tDirections:\n'
        for index, step in enumerate(self.steps):
            print_str += '\t\tStep' + str(index + 1) + ': ' + step.raw + '.\n'
        return print_str

    def adjust_portions(self, amount):
        print('Here is the list of changes we are making:')
        saute_preps = ['sear', 'brown', 'saute']
        not_adjusted_list = []
        for ingredient in self.ingredients:
            adjusted = False
            for prep in saute_preps:
                for step in self.steps:
                    if ingredient in step.ingredients and prep in step.methods and ingredient.name in oily_ingredients:
                        if amount < 1.0:
                            if not adjusted:
                                adjusted = True
                                print('\tBecause of the {} method, we are using {} times the amount of {}.'.format(prep, 1.5 * amount, ingredient.name))
                                ingredient.quantity *= 1.5 * amount
                        else:
                            if not adjusted:
                                adjusted = True
                                print('\tBecause of the {} method, we are using {} times the amount of {}.'.format(prep, 0.75 * amount, ingredient.name))
                                ingredient.quantity *= amount * .75
            if not adjusted:
                not_adjusted_list.append(ingredient.name)
                ingredient.quantity *= amount

        if len(not_adjusted_list) > 0:
            print('\tWe will be using ' + str(amount) + ' times the amount of ' + ' and '.join(
                ', '.join(not_adjusted_list).rsplit(', ', 1)) + '.')

        adjusted_steps = []
        for index, step in enumerate(self.steps):
            if len(step.current_time_string) > 0 and step.time_in_minutes > 0:
                if amount >= 1:
                    new_time = step.time_in_minutes + step.time_in_minutes * (amount - 1) * .5
                else:
                    # some math so that doubling and halfing a recipe brings you back to the starting point ;)
                    new_time = step.time_in_minutes / (1 + ((1 / amount) - 1) * .5)

                step.time_in_minutes = new_time
                if step.current_time_string in step.raw:
                    adjusted_steps.append('step ' + str(index + 1))
                    step.raw = step.raw.replace(step.current_time_string, str(int(step.time_in_minutes)) + ' minutes')
                    step.current_time_string = str(int(step.time_in_minutes)) + ' minutes'

        if len(adjusted_steps) > 0:
            if amount > 1:
                print('\tWe will go for ' + str(100 * (amount - 1) / 2) + '% more time in ' + ' and '.join(
                    ', '.join(adjusted_steps).rsplit(', ', 1)) + '.')
            else:
                print('\tWe will go for ' + str(
                    100 * (1 - (1 / (1 + ((1 / amount) - 1) * .5)))) + '% less time in ' + ' and '.join(
                    ', '.join(adjusted_steps).rsplit(', ', 1)) + '.')

    def vegify(self):
        for i in range(len(self.ingredients)):
            found = None
            for kind, matches in meat_types.items():
                for match in matches:
                    if match in self.ingredients[i].name:
                        found = kind
                        break

            if found is None:
                continue

            old = self.ingredients[i].name
            new = random.choice(meat_to_veg[found])
            if self.ingredients[i].measure == 'item':
                self.ingredients[i].quantity /= 2.0
                self.ingredients[i].measure = 'cup'
            descs = ' '.join(self.ingredients[i].descriptors)
            descs = descs + ' ' + ' '.join(self.ingredients[i].preparations)
            descs.strip()
            new_ing = Ingredient(
                '{} {} {} {}'.format(self.ingredients[i].quantity, self.ingredients[i].measure, descs, new))
            new_ing = Ingredient('{} {} {}'.format(self.ingredients[i].quantity, self.ingredients[i].measure, new))
            self.ingredients[i] = new_ing

            yield old, new

    def veganify(self):
        for i in range(len(self.ingredients)):
            found = None
            for kind, matches in meat_types.items():
                for match in matches:
                    if match in self.ingredients[i].name:
                        found = kind
                        break

            if found is None:
                for replacement, matches in vegan_to_meat.items():
                    for match in matches:
                        if match in self.ingredients[i].name.lower():
                            old = self.ingredients[i].name
                            new = replacement
                            new_ing = Ingredient(
                                '{} {} {}'.format(self.ingredients[i].quantity, self.ingredients[i].measure,
                                                     new))
                            self.ingredients[i] = new_ing
                            yield old, new
                continue

            old = self.ingredients[i].name
            new = random.choice(meat_to_veg[found])
            if self.ingredients[i].measure == 'item':
                self.ingredients[i].quantity /= 2.0
                self.ingredients[i].measure = 'cup'
            descs = ' '.join(self.ingredients[i].descriptors)
            descs = descs + ' ' + ' '.join(self.ingredients[i].preparations)
            descs.strip()
            new_ing = Ingredient(
                '{} {} {} {}'.format(self.ingredients[i].quantity, self.ingredients[i].measure, descs, new))
            new_ing = Ingredient('{} {} {}'.format(self.ingredients[i].quantity, self.ingredients[i].measure, new))
            self.ingredients[i] = new_ing

            yield old, new

    def meatify(self):
        num_items_replaced = 0
        max_items_replaced = round((3 + (len(self.ingredients) * 0.2)) / 2)

        for i in range(len(self.ingredients)):
            if num_items_replaced > max_items_replaced:
                break

            found = None
            for kind, matches in veg_types.items():
                for match in matches:
                    if match in self.ingredients[i].name:
                        found = kind
                        break

            if found is None:
                continue

            old = self.ingredients[i].name
            new = random.choice(veg_to_meat[found])
            if self.ingredients[i].measure == 'item':
                self.ingredients[i].quantity /= 2.0
                self.ingredients[i].measure = 'cup'
            descs = ' '.join(self.ingredients[i].descriptors)
            descs = descs + ' ' + ' '.join(self.ingredients[i].preparations)
            descs.strip()
            new_ing = Ingredient('{} {} {} {}'.format(self.ingredients[i].quantity, self.ingredients[i].measure, descs, new))
            self.ingredients[i] = new_ing

            num_items_replaced += 1
            yield old, new

        if num_items_replaced == 0:
            # try to guess new meat
            ing_str, prep_str, comb_str = random.choice(meat_additions)

            # add ingredient
            new_ingredient = Ingredient(ing_str)
            self.ingredients.append(new_ingredient)

            # add step to cook ingredient
            cook_step = Step(prep_str, self.ingredients)
            self.steps.insert(0, cook_step)

            # add step to combine ingredient
            combine_step = Step(comb_str, self.ingredients)
            self.steps.append(combine_step)

            yield None, new_ingredient

    def healthier(self):
        num_items_replaced = 0
        for i in range(len(self.ingredients)):
            found = None
            for kind, matches in healthy_conversions.items():
                for match in matches:
                    if match in self.ingredients[i].name:
                        found = kind
                        break

            if found is None:
                continue

            old = self.ingredients[i].name
            if self.ingredients[i].measure == 'item':
                self.ingredients[i].quantity /= 2.0
                self.ingredients[i].measure = 'cup'
            descs = ' '.join(self.ingredients[i].descriptors)
            descs = descs + ' ' + ' '.join(self.ingredients[i].preparations)
            descs.strip()
            new_ing = Ingredient('{} {} {} {}'.format(self.ingredients[i].quantity, self.ingredients[i].measure, descs, found))
            self.ingredients[i] = new_ing

            new = self.ingredients[i].name

            num_items_replaced += 1
            yield old, new

        if num_items_replaced == 0:
            # guess new ingredient
            ing_str, stp_str = random.choice(healthy_conversions)

            # add new ingredient
            new_ing = Ingredient(ing_str)
            self.ingredients.append(new_ing)

            # add new step
            new_stp = Step(stp_str, self.ingredients)
            self.steps.append(new_stp)

            yield None, new_ing.name

    def less_healthy(self):
        num_items_replaced = 0
        for i in range(len(self.ingredients)):
            found = None
            for kind, matches in less_healthy_conversions.items():
                for match in matches:
                    if match in self.ingredients[i].name:
                        found = kind
                        break

            if found is None:
                continue

            old = self.ingredients[i].name
            if self.ingredients[i].measure == 'item':
                self.ingredients[i].quantity /= 2.0
                self.ingredients[i].measure = 'cup'
            descs = ' '.join(self.ingredients[i].descriptors)
            descs = descs + ' ' + ' '.join(self.ingredients[i].preparations)
            descs.strip()
            new_ing = Ingredient(
                '{} {} {} {}'.format(self.ingredients[i].quantity, self.ingredients[i].measure, descs, found))
            self.ingredients[i] = new_ing

            new = self.ingredients[i].name

            num_items_replaced += 1
            yield old, new

        if num_items_replaced == 0:
            # guess new ingredient
            ing_str, stp_str = random.choice(less_healthy_conversions)

            # add new ingredient
            new_ing = Ingredient(ing_str)
            self.ingredients.append(new_ing)

            # add new step
            new_stp = Step(stp_str, self.ingredients)
            self.steps.append(new_stp)

            yield None, new_ing.name

    def to_cuisine(self, cuisine):
        replacer_map = {
            'mexican': mexican_conversions,
            'italian': italian_conversions
        }
        replacer = replacer_map[cuisine]

        replaced_count = 0
        for ing in range(len(self.ingredients)):
            for repl, matches in replacer.items():
                if self.ingredients[ing].name in matches:
                    old = self.ingredients[ing].name
                    self.ingredients[ing].name = repl
                    new = self.ingredients[ing].name

                    replaced_count += 1
                    yield old, new
                    break

        if replaced_count == 0:
            additions_map = {
                'mexican': mexican_spices,
                'italian': italian_spices
            }
            possible_spices = additions_map[cuisine]

            additions = []
            for spice in possible_spices:
                found = False
                for ing in self.ingredients:
                    if spice in ing.name:
                        found = True
                        break

                if not found:
                    additions.append(spice)

            additions_to_make = 2
            actually_added = []
            for i in range(2):
                if len(additions) == 0 or len(actually_added) > additions_to_make:
                    break

                # guess a spice
                this_spice = random.choice(additions)
                spice = Ingredient('{}, to taste'.format(this_spice))
                additions.remove(this_spice)

                # add spice to ingredients
                self.ingredients.append(spice)

                actually_added.append(this_spice)
                yield None, spice.name

            # add spices to steps
            if len(actually_added) > 0:
                spices = ', '.join(actually_added)
                new_step = Step('Top with {}.'.format(spices), self.ingredients)
                self.steps.append(new_step)

    def get_verbose(self):
        print_str = '\nHere is the recipe for "' + self.recipe_name + '" with the representation details shown:' + \
                    '\n\tAll the preparatory methods (for preparing the ingredients, aka "secondary" methods):\n\t\t' +\
                    ' and '.join(', '.join(self.prep_methods).rsplit(', ', 1)) + \
                    '\n\tAll the direction methods (for doing the steps, aka "primary" methods):\n\t\t' + \
                    ' and '.join(', '.join(self.step_methods).rsplit(', ', 1)) + \
                    '\n\tAll the necessary tools :\n\t\t' + \
                    ' and '.join(', '.join(self.tools).rsplit(', ', 1)) + \
                    '\n\n\tIngredients:\n'
        for ingredient in self.ingredients:
            if ingredient.quantity_is_set and isinstance(ingredient.quantity, float):
                if ingredient.measure == 'item':
                    description = '\t\tQuantity: ' + str(ingredient.quantity) + '; '
                else:
                    description = '\t\tQuantity: ' + str(ingredient.quantity) + '; Measure: ' + ingredient.measure
                    if ingredient.quantity > 1:
                        description += 's; '
                    else:
                        description += '; '
            else:
                description = '\t\t'
            if ingredient.to_taste and ingredient.quantity_is_set:
                description += 'Alternative Quantity: (or to taste); '
            elif ingredient.to_taste:
                description += 'Quantity: (to taste); '
            remove_comma = False
            for prep in ingredient.preparations:
                if prep not in ingredient.descriptors:
                    if not remove_comma:
                        description += 'Preparations: '
                    description += prep + ', '
                    remove_comma = True
            if remove_comma:
                description = description[0:len(description) - 2] + '; '
            remove_comma = False
            for descriptor in ingredient.descriptors:
                if not remove_comma:
                    description += 'Descriptors: '
                remove_comma = True
                description += descriptor + ', '
            if remove_comma:
                description = description[0:len(description) - 2] + '; '
            description += 'Name: ' + ingredient.name + ';'

            print_str += description + '. Tools:' + ' and '.join(
                ', '.join(ingredient.tools).rsplit(', ', 1)) + ';  Methods:' + \
                         ' and '.join(', '.join(ingredient.methods).rsplit(', ', 1)) + ';\n'

        print_str += '\n\tDirections:\n'
        for index, step in enumerate(self.steps):
            print_str += '\t\tStep ' + str(index + 1) + ': ' + step.raw + '.\n\t\t\tIngredients: ' \
                         + ' and '.join(', '.join(step.ingredients).rsplit(', ', 1)) + '\n\t\t\tTime: ' + \
                         step.current_time_string + '\n\t\t\tTools: ' + ' and '.join(
                ', '.join(step.tools).rsplit(', ', 1)) + \
                         '\n\t\t\tMethods: ' + ' and '.join(', '.join(step.methods).rsplit(', ', 1)) + '\n'
        return print_str

    def change_step_ingredients(self, changes):
        for old, new in changes:
            if old is not None:
                for s in range(len(self.steps)):
                    for i in range(len(self.steps[s].ingredients)):
                        if old in self.steps[s].ingredients[i]:
                            self.steps[s] = Step(self.steps[s].raw.replace(old, new), self.ingredients)
                            break
