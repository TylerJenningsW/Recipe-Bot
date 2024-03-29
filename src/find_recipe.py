from string import capwords
from src.recipe_object import db

 
def recipe_find(input: str) -> list:
    try:
        # "<@!" Refers to when a user auto-completes using "@" to find a user
        if input.startswith("<@!"):
            author_id = int(''.join(filter(str.isdigit, input)))
            recipes = db.child("Recipes").order_by_child(
                "Author").equal_to(author_id).get()
        else:
            recipe_name = input.lower()
            recipes = db.child("Recipes").order_by_child(
                "Recipe").equal_to(recipe_name).get()
        our_recipe = recipes.val()
        items = list(our_recipe.items())
        return items
    except:
        return 0


def recipe_delete(input: str, user_id: int, user: str) -> str:
    try:
        recipes = db.child("Recipes").order_by_child(
            "Recipe").equal_to(input).get()
        our_recipe = recipes.val()
        items = list(our_recipe.items())
        
       # Delete recipe if record exists, and user has permission
        if user_id == items[0][1]["Author"]:
            try:
                db.child("Recipes").child(
                    f"{input} by {user}").remove()
                end = f"\"{capwords(input)}\" has been deleted!"
            except:
                end = f"You do not have a recipe with the name \"{input}\"."
                return end
        else:
            end = f"You do not own the recipe \"{input}\"."

    except:
        end = f"No recipes with the name \"{input}\" exist."

    return end

def separate_ingredients(items: list) -> str:
    recipe_ingredients = items
    ingredients = ' '
    for x in recipe_ingredients:
        if x != recipe_ingredients[-1]:
            ingredients += x + ', '
        else:
            ingredients += x
    return ingredients
