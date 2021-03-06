# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 14:59:41 2018

@author: chhabriv
"""

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns 
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder,LabelEncoder,StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split

def preprocess():
    # Importing the dataset
    dataset = pd.read_csv('../../dataset/movie_metadata.csv')
    
    dataset.info()
    
    #droping the columns which is not necessary
    dataset.drop(["color","actor_1_facebook_likes","actor_3_facebook_likes",
               "genres","actor_1_name","actor_2_name","movie_title","actor_3_name","facenumber_in_poster",
               "plot_keywords","title_year","movie_imdb_link","actor_2_facebook_likes","aspect_ratio","country","language","director_name"],axis=1,inplace=True)
    
    dataset.isna().sum()
    dataset.info()
    
    #Data imputation
    dataset.replace({"country":np.NaN,
                     #"director_name":np.NaN,
                  "language":np.NaN,
                 "content_rating":np.NaN},value="Missing",inplace=True)
    
    dataset['duration']=dataset['duration'].fillna(value=dataset['duration'].mean())
    dataset['num_user_for_reviews']=dataset['num_user_for_reviews'].fillna(value=dataset['num_user_for_reviews'].mean())
    dataset['budget']=dataset['budget'].fillna(value=dataset['budget'].mean())
    dataset['gross']=dataset['gross'].fillna(value=dataset['gross'].mean())
    dataset['director_facebook_likes']=dataset['director_facebook_likes'].fillna(value=0)
    dataset['num_critic_for_reviews']=dataset['num_critic_for_reviews'].fillna(value=0)
    
    #remove duplicates
    dataset.drop_duplicates(subset=None, keep='first',inplace=True)
    
    dataset.isna().sum()
    dataset.info()
    
    #plotting heat map to visualize correlation:
    plt.figure(figsize=(18,8),dpi=100,)
    plt.subplots(figsize=(18,8))
    sns.heatmap(data=dataset.corr(),square=True,vmax=0.8,annot=True)
    
    datasetEdit=dataset
    
    #encode categorical values
    encode=LabelEncoder()
    #datasetEdit['director_name'] = encode.fit_transform(datasetEdit['director_name'] ) 
    #datasetEdit['language'] = encode.fit_transform(datasetEdit['language'] ) 
    #datasetEdit['country'] = encode.fit_transform(datasetEdit['country'] ) 
    datasetEdit['content_rating'] = encode.fit_transform(datasetEdit['content_rating'] ) 
    
    #creating labels based on IMDB score
    datasetEdit['verdict']=pd.cut(datasetEdit['imdb_score'],bins=[0,7,8,8.5,9,10],labels=["poor","average","good","very good","excellent"],right=False)
    datasetEdit['verdict'].value_counts() # Distribution of classes after split
    datasetEdit['verdict'] = encode.fit_transform(datasetEdit['verdict'] ) 
    
    #results=pd.DataFrame(columns=["Random Forest Train","Random Forest Validate","Random Forest Test","Logistic Train","Logistic Validate","Logistic Test","SVC Train","SVC Validate","SVC Test"])
    results=pd.DataFrame(columns=["Random Forest Accuracy","Random Forest Precision","Random Forest F1 Score",
                                  "Logistic Accuracy","Logistic Precision","Logistic F1 Score",
                                  "SVC Accuracy","SVC Precision","SVC F1 Score"]) #Dataframe for each result
    
    prePruneCount=datasetEdit.shape[0]
    print('Dataset size before pruning: ',prePruneCount)
    return datasetEdit,results
#incrementally prune
#for prune in range(1,11):
#    
#    resultList=[]
#    print("For data pruning with ",prune)
#    #Pruning based on review count < 10
#    datasetEdit=datasetEdit.drop(datasetEdit[(datasetEdit['num_user_for_reviews']<prune)].index).reset_index(drop=True)
#    #datasetEdit.info()
#    
#    #Setting predictors and target variables
#    X = datasetEdit.iloc[:, np.r_[0:9,10]].values
#    y = datasetEdit.iloc[:, -1].values
#    
#    #split categorical labeled data into columns
#    onehotencoder=OneHotEncoder(categorical_features= [0])
#    X=onehotencoder.fit_transform(X).toarray()
#    
#    #Split to train, validate, test
#    from sklearn.model_selection import train_test_split
#    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=19)
#    #X_train,X_validate,y_train,y_validate=train_test_split(X_train,y_train,test_size=0.15,random_state=19)
#    
#    #Normalising the features
#    scaler=StandardScaler()
#    X_train=scaler.fit_transform(X_train)
#    X_test=scaler.transform(X_test)
#    
#    # ============================================================================= 
#    # # # Fitting Random Forest Regression to the dataset
#    # from sklearn.linear_model import LinearRegression
#    # regressor = LinearRegression()
#    # regressor.fit(X_train, y_train)
#    # 
#    # print('RMSE:')
#    # print(np.sqrt(metrics.mean_squared_error(y_test, regressor.predict(X_test))))
#    # print ('')
#    # =============================================================================
#    
#    """
#    # Fitting Random Forest Regression to the dataset
#    from sklearn.ensemble import RandomForestRegressor
#    regressor = RandomForestRegressor(n_estimators = 10, random_state = 0)
#    regressor.fit(X_train, y_train)
#     
#    #prediction
#    predict=regressor.predict(X_test)
#    print('Regressor Score',regressor.score(X_test,y_test))
#    
#    print('RMSE:')
#    print(np.sqrt(metrics.mean_squared_error(y_test, regressor.predict(X_test))))
#    print ('')
#    """
#    from sklearn.ensemble import RandomForestClassifier
#    #for num in range(10,100,10):
#    regressor = RandomForestClassifier(n_estimators = 40, random_state = 19)
#    regressor.fit(X_train, y_train)
#     
#    #prediction
#    #predict_train_R=regressor.predict(X_train)
#    #predict_val_R=regressor.predict(X_validate)
#    predict_test_R=regressor.predict(X_test)
#    #resultList.append(accuracy_score(y_train,predict_train_R)*100)
#    #resultList.append(accuracy_score(y_validate,predict_val_R)*100)
#    #print(accuracy_score(y_test,predict_test_R)*100)
#    resultList.append(accuracy_score(y_test,predict_test_R)*100)
#    resultList.append(metrics.precision_score(y_test,predict_test_R,average='weighted')*100)
#    resultList.append(metrics.f1_score(y_test,predict_test_R,average='weighted')*100)
#    
#    from sklearn.linear_model import LogisticRegression  
#    logistic = LogisticRegression()
#    logistic.fit(X_train,y_train)
#    #predict_train_L=logistic.predict(X_train)
#    #predict_val_L=logistic.predict(X_validate)
#    predict_test_L=logistic.predict(X_test)
#    #resultList.append(accuracy_score(y_train,predict_train_L)*100)
#    #resultList.append(accuracy_score(y_validate,predict_val_L)*100)
#    #print(accuracy_score(y_test,predict_test_L)*100)
#    resultList.append(accuracy_score(y_test,predict_test_L)*100)
#    resultList.append(metrics.precision_score(y_test,predict_test_L,average='weighted')*100)
#    resultList.append(metrics.f1_score(y_test,predict_test_L,average='weighted')*100)
#
#    from sklearn.svm import SVC 
#    C_param_range = [0.001, 0.01, 0.1, 10, 25, 50, 100, 1000]
#    for i in C_param_range:
#        svc = SVC(C=i)
#        svc.fit(X_train,y_train)
#        #predict_train_S=svc.predict(X_train)
#        #predict_val_S=svc.predict(X_validate)
#        predict_test_S=svc.predict(X_test)
#        #resultList.append(accuracy_score(y_train,predict_train_S)*100)
#        #resultList.append(accuracy_score(y_validate,predict_val_S)*100)
#        print(accuracy_score(y_test,predict_test_S)*100)
#    resultList.append(accuracy_score(y_test,predict_test_S)*100)
#    resultList.append(metrics.precision_score(y_test,predict_test_S,average='weighted')*100)
#    resultList.append(metrics.f1_score(y_test,predict_test_S,average='weighted')*100)
#
#    #results=results.append(pd.Series(resultList,index=["Random Forest Train","Random Forest Validate","Random Forest Test","Logistic Train","Logistic Validate","Logistic Test","SVC Train","SVC Validate","SVC Test"]),ignore_index=True)
#    results=results.append(pd.Series(resultList,index=["Random Forest Accuracy","Random Forest Precision","Random Forest F1 Score",
#                                                       "Logistic Accuracy","Logistic Precision","Logistic F1 Score",
#                                                       "SVC Accuracy","SVC Precision","SVC F1 Score"]),ignore_index=True)
#    
#results.to_csv("Accuracy.csv")
#print(results)
#postPruneCount=datasetEdit.shape[0]
#totalRecordsPruned=(prePruneCount-postPruneCount)
#percRecordsPruned=totalRecordsPruned/prePruneCount
#print('Dataset size after pruning: ',postPruneCount)
#print('Dataset records pruned: ',totalRecordsPruned)
#print('% of dataset pruned: ',percRecordsPruned)

