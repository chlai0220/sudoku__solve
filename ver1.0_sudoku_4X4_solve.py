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
    source_sudoku_model = []
    ans1 = ""
    while not ans1.upper()=="Y":
        print("請由上至下，由左至右依序輸入數字。")
        print("未知數字請輸入0")
        print("輸入範例:0230(共4碼)")
        for i in range(4):
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
        ans1 = input("請確認輸入的數獨是否正確(Y/N)?\n")
        
        if ans1.upper()=="N":
            ans2 = input("是否要離開本程式(Y/N)?")
            if ans2.upper()=="Y":
                print("謝謝使用本程式")
                sys.exit(0)
            else:
                print("請重新輸入!!!\n")
    return source_sudoku_model
    #---------------------------------------------------------------------------------------------------------------------------------

class Create_Sudoku:
    #---------------------------------------------------------------------------------------------------------------------------------
    def __init__(self  , rows=4 , sudoku_model=None):
        self.rows = rows
        self.sudoku_model = np.zeros((rows,rows) , np.int)

    def main(self , source_sudoku_model):
        row_num = self.rows
        for i in range(row_num):
            for j in range(row_num):
                self.sudoku_model[i][j] = source_sudoku_model[i][j]
        return self.sudoku_model 
    #---------------------------------------------------------------------------------------------------------------------------------

def Sudoku_Solve(rows , sudoku_model):
    #---------------------------------------------------------------------------------------------------------------------------------
    cols = rows
    num_list = [1,2,3,4]
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
                    list3 = Block_Solve(rows , i , j , sudoku_model)

                    #diff_list2 = 
                    match_list = list(set(list3).intersection(set(diff_list)))
       
                    if len(diff_list)==1:
                        sudoku_model[i][j] = diff_list[0]
                        #print(set(list1)+set(list2))

                    if len(match_list)==1:
                        sudoku_model[i][j] = match_list[0]
                        #print(set(list1)+set(list2))
                        
                if sudoku_error==1:
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
    num_list = [1,2,3,4]
    
    if rows==4:
        if blk_area=="00" or blk_area=="01" or blk_area=="10" or blk_area=="11":
            area_lists = [[0,0] , [0,1] , [1,0] , [1,1]]
            
        elif blk_area=="02" or blk_area=="03" or blk_area=="12" or blk_area=="13":
            area_lists = [[0,2] , [0,3] , [1,2] , [1,3]]

        elif blk_area=="20" or blk_area=="21" or blk_area=="30" or blk_area=="31":
            area_lists = [[2,0] , [2,1] , [3,0] , [3,1]]

        elif blk_area=="22" or blk_area=="23" or blk_area=="32" or blk_area=="33":
            area_lists = [[2,2] , [2,3] , [3,2] , [3,3]]
            
        temp_list = []
        for area_list in area_lists:
            (x, y) = area_list[0] , area_list[1]
            if not sudoku_model[x][y]==0:
                temp_list.append(sudoku_model[x][y])

        list3 = list(set(num_list).difference(set(temp_list))) #差集
    return list3
    #---------------------------------------------------------------------------------------------------------------------------------
    

class Sudoku_Verify:
    #---------------------------------------------------------------------------------------------------------------------------------
    def __init__(self , rows=4):
        self.rows = rows
        #self.main()

    def main(self , sudoku_model):
        row_num = self.rows
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

            print("=" * 20 + "\n4X4數獨解題成功~^^~\n" + "=" * 20)
        else:
            print("\n*** 本次數獨解答如下: ***")
            print(sudoku_model)
            print("=" * 20 + "\n4X4數獨解題失敗~><~\n" + "=" * 20)
        #......................................................................................
        
    def verify1(self , new_model , row_num):
        if row_num==4:Row_Sum = 10
        if row_num==9:Row_Sum = 45
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
            
        Row_Sum = int(row_num * (1+row_num)*0.5)    
        check_count = 0
        
        for i in myRange:
            for j in myRange:
                cell_sum = 0
                for ii in i:
                    for jj in j:
                        #print(ii , jj)
                        cell_sum += new_model[ii][jj]
                if cell_sum==10:
                    check_count += 1

        if not check_count==row_num:
            #print("Verify Rule2 - Pass!")
            #print(new_model)
            #print("Verify Rule2 - Fail!")
            #print("Create Sudoku Again")
            #print(new_model)
            #self.main()
            return False
        return True

    def verify3(self , new_model , row_num):
        if row_num==4:myRange = [[0,1] , [2,3]]   
        if row_num==9:myRange = [[0,1,2] , [3,4,5] , [6,7,8]]
        
        Row_Sum = int(row_num * (1+row_num)*0.5)
        check_count = 0

        if row_num==4:
            for i in myRange:
                for j in myRange:
                    temp_list = []
                    for ii in i:
                        for jj in j:
                            temp_list.append(int(new_model[ii][jj]))
                            
                    #Rule3
                    temp_list.sort()
                    str_num = "".join([str(num) for num in temp_list])
                    if str_num=="1234":
                        check_count += 1
                    
        if not check_count==row_num:
            #print("Verify Rule3 - Pass!")
            #print(new_model)
            #sys.exit(0)    
            #else:
            #print("Verify Rule3 - Fail!")
            #print("Create Sudoku Again")
            #print(new_model)
            #self.main()
            return False
        return True
    #---------------------------------------------------------------------------------------------------------------------------------    

#============================================================================#
if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    time1 = time.time()

    source_sudoku_model = Input_Soduku()

    #source_sudoku_model = [[0, 0, 0, 0], [3, 0, 0, 0], [0, 0, 4, 0], [0, 2, 3, 0]]
    cs = Create_Sudoku()
    new_sudoku_model = cs.main(source_sudoku_model)
    fin_sudoku_model = Sudoku_Solve(len(new_sudoku_model ), new_sudoku_model)
    sv = Sudoku_Verify()
    sv.main(fin_sudoku_model)                   

    time2 = time.time()
    Exe_Time(time1 , time2)
#============================================================================#

