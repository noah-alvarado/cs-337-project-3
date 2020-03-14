# cs-337-project-3

# Recipes Bot.  Codename Ramsay
## Initialization
First, make sure you cd into the bot folder.
Ensure that you are running Python 3.7 or higher using the command `python3 --version`. The output should be of the form:
```commandline
Noahs-MacBook-Air:cs-337-project-2 noahalvarado$ python3 --version
Python 3.7.4
```

Install `virtualenv` and initialize a virtual environment.
```commandline
python3 -m pip install virtualenv
python3 -m venv venv
```

Swtich to the virtual environment you just created and install the necessary packages.
```commandline
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

Because Rasa has different dependencies on different operating systems, you now need to install Rasa separately:
```commandline
pip install rasa
```

Now, you are ready to run Recipes Tool.

## Running
To use our tool, run the commands:

```commandline
rasa train
rasa run actions
```
and then, on another command line / terminal window in the same directory, run:
```commandline
rasa shell
```

From now, you have the bot, Ramsay, at your service.  Try it out.  Say hi!

## Usage
It'll ask you for the recipe, so enter the URL at the prompt that appears.
Enter the url of the recipe at the prompt that appears.  Sample URL:
```commandline
https://www.allrecipes.com/recipe/218091/classic-and-simple-meat-lasagna/?clickId=right%20rail0&internalSource=rr_feed_recipe_sb&referringId=86587%20referringContentType%3Drecipe
```

From now on out, you can interact with the bot in a variety of ways.

To print the ingredients at any time, just type "ingredients."

To start the directions, say "directions."
From then on out, say "next" to go to the next direction.

To do a transform, type "transform" at any time.
Then, type the transform when prompted for it.

The [available transformations](#transformations) are:
- [Adjust amount](#adjust-amount)
- [Make vegetarian](#make-vegetarian)
- [Make vegan](#make-vegan)
- [Make non-vegetarian](#make-non-vegetarian)
- [Change cuisine](#change-cuisine)
- [Make healthier](#make-more-healthy)
- [Make less healthy](#make-less-healthy)

## Transformations
### Adjust Amount
This transformation adjust the amount of food the recipe yields by the specified factor.
This factor can be in decimal, fraction, or mixed number format.
This factor must be a real, positive value.
```shell script
adjust 2.0      # double the amount
adjust 0.5      # half the amount
adjust 1 1/2    # one and a half times the amount
adjust 6/8      # six eighths (three quarters) of the amount
```

### Make Vegetarian
This will replace all non-vegetarian ingredients with vegetarian ones.
The specific ingredient used to replace non-vegetarian ingredients is variable, and may changed based on the ingredient itself and random selection.
```shell script
vegify
```

### Make Vegan
This will replace all non-vegan ingredients with vegan ones.
The specific ingredient used to replace non-vegan ingredients is variable, and may changed based on the ingredient itself and random selection.
```shell script
veganify
```

### Make Non-vegetarian
This will replace some vegetarian ingredients with some non-vegetarian ones.
The amount of ingredients replaced and/or added depends on the number of ingredients in the original recipe.
The specific non-vegetarian ingredient added is variable, and may changed based on the replaced ingredient and/or random selection.
```shell script
meatify
```

### Change Cuisine
This transformation attempts to change the cuisine of the current recipe by replacing and/or adding comparable ingredients.
```shell script
cuisine mexican    # change to mexican
cuisine italian    # change to italian
```

### Make More Healthy
This transformation tries to find "unhealthy" ingredients and replace them with "healthy" alternatives.
An example would be using avocado oil instead of butter to sautee onions and peppers.
```shell script
healthy
```

### Make Less Healthy
This transformation attempts to do the opposite of making the recipe more healthy, using the same general concepts.
If a recipe is already very "unhealthy" more ingredients will be added. Yum?
```shell script
not-healthy
```

### Reserved Transformations
#### Quitting
This transformation halts execution and returns control to the terminal.
This serves the same purpose as halting the program using ctrl/command + c.
```commandline
stop
```

#### New Recipes
Entering a recipe url as the transformation will reset the recipe to the one pointed to by the entered url.
This deletes the data of the current recipe, beginning again from scratch.

#### Notes
This is a trained model.  The strings provided here are samples.  They are not the only way to trigger the commands.  You can say things like "I want a transformation" instead of "transform," for example.
Also, there is no verbose printing,  because people don't typically want that kind of information from a bot.