import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
# session = get_active_session()

# Get fruit options with both display and search values
fruit_df = session.table("smoothies.public.fruit_options").select(
    col("FRUIT_NAME"), col("SEARCH_ON")
).collect()

# Create a mapping from display name to search term
fruit_map = {row["FRUIT_NAME"]: row["SEARCH_ON"] for row in fruit_df}
fruit_list = list(fruit_map.keys())

# Multiselect input
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_list,
    max_selections=5
)

# Submit button
if st.button('Submit Order'):
    if ingredients_list and name_on_order:
        ingredients_string = ' '.join(ingredients_list)
        my_insert_stmt = f"""
            INSERT INTO smoothies.public.orders (ingredients, name_on_order, order_filled)
            VALUES ('{ingredients_string}', '{name_on_order}', 0)
        """
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered! {name_on_order}", icon="✅")
    else:
        st.warning("Please enter a name and select at least one ingredient.")


if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    for fruit_display in ingredients_list:
        search_term = fruit_map[fruit_display].lower()
        response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_term}")

        if response.status_code == 200:
            fruit_data = response.json()
            st.subheader(f"{fruit_display} Nutrition Information")
            st.dataframe(data=fruit_data, use_container_width=True)
        else:
            st.warning(f"Could not fetch data for {fruit_display}")

