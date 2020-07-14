#---------------------------------Student ID: 31131867---------------------------------------
#---------------------------------Name: Angel Das--------------------------------------------
#---------------------------------Create Date: 11-04-2020------------------------------------
#---------------------------------Last Modified: 1-05-2020-----------------------------------
#---------------------------------Note: Version Control is used to save files----------------

"""
Description: Creating an algorithm that reads start date, start stock, start revenue from a file stores
it in a dictionary and calculates the final stock and revenue for the number of years simulated based on business rules
outlined in the assignment document
"""

# ---------------------------------Importing required packages---------------------------------
import math as m
import sys as sy

#---------------------------------Declaring variables-----------------------------------------

days_month_data=[['Jan',1,31],['Feb',2,28],['Mar',3,31], ['Apr',4,30],['May',5,31],['Jun',6,30],['Jul',7,31], \
                 ['Aug',8,31],['Sep',9,30],['Oct',10,31],['Nov',11,30],['Dec',12,31]]

#----------------------------------Variables that can be simulated (Update on Need basis)-----------------------------
no_year_sim=3
per_def=5 #------------------------Input percentage as whole number; It is divided/100 later for calculation
cris_recur_frequency=9

#---------------------------------Initial inputs when the firm was established--------------------------------
firm_start_year=2000
firm_start_stock=1000
firm_start_RRP=705
firm_dist_day=36
revenue=0
count=0 #--------------------counter for tracking 9 year leap year cycle
defective_stock = 0
rrp_prev=0

dic_firm_start_data={"start_year":2005, "start_stock": 1000, "start_revenue": 1000}
dic_firm_cal_data={"start_year":0, "start_stock":0, "start_revenue":0}
calculated_data={"end_year":0, "end_stock":0, "end_revenue":0}



#---------------------------------Error Handling: Checking Start Year provided by user in the file----------------------

"""
FUNCTION DEFINITION:
Since the firm was established in January 1st, 2000, any input lesser than that year will be shown as an error.
Since the current input is YYYY-MM-DD it check for accuracy of month and date.
"""

def check_year_month_date_input(yr,mth,dt):

    #----------------------------Checking for year < firm established year----------------------------------------------
    if yr<2000:
        return -1
    # ----------------------------Checking for accuracy of month--------------------------------------------------------
    elif mth<1 or mth>12:
        return -1
    # ----------------------------Checking for accuracy of date---------------------------------------------------------
    elif dt<1 or dt>31:
        return -1
    # ----------------------------If above checks are cleared - the correct format is entered---------------------------
    #-----------------------------Need to check for dates based on leap year and month----------------------------------
    else:
        if (yr % 4 == 0) and (yr % 100 != 0) or (yr % 400 == 0):
            if mth==2:
                if dt>29:
                    return -1
                else:
                    return 1
            else:
                if dt>days_month_data[mth-1][2]:
                    return -1
                else:
                    return 1
        else:
            if dt>days_month_data[mth-1][2]:
                return -1
            else:
                return 1
    return 0



"""
FUNCTION DEFINITION:
Function cal_stock_revenue_yearly() calculates the yearly figures of revenue, RRP, stock, defective stock and
distribution/day. Used mainly for looping through days of a month and readjusting RRP & Dist/day
"""

