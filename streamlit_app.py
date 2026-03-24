# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

cnx = st.connection("snowflake")
session = cnx.session() 
#get_active_session()


# Write directly to the app
st.title(f":cup_with_straw: Customise Your Smoothie:cup_with_straw: ")
st.write(
  """Choose the fruits you want in your smoothie!
  """
)

# option = st.selectbox(
#     "What is your favourite Fruit?",
#     ("Banana", "Strawberries", "Peaches"),

# )

# st.write("You selected:", option)


name_on_order = st.text_input('Name on order')


my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to five ingredients: ', my_dataframe, max_selections = 5)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    # st.write(ingredients_string)

#my_dataframe = session.table("smoothies.public.orders").select(col('ingredients'))
# st.dataframe(data=my_dataframe, use_container_width=True)



# st.write(my_insert_stmt)
time_to_insert = st.button('Submit Order')

if time_to_insert and ingredients_list:
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered ' + name_on_order, icon="✅")
    
