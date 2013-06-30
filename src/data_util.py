import pandas as pd
import json
import sklearn.feature_extraction.text as feText

def json2dataframe(file, exclude = None):
    """ this is a utility to be used for converting json files to pandas dataframes 
    
    Input:  file = a filepath to a json data file
            exclude = a list of variables to exclude from output dataframe. If None, then all variables are included
    """

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
   
    data = []
    with open(file,'r') as f:
        for line in f:
            data.append(json.loads(line))
            
    print data[1].keys()


def checkin2dataframe (file):
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

    newData = pd.DataFrame(index = masterdata.index)
    for variable in include_list:
        if type(masterdata[variable][0]) == unicode or type(masterdata[variable][0]) == str :
            temp = pd.get_dummies(masterdata[variable])   
            for col in temp:
                newData['d_' + str(variable) + str(col)] = temp[col]        
        else:
            newData[variable] = masterdata[variable]
    return newData
    
    
def combineIntersectXY(x,y):
    """ combines x and y dataframes and produces an intersection of nonmissing data. Returns new X and new Y"""
    tempData = y.join(x)
    temp2Data = tempData.dropna(how = 'any')
    newY = temp2Data.ix[:,0]
    newX = temp2Data.ix[:,1:]
    return newX, newY

def text2featureArray(training_df, corpus, y_var, max_features):
    """ 
    convert a corpus to a dataframe to be added to the master dataset. Returns new master dataset and the vectorizer used

    master: training dataframe
    corpus: string referring to corpus of training df
    y_var: string referring to dependent variable of training df
    max_features: max number of features to extract

    """

    vectorizer = feText.TfidfVectorizer(stop_words = 'english', max_features = max_features)
  
    data = vectorizer.fit_transform(training_df[corpus].values, y = training_df[y_var].values)
    
    feature_list = vectorizer.get_feature_names()
    
    df = pd.DataFrame(data = data.toarray(), columns = feature_list, index = training_df.index)
    new_data = training_df
    for feature in feature_list:
        new_data['f_' + str(feature)] = df[feature]
    return new_data, vectorizer
    
    
    
def imputer(fromData, toData, impute_vars, by_var = None, mean = True):
    """
from_data: dataset where the imputation data will come from
to_data: dataset where the imputation data will be merged to
impute_var: variable to impute
by_var: categorical variable to calc imputation for
agg_method: median or mean
"""
    from_data= fromData.copy()
    to_data = toData.copy()
    
    if by_var is None:
        for impv in impute_vars:
            if mean == True:
                Filler = from_data[impv].mean()
            else:
                Filler = from_data[impv].median()
            to_data[impv].fillna(Filler, inplace = True)
        merged = to_data
    else:
        merged = to_data
        for impv in impute_vars:
            if mean == True:
                Filler = from_data[impv].mean()
            else:
                Filler = from_data[impv].median()

            if mean == True:
                a = from_data[impv].groupby(by = [from_data[by_var]]).mean()
            else:
                a = from_data[impv].groupby(by = [from_data[by_var]]).median()
            a.name = 'imp_' + impv
            # fill any thing that may still be missing
            merged = merged.join(a, on = by_var)
            merged['imp_' + impv].fillna(Filler, inplace = True)
    return merged   
    
    
def get_features(dataframe):
    """ Returns a list of column names representing all features in dataframe. Features are prefixed with f_ """
    features = []
    for col in dataframe.columns:
        if col[0:2] == 'f_':
            features.append(col)
    return features
    
def applyVectorizer(vectorizer, to_data, corpus_var): 
    """
    Add vectorized features to target dataframe using a trained vectorizer
     
    vectorizer: a trained vectorizer
    to_data: a target dataframe
    corpus_var: string for the column in to_data referring to the corpus
    """
    data = vectorizer.transform(to_data[corpus_var]).toarray()
    feature_list = vectorizer.get_feature_names()
    df = pd.DataFrame(data = data, columns = feature_list, index = to_data.index)
    new_data = to_data.copy()
    for feature in feature_list:
        new_data['f_' + str(feature)] = df[feature]
    return new_data
    
    
def round_array(array, precision):
    new_array = []
    for n in array:
        correction = 0.5 if n >= 0 else -0.5
        new_array.append(int(n/precision + correction)*precision) 
    return new_array
    
def rescale(array, min_prime, max_prime):
    new_array = []
    min_ori = min(array)
    max_ori = max(array) 
   
    for val in array:
        item =  (max_prime - min_prime) / (max_ori - min_ori) * (val - min_ori) + min_prime    
        new_array.append(item)
    return new_array
    