def cal_stock_revenue_yearly(st_stock, st_RRP, st_dist_day, yr_data, end_mth, end_dt):

    global firm_start_stock, firm_start_RRP, firm_dist_day, revenue, defective_stock,rrp_prev

    st_stk = dic_firm_cal_data['start_stock']
    st_rev = dic_firm_cal_data['start_revenue']
    st_dt = int(dic_firm_cal_data['start_year'])

    #------------------------------Declaring local variables---------------------------------------
    stock_upd=st_stock #-------------------stock quantity
    rrp_upd=st_RRP #--------------------RRP
    dist_upd=st_dist_day #-------------------Distribution/Day

    # rrp_prev=0 #-----------------------Need to store previous month's RRP as defective \
                                            # stocks for the current month are sold using prev month's  value

   #-------------------------------Loop to traverse across month of a year----------------------------------------------
    for i in range(0,end_mth,1):


     #----------------------------Business Rule: Defective stocks are not carry forwarded to next year------------------
        # if i==0:
            # defective_stock=0

        distributed = 0
        revenue_normal = 0

        # -------------------------------Readjustment post peak selling season; 3 represents March----------------------
        if (i+1)==3:
            rrp_upd = (rrp_upd/1.20)
            dist_upd = (dist_upd/1.35)

        # -------------------------------Readjustment for start of financial year; 7 represents July--------------------
        elif (i+1)==7:
            rrp_upd=(1.05*rrp_upd)
            dist_upd=(1.10*dist_upd)

        # -------------------------------Readjustment for peak selling season; 11 represents November-------------------
        elif (i+1)==11:
            rrp_upd = (1.20 * rrp_upd)
            dist_upd =(1.35 * dist_upd)

        # print((days_month_data[i][1])+1)

        # print((days_month_data[i][2]))

     # ------------------------------------Fine tuning number of days to be used-------------------------------
        # ------------------------------------if one complete year needs to be calculated----------------------------
        if end_mth == 12:
            days_to_calculate = (days_month_data[i][2]) + 1
        # ------------------------------------if we are in the last month for which data needs to be calculated----------
        elif (i + 1) == end_mth:
            days_to_calculate = end_dt + 1
        else:
            days_to_calculate = (days_month_data[i][2]) + 1

    #-------------------------------------Loop: Calculating distribution and stock for days of the month----------------
        for y in range(1,days_to_calculate,1):
            cal_dt = yr_data * 10000 + (i+1)*100 + y  # --------------Calculating date
            #print(cal_dt, "==",st_dt)

            #--------------------Updating stock and revenue based on input file
            if cal_dt == st_dt:
                stock_upd = st_stk
                revenue = st_rev
                distributed=0
                defective_stock=0

                # print("Rev Start",revenue)

            if stock_upd <= 400:
                stock_upd += 600  # -------------------------updating stock in case of stock out; Business Rule
                # --------------------If distribution/day >stocks allocated, code should stop simulating
                if dist_upd > stock_upd:
                    sy.exit('Can\'t simulate as distribution/day exceeds allocated stock')

                stock_upd -= dist_upd
            else:
                stock_upd -= dist_upd  # --------------------removing distributed items from stock

            distributed += dist_upd  # ----------------------Calculating total distribution for the month (each day)

            # print(stock_upd)
            # print(y)


        #-----------------------------Adjusting revenue for defective stocks--------------------------------------------

        if defective_stock > 0:
            #----------------------------------Business Rule: Defective stocks are distributed first--------------------
            if defective_stock >= distributed:
                revenue_normal = distributed * (rrp_prev*0.80)

            elif defective_stock < distributed:
                # print("Check Mate", defective_stock)
                revenue_normal = ((distributed-defective_stock) * rrp_upd) + (defective_stock * (rrp_prev * 0.80))
        else:    #---------------------------------------This if condition takes care of the starting year's starting
                 #---------------------------- month when the firm was established; No defective items in first month
                 #----------Also start of every year since distributed items are not carried forward to next year

            revenue_normal = distributed * rrp_upd

        rrp_prev=rrp_upd #-------------------By end of a month storing current month's value is a variable

        #-----------------------------Defective stock is calculated on good stocks that were sold-----------------------
        defective_stock = (per_def/100) * (distributed-defective_stock)
        # print("Normal Revenue", revenue_normal)
        revenue+=revenue_normal

        # print("-----------------------------------------------------------------")
        # print("Revenue for ", days_month_data[i][0],revenue_normal)
        # print("Distributed/Day for ", days_month_data[i][0], dist_upd)
        # print("Distributed Items for ", days_month_data[i][0], distributed)
        # print("RRP ", days_month_data[i][0], rrp_upd)
        # print("Stock for ", days_month_data[i][0], stock_upd)
        # print("Defective Stock for ", days_month_data[i][0], defective_stock)
        # print("-----------------------------------------------------------------")


    # print('Total Revenue:', revenue)


    firm_start_stock=stock_upd #--------------End of the year, updating starting stock for next year
    firm_start_RRP=rrp_upd #------------------End of the year, updating starting RRP for next year
    firm_dist_day=dist_upd #------------------End of the year, updating Distribution/Day for next year