def doRFClassification(X_train,y_train,X_test,y_test):
    result = []
     
    #n_estimators=40 is giving the best result on unpruned data, hence we will use it for our further iterations
    #for num in range(10,110,10): 
    regressor = RandomForestClassifier(n_estimators = 40, random_state = 19)
    regressor.fit(X_train, y_train)
    predict_test_R=regressor.predict(X_test)
    result.append(accuracy_score(y_test,predict_test_R)*100)
    #print(accuracy_score(y_test,predict_test_R)*100)
    result.append(metrics.precision_score(y_test,predict_test_R,average='weighted')*100)
   # print(metrics.precision_score(y_test,predict_test_R,average='weighted')*100)
    result.append(metrics.f1_score(y_test,predict_test_R,average='weighted')*100)
   # print(metrics.f1_score(y_test,predict_test_R,average='weighted')*100)
   # print(result)
    return result


def doLogisticClassification(X_train,y_train,X_test,y_test):
    result = []
    
    #C=1 is giving the best result on unpruned data, hence we will use it for our further iterations
    
    logistic = LogisticRegression(C=1)
    logistic.fit(X_train,y_train)
    #predict_train_L=logistic.predict(X_train)
    #predict_val_L=logistic.predict(X_validate)
    predict_test_L=logistic.predict(X_test)
    #resultList.append(accuracy_score(y_train,predict_train_L)*100)
    #resultList.append(accuracy_score(y_validate,predict_val_L)*100)
    #print(accuracy_score(y_test,predict_test_L)*100)
    result.append(accuracy_score(y_test,predict_test_L)*100)
    #print(accuracy_score(y_test,predict_test_L)*100)
    result.append(metrics.precision_score(y_test,predict_test_L,average='weighted')*100)
   # print(metrics.precision_score(y_test,predict_test_L,average='weighted')*100)
    result.append(metrics.f1_score(y_test,predict_test_L,average='weighted')*100)
    #print(metrics.f1_score(y_test,predict_test_L,average='weighted')*100)
    #print(result)
    return result

