####################################################################################
# Python Version : 3.7.3
# File Name     : 
# Coder            : Weder Lai
# Purpose        : 
####################################################################################
# History: 
#  Ver        Date               Descripition
# -------  ------------  ----------------------------
#  1.0          2019/08/20   * New Issue
#  1.1          2019/08/21   * Add New Solve 
####################################################################################
#+--------------------+
#|       MODULE       |     
#+--------------------+
#==================================
import os , sys
import random
import time
import numpy as np
#==================================

#*******************************************#
# FUNCTION 
#*******************************************#
##############################################################################
 
def Exe_Time(t1 , t2):
    #---------------------------------------------------------------------------------------------------------------------------------
    print("啟動時間  : " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t1))  )
    print("結束時間  : " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t2))  )
    print("執行時間  : " + str(round(t2-t1,3))+ "秒")
    #---------------------------------------------------------------------------------------------------------------------------------

def Input_Soduku():
    #---------------------------------------------------------------------------------------------------------------------------------
    input_err = 0
    print("請選擇數獨型態")
    
    while input_err<3:
        #print("請選擇數獨型態")
        print("1. 4X4 ")
        print("2. 9X9 ")
        ans = input(">")
        if str(ans)=="1" or str(ans)=="2":
            break
        else:
            input_err += 1
            print("請重新選擇數獨型態")

    if input_err>=3:
        print("輸入錯誤超過3次!!!")
        print("結束本程式.")
        sys.exit(0)
            
    if ans=="1":row_num=4
    elif ans=="2":row_num=9
    
    source_sudoku_model = []
    ans1 = ""
    while not ans1.upper()=="Y":
        print("請由上至下，由左至右依序輸入數字。")
        print("未知數字請輸入0")
        if row_num==4:print("輸入範例:0402(共" + str(row_num) + "碼)")
        if row_num==9:print("輸入範例:040250008(共" + str(row_num) + "碼)")
        for i in range(row_num):
            row = []
            ans = input("請輸入第" + str(i+1) + "列數字:")

                #輸入檢查機制
            for element in ans:
                if int(element)<10:
                    pass
                else:
                    print("輸入錯誤!!!重新輸入")
                    self.input_num()

            for element in ans:
                row.append(int(element))
            source_sudoku_model.append(row)
        print("你輸入的數獨為:")
        print(np.array(source_sudoku_model))
        ans1 = input("請確認輸入的數獨是否正確(Y/N)?")
        
        if ans1.upper()=="N":
            ans2 = input("是否要離開本程式(Y/N)?")
            if ans2.upper()=="Y":
                print("謝謝使用本程式")
                sys.exit(0)
            else:
                source_sudoku_model = []
                print("請重新輸入!!!\n")
                
        for i in range(row_num):
            if not len(source_sudoku_model[i])==row_num:
                print("數獨第" + str(i+1) + "行數目不符!")
                print(source_sudoku_model[i])
                print("請重新輸入!!!\n")
                source_sudoku_model = []
            
    return source_sudoku_model
    #---------------------------------------------------------------------------------------------------------------------------------

class Create_Sudoku:
    #---------------------------------------------------------------------------------------------------------------------------------
    def __init__(self  , rows=4):
        self.rows = rows
        #self.sudoku_model = np.zeros((rows,rows) , np.int)

    def main(self , source_sudoku_model):
        #row_num = self.rows
        row_num = len(source_sudoku_model)
        sudoku_model = np.zeros((row_num,row_num) , np.int)
        
        for i in range(row_num):
            for j in range(row_num):
                sudoku_model[i][j] = source_sudoku_model[i][j]
        return sudoku_model 
    #---------------------------------------------------------------------------------------------------------------------------------

