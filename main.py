import argparse
from os import path
from StartFlowDroid import runFlowDroid
from UserParser.UserParserComponent import parser_steps
import os
import pickle
import sklearn
import numpy as np




drd_dir = os.getcwd() + "/"  #droidlicious working dircroty
output_folder = drd_dir + "Analysis_Output/"



def  main(file_path,input_options,sdk_path):# the working flow start from here

    fd_options= set_option(input_options) # parsing the option to match for flowdroid

    isDirValide(file_path)
####################################################Flowdroid step####################################################
    if (not path.exists(output_folder)):  # if the ouput folder not exists
        os.mkdir(output_folder)

    if(path.basename(file_path).endswith(".apk")):

        if(sdk_path.__eq__('None')): #must  enter SDK folder
            print("To analyze apk file, must enter -sdk")
            exit()
        elif (not path.isdir(sdk_path)):
            print("can not find SDK path")
            exit()

        analysis_Result_file= runFlowDroid(file_path,fd_options,sdk_path)

        if(not analysis_Result_file): exit() #exit if analysis time out


    ####################################################parser step####################################################

    elif (path.basename(file_path).endswith(".txt")): # .txt file only need parsing
             analysis_Result_file = file_path
    else:
     print("file type  not supported")
    # return "file type  not supported"
     exit()

    print("Parsing the analysis output")

    App= parser_steps(analysis_Result_file,output_folder)
    #App= parseP(ParseFD(droidlicious_DIR+"UserParser/", ))
    print("Parser done")
    os.chdir(drd_dir)
    #delete_Output()  # delete all the outpute during the analysis and parsing :)

    ####################################################prediction step####################################################
    predict(App)


def isDirValide(file_dir):
    if(not path.exists(file_dir)):
        print("Cant find the file")
        exit()
    if(path.getsize(file_dir)==0):
        print ("file is empty")
        exit()


def predict(X_test):
    sample=np.array(X_test[1:])
    k= sample.reshape(1,-1)
    print(k)
    model_file ='initial_model.sav'
    load_lr_model = pickle.load(open(model_file, 'rb'))
    y= load_lr_model.predict(k)
    print(y)


def delete_Output():
   os.chdir(output_folder)
   for root,dir,files in os.walk(output_folder):
       for f in files:
           if (path.isfile(f)):
            os.remove(f)
   os.chdir(drd_dir)

def set_option(input_option):
    if(input_option.__eq__('None')):
        return 'None'

    fd_option = ""
    space = ' '
    arr = input_option.split(' ')
    if (arr.__contains__('af')):
        fd_option += '--aliasflowins' + space

    if (arr.__contains__('stat')):
        fd_option += '--static' + space
    elif (arr.__contains__('nostat')):
        fd_option += '--nostatic' + space

    if (arr.__contains__('len')):
        i = arr.index('len') + 1
        fd_option += '--aplength ' + arr[i] + space
        if (not arr[i].isdecimal()):
            print("enter length correctly")
            exit()
    else:
        fd_option +='--aplength 2'  # defult option
    if (arr.__contains__('noback')):
        fd_option += '--nocallbacks' + space

    if (arr.__contains__('src')):
        fd_option += '--pathalgo sourcesonly' + space
    if (arr.__contains__('sen')):
        fd_option += '--pathalgo contextsensitive' + space
    if (arr.__contains__('insen')):
        fd_option += '--pathalgo contextinsensitive' + space

    if (arr.__contains__('nopaths')):
        fd_option += '--nopaths' + space

    if (arr.__contains__('nosize')):
        fd_option += '--noarraysize' + space

    if (arr.__contains__('nopaths')):
        fd_option += '--nopaths' + space

    return fd_option


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help="get the result")
    parser.add_argument("-op", type=str, required=False, dest='options', help=" Enter the option of FlowDroid ")
    parser.add_argument('-sdk', type=str, required=False, action='store', dest="sdks", help="sdk path")
    parser.add_argument('--version', action='version', version='DroidLicious 1.0')

    args = parser.parse_args()
    file_path = args.file
    input_options = args.options
    sdk_path = args.sdks
    main(file_path,input_options,sdk_path)