import streamlit as st
import time
from cash_functions import *
import numpy as np
import pandas as pd
import plotly.graph_objects as go


st.set_page_config(page_title="Value Calculator ", layout="wide")

##future_State 1 sessoion
if "list_append" not in st.session_state:
    st.session_state.list_append = []
    
##future_State 2 sessoion
if "list_append_b" not in st.session_state:
    st.session_state.list_append_b = []

##NV  sessoion
if "new_list" not in st.session_state:
    st.session_state.new_list = []
if "sumofvalues" not in st.session_state:
    st.session_state.sumofvalues = []
if "d" not in st.session_state:
    st.session_state.d = {}

#terminal value
if "terminal_value" not in st.session_state:
    st.session_state.terminal_value = []
if "formula" not in st.session_state:
    st.session_state.formula = []
if "netcash" not in st.session_state:
    st.session_state.netcash = []
if "total_share" not in st.session_state:
    st.session_state.total_share = []
if "min" not in st.session_state:
    st.session_state.min = []
if "max" not in st.session_state:
    st.session_state.max = []
    




def main():
    st.title(f'DCF | Value Calculator: means time value of money')



 
    with st.form(key='future_value_form'):
        st.header("Future Cash Calculator 1")
        amount_future = st.number_input("Amount value (CF)", key="af", step=50)
        opration_future = st.number_input("Operational percentage", key="of", step=1)
        future_year = st.number_input("Year", min_value=1, key="fy")
        if st.form_submit_button("Calculate Future Value"):
            result = FvCalculator(amount_future, opration_future, future_year)
            if result:
                st.success(f"Future Value is {result}")

    st.markdown('''DCF based on time value of money, ***Future value(FV)*** is what would be the value of money that we have today sometime in the future ,then we move the money today through the future. Its called as **COMPOUNDING**
 ''')
    

    with st.form(key='future_value_form_b'):
        st.header("Future Cash Calculator 2")
        amount_future_b = st.number_input("Amount value (CF)", key='amount_b', step=50)
        opration_future_b = st.number_input("Operational percentage", key='opertunity_b', step=1)
        future_year_b = st.number_input("Year", min_value=1, key='year_b', step=1)
        if st.form_submit_button("Calculate Future Value B"):
            result_b = FvCalculator_b(amount_future_b, opration_future_b, future_year_b)
            if result_b:
                st.success(f"Future Value B: {result_b}")


    with st.form(key='npv_form'):
        st.header("NPV Calculator")
        st.markdown('''The sum of all the *+*present values** of the future cash flows''')
        if st.form_submit_button("Calculate NPV"):
            result = Nv()
            print(st.code(result))


    with st.form(key='terminal_value_form'):
        st.header("Terminal Value Calculator")
        st.markdown("""The rate at which free cash flow grows beyond 10 years called ***Terminal growth rate***
                    and ***Terminal value*** is the sum of all the future cash flows, beyond 10 years""")
        
        # generate = st.slider("Terminal growth rate", min_value=1, max_value=5, step=0.5)
        if st.form_submit_button("Calculate Terminal Value"):
            try:
                Terminal_VAlue = TerminalValue()
                st.success(f"Terminal Value: {round( Terminal_VAlue)}")
            except:
                st.error("Invalid input for Terminal CF")

    with st.form(key='present_value_form'):
        st.header("Present Value Calculator")
        st.markdown('''***Present value(FV)*** if we have to evaluate the value of money that we are expected to recieve in the future in today's term this is called **DISCOUNTING**''')
        if st.form_submit_button("Calculate Present Value"):
            try:
                pv = PVcalculate()
                st.success(f"Present Value: {round(pv, 2)}")
            except:
                st.error("Invalid input for Terminal Value or Years")

    with st.form(key='net_cash_form'):
        st.header("Net Cash per Share Calculator")
        net_cash = st.text_input("Net cash (in cr.)")
        shares = st.text_input("Shares (in cr.)")
        if st.form_submit_button("Calculate Net Cash per Share"):
            try:
                net_cash_value, total_shares = netCash(float(net_cash), float(shares))
                st.success(f"Net Cash: {net_cash_value:.2f}, Shares: {total_shares:.2f}")
            except:
                st.error("Invalid input for Net Cash or Shares")


    col1 , col2 = st.columns( [50,100], gap="large")
    with col1:
        if st.button("Calculate Fair Value"):
            try:
                fair = fairValue()
                progress_text = "Operation in progress. Please wait."
                my_bar = st.progress(0, text=progress_text)

                for percent_complete in range(100):
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1, text=progress_text)
                time.sleep(1)
                my_bar.empty()
                st.success(f"The possible valie range is {fair}")

            except:
                st.warning("Not applicable")
    with col2:

        if st.button("Exit",):
            st.cache_data.clear()
            st.stop()
    
    
    
    

    agree = st.checkbox("Visuals")
    if agree:
        ##cashflow visuals
        list_append_arr = np.array(st.session_state.new_list )
        years = []
        for i in range(1, len(list_append_arr)+1):
            years.append(f"year {i}")
        
     
        data = [go.Bar(
        x = years,
        y = list_append_arr
        )]

        fig = go.Figure(data=data)
        fig.update_layout(title={
            'text': "CFO growth YoY",
            'xanchor':'center',
            'yanchor':'top',
              'y':0.9,
            'x':0.5,
        }, font=dict(color='red',family="Courier New, monospace",
            size=18,))
    
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")



        ## net present value or reverse compounding
        data = st.session_state.d
        df = pd.DataFrame(list(data.items()), columns=['compound', 'discount'])
        fig = go.Figure(
            data=[
                go.Bar(name="compound", x=years, y=df['compound']),
                go.Bar(name="discount", x=years, y=df['discount']),

            ]
        )
        fig.update_layout(title={
            'text': "COMPOUNDING VS DISCOUNTING over the years",
            'xanchor':'center',
            'yanchor':'top',
              'y':0.9,
            'x':0.5,
        }, font=dict(color='red',family="Courier New, monospace",
            size=10,))
        
        st.plotly_chart(fig, theme='streamlit', use_container_width=True)
        

    st.caption(":black[More to come......for US by Me]")    

st.sidebar.title("Bit of explainations")
st.sidebar.markdown("""
1) :red[DCF analysis] attempts to determine the value of an investment today, based on projections of how much money that investment will generate in the future.


2) If the DCF is :green[higher than the current cost of the investment], **:blue[the opportunity could result in positive returns and may be worthwhile.]**
Companies typically use the ***weighted average cost of capital (WACC)*** for the discount rate because it accounts for the rate of return expected by shareholders.
                    
3) A disadvantage of DCF is its ***:reliance on estimations of future cash flows, which could prove inaccurate.***
                    
4) Its most useful when company is :green[generating roboust continous cash flow]  while bottom line or net profit is null
""")
st.sidebar.image('img.png', caption="DCF Analysis")

st.sidebar.caption(":black[More to come......for US by Me]")
if __name__ == "__main__":
    main()