def Sudoku_Solve(rows , sudoku_model):
    #---------------------------------------------------------------------------------------------------------------------------------
    cols = rows
    row_num = len(sudoku_model)
    if row_num==4:num_list = [1,2,3,4]
    if row_num==9:num_list = [1,2,3,4,5,6,7,8,9]
    sudoku_error = 0
    run_count = 0
    #print(sudoku_model)
    
    while run_count<3000:
        run_count += 1
        for i in range(rows):
            for j in range(cols): 
                num = sudoku_model[i][j]
                if num==0:
                    #Row - List
                    list1 = [i for i in sudoku_model[i] if not i==0]

                    #Col - List
                    list2 = [i for i in [sudoku_model[l][j] for l in range(cols)] if not i==0]

                    #Row - List & Col - List Intersection
                    merge_list = list(set(list1).union(set(list2)))

                    if len(merge_list)==rows:
                        sudoku_error  += 1 
                        print("\nSudoku 經自動檢驗後，本空格此無符合數字")
                        print("(Row , Col ) :  "  , i , " , " , j)
                        print("錯誤次數 : " , sudoku_error)
                        pass              
                     
                    diff_list = list(set(num_list).difference(set(merge_list)))
                    
                    #Block - List
                    #Can Input Number
                    list3 = Block_Solve(rows , i , j , sudoku_model)

                    #diff_list2 = 
                    match_list = list(set(list3).intersection(set(diff_list)))
       
                    if len(diff_list)==1:
                        sudoku_model[i][j] = diff_list[0]
                        #print(set(list1)+set(list2))

                    if len(match_list)==1:
                        sudoku_model[i][j] = match_list[0]
                        #print(set(list1)+set(list2))

                    #Ver 1.1
                    sudoku_model = Block_Center_Remove_Solve(9 , i , j ,sudoku_model , match_list)
                        
                if sudoku_error>100:
                    print("\n無符合自動檢驗超過" + str(sudoku_error)+ "次")
                    print("請確認填入數字是否正確!!!")
                    print("3秒後，將自動離開本程式!")
                    time.sleep(3)
                    sys.exit(0)
                    
        if (run_count%100)==0:
            zero_count = 0
            for i in range(rows):
                for j in range(cols):
                    if sudoku_model[i][j]==0:
                        zero_count += 1
            if zero_count==0:
                run_count = 9999
                print("\n<<< 完成自動填寫數獨 >>>")

    return sudoku_model
    #input("XXX")

    #---------------------------------------------------------------------------------------------------------------------------------

