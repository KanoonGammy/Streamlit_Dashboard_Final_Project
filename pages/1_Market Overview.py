# import necessary libraries
import pandas as pd
import streamlit as st
import yfinance as yf
import pandas_ta as ta
import seaborn as sns
import datetime
import matplotlib.pyplot as plt
import time
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from select_market import select_market
st.set_page_config(layout="wide")

#https://docs.streamlit.io/develop/api-reference/data/st.metric
#"""===================================IMPORT DATA==================================="""
@st.cache_resource()
def import_data(period = 3650):
    # import data price
    dp = pd.read_csv("source_price.csv").tail(period) # from souce
    dp.Date = pd.to_datetime(dp["Date"]) # set Date as Datetime
    dp = dp.set_index("Date") # set index

    # rename columns
    t = [x.split(".")[0] for x in dp.columns] # list comprehesion >> split .BK
    index_set = t.index("^SET") # find ^SET index
    t[index_set] = "SET" # rename ^SET as SET
    dp.columns = t # rename index

    # clean data
    pass

    # import data volume
    dv = pd.read_csv("source_volume.csv",).tail(3650) 
    dv.Date = pd.to_datetime(dv['Date'])
    dv = dv.set_index("Date")
    dv.columns = t #use columns dp

    # import data marketcap
    mc = pd.read_csv("source_mkt.csv")
    mc = mc.set_index(mc.columns[0]).T
    m = [x.split(".")[0] for x in mc.columns]
    mc.columns = m
    mc = mc.T.reset_index().rename(columns = {"index": "Symbols"})
    mc["MarketCap"] = mc["MarketCap"].astype(float).fillna(0)

    return dp,dv,mc

#import data
dp,dv,mc = import_data()
#raw standard
raw_std = pd.read_csv("https://raw.githubusercontent.com/KanoonGammy/Technical-Analysis-Project/refs/heads/main/SET_Index.csv", index_col= "Unnamed: 0").sort_values(["symbol"], ascending= True)
raw_set50 = pd.read_csv("https://raw.githubusercontent.com/KanoonGammy/Technical-Analysis-Project/refs/heads/main/SET50.csv")['symbol'].tolist()
raw_set100 = pd.read_csv("https://raw.githubusercontent.com/KanoonGammy/Technical-Analysis-Project/refs/heads/main/SET100.csv")['symbol'].tolist()

hc1,hc2,hc3 = st.columns([7,7,2])
with hc1:
    st.header("APG Station: Market Overviews")
    pass
#"""===================================Count Change==================================="""
with hc2: # พักเก็บ counting daily
    pass
    #     def count_change(data):
    #         df = data[selection].copy()
    #         df = df.pct_change()
    #         df = df.iloc[-1]

    #         gtz = (df > 0).sum()
    #         eqz = (df == 0).sum()
    #         ltz = (df < 0).sum()

    #         count = {"Positive": [gtz], "Unchanged": [eqz], "Negative": [ltz]}
    #         df_count = pd.DataFrame(count).T
    #         df_count.index.name = "Status"
    #         df_count.columns = ["Count"]
    #         df_count = df_count.reset_index()
    #         fig_count = px.bar(df_count, y = "Status",
    #                             x =  "Count",
    #                             color = "Status",
    #                             color_discrete_map= {'Negative': "red", "Unchanged": "yellow", "Positive": "green"},
    #                             title = f"Market:'{sl11}' Sector:'{sl13}' Options:'{sl12}'  Sub-sector:'{sl14}' ",
    #                             labels = {"Count": f"date: {str(df.name).split(" ")[0]}", "Status": ""},
    #                             text = "Count", text_auto= False,
    #                             width= 800, height = 250)

    #         return fig_count
    #     st.write(count_change(dp))

with hc3: # พับเก็บ counting all the past
    #"""===================================SHOW SET INDEX==================================="""
    SI = dp[["SET"]].copy().ffill().bfill()
    SI["Change"] = SI.pct_change()
    st.metric("SET Index", value = f"{SI["SET"].iloc[-1]:.2f}", delta = f"{SI["Change"].iloc[-1]:.4f}%" )
    # def count_change_line(data):
    #     # pct change
    #     df = data[selection].copy()
    #     df = df.resample("B").last()
    #     df = df.pct_change()

    #     # rule >, <, =
    #     gtz = (df>0).sum(1)
    #     eqz = (df==0).sum(1)
    #     ltz = (df<0).sum(1)

    #     # insert value to df
    #     df["Positive"] = gtz.values
    #     df["Unchanged"] = eqz.values
    #     df["Negative"] = ltz.values
    #     # resamping as Weekly using last price
    #     df = df[["Positive", "Unchanged", "Negative"]].reset_index()
    #     df['Date'] = pd.to_datetime(df['Date'])
    #     l,h = st.slider("Choose Datetime", 
    #                     min_value=  df['Date'].iloc[0].to_pydatetime(),
    #                     max_value= df['Date'].iloc[-1].to_pydatetime(),
    #                     value = (df['Date'].iloc[0].to_pydatetime(),df['Date'].iloc[-1].to_pydatetime()),
    #                     format= "YYYY-MM")
    #     l = l.strftime("%Y-%m-%d")
    #     h = h.strftime("%Y-%m-%d")
    

    #     melted_df = pd.melt(df, id_vars = ["Date"],
    #                         value_vars= ["Positive", "Unchanged", "Negative"],
    #                         var_name = "Status",
    #                         value_name= "Count")
    #     melted_df.set_index("Date", inplace = True)
    #     # melted_df = melted_df.loc[l:h]

    #     fig_bar = px.bar(melted_df, x= melted_df.index, y = "Count",
    #                     color = "Status",
    #                     color_discrete_map= {'Negative': "red", "Unchanged": "yellow", "Positive": "green"},
    #                     barmode= "stack")
    #     fig_bar.update_layout(bargap=0) 
    #     return fig_bar
    # st.write(count_change_line(dp))
#"""===================================SETTING TAB==================================="""
tab1, tab2, tab3, tab4 = st.tabs(["          🏆 Ranking and Change          ", "          📈 Performance and 52 Week High Low          ",
                             "          📊 Volume Analysis          ", "          🔥 Sector Heatmap          "])

#"""===================================TAB 1==================================="""
with tab1:
    #"""===================================SETTING Sidebar==================================="""
    selection = None
    # with st.sidebar:
    rawt1,sl11,sl12,sl13,sl14 = select_market("tab1")
    rawt1["sub-sector"] = rawt1["sub-sector"].fillna("None")
    
    selection = rawt1.reset_index(drop = True)
    selection.index = selection.index + 1
    selection = selection["symbol"]

