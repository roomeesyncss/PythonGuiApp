class RecipeNode:
    def __init__(self, recipe):
        self.recipe = recipe
        self.children = []

class RecipeTree:
    def __init__(self, recipe):
        self.root = RecipeNode(recipe)

def display_recipe(recipe):
    print("-------------------------------------")
    print(f"Recipe ID:      {recipe['RecipeId']}")
    print(f"Recipe Name:    {recipe['RecipeName']}")
    print(f"Meal Type:      {recipe['MealType']}")
    print(f"Time Duration:  {recipe['TimeDuration']} minutes")
    print(f"Chef ID:        {recipe['ChefId']}")
    print("-------------------------------------\n")

def display_all_recipes(node):
    for recipe_node in node.children:
        display_recipe(recipe_node.recipe)
        display_all_recipes(recipe_node)

def display_recipe_menu(recipe, depth):
    print(f" | {recipe['RecipeName']:<17} |")
    print("+-------------------+-------------------+")

def display_recipe_tree(node, depth=0):
    if depth == 0:
        print("+-------------------+-------------------+")
        print("|                Recipe                |")
        print("+-------------------+-------------------+")

    for child in node.children:
        if depth == 0:
            print("/")
            print("/")
            print(f"      +--- {child.recipe['MealType']} ---+")

        display_recipe_menu(child.recipe, depth)
        display_recipe_tree(child, depth + 1)

def build_recipe_tree(connection):
    root_recipe = {'RecipeId': 0, 'MealType': 'Root', 'RecipeName': 'All Recipes', 'Ingredients': '', 'Steps': '', 'TimeDuration': 0, 'ChefId': 0}
    recipe_tree = RecipeTree(root_recipe)

    cursor = connection.cursor()

    query = "SELECT [RecipeId], [MealType], [RecipeName], [Ingredients], [Steps], [TimeDuration], [ChefId] FROM [master].[dbo].[RecipeData] ORDER BY [MealType], [RecipeName]"
    cursor.execute(query)

    current_parent = recipe_tree.root

    for row in cursor.fetchall():
        recipe = {
            'RecipeId': row[0],
            'MealType': row[1],
            'RecipeName': row[2],
            'Ingredients': row[3],
            'Steps': row[4],
            'TimeDuration': row[5],
            'ChefId': row[6]
        }

        new_node = RecipeNode(recipe)

        if recipe['MealType'] != current_parent.recipe['MealType']:
            current_parent = recipe_tree.root

        current_parent.children.append(new_node)
        current_parent = current_parent.children[-1]

    return recipe_tree
