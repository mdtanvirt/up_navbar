import sys
import time
import openai
import random
import pandas as pd
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
import json
import uuid
import numpy as np
# from datetime import datetime
import hydralit_components as hc
#import auth_functions
from streamlit_ace import st_ace
from components import logic_generator
from components import plot_graphs
from components import login_form
from components import user_info
from components import buy_and_hold
from components import save_data
from components import date_range_validator
from ui_components import custom_navigator
from models import create_logic_model
import datetime
# from helpers import cookies_manager




st.set_page_config(layout="wide")
col1, col2 = st.columns([3, 1])
inputParams = ""
optimizer_code = ""
generated_code = ""
saved_strategies = []



## -------------------------------------------------------------------------------------------------
## Not logged in -----------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
if 'user_info' not in st.session_state:
    auth_notification = login_form.lform()

## -------------------------------------------------------------------------------------------------
## Logged in --------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
else:
    
    # Define the Streamlit app layout
    col1.title('Trading Strategy Simulator')
    information = user_info.showUserInfo(),
    
    
    st.sidebar.title('Trading Actions')
    if 'user_info' in st.session_state:
        saved_strategies = save_data.fetch_logic_for_user(st.session_state.user_info["email"])
    
    if 'el_logic_script' not in st.session_state:
        st.session_state['el_logic_script'] = ""
        
    if 'current_strategy_name' not in st.session_state:
        current_strategy_name = f"Strategy-{datetime.datetime.now().date()}"
        st.session_state['current_strategy_name'] = current_strategy_name
        
    
    ## Editor --------------------------------------------------------------------------------------
    with col1:
        st.write("EasyLanguage Here:")
        # el_script = code_editor(st.session_state['el_logic_script'], lang="EasyLanguage", allow_reset=True, height=[6, 12])
        el_script = st_ace(auto_update=True, theme="github", key="ace-editor")
    
    ## Asset Name Input Field --------------------------------------------------------------------------------------
    asset_name = col1.text_input('Please Enter Asset names sepread with comma (,):', value="AAPL")
    
    ## Propose Logic Name --------------------------------------------------------------------------------------
    logic_name = col1.text_input('Strategy Name:', st.session_state['current_strategy_name'])
    
    ## Add a dropdown for selecting the interval 
    interval_options = {
        '1h': '1h',  # Yahoo Finance uses '1h', '2h' format for hourly data
        '2h': '2h',  # Yahoo Finance uses '1h', '2h' format for hourly data
        '1d': '1d'
    }
    # Set '1d' as the default interval
    selected_interval = col2.selectbox('Select Bar Interval:', list(interval_options.keys()), index=2)
    # Get the corresponding interval value
    interval_value = interval_options[selected_interval]
    
    ## --------------------------------------------------------------------------------------
    ## Left Bar ---------------------------------------------------------------
    ## --------------------------------------------------------------------------------------
    col2.subheader("Time Period")
    
    ## Date Period ---------------------------------------------------------------
    start_date = col2.date_input('Start Date:',datetime.date(2022, 7, 6)).strftime('%Y-%m-%d')
    end_date = col2.date_input('End Date:',datetime.date(2023, 7, 6)).strftime('%Y-%m-%d')
    
    valid_start_date, valid_end_date, date_range =  date_range_validator.get_valid_date_range(start_date, end_date, interval_value)
    
    # col1.warning(f"Note: Make sure that the time period for given interval is between: 1 and {date_range}")
    
    
    def strategy_logic(data):
        # Default strategy logic goes here - to be replaced with the generated code
        pass

    def grid_optimizer(data, strategy_logic):
        # Default strategy logic goes here - to be replaced with the generated code
        pass
    ## Fetch Saved Logics --------------------------------------------------------------------------------------

    def simulate_trading_strategy(strategy_logic, data):
        balance_history, trade_actions, final_balance, max_drawdown_percentage = strategy_logic(data)
        return balance_history, trade_actions, final_balance, max_drawdown_percentage
    
    def opt_trading_strategy(data, grid_optimizer, strategy_logic):
        balance_history, trade_actions, final_balance, max_drawdown_percentage, opt_params = grid_optimizer(data, strategy_logic)
        return balance_history, trade_actions, final_balance, max_drawdown_percentage, opt_params
                
                
    
    ## Saved Logics ---------------------------------------------------------------
    def on_button_click(logic_item):
        st.session_state['params'] = logic_item.params
        st.session_state['current_strategy_name'] = logic_item.logic_name
        st.session_state['active_strategy_id'] = logic_item.logic_id
        st.session_state['optimizer_code'] = logic_item.optimizer_code
        st.session_state['generated_logic'] = logic_item.original_logic_script
        st.session_state['el_logic_script'] = logic_item.el_script
        
    
    col2.subheader("Saved Logics")
    
    if 'all_logic_names' not in st.session_state:
        st.session_state['all_logic_names'] = []
    if saved_strategies:
        if 'active_strategy_id' not in st.session_state:
            st.session_state['active_strategy_id'] = saved_strategies[0].logic_id;
        navigators = custom_navigator.CustomNavigation(saved_strategies, st.session_state['active_strategy_id'], on_button_click)
        navigators.render(col2)
        # print(st.session_state['all_logic_names'])
    
    ## -------------------------------------------------------------------------------------------------
    ## Start Simulator ---------------------------------------------------------------------------------
    ## -------------------------------------------------------------------------------------------------
    if col1.button("Run Simulator"):
        
        if not el_script:
            alert = col1.error("Please provide the Easy Language Script!") # Display the alert
            time.sleep(3) # Wait for 3 seconds
            alert.empty()
            
        else:
            if 'generated_logic' in st.session_state and 'optimizer_code' in st.session_state and st.session_state['current_strategy_name']:
                del st.session_state['generated_logic']
                del st.session_state['optimizer_code']
                del st.session_state['params']
        
        if 'generated_logic' not in st.session_state:
            with col1:
                with st.spinner('Generating input fields...'):
                    inputParams = logic_generator.generate_parameters_inputs(el_script)
                    # st.session_state['params'] = inputParams
            with col1:   
                with st.spinner('Generating Logic Code Please Wait...'):
                    generated_code = logic_generator.generate_strategy_code(el_script, inputParams)
                    # print(generated_code)
                    # st.session_state['generated_code'] = generated_code
            with col1:    
                with st.spinner('Building Optimizer Please Wait...'):
                    optimizer_code = logic_generator.generate_opt_code(generated_code, inputParams)
                    # st.session_state['optimizer_code'] = optimizer_code
        else:
            generated_code = st.session_state['generated_code']
            optimizer_code = st.session_state['optimizer_code']
            inputParams = st.session_state['params']
            
        col1.success("DONE")
        
        # print(generated_code)
        # print("-----------------------------------------")
        # print(inputParams)
        # print("-----------------------------------------")
        # print(optimizer_code) 
        

        # Execute the generated code to replace the placeholder strategy_logic function
        try:
            exec(inputParams)
            exec(generated_code)
            exec(optimizer_code)
            st.session_state['params'] = inputParams
            st.session_state['generated_logic'] = generated_code
            st.session_state['optimizer_code'] = optimizer_code
        except Exception as e:
            col1.warning(e)
            col1.error("Apologies: The Generated Optimizer Code Or Generated Strategy Logic code has an error, please run simulator again")

    all_assets = asset_name.replace(" ", "").split(",")
    if 'generated_logic' in st.session_state and 'optimizer_code' in st.session_state and 'params' in st.session_state:
        generated_code = st.session_state['generated_logic']
        optimizer_code = st.session_state['optimizer_code']
        params = st.session_state['params']
        exec(params)
        exec(generated_code)
        exec(optimizer_code)
        
        for asset in all_assets: 
            col1.title(asset)
            try:
                # Fetch the data with the specified interval
                data = yf.download(tickers=asset, interval=interval_value, start=start_date, end=end_date)
                
                if data.empty:
                    col1.error("No data returned for the selected interval and date range. Please try a different interval or date range.")
                    
            except Exception as e:
                st.error(f"An error occurred while fetching the data: {e}")
            balance_history, trade_actions, final_balance, max_drawdown_percentage = simulate_trading_strategy(strategy_logic, data)
            balance_df = pd.DataFrame(balance_history)
            # Plot the charts
            balance_chart = plot_graphs.plot_balance_chart(balance_df, trade_actions)
            candlestick_chart = plot_graphs.plot_candlestick_chart(data, trade_actions)

            col1.header('Trader Logic')
            # Display charts
            col1.plotly_chart(balance_chart, use_container_width=True)
            col1.plotly_chart(candlestick_chart, use_container_width=True)
            col1.write(f'Final Balance: ${(final_balance):,.2f}')
            col1.write(f'Maximum Drawdown: ${(max_drawdown_percentage):,.2f}')
            
            bh_balance_history, bh_trade_actions, bh_final_balance, bh_max_drawdown_percentage = buy_and_hold.buy_hold_logic(data)
            bh_balance_df = pd.DataFrame(bh_balance_history)
            
            # Buy Hold charts
            bh_balance_chart = plot_graphs.plot_balance_chart(bh_balance_df, bh_trade_actions)
            bh_candlestick_chart = plot_graphs.plot_candlestick_chart(data, bh_trade_actions)


            col1.header('Buy And Hold Logic')
            # Display charts
            col1.plotly_chart(bh_balance_chart, use_container_width=True)
            col1.plotly_chart(bh_candlestick_chart, use_container_width=True)
            col1.write(f'Buy And Hold Strategy Final Balance: ${(bh_final_balance):,.2f}') 
            col1.write(f'Maximum Drawdown: ${(bh_max_drawdown_percentage):,.2f}')

            # Start Optimizer
            opt_balance_history, opt_trade_actions, opt_final_balance, opt_max_drawdown_percentage, opt_params = opt_trading_strategy(data, grid_optimizer, strategy_logic)
            opt_balance_df = pd.DataFrame(opt_balance_history)
            
            # Optimized Charts
            opt_balance_chart = plot_graphs.plot_balance_chart(opt_balance_df, opt_trade_actions)
            opt_candlestick_chart = plot_graphs.plot_candlestick_chart(data, opt_trade_actions)

            col1.header('Optimized')
            # Display charts
            col1.plotly_chart(opt_balance_chart, use_container_width=True)
            col1.plotly_chart(opt_candlestick_chart, use_container_width=True)
            col1.write(f'Best Parameters: ${opt_params}')
            col1.write(f'Optimized Final Balance: ${(opt_final_balance):,.2f}')
            col1.write(f'Maximum Drawdown: ${(opt_max_drawdown_percentage):,.2f}')

            user_email = st.session_state.user_info["email"]

            if st.session_state['current_strategy_name'] not in st.session_state['all_logic_names']:
                new_logic_document_id = uuid.uuid4()
                logic_model = create_logic_model.CreateLogicScript(
                    params=params,
                    original_logic_script=generated_code,
                    optimizer_code=optimizer_code,
                    el_script=el_script, 
                    created_by=user_email,
                    logic_name=logic_name,
                    logic_id=f"{new_logic_document_id}"
                )

                model_data = logic_model.to_dict()
                save_data.save_logic_for_user(user_email, model_data, new_logic_document_id)

        ## -------------------------------------------------------------------------------------------------
        ## Show User Info (Email) --------------------------------------------------------------------------
        ## -------------------------------------------------------------------------------------------------