def Block_Solve(rows , i , j , sudoku_model):
    #--------------------------------------------------------------------------------------------------------------------------------- 
    blk_area = str(i)+str(j)
    row_num = len(sudoku_model)
    if row_num==4:num_list = [1,2,3,4]
    if row_num==9:num_list = [1,2,3,4,5,6,7,8,9]
    
    if rows==4:
        if blk_area=="00" or blk_area=="01" or blk_area=="10" or blk_area=="11":
            area_lists = [[0,0] , [0,1] , [1,0] , [1,1]]
            
        elif blk_area=="02" or blk_area=="03" or blk_area=="12" or blk_area=="13":
            area_lists = [[0,2] , [0,3] , [1,2] , [1,3]]

        elif blk_area=="20" or blk_area=="21" or blk_area=="30" or blk_area=="31":
            area_lists = [[2,0] , [2,1] , [3,0] , [3,1]]

        elif blk_area=="22" or blk_area=="23" or blk_area=="32" or blk_area=="33":
            area_lists = [[2,2] , [2,3] , [3,2] , [3,3]]

    if rows==9:
        if blk_area=="00" or blk_area=="01" or blk_area=="02" or blk_area=="10" or blk_area=="11" or blk_area=="12" or blk_area=="20" or blk_area=="21" or blk_area=="22":
            area_lists = [[0,0] , [0,1] , [0,2] , [1,0] , [1,1] , [1,2] ,[2,0] , [2,1] , [2,2]]
            
        elif blk_area=="03" or blk_area=="04" or blk_area=="05" or blk_area=="13" or blk_area=="14" or blk_area=="15" or blk_area=="23" or blk_area=="24" or blk_area=="25":
            area_lists = [[0,3] , [0,4] , [0,5] , [1,3] , [1,4] , [1,5] ,[2,3] , [2,4] , [2,5]]
            
        elif blk_area=="06" or blk_area=="07" or blk_area=="08" or blk_area=="16" or blk_area=="17" or blk_area=="18" or blk_area=="26" or blk_area=="27" or blk_area=="28":
            area_lists = [[0,6] , [0,7] , [0,8] ,[1,6] , [1,7] , [1,8] ,[2,6] , [2,7] , [2,8]]
            
        elif blk_area=="30" or blk_area=="31" or blk_area=="32" or blk_area=="40" or blk_area=="41" or blk_area=="42" or blk_area=="50" or blk_area=="51" or blk_area=="52":
            area_lists = [[3,0] , [3,1] , [3,2] ,[4,0] , [4,1] , [4,2] , [5,0] , [5,1] , [5,2]]
            
        elif blk_area=="33" or blk_area=="34" or blk_area=="35" or blk_area=="43" or blk_area=="44" or blk_area=="45" or blk_area=="53" or blk_area=="54" or blk_area=="55":
            area_lists = [[3,3] , [3,4] , [3,5] ,[4,3] , [4,4] , [4,5] ,[5,3] , [5,4] , [5,5]]
            
        elif blk_area=="36" or blk_area=="37" or blk_area=="38" or blk_area=="46" or blk_area=="47" or blk_area=="48" or blk_area=="56" or blk_area=="57" or blk_area=="58":
            area_lists = [[3,6] , [3,7] , [3,8] ,[4,6] , [4,7] , [4,8] ,[5,6] , [5,7] , [5,8]]
            
        elif blk_area=="60" or blk_area=="61" or blk_area=="62" or blk_area=="70" or blk_area=="71" or blk_area=="72" or blk_area=="80" or blk_area=="81" or blk_area=="82":
            area_lists = [[6,0] , [6,1] , [6,2] ,[7,0] , [7,1] , [7,2] ,[8,0] , [8,1] , [8,2]]
            
        elif blk_area=="63" or blk_area=="64" or blk_area=="65" or blk_area=="73" or blk_area=="74" or blk_area=="75" or blk_area=="83" or blk_area=="84" or blk_area=="85":
            area_lists = [[6,3] , [6,4] , [6,5] ,[7,3] , [7,4] , [7,5] ,[8,3] , [8,4] , [8,5]]
            
        elif blk_area=="66" or blk_area=="67" or blk_area=="68" or blk_area=="76" or blk_area=="77" or blk_area=="78" or blk_area=="86" or blk_area=="87" or blk_area=="88":
            area_lists = [[6,6] , [6,7] , [6,8] ,[7,6] , [7,7] , [7,8] ,[8,6] , [8,7] , [8,8]]

    if True:
        temp_list = []
        for area_list in area_lists:
            (x, y) = area_list[0] , area_list[1]
            if not sudoku_model[x][y]==0:
                temp_list.append(sudoku_model[x][y])
        list3 = list(set(num_list).difference(set(temp_list)))
    return list3
    #---------------------------------------------------------------------------------------------------------------------------------

def BCRS_INSERT(i , j , sudoku_model , match_num , msg):
    #---------------------------------------------------------------------------------------------------------------------------------
    sudoku_model[i][j] = match_num
    print("Block-Line Delete Rule")
    print(msg)
    #print(np.array(sudoku_model))
    return sudoku_model
    #---------------------------------------------------------------------------------------------------------------------------------
    