# create columns
    col0, col1 = st.columns([1,3])
    
    with st.spinner("Loading..."):
        with col1:
            ct1c1, ct1c2 = st.columns([1,2]) 
            with ct1c1:
                st.subheader("Price vs Volume Percentage Change")
            with ct1c2:
                st.write("")
                #create tickbox
                show_name = st.checkbox("🎉 Show Name")

    def VP_change(interval = "D", show_name = False):
        #setting percent change period
        period = None
        if interval == "D":
            period = 1
        elif interval == "W":
            period = 5
        elif interval == "M":
            period = 22
        elif interval == "3M":
            period = 65
        else:
            period = 1

        #check na
        select_df = dv[selection]
        check = select_df.iloc[-1].dropna().index.tolist()

        #price change
        pc = dp[check].pct_change(period).iloc[-1]
        pc = pc.T
        #volume
        pv = dv[check].ewm(span = 5, adjust = False).mean().pct_change(period).iloc[-1] #เรียก libs ไม่ได้
        pv = pv.T

        #combine
        cb_df = pd.DataFrame()
        cb_df["Symbols"] = pc.index
        cb_df[f"Price %Change {interval}"] =  pc.values*100
        cb_df[f"Volume %Change {interval}"] =  pv.values*100
        cb_df = cb_df.merge(rawt1, left_on= "Symbols" ,right_on= "symbol", how = "left")
        cb_df = cb_df.merge(mc, left_on = "Symbols", right_on = "Symbols", how = "left")

        df_use = cb_df.copy()
        data_source = df_use.drop(["symbol","full name", "market", "sector", "sub-sector"], axis = 1)

        #chart show
        text_interval = "Daily" if interval == "D" else "Weekly" if interval == "W" else "Montly" if interval == "M" else "Quaterly" if interval == "3M" else None 
        VP_chart = px.scatter(df_use, x = f"Price %Change {interval}",
                            y = f"Volume %Change {interval}",
                            color = "sector",
                            text = "Symbols" if show_name else None,
                            #facet_col= "market", facet_col_spacing= None,
                            custom_data= ["Symbols", "MarketCap", "sub-sector", f"Price %Change {interval}", f"Volume %Change {interval}"], #send details to update_traces becuase plotly already has relocated the data
                            size = "MarketCap",
                            title = f"{text_interval} Price vs Volume Percentage Change",
                            template = "seaborn")
        
        # update details in the hover
        VP_chart.update_traces(
        hovertemplate="<b>Name:</b> %{customdata[0]}<br>" +
                    "<b>Marketcap:</b> %{customdata[1]:,.0f} THB<extra></extra><br>" + 
                    "<b>SubSector:</b> %{customdata[2]}<br>"+
                    f"<b>{text_interval} Price %Change: </b>" "%{customdata[3]:.2f}<br>"+
                    f"<b>{text_interval} Volume %Change: </b>" "%{customdata[4]:.2f}<br>",
        textposition = "bottom center",)

        VP_chart.update_layout(
            hovermode= "closest"
            )
        
        #add red line
        VP_chart.add_vline(x=0, line_color='red', line_width=2, opacity=0.6)
        VP_chart.add_hline(y=0, line_color='red', line_width=2, opacity=0.6)

        return VP_chart, data_source

    def RS_Score():
        #clean data by ffill then bfill
        data = dp.copy().ffill()
        data = data.bfill()

        #calcuate return quarterly
        Q1 = data.pct_change(65).iloc[-1]
        Q2 = data.pct_change(130).iloc[-1]
        Q3 = data.pct_change(195).iloc[-1]
        Q4 = data.pct_change(260).iloc[-1]

        #build dataframe
        rs_data = pd.DataFrame()
        rs_data["Q1"] = Q1
        rs_data["Q2"] = Q2
        rs_data["Q3"] = Q3
        rs_data["Q4"] = Q4
        rs_data["RS Score"] = np.round(0.4*Q1 + 0.2*Q2 + 0.2*Q3 + 0.2*Q4,4)

        #rs score
        rs_data["Rank"] = rs_data["RS Score"].rank(ascending= False, method = "max")
        rs_data.reset_index(inplace = True,)
        rs_data = rs_data.sort_values("Rank",ascending= True)
        rs_data["Return"] = rs_data["RS Score"]

        rs_data.rename(columns = {"index": "Name"}, inplace =True)
        rs_data["RS Score"] = 1 / (1+ np.e**(-rs_data["RS Score"]))

        #for display
        rs_data = rs_data.merge(rawt1, left_on = "Name", right_on = "symbol", how = "left")
        sorted_data = rs_data[["Name", "RS Score","market","sector", "sub-sector", "Rank", "Return"]] #"Q1", "Q2","Q3", "Q4"]]
        sorted_data.dropna(inplace = True)
        data_source = sorted_data.copy()
        # sorted_data.index = sorted_data.index.astype(int)
        sorted_data.set_index("Rank", inplace = True)
        sorted_data = sorted_data[sorted_data["Name"].isin(selection)]
        return sorted_data, data_source
    
    with col0:
        rs_score, rs_score_data = RS_Score()
        rs_score_data.attrs["description"] = "RS_Score Ranking contains a performance score"
        st.subheader("RS Ranking")
        st.dataframe(rs_score,height= 850, width= 500)
        # st.write("rs_score_data") ################################################ data source ################################################

    with col1:
        scol0, scol1 = st.columns(2)

        with scol0:
            
            VP_change_D, VP_change_D_data = VP_change(interval = "D", show_name= show_name)
            # st.write("VP_change_D_data") ################################################ data source ################################################
            st.plotly_chart(VP_change_D)
            VP_change_D_data.attrs["description"] = "Price and Volume Percentage Change in Daily" 

        with scol1:
            VP_change_W, VP_change_W_data = VP_change(interval = "W", show_name= show_name)
            # st.write("VP_change_W_data") ################################################ data source ################################################
            st.plotly_chart(VP_change_W)
            VP_change_W_data.attrs["description"] = "Price and Volume Percentage Change in Weekly"


        scol2, scol3 = st.columns(2)
        with scol2:
            VP_change_M, VP_change_M_data = VP_change(interval = "M", show_name= show_name)
            # st.write("VP_change_M_data") ################################################ data source ################################################
            st.plotly_chart(VP_change_M)
            VP_change_M_data.attrs["description"] = "Price and Volume Percentage Change in Monthly"


        with scol3:
            VP_change_3M, VP_change_3M_data = VP_change(interval = "3M",  show_name= show_name)
            # st.write("VP_change_3M_data") ################################################ data source ################################################
            st.plotly_chart(VP_change_3M)
            VP_change_3M_data.attrs["description"] = "Price and Volume Percentage Change in Quaterly"


    st.divider()
