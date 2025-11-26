```mermaid
classDiagram
    direction LR

    %% --- AUTH ---
    class Auth {
        + loginGoogle() (GET /auth/google/init)
        + callbackGoogle() (GET /auth/google/callback)
        + me() (GET /auth/me)
    }

    %% --- USERS ---
    class Users {
        + getUser() (GET /users/:id)
        + updateUser() (PATCH /users/:id)
        + getProgress() (GET /users/:id/progress)
        + addProgress() (POST /users/:id/progress)
    }

    %% --- INGREDIENTS ---
    class Ingredients {
        + listIngredients() (GET /ingredients)
        + createIngredient() (POST /ingredients)
        + getIngredient() (GET /ingredients/:id)
        + updateIngredient() (PATCH /ingredients/:id)
        + deleteIngredient() (DELETE /ingredients/:id)
    }

    %% --- RECIPES ---
    class Recipes {
        + listRecipes() (GET /recipes)
        + createRecipe() (POST /recipes)
        + getRecipe() (GET /recipes/:id)
        + updateRecipe() (PATCH /recipes/:id)
        + deleteRecipe() (DELETE /recipes/:id)
        + addIngredient() (POST /recipes/:id/ingredients)
    }

    %% --- MEAL TYPES ---
    class MealTypes {
        + listMealTypes() (GET /meal-types)
        + getMealType() (GET /meal-types/:id)
    }

    %% --- DAYS ---
    class Days {
        + listDays() (GET /plans/:plan_id/days)
        + getDay() (GET /plans/:plan_id/days/:day_id)
        + assignRecipe() (POST /plans/:plan_id/days/:day_id/assign)
    }

    %% --- PLANS ---
    class Plans {
        + getWeeklyPlan() (GET /plans/:user_id/weekly)
        + createWeeklyPlan() (POST /plans/:user_id/weekly)
        + getPlan() (GET /plans/:plan_id)
        + updatePlan() (PATCH /plans/:plan_id)
        + deletePlan() (DELETE /plans/:plan_id)
    }

    %% --- SHOPPING LIST ---
    class ShoppingList {
        + generateList() (GET /plans/:plan_id/shopping-list)
        + exportToGoogleTasks() (POST /plans/:plan_id/shopping-list/export/google-tasks)
    }

    %% --- RELACIONES ---
    Auth --> Users
    Users --> Plans
    Plans --> Days
    Days --> Recipes
    Recipes --> Ingredients
    Days --> MealTypes
    Plans --> ShoppingList
