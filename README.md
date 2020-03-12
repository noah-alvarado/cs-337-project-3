# cs-337-project-3
# Recipes Tool
## Initialization
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
Now, you are ready to run Recipes Tool.

## Running
To use our tool, run the command:
```commandline
python3 recipes_tool.py
```

Enter the url of the recipe at the prompt that appears.
```commandline
Recipe URL: https://www.allrecipes.com/recipe/218091/classic-and-simple-meat-lasagna/?clickId=right%20rail0&internalSource=rr_feed_recipe_sb&referringId=86587%20referringContentType%3Drecipe
```

## Usage
The first thing you see when running our tool is a prompt to enter a recipe url.
Simply paste the recipe's url in this area and hit return.

This will automatically load the online recipe, parse the ingredients and step, and display a prompt for transforming the recipe.

The [available transformations](#transformations) are:
- [Adjust amount](#adjust-amount)
- [Make vegetarian](#make-vegetarian)
- [Make vegan](#make-vegan)
- [Make non-vegetarian](#make-non-vegetarian)
- [Change cuisine](#change-cuisine)
- [Make healthier](#make-more-healthy)
- [Make less healthy](#make-less-healthy)

Also available at this prompt are quitting the program, verbosely printing the recipe, and resetting to a new recipe.
These are referred to as [reserved transformations](#reserved-transformations).

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

#### Verbose Printing
This prints the recipe's representation in much more detail than is typically shown before and after transformations.
This print only happens once and the transformation is not remembered as a preference, so this transformation must be called whenever a verbose print is desired.
```commandline
verbose
```
#### New Recipes
Entering a recipe url as the transformation will reset the recipe to the one pointed to by the entered url.
This deletes the data of the current recipe, beginning again from scratch.

This can be used to reset the current recipe to it's original state (by entering the same url) or load a new recipe (by entering a different url).
```commandline
# any http:// or https:// link
```