import streamlit as st
from colorama import Fore

def FvCalculator(amount_future, opration_future, future_year):
    try:
                                         #change
        sixth_term = 0
        list_append = []
        for i in range(1,int(future_year)+1):
            amount = float(amount_future)
            oppertunity_cost = float(opration_future)
            oppertunity_cost = oppertunity_cost/100
            formula = amount*((1+ oppertunity_cost)**i)
            list_append.append(formula)

        st.session_state.list_append = list_append
            # ----------------

        print(list_append)
        sixth_term = list_append[len(list_append)-1] * 1.1
        # return list_append, sixth_term
        st.code(f"{round(sixth_term, 2)}" )
    
    except:
        st.error("Only numerical values are accepted! Please fill in all the inputs.")
        return None




def FvCalculator_b(amount_future_b, opration_future_b, future_year_b):
    try:
        # global list_append_b, new_list
        list_append_b = []
        get_amount = amount_future_b
        list_append_b.append(float(get_amount))
        for i in range(1,int(future_year_b)+1):
            amount = float(amount_future_b)
            oppertunity_cost = float(opration_future_b)
            oppertunity_cost = oppertunity_cost/100
            formula = amount*((1+ oppertunity_cost)**i)
            list_append_b.append(formula)

        st.session_state.list_append_b = list_append_b
        new_list  = st.session_state.list_append+list_append_b
        return new_list
        
    except:
        st.error("Only numerical values are accepted! Please fill in all the inputs.")
        return None




def Nv():

    try:
        percentage = 0.09
        amount_list = []
        new_list = st.session_state.list_append + st.session_state.list_append_b
        st.session_state.new_list = new_list
        d = {}
        for i in range(len(new_list)):
            amount = (new_list)
            formula = amount[i]/((1+ percentage)**(i+1))
            amount_list.append(formula)
            d[(new_list[i])] = amount_list[i]
        print(Fore.CYAN +"{future value : current value }"+ str(d))
        pvvaluelist = list(d.values())
        sumofvalues = sum(pvvaluelist)
        st.session_state.sumofvalues = sumofvalues
        st.session_state.d = d
        return d
    except:
        print(Fore.RED + "Couldn't get sufficient value")




def TerminalValue():
    fcashFlow = st.session_state.new_list[len(st.session_state.new_list)-1]
    getrate = 0.035
    discountrate = 0.09
    Terminal_VAlue = fcashFlow * (1 + float(getrate)) / (discountrate - float(getrate))
    st.session_state.terminal_value = Terminal_VAlue
    # st.success("submitted..")
    return Terminal_VAlue

def PVcalculate():
    formula = st.session_state.terminal_value / ((1 + 0.09) ** len(st.session_state.new_list))
    st.session_state.formula = formula
    st.code(st.session_state.formula)
    return formula

def netCash(netcah, totalShare):
    st.session_state.netcash = netcah
    st.session_state.total_share = totalShare
    return netcah, totalShare

def fairValue():
    valuation = st.session_state.formula  +  st.session_state.sumofvalues  + st.session_state.netcash 
    FairValue = valuation / float(st.session_state.total_share)
    possibleValuemin = FairValue * (1 - 0.1)
    possibleValuemax = FairValue * (1 + 0.1)
    # st.success(f"The possible valie range is {possibleValuemin} and {possibleValuemax}")
    st.session_state.min = possibleValuemin
    st.session_state.max = possibleValuemax
    return possibleValuemin, possibleValuemax