#"""===================================TAB 2==================================="""
with tab2:
    st.markdown("""
    <style>
    div.stRadio {
        margin-top: 0.1px;  /* ระยะห่างด้านบน */
        margin-bottom: 0.1px;  /* ระยะห่างด้านล่าง */
        gap: 0.2px;
    }
    div.stCheckbox {
    margin-top: 0.1px;  /* ลดระยะห่างด้านบนของ checkbox */
    margin-bottom: 0.1px;  /* ลดระยะห่างด้านบนของ checkbox */
    }
    </style>
    """, unsafe_allow_html=True)
    start = (datetime.datetime.now() - datetime.timedelta(100)).strftime("%Y-%m")

    #=================== Performance 100 days =========================
    @st.cache_resource
    def geo_calculation(start , end = None):
        df = dp[start: end].copy().ffill().bfill()
        geo_df = (df.pct_change()+1).cumprod()
        geo_df = geo_df.reset_index().melt(id_vars = ["Date"], value_vars= geo_df.columns, var_name= "Name", value_name= "Return")
        geo_df = geo_df.merge(raw_std, left_on = "Name", right_on = "symbol",how = "left").drop(["full name", "symbol"], axis = 1)

        SET_t2 = geo_df[geo_df["market"] == "SET"]
        mai_t2 = geo_df[geo_df["market"] == "mai"]

        return SET_t2,mai_t2
    
    # @st.cache_resource
    def plot_geo(data, select_sector, select_sub):
        data = data[data["sector"] == select_sector]
        if select_sub != None:
            data = data[data["sub-sector"] == select_sub]
        geo_fig = px.line(data, x = "Date",
                        y = "Return",
                        color = "Name",
                        title = f"Performance: Sector:<br> &nbsp;Sector: <i>{select_sector}<i> <br> &nbsp;Sub-Sector: <i>{select_sub}</i>",
                        labels= {"Date": "", "Return" : "Cumulative Return"}, template = "seaborn"
                        )
        geo_fig.update_xaxes(rangeslider_visible=True)
        geo_fig.update_layout(
            xaxis = dict(
                rangeselector = dict(
                    buttons = [
                        dict(count = 7, label = "1w", step = "day", stepmode = "backward"),
                        dict(count = 1, label = "1m", step = "month", stepmode = "backward"),
                        dict(count = 3, label = "3m", step = "month", stepmode = "backward"),
                        # dict(count = 6, label = "6m", step = "month", stepmode = "backward"),
                        # dict(count = 1, label = "1y", step = "year", stepmode = "backward"),
                        # dict(count = 3, label = "3y", step = "year", stepmode = "backward"),
                        # dict(label = "YTD", step = "year", stepmode = "todate")
                    ], xanchor = "left", yanchor = "top"
                ),
            rangeslider = dict(visible = False),
            type = "date"
            ),
            yaxis=dict(
                autorange=True,         # ให้แกน Y ปรับช่วงอัตโนมัติ
                fixedrange=False,       # ปลดล็อกการเลื่อน/ขยายแกน Y
                showspikes=True,        # เพิ่มเส้น spike ชี้จุดข้อมูล
                spikemode='across'      # แสดง spike ทั้งแกน X และ Y
            ),
            dragmode="zoom"
        )
        # geo_fig.update_yaxes(dtick=1)

        return geo_fig
    
    #=================== 52Week High Low =========================
    def _52WHL(data):
        df = data.tail(265)
        df_close = df.iloc[-1].rename("Close")
        df_high = df.max().rename("High")
        df_low = df.min().rename("Low")
        df_5WHL = (df - df_low) / (df_high - df_low)
        df_SET = df_5WHL[["SET"]]
        df_5WHL = df_5WHL.iloc[-1].rename("52WHL")
        df_ROC = df.pct_change(10)*100
        df_ROC = df_ROC.iloc[-1].rename("ROC_10")

        df_close.index.rename("Name", inplace = True)
        df_high.index.rename("Name", inplace = True)
        df_low.index.rename("Name", inplace = True)
        df_5WHL.index.rename("Name", inplace = True)
        df_ROC.index.rename("Name", inplace = True)

        df_close.reset_index()
        df_high = df_high.reset_index()
        df_low = df_low.reset_index()
        df_5WHL = df_5WHL.reset_index()
        df_ROC = df_ROC.reset_index()

        mkt_cap_tab2 = mc.copy()
        mkt_cap_tab2["MarketCap"] = (mkt_cap_tab2["MarketCap"]/1000000)
        mkt_cap_tab2.rename(columns = {"MarketCap": "MarketCap (million THB)"}, inplace = True)
        sector_sub = raw_std[["symbol","market" ,"sector", "sub-sector"]]

        df_plot = pd.merge(left = df_high, right = df_low,
                left_on= "Name", right_on = "Name",
                how = "left").merge(right = df_close, left_on= "Name", right_on= "Name",
                how = "left").merge(right = df_5WHL, left_on= "Name", right_on = "Name",
                how = "left").merge(right = df_ROC, left_on= "Name", right_on = "Name",
                how = "left").merge(right = mkt_cap_tab2, left_on= "Name", right_on = "Symbols",
                how = "left").merge(right = sector_sub, left_on= "Name", right_on = "symbol",
                how = "left")
        df_plot["MarketCap (million THB)"] = df_plot["MarketCap (million THB)"]

        df_SET = df_plot[df_plot["market"] == "SET"]
        df_mai = df_plot[df_plot["market"] == "mai"]

        
        return df_SET, df_mai
    

    _52SET, _52mai = _52WHL(dp)
    source_52SET = _52SET.drop(["Symbols", "MarketCap (million THB)", "symbol", "market", "sector", "sub-sector"], axis = 1)
    source_52SET.attrs['Description'] = "Technical Analysis with 52 Weeks High Low and Rate of Change in 10 Days also included the current High Low Close Price"
    source_52mai = _52mai.drop(["Symbols", "MarketCap (million THB)", "symbol", "market", "sector", "sub-sector"], axis = 1)
    source_52mai.attrs['Description'] = "Technical Analysis with 52 Weeks High Low and Rate of Change in 10 Days also included the current High Low Close Price"

    # st.write("source_52SET") ################################################ data source ################################################
    # st.write("source_52mai") ################################################ data source ################################################

    def plot_52WHL(data, select_sector, select_sub):
        data = data[data["sector"] == select_sector]
        if select_sub != None:
            data = data[data["sub-sector"] == select_sub]
        fig_52WHL = px.scatter(data, x = "ROC_10", y = "52WHL",
                            color = "Name", size = "MarketCap (million THB)",
                            title = f"52 Weeks High Low vs Rate of Change 10:<br> &nbsp;Sector: <i>{select_sector}<i> <br> &nbsp;Sub-Sector: <i>{select_sub}</i>",
                            text = "Name",
                            custom_data= ["Name", "ROC_10", "52WHL","sector" ,"sub-sector","MarketCap (million THB)", 'Close'],
                            template = "seaborn")
        
        fig_52WHL.add_vline(x=0, line_color='red', line_width=2, opacity=0.6)
        fig_52WHL.add_hline(y=0, line_color='red', line_width=2, opacity=0.6)
        fig_52WHL.add_hline(y=1, line_color='red', line_width=2, opacity=0.6)

        # update details in the hover
        fig_52WHL.update_traces(
        hovertemplate="<b>Name:</b> %{customdata[0]}<br>" +
                    "<b>Close:</b> %{customdata[6]:,.2f} <br>" + 
                    "<b>ROC_10:</b> %{customdata[1]:,.2f}% <br>"
                    "<b>52WHL:</b> %{customdata[2]:,.2f} <br>" + 
                    "<b>sector:</b> %{customdata[3]} <br>"
                    "<b>sub-sector:</b> %{customdata[4]} <br>" + 
                    "<b>MarketCap:</b> %{customdata[5]:,.0f} million THB <br>",
        textposition = "bottom center",)

        fig_52WHL.update_layout(
            hovermode= "closest"
            )
        
        # fig_52WHL.update_xaxes(dtick=5)
        # fig_52WHL.update_yaxes(dtick=5)

        return fig_52WHL

    #=================== Slider =========================
    # filtered_data = dp.reset_index().tail(1200)
    # start, end = st.slider("Select Datetime", 
    #             min_value=  filtered_data.reset_index()['Date'].iloc[0].to_pydatetime(),
    #             max_value= filtered_data.reset_index()['Date'].iloc[-1].to_pydatetime(),
    #             value = (filtered_data.reset_index()['Date'].iloc[0].to_pydatetime(), filtered_data.reset_index()['Date'].iloc[-1].to_pydatetime()),
    #             format= "YYYY-MM")

    SET_t2,mai_t2 = geo_calculation(start)
    perf_source_SET = pd.pivot(SET_t2, index = "Name", columns= "Date", values= "Return").reset_index()
    perf_source_mai = pd.pivot(mai_t2, index = "Name", columns= "Date", values= "Return").reset_index()
    perf_source_SET.attrs["description"] = 'This dataset contains performance data within 100 days.'
    perf_source_mai.attrs["description"] = 'This dataset contains performance data within 100 days.'
    # st.write("perf_source_SET") ################################################ data source ################################################
    # st.write("perf_source_mai") ################################################ data source ################################################

    tcol1, tcol2 = st.columns(2)
    st.divider()
    tcol3, tcol4 = st.columns(2)
    with tcol1:
        st.subheader("SET Performance 100 Days")

        stcol1,stcol2 = st.columns(2)
        with stcol1:
            SetSectorSeclect_1_tab2 = st.radio("Select Sector", sorted(raw_std[raw_std["market"] == "SET"]['sector'].unique()), horizontal= True, key = "tab2 SET radio1")
        with stcol2:
            SetSectorSeclect_2_tab2 = st.radio("Select Sub-Sector",
                                    sorted(raw_std[raw_std["sector"] == SetSectorSeclect_1_tab2]["sub-sector"].dropna().unique()),
                                    horizontal= True, label_visibility= "collapsed", key = "tab2 SET radio2") if st.checkbox("include sub-sector", key = "tab2 SET checkbox1") else None\
                                    # st.radio("Select Sub-Sector",
                                    # sorted(raw_std[raw_std["sector"] == SetSectorSeclect_1]["sub-sector"].dropna().unique()),
                                    # horizontal= True, label_visibility= "collapsed", disabled= True, key = "tab2 SET radio2")
        
        st.plotly_chart(plot_geo(SET_t2, SetSectorSeclect_1_tab2, SetSectorSeclect_2_tab2))
    with tcol2:
        st.subheader("SET 52 Weeks High-Low vs Rate of Change 10 Days")
        st.plotly_chart(plot_52WHL(_52SET, SetSectorSeclect_1_tab2, SetSectorSeclect_2_tab2))
        
    with tcol3:
        st.subheader("mai Performance 100 Days")
        stcol3,stcol4 = st.columns(2)
        with stcol3:
            maiSectorSeclect_1_tab2 = st.radio("Select Sector", sorted(raw_std[raw_std["market"] == "mai"]['sector'].unique()), horizontal= True, key = "tab2 mai radio1")
        
        st.plotly_chart(plot_geo(mai_t2, maiSectorSeclect_1_tab2, None))
    with tcol4:
        st.subheader("mai 52 Weeks High-Low vs Rate of Change 10 Days")
        st.plotly_chart(plot_52WHL(_52mai, maiSectorSeclect_1_tab2, None))
    
    st.divider()

