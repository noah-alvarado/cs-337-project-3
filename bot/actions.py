# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"
from asyncore import dispatcher
from typing import Any, Text, Dict, List
from recipe import Recipe
from recipes_tool import parse_factor
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class Global_Vars():
    recipe = None
    current_step = 0


class ActionAcceptUrl(Action):

    def name(self) -> Text:
        return "action_accept_url"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        Global_Vars.recipe = Recipe((tracker.latest_message)['text'])
        Global_Vars.current_step = 0;
        dispatcher.utter_message(text="Cool, let's get started with " + Global_Vars.recipe.recipe_name + "!")
        dispatcher.utter_message(text="Do you wanna go through the ingredients first (say ingredients) or go straight to the directions (say directions)?")

        return []

class ActionListIngredients(Action):

    def name(self) -> Text:
        return "action_list_ingredients"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if Global_Vars.recipe == None :
            dispatcher.utter_message(text="You need a recipe before you ask for ingredients!")
        else:
            dispatcher.utter_message(text="Here's the ingredient list:")
            print_str = ''
            for ingredient in Global_Vars.recipe.ingredients:
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

            dispatcher.utter_message(text=print_str)
            dispatcher.utter_message(text="When you're ready for the steps, just ask for \"directions\" :)")

        return []


class ActionNextStep(Action):

    def name(self) -> Text:
        return "action_next_step"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if Global_Vars.recipe == None:
            dispatcher.utter_message(text="You need a recipe before you ask for directions!")
        else:
            if Global_Vars.current_step >= len(Global_Vars.recipe.steps):
                dispatcher.utter_message(text="You've already made it to the end!  Enjoy!")
            else:
                dispatcher.utter_message(text=Global_Vars.recipe.steps[Global_Vars.current_step].raw + ".")
                Global_Vars.current_step += 1
                if Global_Vars.current_step >= len(Global_Vars.recipe.steps):
                    dispatcher.utter_message(text="And that's it!  Enjoy!")
        return []

class ActionDoTransformation(Action):

    def name(self) -> Text:
        return "action_do_transformation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if Global_Vars.recipe == None:
            dispatcher.utter_message(text="You need a recipe before you can transform it!")
        else:
            output = ""
            transformation = (tracker.latest_message)['text']
            transformation = transformation.lower()
            transformation = transformation.split(' ')

            args = ' '.join(transformation)

            if transformation[0] == 'adjust':
                factor = ' '.join(transformation[1:])
                factor = factor.strip()
                try:
                    factor = parse_factor(factor)
                except ValueError:
                    output = '\nInvalid input for %factor%, it must be a number in either decimal or fraction form.\n'


                output = 'Adjusted the recipe by a factor of: ' + str(factor) + ' :)'
                Global_Vars.recipe.adjust_portions(factor)

            if transformation[0] == 'vegify':
                replacements = Global_Vars.recipe.vegify()
                replacements = list(replacements)

                # change steps to reflect changed ingredients
                Global_Vars.recipe.change_step_ingredients(replacements)

                # remove steps with "meat"
                removals = []
                for i in range(len(Global_Vars.recipe.steps)):
                    if 'meat' in Global_Vars.recipe.steps[i].raw:
                        removals.append(i)
                removals.reverse()
                for i in removals:
                    Global_Vars.recipe.steps.pop(i)

                output = 'Made the recipe vegetarian :)'

            if transformation[0] == 'veganify':

                replacements = Global_Vars.recipe.veganify()
                replacements = list(replacements)

                # change steps to reflect changed ingredients
                Global_Vars.recipe.change_step_ingredients(replacements)

                # remove steps with "meat"
                removals = []
                for i in range(len(Global_Vars.recipe.steps)):
                    if 'meat' in Global_Vars.recipe.steps[i].raw:
                        removals.append(i)
                removals.reverse()
                for i in removals:
                    Global_Vars.recipe.steps.pop(i)

                output = 'Made the recipe vegan :)'

            if transformation[0] == 'meatify':

                replacements = Global_Vars.recipe.meatify()
                replacements = list(replacements)

                # change steps to reflect changed ingredients
                Global_Vars.recipe.change_step_ingredients(replacements)

                output = 'Gave the recipe some meat :)'

            if transformation[0] == 'cuisine':

                cuisine = transformation[1]

                if cuisine in ['mexican', 'italian']:
                    replacements = Global_Vars.recipe.to_cuisine(cuisine)
                    replacements = list(replacements)

                    # change steps to reflect changed ingredients
                    Global_Vars.recipe.change_step_ingredients(replacements)

                    output = 'Changed the cuisine to ' + cuisine

            if transformation[0] == 'healthy':
                replacements = Global_Vars.recipe.healthier()
                replacements = list(replacements)

                # change steps to reflect changed ingredients
                Global_Vars.recipe.change_step_ingredients(replacements)

                output = 'Made the recipe healthy'

            if transformation[0] == 'not-healthy':

                replacements = Global_Vars.recipe.less_healthy()
                replacements = list(replacements)

                # change steps to reflect changed ingredients
                Global_Vars.recipe.change_step_ingredients(replacements)

                output = 'Made the recipe unhealthy'

            if len(output) > 0:
                dispatcher.utter_message(text=output)
                dispatcher.utter_message(text="We've applied your transform, so we're ready to start from the top.")
                dispatcher.utter_message(text="Wanna start with directions, or ingredients?")
                Global_Vars.current_step = 0;
            else:
                dispatcher.utter_message(text="Hmm, that doesn't seem to be a valid transform.")

        return []