def Block_Center_Remove_Solve(rows , i , j , sudoku_model , block_list):
    #---------------------------------------------------------------------------------------------------------------------------------
    pos = str(i)+str(j)
    pos_list = [0,1,2,3,4,5,6,7,8]

    if pos=="11" or pos=="14" or pos=="17" or pos=="41" or pos=="44" or pos=="47" or pos=="71" or pos=="74" or pos=="77":
        
        value = sudoku_model[i][j]
        
        if value==0:
            #(pos1 , pos2) = (x, y)
            top_row = [i-1,list(set(pos_list).difference(set([j-1,j,j+1])))]
            button_row = [i+1,list(set(pos_list).difference(set([j-1,j,j+1])))]
            left_col = [list(set(pos_list).difference(set([i-1,i,i+1]))),j-1]
            right_col = [list(set(pos_list).difference(set([i-1,i,i+1]))),j+1]
            
            top_list = [ sudoku_model[top_row[0]][y] for y in top_row[1] if sudoku_model[top_row[0]][y]>0]
            button_list = [ sudoku_model[button_row[0]][y] for y in button_row[1] if sudoku_model[button_row[0]][y]>0]       
            left_list = [ sudoku_model[x][left_col[1]] for x in left_col[0] if sudoku_model[x][left_col[1]]>0]
            right_list = [ sudoku_model[x][right_col[1]] for x in right_col[0] if sudoku_model[x][right_col[1]]>0]

            t_value , b_value , l_value , r_value = sudoku_model[i-1][j] , sudoku_model[i+1][j] , sudoku_model[i][j-1] , sudoku_model[i][j+1]
            zero_list = [v for v in [t_value , b_value , l_value , r_value] if v==0]      
            if len(zero_list)==0:
                #共有7種規則
                #Rule1
                for c in range(7):
                    if c==0:
                        #   V   V
                        #>O+O
                        #   +++
                        #>O+O
                        merge_list1 = [element for element in top_list if element in button_list]
                        merge_list2 = [element for element in left_list if element in right_list]
                        merge_list = [element for element in merge_list1 if element in merge_list2]
                    elif c==1:
                        #   V   
                        #>O+O
                        #   +++
                        #>O+O
                        merge_list1 = [element for element in top_list if element in button_list]
                        merge_list = [element for element in merge_list1 if element in left_list]
                    elif c==2:
                        #         V
                        #>O+O
                        #   +++
                        #>O+O
                        merge_list1 = [element for element in top_list if element in button_list]
                        merge_list = [element for element in merge_list1 if element in right_list]
                    elif c==3:
                        #   V   V
                        #>O+O
                        #   +++
                        #   O+O
                        merge_list1 = [element for element in left_list if element in right_list]
                        merge_list = [element for element in merge_list1 if element in top_list]
                    elif c==4:
                        #   V   V
                        #   O+O
                        #   +++
                        #>O+O
                        merge_list1 = [element for element in left_list if element in right_list]
                        merge_list = [element for element in merge_list1 if element in button_list]
                    elif c==5:
                        #   V   V
                        #   O+O
                        #   +++
                        #   O+O
                        merge_list =  [element for element in left_list if element in right_list]
                    elif c==6:
                        #   
                        #>O+O
                        #   +++
                        #>O+O
                        merge_list = [element for element in top_list if element in button_list]
                        
                    match_list =[ i for i in merge_list if i in block_list]
                    if len(match_list)==1:
                        sudoku_model = BCRS_INSERT(i,j,sudoku_model , match_list[0] , "Rule1")
                        break
                    
            elif len(zero_list)==1:
                if t_value==0:
                    #OOO
                    #+++
                    #O+O
                    for c in range(3):
                        if c==0:
                            merge_list = [element for element in top_list if element in button_list]
                            
                        elif c==1:
                            merge_list1 = [element for element in top_list if element in left_list]
                            merge_list = [element for element in merge_list1 if element in button_list]
                            
                        elif c==2:
                            merge_list1 = [element for element in top_list if element in left_list]
                            merge_list = [element for element in merge_list1 if element in right_list]

                        match_list =[ i for i in merge_list if i in block_list]
                        if len(match_list)==1:
                            sudoku_model = BCRS_INSERT(i,j,sudoku_model , match_list[0] , "Rule2-1 : Top_Num = Zero")
                            break
                        
                elif b_value==0:
                    #O+O
                    #+++
                    #OOO
                    for c in range(3):
                        if c==0:
                            merge_list = [element for element in top_list if element in button_list]
                            
                        elif c==1:
                            merge_list1 = [element for element in right_list if element in button_list]
                            merge_list = [element for element in merge_list1 if element in top_list]
                            
                        elif c==2:
                            merge_list1 = [element for element in right_list if element in button_list]
                            merge_list = [element for element in merge_list1 if element in left_list]

                        match_list =[ i for i in merge_list if i in block_list]
                        
                        if len(match_list)==1:
                            sudoku_model = BCRS_INSERT(i,j,sudoku_model , match_list[0] , "Rule2-2 : Button_Num = Zero")
                            break
                        
                elif l_value==0:
                    #O+O
                    #O++
                    #O+O
                    for c in range(3):
                        if c==0:
                            merge_list = [element for element in left_list if element in right_list]
                            
                        elif c==1:
                            merge_list1 = [element for element in left_list if element in top_list]
                            merge_list = [element for element in merge_list1 if element in button_list]
                            
                        elif c==2:
                            merge_list1 = [element for element in left_list if element in top_list]
                            merge_list = [element for element in merge_list1 if element in right_list]
                            
                        match_list =[ i for i in merge_list if i in block_list]
                        
                        if len(match_list)==1:
                            sudoku_model = BCRS_INSERT(i,j,sudoku_model , match_list[0] , "Rule2-3 : Left_Num = Zero")
                            break
                        
                elif r_value==0:
                    #O+O
                    #++O
                    #O+O
                    for c in range(3):
                        if c==0:
                            merge_list = [element for element in left_list if element in right_list]
                            
                        elif c==1:
                            merge_list1 = [element for element in top_list if element in right_list]
                            merge_list = [element for element in merge_list1 if element in left_list]
                            
                        elif c==2:
                            merge_list1 = [element for element in top_list if element in right_list]
                            merge_list = [element for element in merge_list1 if element in button_list]
                            
                        match_list =[ i for i in merge_list if i in block_list]
                        
                        if len(match_list)==1:
                            sudoku_model = BCRS_INSERT(i,j,sudoku_model , match_list[0] , "Rule2-4 : Right_Num = Zero")
                            break

            elif len(zero_list)==2:
                if t_value==0 and b_value==0:
                    #OOO
                    #+++
                    #OOO
                    for c in range(4):
                        if c==0:
                            merge_list = [element for element in top_list if element in button_list]
                            
                        elif c==1:
                            merge_list1 = [element for element in top_list if element in button_list]
                            merge_list = [element for element in merge_list1 if element in left_list]
                            
                        elif c==2:
                            merge_list1 = [element for element in top_list if element in button_list]
                            merge_list = [element for element in merge_list1 if element in right_list]

                        elif c==3:
                            merge_list1 = [element for element in top_list if element in button_list]
                            merge_list2 = [element for element in left_list if element in right_list]
                            merge_list = [element for element in merge_list1 if element in merge_list2]

                        match_list =[ i for i in merge_list if i in block_list]
                        
                        if len(match_list)==1:
                            sudoku_model = BCRS_INSERT(i,j,sudoku_model , match_list[0] , "Rule3-1 : Top_Num & Button_Num = Zero")
                            break
                        
                elif t_value==0 and l_value==0:
                    #OOO
                    #O++
                    #O+O
                    for c in range(3):
                        if c==0:
                            merge_list1 = [element for element in top_list if element in left_list]
                            merge_list = [element for element in merge_list1 if element in right_list]
                            
                        elif c==1:
                            merge_list1 = [element for element in top_list if element in left_list]
                            merge_list = [element for element in merge_list1 if element in button_list]

                        elif c==2:
                            merge_list1 = [element for element in top_list if element in button_list]
                            merge_list2 = [element for element in left_list if element in right_list]
                            merge_list = [element for element in merge_list1 if element in merge_list2]

                        match_list =[ i for i in merge_list if i in block_list]
                        
                        if len(match_list)==1:
                            sudoku_model = BCRS_INSERT(i,j,sudoku_model , match_list[0] , "Rule3-2 : Top_Num & Left_Num = Zero")
                            break
                        
                elif t_value==0 and r_value==0:
                    #OOO
                    #++O
                    #O+O
                    for c in range(3):
                        if c==0:
                            merge_list1 = [element for element in top_list if element in right_list]
                            merge_list = [element for element in merge_list1 if element in left_list]
                            
                        elif c==1:
                            merge_list1 = [element for element in top_list if element in right_list]
                            merge_list = [element for element in merge_list1 if element in button_list]

                        elif c==2:
                            merge_list1 = [element for element in top_list if element in button_list]
                            merge_list2 = [element for element in left_list if element in right_list]
                            merge_list = [element for element in merge_list1 if element in merge_list2]

                        match_list =[ i for i in merge_list if i in block_list]
                        
                        if len(match_list)==1:
                            sudoku_model = BCRS_INSERT(i,j,sudoku_model , match_list[0] , "Rule3-3 : Top_Num & Right_Num = Zero")
                            break

                elif b_value==0 and r_value==0:
                    #O+O
                    #++O
                    #OOO
                    for c in range(3):
                        if c==0:
                            merge_list1 = [element for element in button_list if element in right_list]
                            merge_list = [element for element in merge_list1 if element in top_list]
                            
                        elif c==1:
                            merge_list1 = [element for element in button_list if element in right_list]
                            merge_list = [element for element in merge_list1 if element in left_list]

                        elif c==2:
                            merge_list1 = [element for element in top_list if element in button_list]
                            merge_list2 = [element for element in left_list if element in right_list]
                            merge_list = [element for element in merge_list1 if element in merge_list2]

                        match_list =[ i for i in merge_list if i in block_list]
                        
                        if len(match_list)==1:
                            sudoku_model = BCRS_INSERT(i,j,sudoku_model , match_list[0] , "Rule3-4 : Button_Num & Right_Num = Zero")
                            break
                        
                elif b_value==0 and l_value==0:
                    #O+O
                    #O++
                    #OOO
                    for c in range(3):
                        if c==0:
                            merge_list1 = [element for element in button_list if element in left_list]
                            merge_list = [element for element in merge_list1 if element in top_list]
                            
                        elif c==1:
                            merge_list1 = [element for element in button_list if element in left_list]
                            merge_list = [element for element in merge_list1 if element in right_list]

                        elif c==2:
                            merge_list1 = [element for element in top_list if element in button_list]
                            merge_list2 = [element for element in left_list if element in right_list]
                            merge_list = [element for element in merge_list1 if element in merge_list2]

                        match_list =[ i for i in merge_list if i in block_list]
                        
                        if len(match_list)==1:
                            sudoku_model = BCRS_INSERT(i,j,sudoku_model , match_list[0] , "Rule3-5 : Button_Num & Left_Num = Zero")
                            break

                elif b_value==0 and l_value==0:
                    #O+O
                    #O+O
                    #O+O
                    for c in range(4):
                        if c==0:
                            merge_list = [element for element in left_list if element in right_list]
                            
                        elif c==1:
                            merge_list1 = [element for element in left_list if element in right_list]
                            merge_list = [element for element in merge_list1 if element in top_list]
                            
                        elif c==2:
                            merge_list1 = [element for element in left_list if element in right_list]
                            merge_list = [element for element in merge_list1 if element in button_list]

                        elif c==3:
                            merge_list1 = [element for element in top_list if element in button_list]
                            merge_list2 = [element for element in left_list if element in right_list]
                            merge_list = [element for element in merge_list1 if element in merge_list2]

                        match_list =[ i for i in merge_list if i in block_list]
                        
                        if len(match_list)==1:
                            sudoku_model = BCRS_INSERT(i,j,sudoku_model , match_list[0] , "Rule3-6 : Left_Num & Right_Num = Zero")
                            break
            
            elif len(zero_list)==3:
                if t_value==0 and b_value==0 and l_value==0:
                    #OOO
                    #O++
                    #OOO
                    for c in range(2):
                        if c==0:
                            merge_list1 = [element for element in top_list if element in button_list]
                            merge_list = [element for element in merge_list1 if element in left_list]
                            
                        elif c==1:
                            merge_list1 = [element for element in top_list if element in button_list]
                            merge_list2 = [element for element in left_list if element in right_list]
                            merge_list = [element for element in merge_list1 if element in merge_list2]

                        match_list =[ i for i in merge_list if i in block_list]
                        
                        if len(match_list)==1:
                            sudoku_model = BCRS_INSERT(i,j,sudoku_model , match_list[0] , "Rule4-1 : Top_Num & Button_Num & Left_Num= Zero")
                            break
                        
                elif t_value==0 and b_value==0 and r_value==0:
                    #OOO
                    #++O
                    #OOO
                    for c in range(2):
                        if c==0:
                            merge_list1 = [element for element in top_list if element in button_list]
                            merge_list = [element for element in merge_list1 if element in right_list]
                            
                        elif c==1:
                            merge_list1 = [element for element in top_list if element in button_list]
                            merge_list2 = [element for element in left_list if element in right_list]
                            merge_list = [element for element in merge_list1 if element in merge_list2]

                        match_list =[ i for i in merge_list if i in block_list]
                        
                        if len(match_list)==1:
                            sudoku_model = BCRS_INSERT(i,j,sudoku_model , match_list[0] , "Rule4-2 : Top_Num & Button_Num & Right_Num= Zero")
                            break
                        
                elif b_value==0 and l_value==0 and r_value==0:
                    #O+O
                    #O+O
                    #OOO
                    for c in range(2):
                        if c==0:
                            merge_list1 = [element for element in left_list if element in right_list]
                            merge_list = [element for element in merge_list1 if element in button_list]
                            
                        elif c==1:
                            merge_list1 = [element for element in top_list if element in button_list]
                            merge_list2 = [element for element in left_list if element in right_list]
                            merge_list = [element for element in merge_list1 if element in merge_list2]

                        match_list =[ i for i in merge_list if i in block_list]
                        
                        if len(match_list)==1:
                            sudoku_model = BCRS_INSERT(i,j,sudoku_model , match_list[0] , "Rule4-3 : Button_Num & Left_Num & Right_Num= Zero")
                            break

                elif t_value==0 and l_value==0 and r_value==0:
                    #OOO
                    #O+O
                    #O+O
                    for c in range(2):
                        if c==0:
                            merge_list1 = [element for element in left_list if element in right_list]
                            merge_list = [element for element in merge_list1 if element in top_list]
                            
                        elif c==1:
                            merge_list1 = [element for element in top_list if element in button_list]
                            merge_list2 = [element for element in left_list if element in right_list]
                            merge_list = [element for element in merge_list1 if element in merge_list2]
                        match_list =[ i for i in merge_list if i in block_list]
                        
                        if len(match_list)==1:
                            sudoku_model = BCRS_INSERT(i,j,sudoku_model , match_list[0] , "Rule4-4 : Top_Num & Left_Num & Right_Num= Zero")
                            break
                        
            elif len(zero_list)==4:
                if t_value==0 and b_value==0 and l_value==0 and r_value==0:
                    #OOO
                    #O+O
                    #OOO
                    merge_list1 = [element for element in top_list if element in button_list]
                    merge_list2 = [element for element in left_list if element in right_list]
                    merge_list = [element for element in merge_list1 if element in merge_list2]
                    match_list =[i for i in merge_list if i in block_list]
                    if len(match_list)==1:
                        sudoku_model = BCRS_INSERT(i,j,sudoku_model , match_list[0] , "Rule4-4 : Top_Num & Left_Num & Right_Num= Zero")
                        
    #Fin
    return sudoku_model
    #---------------------------------------------------------------------------------------------------------------------------------
         

 

