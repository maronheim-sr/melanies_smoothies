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

# Get fruit options
fruit_df = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME")).collect()
fruit_list = [row["FRUIT_NAME"] for row in fruit_df]

# Multiselect input
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_list,
    max_selections=5
)

# # Submit button
# if st.button('Submit Order'):
#     if ingredients_list and name_on_order:
#         ingredients_string = ' '.join(ingredients_list)
#         my_insert_stmt = f"""
#             INSERT INTO smoothies.public.orders (ingredients, name_on_order)
#             VALUES ('{ingredients_string}', '{name_on_order}')
#         """
#         session.sql(my_insert_stmt).collect()
#         st.success(f"Your Smoothie is ordered! {name_on_order}", icon="✅")
#     else:
#         st.warning("Please enter a name and select at least one ingredient.")

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    for fruit_chosen in ingredients_list:
        # Dynamically fetch data for each selected fruit
        fruit_name = fruit_chosen.lower()
        response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{fruit_name}")
        
        if response.status_code == 200:
            fruit_data = response.json()
            st.subheader(f"Nutrition Info for {fruit_chosen}")
            st.dataframe(data=fruit_data, use_container_width=True)
        else:
            st.warning(f"Could not fetch data for {fruit_chosen}")

