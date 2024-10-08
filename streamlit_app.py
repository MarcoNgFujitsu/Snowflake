# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothies! 
    """
)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))


option = st.multiselect(
    'Choose up to 5 ingredients',
    my_dataframe,
    max_selections = 5
)


customer_name = st.text_input('Customer Name')


if st.button('Submit Order'):
    if not option:
        st.write('Please select at least 1 fruit')
    else:
    # elif len(option) <= 5:
        st.write('The fruits you have selected')
        ingredients = ','.join(option)
        st.write(ingredients)
        try:
            result = session.sql('insert into smoothies.public.orders (ingredients, customer_name) values (\'' + ingredients + '\',\''+customer_name + '\')')
            for r in result.collect()[0]:
                if r > 0: st.success('Your Smoothie is ordered!', icon="✅") 
                st.dataframe(data=session.sql('select * from smoothies.public.orders'))
        except:
            st.write('ERROR')            
        
    # else:
    #     st.write('You have selected', len(option), ' fruits. Only can select up to 5 fruits')

import requests
fruitvice_response = requests.get("https://fruitvice.com/api/fruit/watermelon")
st.text(fruitvice_response)