"""
FUNCTION DEFINITION:
Function cal_stock_revenue() takes in the dictionary variable, extracts date for which the start stock and revenue
needs to be calculated, and outputs a dictionary variable where these figures are stored. This function accounts
for financial crises and loops year over year calculation.
"""

def cal_stock_revenue(dt):

    global dic_firm_cal_data, calculated_data, no_year_sim

    end_yr = int(dt[0:4]) + no_year_sim
    end_mth = int(dt[4:6])
    end_dt = int(dt[6:8])

    cal_data = {"end_year": 0, "end_stock": 0, "end_revenue": 0}

    #---------------------------Storing data in a local variable; Used for loop iteration-------------------------------
    end_year=end_yr
    st_stk=dic_firm_cal_data['start_stock']
    st_rev=dic_firm_cal_data['start_revenue']

    # print(end_year)
    # print(end_year)

    global firm_start_stock, firm_dist_day, firm_start_RRP, revenue, count, days_month_data, \
        defective_stock

    for i in range(firm_start_year,end_year+1,1):

        # print(i,",",end_year)

        #--------------------------------Adjusting leap year days for February----------------------------------------
        if i%4==0:
            if i%100==0:
                if i%400==0:
                    days_month_data[1][2] = 29
                else:
                    days_month_data[1][2] = 28
            else:
                days_month_data[1][2] = 29
        else:
            days_month_data[1][2] = 28

        #-------------------------------Adjusting RRP and Distribution/Day for financial crises------------------------
        #-------------------------------cris_recur_frequency is used for the crisis cycle---------------
        if count== cris_recur_frequency:
            firm_dist_day=(firm_dist_day*0.80)
            firm_start_RRP=(firm_start_RRP*1.10)

        elif count== (cris_recur_frequency+1):
            firm_dist_day = (firm_dist_day * 0.90)
            firm_start_RRP = (firm_start_RRP * 1.05)

        # -------------------------------Using this extra elif to rest counter for next financial crises----------------
        elif count== (cris_recur_frequency+2):
            firm_dist_day = (firm_dist_day * 0.95)
            firm_start_RRP =(firm_start_RRP * 1.03)
            count=0 #--------------------Counter is set to 0 to account for next financial crisis cycle-----------------

        """
        Note: The code simulates all business variables like stock, RRP, distribution/day, defective stock and
        revenue using the values provided when the firm was established. Hence to account for task 1, where the starting
        stock and revenue should be used from the input file, few decision statements are used to account these changes.
        """
#-----------------------------Start Stock & Start Revenue needs to be considered for this analysis
        if i==(end_year-no_year_sim):
            defective_stock = 0
            # revenue=st_rev #---------Assigning revenue with user input--------------------------------------------------

            # print('Calculation for Year: ', i)
            # print('Starting Stock for the year:', firm_start_stock)
            # print('Starting RRP for the year:', firm_start_RRP)
            # print('Starting Dist/Day the next year:', firm_dist_day)
            # print('Revenue:', revenue)



            # firm_start_stock=st_stk
            # cal_stock_revenue_yearly(st_stk, firm_start_RRP, firm_dist_day)
        #
        # else:
        #
        #     # print('Calculation for Year: ', i)
        #     # print('Starting Stock for the year:', firm_start_stock)
        #     # print('Starting RRP for the year:', firm_start_RRP)
        #     # print('Starting Dist/Day the next year:', firm_dist_day)
        #     # print('Revenue:', revenue)

        """
        To simulate the last year, we need to carefully select the end dates and month figures.
        i.e. if start date is 20000201 then simulation should be done only till jan end of 2003
        """

        if i != (end_yr):
            cal_stock_revenue_yearly(firm_start_stock, firm_start_RRP, firm_dist_day, i, 12, 31)

        else:

            if end_dt != 1:
                cal_stock_revenue_yearly(firm_start_stock, firm_start_RRP, firm_dist_day, i, end_mth, end_dt - 1)

            else:
                cal_stock_revenue_yearly(firm_start_stock, firm_start_RRP, firm_dist_day, i, \
                                         end_mth - 1, days_month_data[end_mth - 2][2])

        count+=1

    # calculated_data['end_year']=dic_firm_cal_data['start_year']+1
    # calculated_data['end_stock'] = firm_start_stock
    # calculated_data['end_revenue'] = revenue

    calculated_data['end_year'] = dic_firm_cal_data['start_year'] + no_year_sim*10000
    calculated_data['end_stock'] = firm_start_stock
    calculated_data['end_revenue'] = revenue

    return calculated_data

