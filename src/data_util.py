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