def doSVMClassification(X_train,y_train,X_test,y_test):
    result = []
    #C_param_range = [0.001, 0.01, 0.1,1, 10, 25, 50, 100, 1000]
    #for i in C_param_range:
    
    #C=0.1 is giving the best result on unpruned data, hence we will use it for our further iterations
    #for i in C_param_range:
    svc = SVC(C=0.1)
    svc.fit(X_train,y_train)
    #predict_train_S=svc.predict(X_train)
    #predict_val_S=svc.predict(X_validate)
    predict_test_S=svc.predict(X_test)
    #resultList.append(accuracy_score(y_train,predict_train_S)*100)
    #resultList.append(accuracy_score(y_validate,predict_val_S)*100)
    #print(accuracy_score(y_test,predict_test_S)*100)
    result.append(accuracy_score(y_test,predict_test_S)*100)
    #print(accuracy_score(y_test,predict_test_S)*100)
    result.append(metrics.precision_score(y_test,predict_test_S,average='weighted')*100)
    #print(metrics.precision_score(y_test,predict_test_S,average='weighted')*100)
    result.append(metrics.f1_score(y_test,predict_test_S,average='weighted')*100)
    #print(metrics.f1_score(y_test,predict_test_S,average='weighted')*100)
    #print(result)
    return result

def main():
    datasetEdit,results = preprocess()
    prePruneCount=datasetEdit.shape[0]
    for prune in range(1,2):
    
        resultList=[]
        #print("For data pruning with ",prune)
        #Pruning based on review count < 10
        datasetEdit=datasetEdit.drop(datasetEdit[(datasetEdit['num_user_for_reviews']<prune)].index).reset_index(drop=True)
        #datasetEdit.info()
        
        #Setting predictors and target variables
        X = datasetEdit.iloc[:, np.r_[0:9,10]].values
        y = datasetEdit.iloc[:, -1].values
        
        #split categorical labeled data into columns
        onehotencoder=OneHotEncoder(categorical_features= [0])
        X=onehotencoder.fit_transform(X).toarray()
        
        #Split to train, validate, test   
        
        X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=19)
        #X_train,X_validate,y_train,y_validate=train_test_split(X_train,y_train,test_size=0.15,random_state=19)
        
        #Normalising the features
        scaler=StandardScaler()
        X_train=scaler.fit_transform(X_train)
        X_test=scaler.transform(X_test)
        res1 = doRFClassification(X_train,y_train,X_test,y_test)
        #print('res1 --> ',res1)
        res2 = doLogisticClassification(X_train,y_train,X_test,y_test)
        #print('res2 --> ',res2)
        res3 = doSVMClassification(X_train,y_train,X_test,y_test)
        #print('res3 --> ',res3)
        res = np.hstack((res1,res2,res3))
        #print('res --> ',res)
        resultList.extend(res)
        
        #resultList.append(doLogisticClassification(X_train,y_train,X_test,y_test))
        #resultList.append(doSVMClassification(X_train,y_train,X_test,y_test))
        print(resultList)
        
        results=results.append(pd.Series(resultList,index=["Random Forest Accuracy","Random Forest Precision","Random Forest F1 Score",
                                                       "Logistic Accuracy","Logistic Precision","Logistic F1 Score",
                                                       "SVC Accuracy","SVC Precision","SVC F1 Score"]),ignore_index=True)
    results.to_csv("Accuracy_70-30.csv")
    print(results)
    postPruneCount=datasetEdit.shape[0]
    totalRecordsPruned=(prePruneCount-postPruneCount)
    percRecordsPruned=totalRecordsPruned/prePruneCount
    print('Dataset size after pruning: ',postPruneCount)
    print('Dataset records pruned: ',totalRecordsPruned)
    print('% of dataset pruned: ',percRecordsPruned)

if __name__== "__main__":
    main()