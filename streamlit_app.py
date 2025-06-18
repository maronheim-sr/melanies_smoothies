import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

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

# Submit button
if st.button('Submit Order'):
    if ingredients_list and name_on_order:
        ingredients_string = ' '.join(ingredients_list)
        my_insert_stmt = f"""
            INSERT INTO smoothies.public.orders (ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered! {name_on_order}", icon="✅")
    else:
        st.warning("Please enter a name and select at least one ingredient.")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)