class Sudoku_Verify:
    #---------------------------------------------------------------------------------------------------------------------------------
    def __init__(self , rows=4):
        self.rows = rows
        #self.main()

    def main(self , sudoku_model):
        #row_num = self.rows
        row_num = len(sudoku_model)
        if row_num==4:row_num_list = [1,2,3,4]
        if row_num==9:row_num_list = [1,2,3,4,5,6,7,8,9]
        #......................................................................................
        ans1 = self.verify1(sudoku_model , row_num)
        ans2 = self.verify2(sudoku_model , row_num)
        ans3 = self.verify3(sudoku_model , row_num)
        #print(ans1 , ans2 , ans3)
        
        if ans1:print("『行總合』驗證結果 : PASS !")
        else:print("『行總合』驗證結果 :  FAIL !")

        if ans2:print("『列總合』驗證結果 : PASS !")
        else:print("『列總合』驗證結果 :  FAIL !")

        if ans3:print("『區塊總合』驗證結果 : PASS !")
        else:print("『區塊總合』驗證結果 :  FAIL !")

        if ans1 and ans2 and ans3:
            print("\n*** 本次數獨解答如下: ***")
            print(sudoku_model)

            print("=" * 20 + "\n" + str(row_num) + "X" + str(row_num) +"數獨解題成功~^^~\n" + "=" * 20)
        else:
            print("\n*** 本次數獨解答如下: ***")
            print(sudoku_model)
            print("=" * 20 + "\n" + str(row_num) + "X" + str(row_num) +"數獨解題失敗~><~\n" + "=" * 20)
        #......................................................................................
        
    def verify1(self , new_model , row_num):
        Row_Sum = int(row_num*(1+row_num)*0.5)
        
        new_model_trans = np.transpose(new_model)
        
        for i in range(row_num):
            row_sum = np.sum(new_model_trans[i])
            if not row_sum==Row_Sum:
                #print("Verify Rule1 - Fail!")
                #print("Create Sudoku Again")
                return False
        return True
        #print("Verify Rule1 - Pass!")
                
    def verify2(self , new_model , row_num):
        if row_num==4:myRange = [[0,1] , [2,3]]  
        if row_num==9:myRange = [[0,1,2] , [3,4,5] , [6,7,8]]

        check_count = 0
        
        Col_Sum = int(row_num*(1+row_num)*0.5)
        
        for i in myRange:
            for j in myRange:
                cell_sum = 0
                for ii in i:
                    for jj in j:
                        #print(ii , jj)
                        cell_sum += new_model[ii][jj]
                if cell_sum==Col_Sum:
                    check_count += 1

        if not check_count==row_num:
            return False
        return True

    def verify3(self , new_model , row_num):
        if row_num==4:myRange = [[0,1] , [2,3]]   
        if row_num==9:myRange = [[0,1,2] , [3,4,5] , [6,7,8]]
        
        Row_Sum = int(row_num * (1+row_num)*0.5)
        check_count = 0

        if row_num==4:chk_num_list = "1234"
        if row_num==9:chk_num_list = "123456789"
        for i in myRange:
            for j in myRange:
                temp_list = []
                for ii in i:
                    for jj in j:
                        temp_list.append(int(new_model[ii][jj]))
                            
                #Rule3
                temp_list.sort()
                str_num = "".join([str(num) for num in temp_list])
                if str_num==chk_num_list:
                    check_count += 1
                    
        if not check_count==row_num:
            return False
        return True
    #---------------------------------------------------------------------------------------------------------------------------------    

#============================================================================#
if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    time1 = time.time()

    source_sudoku_model = Input_Soduku()
    
    cs = Create_Sudoku()
    new_sudoku_model = cs.main(source_sudoku_model)
    #print(new_sudoku_model)
    fin_sudoku_model = Sudoku_Solve(len(new_sudoku_model), new_sudoku_model)
    sv = Sudoku_Verify()
    sv.main(fin_sudoku_model)                   

    time2 = time.time()
    Exe_Time(time1 , time2)
#============================================================================#

