def fit_linear(filename):
    my_file=open(filename,'r')#read the file
    list_lins_of_input=my_file.readlines()#make list of lines
    for i in range (len(list_lins_of_input)):#make the chars lower to find the organization eazyer.
        list_lins_of_input[i]=list_lins_of_input[i].lower()
    horizontal,vertical=0,0
    x_axis,y_axis=x_y_axis_name(filename)#save the name of the axis

    if "x" in list_lins_of_input[0] and "y" in list_lins_of_input[0]:#cheke if horizontal or vertical
        vertical=True

    else:
        horizontal=True

    negativety, hori_not_same_length, ver_not_same_length=0,0,0
    x,y,dx,dy,negativety,hori_not_same_length,ver_not_same_length=organize_data(vertical,horizontal,list_lins_of_input)#go to function that returns orgenized Data.
    if negativety!=True and hori_not_same_length!=True and ver_not_same_length!=True:#if there is no problem with negativety or length continue
        a, d_a, b, d_b, chi_squer, chi_2_mini = Fitting_function_and_definitions(x, y, dx, dy)
        output_format(a, d_a, b, d_b, chi_squer, chi_2_mini)  # print the solution
        plot_function(a, b, y, dy, x, dx, x_axis, y_axis)#plot the graph
    else:#if there is a problem in the text
        return
    return



def x_y_axis_name(filename1):#return the axis names
    my_file_aditional = open(filename1, 'r')#read again the file ,to have them in Capital letters.
    list_lins_of_input_2 = my_file_aditional .readlines()

    my_file_aditional.close()
    x_name=0
    y_name=0
    index=0
    while x_name == 0 or y_name == 0:#if it didnt find both title
        if "x axis" in list_lins_of_input_2[index]:
            x_name = list_lins_of_input_2[index][8:]#take just the name of the title
        elif "y axis" in list_lins_of_input_2[index]:
            y_name = list_lins_of_input_2[index][8:]#take just the name of the title
        index=1+index
    return x_name,y_name




def organize_data(ver,horo,list_lines_input):
    total_list=[[],[],[],[],[],[]]
    negative, horizontal_not_same_length, vertical_not_same_length=False,False,False

    x_data ,y_data,dx_data,dy_data=[],[],[],[]

    if ver==True:#if orginaized vertical
        if_its_not_in_the_same_length=0#variable that index if they in the same length
        for sub_data in list_lines_input:
            list1=[]
            list1=sub_data.split()#to make a list from the lines
           # print ("list1",list1,"sub",sub_data)
            #print (sub_data, "and",len(list1))
            if len(list1)==0:#if its an empty list
                continue
            elif len(list1)!=4 :#if the matrix are not in the same length
                if_its_not_in_the_same_length=1
                dx_data, x_data, y_data, dy_data = [], [], [], []
                print("Input file error: Data lists are not the same length.")
                vertical_not_same_length=True
                break
            elif "axis" in sub_data:#not to disturb the organization.
                continue
            elif if_its_not_in_the_same_length==0:#the same length
                for i in range(0, 4):
                    total_list[i].append(list1[i])  # one big orginaized list
                    #print(total_list)
                for index in range(0, 4):#orginize the data in different array
                    if total_list[index][0]=="dy":
                        dy_data=total_list[index][1:]
                    elif total_list[index][0]=="y":
                        y_data=total_list[index][1:]
                    elif total_list[index][0]=="x":
                        x_data=total_list[index][1:]
                    elif total_list[index][0]=="dx":
                        dx_data=total_list[index][1:]

    elif horo==True:#if it is orginized horizontal
        horizontal_not_same_length = False

        for index in range(0,4):#orginize the data in different array
            if "dy" in list_lines_input[index]:
                dy_data=list_lines_input[index].split()
                dy_data=dy_data[1:]
            elif "dx" in list_lines_input[index]:
                dx_data = list_lines_input[index].split()
                dx_data = dx_data[1:]
            elif "x" in list_lines_input[index]:
                x_data = list_lines_input[index].split()
                x_data = x_data[1:]
            elif "y" in list_lines_input[index]:
                y_data = list_lines_input[index].split()
                y_data = y_data[1:]

    negative = False
    if len(y_data) == len(x_data) and len(x_data) == len(dx_data) and len(dx_data) == len(dy_data):#if the same length
        for i in range (len(y_data)):
            x_data[i], y_data[i], dx_data[i], dy_data[i]=float(x_data[i]), float(y_data[i]), float(dx_data[i]), float(dy_data[i])#make the chr to num
            if dx_data[i]<0 or dy_data[i]<0:# check that all the uncertainties bigger than zero
                print("Input file error: Not all uncertainties are positive.")
                negative=True
                x_data, y_data, dx_data, dy_data=[],[],[],[]
                break
    elif vertical_not_same_length!=True:#if the vertical is in the same length,and the horizontal not
        x_data, y_data, dx_data, dy_data = [], [], [], []
        print("Input file error: Data lists are not the same length.")
        horizontal_not_same_length=True#horizontal not in the same length
    return  x_data,y_data, dx_data, dy_data,negative,horizontal_not_same_length,vertical_not_same_length#back to line feat

