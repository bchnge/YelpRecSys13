def json2dataframe(file, exclude = None):
    """ this is a utility to be used for converting json files to pandas dataframes 
    
    Input:  file = a filepath to a json data file
            exclude = a list of variables to exclude from output dataframe. If None, then all variables are included
    """

    import pandas as pd
    import json
    
    data = []
    with open(file,'r') as f:
        for line in f:
            data.append(json.loads(line))
        
    N = len(data)    
    df = pd.DataFrame(columns = data[1].keys()[1:],index = range(0,N))
    finaldata = pd.DataFrame(index = range(0,N))    
   
    # Handle non-dictionary variables
    for col in data[1].keys():
        coltype = type(data[1][col])
        if coltype != dict:
            finaldata[col] = [v[col] for v in data]

    # Handle 1-level nested dictionaries
    for col in data[1].keys():
        coltype = type(data[1][col])
        if coltype == dict:
            for col2 in data[1][col].keys():
                finaldata[col2] = [v[col][col2] for v in data]
                
    # Delete variables to be excluded
    if exclude!=None:
        for v in exclude:
            del finaldata[v]
    return finaldata
    
def preview_json(file):
    """ this utility will print a list of variables provided by the given json filepath
    """
    import json
    
    data = []
    with open(file,'r') as f:
        for line in f:
            data.append(json.loads(line))
            
    print data[1].keys()


def checkin2dataframe (file):
    import pandas as pd
    import json
    """ this utility will convert the checkin data to data frame
    """
    data = []
    with open(file,'r') as f:
        for line in f:
            data.append(json.loads(line))
            
    df = pd.DataFrame(index = range(0,len(data)))
            
    for hour in range(0,24):
        for week in range(0,7):
            df[str(hour) + "-" + str(week)] = pd.Series()    
            
    for d in range(0,len(data)):
        for t in data[d]['checkin_info']:
            df[t][d] = data[d]['checkin_info'][t]
    
    # Missing --> 0
    df = df.fillna(0)
    
    # bring in the rest of the columns
    for col in data[1].keys():
        if col != 'checkin_info':
            df[col] = [v[col] for v in data]
            
    return df
                
def constructData(masterdata, include_list):
    """ Takes in a master dataframe and an array of variables to be included in the produced dataset. This should be used for constructing x and y datasets """
    import pandas as pd
    
    newData = pd.DataFrame(index = masterdata.index)
    for variable in include_list:
        if type(masterdata[variable][0]) == unicode:
            temp = pd.get_dummies(masterdata[variable])   
            for col in temp:
                newData['d_' + str(variable) + str(col)] = temp[col]        
        else:
            newData[variable] = masterdata[variable]
    return newData
    
    
def combineIntersectXY(x,y):
    """ combines x and y dataframes and produces an intersection of nonmissing data. Returns new X and new Y"""
    import pandas as pd
    tempData = y.join(x)
    temp2Data = tempData.dropna(how = 'any')
    newY = temp2Data.ix[:,0]
    newX = temp2Data.ix[:,1:]
    return newX, newY
