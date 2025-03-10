import numpy as np

def calcMAE(valores_reales, valores_estimados):#error absoluto medio (MAE)
    #Mide el error medio en las mismas uidades que los aos reales. Mas bajo es mejor
    MAE = np.mean(np.abs(valores_reales - valores_estimados))
    return MAE


def calcMSE(valores_reales, valores_estimados): #Error Cuadratico Medio (MSE) 
    #Penaliza mas a los errores grandes
    MSE = np.mean((valores_reales - valores_estimados) ** 2)
    return MSE


def calcRMSE(valores_reales, valores_estimados): #Raiz dek errir cuadratico medio (RMSE)
    #Penaliza mas a Los errores grandes. Pone al error en las mismas unidades que loos datos reales
    MSE = calcMSE(valores_reales, valores_estimados)
    RMSE = np.sqrt(MSE)
    return RMSE


def calcMAPE(valores_reales, valores_estimados): #Error Porcentual Absoluto Medio (MAPE)
    #Mide el error en porcentaje. Facilita la iterpretacion en terminos relativos
    MAPE = np.mean(np.abs((valores_reales - valores_estimados)/ valores_reales)) * 100
    return MAPE