def  Fitting_function_and_definitions (xi,yi,dxi,dyi):#to calculate the value that we need
    N=len(xi)#amount of numbers
    xy=multiplay_function(xi,yi)#x*y
    x_sqrt_2=multiplay_function(xi,xi)#x^2
    dy_sqrt_2=multiplay_function(dyi,dyi)#dy^2
    roof_x, roof_y, roof_xy, roof_x_sqrt_2, roof_dy_sqrt_2=roof_function(xi,yi,xy,x_sqrt_2,dy_sqrt_2)#the numbers that are needed with roof
    a_f=(roof_xy-roof_x*roof_y) / ( roof_x_sqrt_2 -( roof_x ** 2 ))#parameter a
    da_f=sqrt(roof_dy_sqrt_2 / ( N *(roof_x_sqrt_2 -(roof_x ** 2))))#parameter a error
    b_f=roof_y-a_f*roof_x#parameter b
    db_f=sqrt((roof_dy_sqrt_2 * roof_x_sqrt_2) / (N * (roof_x_sqrt_2 - ( roof_x** 2))))#parameter b error
    chi_2=chi_sqear(xi,yi,dyi,a_f,b_f)#chi ^2
    chi_2_mini=chi_2/(N-2)#chi^2 min
    return a_f, da_f, b_f, db_f, chi_2, chi_2_mini


def multiplay_function(var1,var2):#multiplay the lists
    new_var=[]
    for i in range(len(var1)):
        new_var.append(var1[i]*var2[i])
    return new_var


def calculated_everage(z,dy_2):#Weighted arithmetic mean
    numerator,denominator=0,0
    for i in range (len (z)):
        numerator+=z[i]/dy_2[i]
        denominator+=1/dy_2[i]
    roof_z=numerator/denominator#the weighted arithmetic mean
    return roof_z


def roof_function(x_n,y_n,xy_n,x_sqrt_2_n,dy_sqrt_2_n):#concentration values
    r_x=calculated_everage(x_n,dy_sqrt_2_n)
    r_y=calculated_everage(y_n,dy_sqrt_2_n)
    r_xy=calculated_everage(xy_n,dy_sqrt_2_n)
    r_x_sqrt_2=calculated_everage(x_sqrt_2_n,dy_sqrt_2_n)
    r_dy_sqrt_2=calculated_everage(dy_sqrt_2_n,dy_sqrt_2_n)

    return r_x, r_y, r_xy, r_x_sqrt_2, r_dy_sqrt_2

def chi_sqear (x_i,y_i,d_yi,ai,bi):

    i_chi_2=0
    for i in range(len(x_i)):
        i_chi_2 += ((y_i[i]-(ai*x_i[i]+bi))/(d_yi[i]))**2
    return i_chi_2

def output_format(a_pr,d_a_pr,b_pr,d_b_pr,chi_squer_pr,chi_2_mini_pr):#printing the wanted valuse
    the_output="a = {0} +- {1} \nb = {2} +- {3} \nchi2 = {4} \nchi2_reduced = {5} ".format(a_pr,d_a_pr,b_pr,d_b_pr,chi_squer_pr,chi_2_mini_pr)#formatin the output
    print(the_output)
    return

def plot_function(a_i,b_i,y_i,dy_i,x_i,dx_i,x_axis_i,y_axis_i):
    the_max_range_of_x=max(x_i)#the max of range of the x scale
    x=the_max_range_of_x*2
    the_max_range_of_x=x//2#take the floor results
    the_max_range_of_x=the_max_range_of_x+1#to have the range needed because the arange take one down

    the_min_range_of_x = min(x_i)#the min of range of the x scale
    x_range = np.arange(the_min_range_of_x, the_max_range_of_x)#the range of x axis

    y_plot=a_i*x_range+b_i#the linear line
    plt.plot(x_range, y_plot,'r-')#plot the graph with read line
    plt.ylabel(y_axis_i)#name for y axis
    plt.xlabel(x_axis_i)#name for x axis
    plt.errorbar(x_i,y_i,dy_i,dx_i,fmt='none')#plot errors
    fig1=plt.gcf()#save the grafh on a vaviable
    plt.show()#show the plot
    plt.figure()
    fname="linear_fit.svg"#the name of the saved figuer
    fig1.savefig(fname)#save the file


#main program
import numpy as np
import matplotlib.pyplot as plt
from math import *
fit_linear("filename")

