import Levenshtein

from recipe import Recipe


def get_closest_transform(transform):
    all_transforms = [
        'adjust',
        'vegify',
        'veganify',
        'meatify',
        'cuisine mexican',
        'cuisine italian',
        'healthy',
        'not-healthy',
        'stop',
        'verbose'
    ]

    dists = {trans: Levenshtein.distance(trans, transform) for trans in all_transforms}

    # actual_transformation, distance_to_input
    best_match = ('nope', 100)

    for trans, dist in dists.items():
        if best_match[1] > dist:
            best_match = (trans, dist)

    if best_match[1] < 10:
        return best_match[0]
    else:
        return None


def parse_factor(nums):
    fac = 0.0

    nums = nums.split(' ')
    if len(nums) == 2 and '/' not in nums[0] and '/' in nums[1]:
        nums = nums.split(' ')
        fac += float(nums[0])
        nums = nums[1].split('/')
        fac += float(nums[0]) / float(nums[1])
    elif len(nums) == 1 and '/' in nums[0]:
        nums = nums[0].split('/')
        fac += float(nums[0]) / float(nums[1])
    elif len(nums) == 1:
        fac += float(nums[0])
    else:
        raise ValueError('Factor not of proper form.')

    if fac > 0:
        return fac
    else:
        raise ValueError('Factor not a real, positive value.')


def print_replacements(changes):
    if len(changes) == 0:
        print('No changes were made!')
        return

    swaps = list(filter(lambda pair: pair[0] is not None, changes))
    additions = list(filter(lambda pair: pair[0] is None, changes))

    if len(swaps) > 0:
        for old, new in swaps:
            print('Replaced {} with {}'.format(old, new))
        print()

    if len(additions) > 0:
        for _, new in additions:
            print('Added {}'.format(new))
        print()


if __name__ == '__main__':
    url = input('Recipe URL: ')
    recipe = Recipe(url)

    # loop forever so we can keep performing transformations
    already_printed = False
    while True:
        # print the recipe
        if not already_printed:
            print(recipe)

        already_printed = False

        # print available transformations
        print('\nAvailable transformations:')

        print('\tAdjust Amount (where %factor% is an integer, decimal, fraction, or mixed number) -> adjust %factor%')
        print('\tMake Vegetarian -> vegify')
        print('\tMake Vegan -> veganify')
        print('\tMake Non-Vegetarian -> meatify')
        print('\tTo Cuisine -> cuisine [italian | mexican]')
        print('\tMake Healthier -> healthy')
        print('\tMake Less Healthy -> not-healthy')

        print('\n\tTo exit the recipe transformer, enter \'stop\'.')
        print('\n\tTo start again with a new recipe, simply enter the recipe\'s url.')
        print('\n\tTo show a verbose version of the recipe, enter \'verbose\'. This must be entered every time you '
              'want a verbose output.')

        transformation = input('\nTransformation: ')

        if 'http://' in transformation or 'https://' in transformation:
            recipe = Recipe(transformation)
            continue

        transformation = transformation.lower()
        transformation = transformation.split(' ')

        args = ' '.join(transformation)

        if transformation[0] == 'stop':
            print('\n========================================')
            print('- {}'.format(args))
            print('========================================\n')
            print('bye!')
            break

        if transformation[0] == 'adjust':
            print('\n========================================')
            print('- {}'.format(args))
            print('========================================\n')

            factor = ' '.join(transformation[1:])
            factor = factor.strip()
            try:
                factor = parse_factor(factor)
            except ValueError:
                print('\nInvalid input for %factor%, it must be a number in either decimal or fraction form.\n')
                continue

            print('Adjusting the recipe by a factor of: ', factor)
            recipe.adjust_portions(factor)
            continue

        if transformation[0] == 'vegify':
            print('\n========================================')
            print('- {}'.format(args))
            print('========================================\n')

            replacements = recipe.vegify()
            replacements = list(replacements)

            # print what was changed
            print_replacements(replacements)

            # change steps to reflect changed ingredients
            recipe.change_step_ingredients(replacements)

            # remove steps with "meat"
            removals = []
            for i in range(len(recipe.steps)):
                if 'meat' in recipe.steps[i].raw:
                    removals.append(i)
            removals.reverse()
            for i in removals:
                recipe.steps.pop(i)

            continue

        if transformation[0] == 'veganify':
            print('\n========================================')
            print('- {}'.format(args))
            print('========================================\n')

            replacements = recipe.veganify()
            replacements = list(replacements)

            # print what was changed
            print_replacements(replacements)

            # change steps to reflect changed ingredients
            recipe.change_step_ingredients(replacements)

            # remove steps with "meat"
            removals = []
            for i in range(len(recipe.steps)):
                if 'meat' in recipe.steps[i].raw:
                    removals.append(i)
            removals.reverse()
            for i in removals:
                recipe.steps.pop(i)

            continue

        if transformation[0] == 'meatify':
            print('\n========================================')
            print('- {}'.format(args))
            print('========================================\n')

            replacements = recipe.meatify()
            replacements = list(replacements)

            # print what was changed
            print_replacements(replacements)

            # change steps to reflect changed ingredients
            recipe.change_step_ingredients(replacements)

            continue

        if transformation[0] == 'cuisine':
            print('\n========================================')
            print('- {}'.format(args))
            print('========================================\n')

            cuisine = transformation[1]

            if cuisine in ['mexican', 'italian']:
                replacements = recipe.to_cuisine(cuisine)
                replacements = list(replacements)

                # print what was changed
                print_replacements(replacements)

                # change steps to reflect changed ingredients
                recipe.change_step_ingredients(replacements)

                continue

        if transformation[0] == 'healthy':
            print('\n========================================')
            print('- {}'.format(args))
            print('========================================\n')

            replacements = recipe.healthier()
            replacements = list(replacements)

            # print what was changed
            print_replacements(replacements)

            # change steps to reflect changed ingredients
            recipe.change_step_ingredients(replacements)

            continue

        if transformation[0] == 'not-healthy':
            print('\n========================================')
            print('- {}'.format(args))
            print('========================================\n')

            replacements = recipe.less_healthy()
            replacements = list(replacements)

            # print what was changed
            print_replacements(replacements)

            # change steps to reflect changed ingredients
            recipe.change_step_ingredients(replacements)

            continue

        if transformation[0] == 'verbose':
            print('\n========================================')
            print('- {}'.format(args))
            print('========================================\n')

            print(recipe.get_verbose())
            already_printed = True
            continue

        print('\nSorry, that transformation was not recognized.')

        closest = get_closest_transform(' '.join(transformation))
        if closest is not None:
            print('Did you mean \'{}\'?'.format(closest))

        print()
        already_printed = True