with tab3:
    tab31, tab32 = st.tabs(["        SET        ", "        mai        "])

    from plotly.subplots import make_subplots

    def Volume_Analysis_iteration_by_Sector(market = "SET", data_volume_in_wide_format = None, period = 30,fig_width = 600, fig_height = 1200):
        #select market
        temp_market = raw_std[raw_std["market"] == market]
        #what sectors in the market
        sectors_for_subplot = sorted(temp_market["sector"].unique())
        #init subplots
        fig_VA = make_subplots(rows = len(sectors_for_subplot), cols = 1, subplot_titles= sectors_for_subplot)
        
        for i,j in enumerate(sectors_for_subplot):
            # select sector
            temp_sector = temp_market[temp_market["sector"]== j]

            # filter tickers
            temp_tickers = sorted(temp_sector["symbol"].unique())

            # call MarketCap using tickers for preparation of weighted volume
            temp_mc = mc[mc["Symbols"].isin(temp_tickers)] # filtered symbols of mc are whether in temp_tickers?
            temp_mc["weight"] = temp_mc["MarketCap"] / temp_mc["MarketCap"].sum() # weight has already done
            # import data
            VA = data_volume_in_wide_format.tail(period + 70).copy().fillna(0)
            # filter with temp_tickers then reset index to get "Date" columns for melting
            VA = VA[temp_tickers].reset_index()
            # melting process to become long format
            VA = pd.melt(VA, id_vars = ["Date"], var_name= "Name", value_name= "Volume")
            # merge with temp_mc to get weighted volume in long format
            VA = VA.merge(right = temp_mc, left_on= "Name", right_on = "Symbols").drop("Symbols", axis =1)
            # calculate weighted volume
            VA["Weighted_Volume"] = VA["Volume"] * VA["weight"]
            # make the dataframe becomes wide format (becase we want to use only one values in a column)
            VA = pd.pivot(VA, index = "Date", columns = "Name", values = "Weighted_Volume")
            # make a summation of weigthed volume and threshold
            VA["Sum"] = VA.sum(1)
            VA["Threshold"] = VA["Sum"].rolling(window = 22).mean() + 2 * VA["Sum"].rolling(window = 22).std()
            VA["Anomaly"] = VA["Sum"] > VA["Threshold"]
            VA.reset_index(inplace = True)
            VA = VA.tail(period)

            fig_VA.add_trace( go.Bar(x = VA["Date"], y = VA["Sum"],
                            name = j,showlegend= False,
                            marker = dict(color = VA["Anomaly"].map({True: "orange", False:"gray"}))),
                            row= i+1,col=1)
            
        fig_VA.update_layout(width = fig_width, height = fig_height, title = f"{market} Sector Volume Analysis Period: {period} Days")
        fig_VA.update_layout(template="seaborn")
        return fig_VA
    
    def Volume_Analysis_iteration_by_Stock(market = "SET",sector = "TECH", data_volume_in_wide_format = None, period = 30,fig_width = 600, fig_height = 1200):
        #select market
        temp_market = raw_std[raw_std["market"] == market]
        #what sectors in the market
        temp_sector = temp_market[temp_market["sector"] == sector]
        page_number = (len(temp_sector["symbol"].unique())//10)+1
        c1, c2 = st.columns(2)
        with c1:
            period = st.radio("Choose Period",[30,60,90], key = f"tab3 Choose period VA Stock {market}", horizontal= True)

        button_labels = [x+1 for x in range(page_number)]
        page = 1
        with c2:
            page = st.radio("Choose Page",button_labels, key = f"tab3 Choose Page VA Stock {market}", horizontal= True)

        #what tickers in the market
        symbols_for_subplot = sorted(temp_sector["symbol"].unique())[10*(page - 1) :page * 10]
        #init subplots
        fig_symbols = make_subplots(rows = len(symbols_for_subplot), cols = 1, subplot_titles= symbols_for_subplot)
        
        for i,j in enumerate(symbols_for_subplot):
        # import data
            Vol_df = data_volume_in_wide_format[symbols_for_subplot].tail( period + period ).copy().fillna(0) #***
            Vol_threshold = Vol_df.rolling(window = 22).mean() + 2 * Vol_df.rolling(window = 22).std()
            Vol_anomaly = Vol_df > Vol_threshold
            
            melted_Vol_df = Vol_df.reset_index().melt(id_vars = "Date", var_name= "Name", value_name= "Volume").set_index("Date")
            melted_Vol_threshold = Vol_threshold.reset_index().melt(id_vars = "Date", var_name= "Name", value_name= "Threshold").set_index("Date")
            melted_Vol_anomaly = Vol_anomaly.reset_index().melt(id_vars = "Date", var_name= "Name", value_name= "Anomaly").set_index("Date")
            
            merged_df = pd.merge(melted_Vol_df,melted_Vol_threshold,"left", left_on= ["Date","Name"], right_on= ["Date","Name"])
            merged_df = pd.merge(merged_df,melted_Vol_anomaly,"left", left_on= ["Date","Name"], right_on= ["Date","Name"])

            cutoff_for_plot = merged_df[merged_df["Name"] == j].reset_index().dropna() #select symbol here

            fig_symbols.add_trace( go.Bar(x = cutoff_for_plot["Date"], y = cutoff_for_plot["Volume"],
                                name = j , #named
                                showlegend= False,
                                marker = dict(color = cutoff_for_plot["Anomaly"].map({True: "orange", False:"gray"}))),
                                row= i+1, col=1)
            
        fig_symbols.update_layout(width = fig_width, height = fig_height, title = f"{market} Sector: {sector} Volume Analysis Period: {period} Days ")
        fig_symbols.update_layout(template="seaborn")

        return fig_symbols
    
    with tab31:
        tab31c1, tab31c2,tab31c3 = st.columns([1,2,1]) 

        with tab31c1:
            st.subheader("SET Sector Volume Analysis")
            ChoosePeriodSET = st.radio("Choose Period",[30,60,90], key = "tab3 Choose period VA SET", horizontal= True)
            st.plotly_chart(Volume_Analysis_iteration_by_Sector(market = "SET", 
                                                            data_volume_in_wide_format= dv,
                                                            period = ChoosePeriodSET,
                                                            fig_width = 600,
                                                            fig_height= 900))
                
        with tab31c3:
            SetSectorSeclect_1_tab3_stock_SET = st.radio("Select Sector", sorted(raw_std[raw_std["market"] == "SET"]['sector'].unique()), horizontal= True, key = "tab3 Stock SET radio2")
            st.plotly_chart(Volume_Analysis_iteration_by_Stock(market = "SET",
                                                            data_volume_in_wide_format = dv,
                                                            sector= SetSectorSeclect_1_tab3_stock_SET, fig_height= 900
                                                            ))
            
    with tab32:
        tab32c1, tab32c2,tab32c3 = st.columns([1,2,1]) 
        with tab32c1:
            st.subheader("mai Sector Volume Analysis")
            ChoosePeriodmai = st.radio("Choose Period",[30,60,90], key = "tab3 Choose period VA mai", horizontal= True)
            st.plotly_chart(Volume_Analysis_iteration_by_Sector(market = "mai", 
                                                            data_volume_in_wide_format= dv,
                                                            period = ChoosePeriodmai,
                                                            fig_width = 600,
                                                            fig_height= 900))
            
        with tab32c3:
            SetSectorSeclect_1_tab3_stock_mai = st.radio("Select Sector", sorted(raw_std[raw_std["market"] == "mai"]['sector'].unique()), horizontal= True, key = "tab3 Stock mai radio2")
            st.plotly_chart(Volume_Analysis_iteration_by_Stock(market = "mai",
                                                    data_volume_in_wide_format = dv,
                                                    sector= SetSectorSeclect_1_tab3_stock_mai, fig_height= 900
                                                    ))
            
    
    def VWAP(market = "SET", sector = "TECH", options:str = None, period_options = 90):
        if options is None:
            period = st.radio("Choose Period",[30,60,90], key = f"tab3 Choose Period VWAP {market} {options}", horizontal= True)
        else:
            period = period_options
        #select market
        temp_market = raw_std[raw_std["market"] == market]
        #what sectors in the market
        if sector is not None:
            temp_sector = temp_market[temp_market["sector"] == sector]
        else:
            temp_sector = temp_market

        symbols_for_subplot = sorted(temp_sector["symbol"].unique())

        price = dp.tail(period*2).copy().ffill()
        vol = dv.tail(period*2).copy().ffill()
        
        #VWAP Calculation
        df_price = price * vol
        df_cum = df_price.cumsum()
        df_vol = vol.cumsum()
        df_VWAP = df_cum / df_vol
        df_VWAP = df_VWAP[symbols_for_subplot]#.reset_index()
        df_VWAP_data = df_VWAP.T.reset_index().rename(columns = {"index": "Name"})
        df_VWAP_data.attrs["description"] = "Volume Weighted Average Price in daily"
        VWAP_cumprod = (df_VWAP.pct_change()+1).cumprod().reset_index()
        VWAP_cumprod_data = VWAP_cumprod.set_index("Date")
        VWAP_cumprod_data = VWAP_cumprod_data.T.reset_index().rename(columns = {"index": "Name"})
        VWAP_cumprod_data.attrs["description"] = "Cumulative Product the Volume Weighted Average Price in daily"

        VWAP_cumprod = VWAP_cumprod.tail(period)

        #Stack bar Calculation
        df_stack = dv.tail(period*2)[symbols_for_subplot].copy().ffill().bfill()#.reset_index()
        df_VWAP_stack = df_VWAP.copy() #period*2 already
        df_stacked_bar = df_stack * df_VWAP_stack
        # df_stacked_bar.reset_index(inplace= True)
        df_stacked_bar["sum"] = df_stacked_bar.sum(1)
        df_stacked_bar_ratio = df_stacked_bar.iloc[:, :-1].div(df_stacked_bar["sum"], axis = 0).reset_index()

        stacked_bar_ratio_datasource = df_stacked_bar_ratio.set_index("Date").T
        # st.write(df_stacked_bar_ratio)
        # mkt_cap  = mc.copy()
        # mkt_cap  = mkt_cap[mkt_cap["Symbols"].isin(symbols_for_subplot)]
        # st.write(df_stacked_bar)
        # mkt_cap["Weight"] = mkt_cap["MarketCap"] / mkt_cap["MarketCap"].sum()
        # df_stack = pd.melt(df_stack, id_vars= "Date", var_name = "Name", value_name= "Volume")

        # merged_df = pd.merge(df_stack, mkt_cap, left_on = "Name", right_on = "Symbols").drop(["MarketCap", "Symbols"], axis = 1)
        # merged_df["Weighted Volume"] = merged_df["Volume"] * merged_df["Weight"]

        # pivoted_df = pd.pivot(merged_df, index = "Date", columns = "Name", values= "Weighted Volume") #for Stack bar
        # pivoted_df["sum"] = pivoted_df.sum(1)
        # pivoted_df = pivoted_df.iloc[:, :-1].div(pivoted_df["sum"], axis = 0).reset_index()
        # pivoted_df = pivoted_df.tail(period)

        fig_VWAP_Stackbar = make_subplots(rows = 3, cols = 1, subplot_titles= ["VWAP Cumulative Product","Stacked Volume"])

        for column in VWAP_cumprod.columns[1:]:
            fig_VWAP_Stackbar.add_trace(go.Scatter(x = VWAP_cumprod["Date"], y = VWAP_cumprod[column],mode = "lines", name = column,),row = 1, col =1)
            # fig_VWAP_Stackbar.add_trace(go.Scatter(x = df_VWAP_for_plot["Date"], y = df_VWAP_for_plot[column],mode = "lines", name = column,),row = 2, col =1)
            fig_VWAP_Stackbar.add_trace(go.Bar(x = df_stacked_bar_ratio["Date"], y = df_stacked_bar_ratio[column], name = column, showlegend= False), row = 2 , col = 1)
        
        # for column in VWAP_cumprod.columns[1:]:
            
        fig_VWAP_Stackbar.update_layout(
            title="VWAP Analysis",
            xaxis_title="Date",
            yaxis_title="VWAP",
            template="seaborn",
            width=1200, 
            height=1200,
            barmode = "stack",
            legend=dict(
                traceorder="normal" 
            ))

        return fig_VWAP_Stackbar, stacked_bar_ratio_datasource, df_VWAP_data, VWAP_cumprod_data
    
    with tab31c2:
        SectorSeclect_tab3_VWAP_SET = st.radio("Select Sector", sorted(raw_std[raw_std["market"] == "SET"]['sector'].unique()), horizontal= True, key = "tab3_VWP_SET radio")
        SET_fig, _, _, _= VWAP(market = "SET", sector = SectorSeclect_tab3_VWAP_SET)
        # st.write("SET_Stacked_bar, SET_VWAP, SET_VWAP_cumprod (descripted)") ################################################ data source ################################################

        st.plotly_chart(SET_fig)

    with tab32c2:
        SectorSeclect_tab3_VWAP_mai = st.radio("Select Sector", sorted(raw_std[raw_std["market"] == "mai"]['sector'].unique()), horizontal= True, key = "tab3_VWP_mai radio")
        mai_fig, _, _, _= VWAP(market = "mai", sector = SectorSeclect_tab3_VWAP_mai)
        # st.write("mai_Stacked_bar, mai_VWAP, mai_VWAP_cumprod (descripted)") ################################################ data source ################################################

        st.plotly_chart(mai_fig)

    #for AI
    _, SET_Stacked_bar, SET_VWAP, SET_VWAP_cumprod= VWAP(market = "SET", sector = None, options= "datasource")
    _, mai_Stacked_bar, mai_VWAP, mai_VWAP_cumprod= VWAP(market = "mai", sector = None, options= "datasource")


with tab4:
    tab4c1, tab4c2 = st.columns([3,1])
    with tab4c2:
        hm_name = str.upper(st.text_input("Stock Name", "ADVANC"))
        st.success(f"กำลังวิเคราะห์หุ้น: {hm_name}")

    with tab4c1:
        if hm_name in dp.columns:
            hm_df = dp.copy()
            #fetch a stock
            hm_df = hm_df[[hm_name]].resample("M").last()
            hm_df["Return"] = hm_df.pct_change()
            hm_df = hm_df.dropna()
            hm_df = hm_df.reset_index()
            hm_df["Y"] = hm_df.Date.dt.strftime("%Y")
            hm_df["M"] = hm_df.Date.dt.strftime("%m")
            pivoted_hm_df = pd.pivot(hm_df, index = "Y", columns = "M", values = "Return")
            pivoted_hm_df.columns = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug","Sep", "Oct", "Nov", "Dec"]
            pivoted_hm_df["Avg Y"] = pivoted_hm_df.mean(1)
            pivoted_hm_df.loc["Avg M"] = pivoted_hm_df.mean(0)

            plt.style.use("ggplot")
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.set_facecolor('none')
            heatmap = sns.heatmap(pivoted_hm_df.round(4), cmap="RdYlGn",annot=True, fmt=".2%", ax=ax, square= True, annot_kws= {"size":4}, center= 0,cbar = False) #cbar_kws={"shrink": 0.5,})
            
            plt.xticks(fontsize=6)
            plt.yticks(fontsize=6)
            ax.set_xlabel("Months", fontsize=8)
            ax.set_ylabel("Years", fontsize=8)
            plt.tight_layout()
            plt.title(f"Historical Return Heatmap of {hm_name}", fontdict= {"size":10,"weight": "bold", "color": "#1A1A1A"})
            st.pyplot(fig)
        else:
            if hm_name != "":
                st.error(f"Stock '{hm_name}' not found in the database. Please try again.")
            else:
                pass

    st.divider()

# ========================= DATA FOR AI =========================
VP_change_D_data = VP_change_D_data.rename(columns = {"Symbols": "Name"})
VP_change_W_data = VP_change_W_data.rename(columns = {"Symbols": "Name"}).drop("MarketCap", axis = 1)
VP_change_M_data = VP_change_M_data.rename(columns = {"Symbols": "Name"}).drop("MarketCap", axis = 1)
VP_change_3M_data = VP_change_3M_data.rename(columns = {"Symbols": "Name"}).drop("MarketCap", axis = 1)
SET_Stacked_bar = SET_Stacked_bar.reset_index(names= "Name")
mai_Stacked_bar = mai_Stacked_bar.reset_index(names= "Name")

lst_df = [rs_score_data, VP_change_D_data, VP_change_W_data, VP_change_M_data, VP_change_3M_data, source_52SET, source_52mai,
perf_source_SET, perf_source_mai, SET_Stacked_bar, SET_VWAP, SET_VWAP_cumprod, mai_Stacked_bar, mai_VWAP, mai_VWAP_cumprod]

lst_df_suffix = ["rs_score", "VolumePrice%Change_D", "VolumePrice%Change_W", "VolumePrice%Change_M", "VolumePrice%Change_3M", "52W_SET", "52W_mai",
"Performance_SET", "Performance_mai", "SET_stacked_bar", "SET_VWAP", "SET_VWAP_cumprod", "mai_stacked_bar", "mai_VWAP", "mai_VWAP_cumprod"]

AIdata_52WHL = pd.concat([source_52SET,source_52mai])
AIdata_Performance = pd.concat([perf_source_SET.iloc[:,[0,-1]],perf_source_mai.iloc[:,[0,-1]]])
AIdata_Performance.columns = ["Name", "Performance 100 Days"]
AIdata_Stacked_Volume = pd.concat([SET_Stacked_bar.iloc[:,[0,-1]],mai_Stacked_bar.iloc[:,[0,-1]]])
AIdata_Stacked_Volume.columns = ["Name", "Volume Trade Ratio in Its Sector"]
AIdata_VWAP = pd.concat([SET_VWAP.iloc[:,[0,-1]],mai_VWAP.iloc[:,[0,-1]]])
AIdata_VWAP.columns = ["Name", "Volume Weighted Average Price"]
AIdata_Cumulative_VWAP = pd.concat([SET_VWAP_cumprod.iloc[:,[0,-1]],mai_VWAP_cumprod.iloc[:,[0,-1]]])
AIdata_Cumulative_VWAP.columns = ["Name", "Cumulative_VWAP"]

#Merge Data
AIdata_ALL = rs_score_data.merge(AIdata_52WHL,how = "outer", on = "Name")
AIdata_ALL = AIdata_ALL.merge(VP_change_D_data,how = "outer", on = "Name")
AIdata_ALL = AIdata_ALL.merge(VP_change_W_data,how = "outer", on = "Name")
AIdata_ALL = AIdata_ALL.merge(VP_change_M_data,how = "outer", on = "Name")
AIdata_ALL = AIdata_ALL.merge(VP_change_3M_data,how = "outer", on = "Name")
AIdata_ALL = AIdata_ALL.merge(AIdata_Performance,how = "outer", on = "Name")
AIdata_ALL = AIdata_ALL.merge(AIdata_Stacked_Volume,how = "outer", on = "Name")
AIdata_ALL = AIdata_ALL.merge(AIdata_VWAP,how = "outer", on = "Name")
AIdata_ALL = AIdata_ALL.merge(AIdata_Cumulative_VWAP,how = "outer", on = "Name")

# st.write(AIdata_ALL)

datasource_for_AI = AIdata_ALL.to_csv("datasource_for_AI.csv")

from AI_sidebar import AI_Overviews


with st.sidebar:
    premium = st.selectbox("คุณเป็นสมาชิก Premium?", ["No", "Yes"])
    if premium == "Yes":
        stock_name = str.upper(st.text_input("ระบุชื่อหุ้นที่ต้องหารวิเคราะห์", ""))
        prompt = f"""
                    ข้อมูลประกอบด้วย:
                        Name: ชื่อหุ้น เช่น 24CS, 2S, 3K-BAT
                        RS_Score: ใช้สูตร (0.4 * ราคาปิดเมื่อ 3 เดือนก่อน + 0.2 * ราคาปิดเมื่อ 6 เดือนก่อน + 0.2 * ราคาปิดเมื่อ 9 เดือนก่อน + 0.2 * ราคาปิดเมื่อ 12 เดือนก่อน) และนำมาใช้ Sigmoid Function ซึ่งถ้านำไปเปรียบเทียบกับหุ้นทั้งตลาดจะบ่งบอกถึงคะแนนที่ดีกว่าหรือแย่กว่า
                        RS_Rank: เป็นการนำ RS_Score มาให้ลำดับ ซึ่งสามารถใช้แทน RS_Score ได้เลย และบอกถึงลำดับของผลตอบแทนของหุ้นนั้นในตลาด
                        market: ตลาดที่หุ้นจดทะเบียน เช่น mai (Market for Alternative Investment), SET (Stock Exchange of Thailand)
                        sector: หมวดธุรกิจ เช่น PROPCON (อสังหาริมทรัพย์และก่อสร้าง), INDUS (อุตสาหกรรม)
                        sub-sector: กลุ่มย่อยของหมวดธุรกิจ เช่น STEEL (เหล็ก), AUTO (ยานยนต์)
                        Return: ผลตอบแทนของหุ้นซึ่งเป็นสูตรเดียวกันกับ RS_Score แต่ไม่ได้ใช้ Sigmoid ใช้เป็นผลตอบแทนเฉลี่ยถ่วงน้ำหนักได้
                        Price %Change D: การเปลี่ยนแปลงราคาต่อวัน
                        Volume %Change D: การเปลี่ยนแปลงปริมาณการซื้อขายต่อวัน
                        Price %Change W: การเปลี่ยนแปลงราคาต่อสัปดาห์
                        Volume %Change W: การเปลี่ยนแปลงปริมาณการซื้อขายต่อสัปดาห์
                        Price %Change M: การเปลี่ยนแปลงราคาต่อเดือน
                        Volume %Change M: การเปลี่ยนแปลงปริมาณการซื้อขายต่อเดือน
                        Price %Change 3M: การเปลี่ยนแปลงราคาต่อไตรมาส
                        Volume %Change 3M: การเปลี่ยนแปลงปริมาณการซื้อขายต่อไตรมาส
                        Volume and Price %Change ทั้งใน D, W, M, 3M ตลาดสามารถบอกแนวโน้มในรายไตรมาสได้
                        High: ราคาสูงสุดใน 52 สัปดาห์
                        Low: ราคาต่ำสุดใน 52 สัปดาห์
                        Close: ราคาปัจจุบัน
                        52WHL: เป็นการทำ Normalization ด้วยการใช้ (Close - Low) / (High- Low) ยิ่งค่าใกล้ 1 ยิ่งสะท้อนถึงราคาที่ใกล้เคียงกับราคาสูงสุด โดยจะพิจารณาร่วมกับ ROC_10 เพื่อจะบอกถึงความน่าสนใจในมิติของราคาที่อาจจะต่ำแต่เปลี่ยนแปลงแรงหรือราคาที่สูงอาจจะเปลี่ยนแปลงต่ำในระยะสั้น เป็นต้น
                        ROC_10: Rate of Change 10 ใช้ร่วมกันกับ 52WHL (สามารถอธิบายเกี่ยวกับ 52WHL เพิ่มเติมและนำมาอธิบายให้สอดคล้องกับ ROC_10 ได้)
                        Performance 100 Days: เป็นค่า Cumulative Return ของหุ้นตัวนั้นที่สะสมมาตลอด 100 วัน
                        Volume Trade Ratio in Its Sector: บ่งบอกถึงสัดส่วนของ Volume ของใน market และ sector นั้น ในวันล่าสุด โดย Weight ด้วยราคาของหุ้นใน market และ Sector นั้น แนะนำว่าให้ดูว่ามีสัดส่วนเท่าไรใน market อะไรและ sector ใด
                        Volume Weighted Average Price: เป็นค่า VWAP 
                        Cumulative_VWAP: เป็นค่าสะสมของ VWAP ล่าสุด 
                        
                    อธิบายความหมายของ market และ sector:
                        market (ตลาด):
                            SET: ตลาดหลักทรัพย์แห่งประเทศไทย (ตลาดหลัก) สำหรับบริษัทขนาดใหญ่
                            mai: ตลาดหลักทรัพย์เอ็มเอไอ สำหรับบริษัทขนาดกลางและขนาดเล็ก
                        sector (หมวดธุรกิจ):
                            AGRO: เกษตรและอุตสาหกรรมอาหาร
                            CONSUMP: สินค้าอุปโภคบริโภค
                            FINCIAL (Financials): กลุ่มการเงินและธนาคาร
                            INDUS (Industrials): อุตสาหกรรม
                            PROPCON (Property & Construction): อสังหาริมทรัพย์และก่อสร้าง
                            RESOURC: ทรัพยากร
                            TECH (Technology): เทคโนโลยี
                            SERVICE: บริการ เช่น ค้าปลีก โรงพยาบาล

                        Analyze the stock data provided for the stock "{stock_name}" based on the following metrics:
                        - Market and Sector Classification
                        - RS_Rank and Return
                        - Volume and Price %Change in [D, W, M and 3M] as Trend เช่น ถ้า Volume %Change 3M เปลี่ยนแปลงต่ำ Volume %Change M เปลี่ยนแปลงสูงขึ้น Volume %Change W เปลี่ยนแปลงสูงขึ้น Volume %Change D อาจจะคงที่ นี่ยังสะท้อน Trend ที่ดีของราคาเป็นต้น
                        - 52WHL and ROC_10
                        - Performance 100 Days
                        - Volume Trade Ratio in Its Sector
                        - Volume Weighted Average Price
                        - Cumulative_VWAP

                        Perform the following technical analysis:
                        1. Trend Analysis: Identify if the stock is in an uptrend or downtrend based on metrics
                        2. Explain why the stock holds its current rank.
                        3. Comparison of the stock with its sector in the same market.
                        4. Try to predict whether that stock can become a leader within its sector. หากมีไม่เพียงพอให้พิจารณาหุ้นที่ปรากฏในตารางเท่านั้น ที่มี sector เหมือนกับหุ้นนั้น (พิจารณาใน sector ไม่ต้องลงลึกถึง sub-sector เช่น พิจารณา Delta แค่ใน TECH พอไม่ต้องลงลึกถึง ETRON)
                        5. Sector & Market Analysis: Describe the stock's market and sector, and how it fits within the overall market.

                        Provide a summarized insight including:
                        - Key technical strengths
                        - Potential risks
                        - Recommendations for investors considering this stock.
                        

                        Generate a natural language summary explaining the findings clearly suitable for both beginners and experienced investors, in 20 lines. ใช้ข้อมูลที่ให้มาทั้งหมดใน [] ต่อจากนี้ให้เป็นประโยชน์
                        [RS_Score, RS_Rank, market, sector,sub-sector ,Return ,Price %Change D ,Volume %Change D ,Price %Change W ,Volume %Change W ,Price %Change M ,Volume %Change M , Price %Change 3M ,
                          Volume %Change 3M, High,Low,Close , 52WHL,ROC_10 ,Performance 100 Days ,Volume Trade Ratio in Its Sector , Volume Weighted Average Price,Cumulative_VWAP ] (ตอบเป็นภาษาไทยนะ)
                      
            """
        csv_data = pd.read_csv("datasource_for_AI.csv")

        AI_Overviews(prompt, csv_data, stock_name)