"""
FUNCTION DEFINITION:
Creating function read_data() to read input file, cross validate the input and store them in a dictionary;
The function calls other functions necessary for calculating end year, end stock and end revenue.
"""
def read_data():

    #---------------------------Using global variable to store data from the file---------------------------------------
    global dic_firm_cal_data
    stk=0
    #----------------------------Reading data from a file-------------------------------------
    #----------------------------Please note that file is stored in the same location as that of the project-------
    file_data=open("AU_INV_START.txt","r")

    counter=1 #---------------------stores line number and uses it to assign appropriate value to dictionary ids
    for line in file_data:

        # ----------------------------Checking and storing year---------------------------------------------------
        if counter==1:
            dic_firm_cal_data['start_year'] = int(line)
            counter += 1
        #----------------------------Checking and storing stock---------------------------------------------------
        elif counter==2:
            #------------------------Since firm restocks 600 units when inventory stock drops to 400, cross
            #------------------------Validating input stock figures-----------------------------------------------
            if int(line)<=400:
                stk=int(line)+600
            else:
                stk=int(line)

            dic_firm_cal_data['start_stock'] = stk
            counter += 1

            #------------------------Checking revenue provided by the user----------------------------------------
        else:
            if int(line)<0:
                dic_firm_cal_data['start_revenue'] = 0
            else:
                dic_firm_cal_data['start_revenue'] = int(line)
            counter += 1

    file_data.close() #------------------------closing the file after data is read into a dictionary

    # print(dic_firm_cal_data)

    dt = str(dic_firm_cal_data['start_year'])

    length_input_date=len(dt)

    if length_input_date!=8: #--------------------Incorrect length of Date: Error Handling
        sy.exit('Incorrect Date input in file')

    st_year = int(dt[0:4])
    st_mth = int(dt[4:6])
    st_dt = int(dt[6:8])

    # -------------------------------------Checking if input date is correct------------------------------------
    ret = check_year_month_date_input(st_year, st_mth, st_dt)
    if ret == -1:
        sy.exit('Incorrect Date input in file')

    #------------------------------------Calling function for stock and revenue calculation-------------------

    # cal_data=cal_stock_revenue(st_year+no_year_sim,st_mth,st_dt)
    # write_data(cal_data)


"""
FUNCTION DEFINITION:
Function write_data is used to write data into an output file.
"""

def write_data(cal_data):
    # --------------------------calculated_data is a local variable here---------------------------------------

    file_write = open("AU_INV_END.txt", "w")

    #--------------------It is possible that start date is 2000-02-29 then 2003-03-01 (March should be displayed)

    dt = str(cal_data['end_year'])
    st_year = int(dt[0:4])
    st_mth = int(dt[4:6])
    st_dt = int(dt[6:8])

    if (st_year % 4 == 0) and (st_year % 100 != 0) or (st_year % 400 == 0):
        if no_year_sim!=4:
            if st_mth==2 and st_dt==29:
                dt=st_year*10000+301



    file_write.write(str(dt) + "\n")

    """
    It is possible that Stock on Dec 31st was slight above 400 and after distributing it fell below 400.
    Such adjustments are taken care of on the next day hence. When calculating data for Jan, we are checking
    if stock is less than 400 and add 600 more accordingly.
    """

    if calculated_data['end_stock'] < 400:
        calculated_data['end_stock'] += 600

    file_write.write(str(m.ceil(calculated_data['end_stock'])) + "\n")
    file_write.write(str(round(calculated_data['end_revenue'], 2)))

    file_write.close()


"""
Calling all functions required for the simulation
"""

if __name__=='__main__':
    read_data()

    dt = str(dic_firm_cal_data['start_year'])

    return_data=cal_stock_revenue(dt)
    write_data(return_data) #---------------sending dictionary variable returned post calculation

