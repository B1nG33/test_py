# coding: utf-8

import re
import os
import sys
import time
import copy
import math

nDim = 3


# 根据输入的原始坐标与姿态以及新时刻的坐标与姿态，输出新时刻的点参数
def RotateModel():
    return 


def MoveRotateXYZ(pit=[], move=[], alfa=0.0, beta=0.0, gama=0.0, alfa1=0.0, beta1=0.0, gama1=0.0):
    tpit= [0.0, 0.0, 0.0]
    # 当前欧拉角alpha，beta，gamma
    # 目标欧拉角alpha_new,beta_new,gamma_new
    # 采用两次变换方法
    # 欧拉角顺序ZYX（内旋） 旋转矩阵=Rz*Ry*Rx
    # 表示先按照计算X矩阵 然后y 然后Z
    # 所以变换回去的次序是 先z 后y 后x
    
    # 绕Z转-gama
    tpit[0] = math.cos(gama)*pit[0]-math.sin(gama)*pit[1]
    tpit[1] = math.sin(gama)*pit[0]+math.cos(gama)*pit[1]
    tpit[2] = pit[2]

    # 绕Y转-beta
    pit[0] = math.cos(beta)*tpit[0]-math.sin(beta)*tpit[2]
    pit[1] = tpit[1]
    pit[2] = math.sin(beta)*tpit[0]+math.cos(beta)*tpit[2]
    

    # 绕X转-alfa
    tpit[0] = pit[0]
    tpit[1] = math.cos(alfa)*pit[1]-math.sin(alfa)*pit[2]
    tpit[2] = math.sin(alfa)*pit[1]+math.cos(alfa)*pit[2]

    for i in range(3):
        pit[i] = tpit[i]
    # 从当前欧拉角为0变换到欧拉角alfa1,beta1,gama1
    # 欧拉角顺序ZYX（内旋） 旋转矩阵=Rz*Ry*Rx
    # 表示先按照计算X矩阵 然后y 然后Z
    
    # 绕X转alpha
    tpit[0] = pit[0]
    tpit[1] = math.cos(alfa1)*pit[1]+math.sin(alfa1)*pit[2]
    tpit[2] = -math.sin(alfa1)*pit[1]+math.cos(alfa1)*pit[2]
    
    # 绕Y转beta
    pit[0] = math.cos(beta1)*tpit[0]+math.sin(beta1)*tpit[2]
    pit[1] = tpit[1]
    pit[2] = -math.sin(beta1)*tpit[0]+math.cos(beta1)*tpit[2]

    # 绕Z转gama
    tpit[0] = math.cos(gama1)*pit[0]+math.sin(gama1)*pit[1]
    tpit[1] = -math.sin(gama1)*pit[0]+math.cos(gama1)*pit[1]
    tpit[2] = pit[2]
    
    for i in range(3):
        pit[i] = tpit[i]
    
    for i in range(3):
        pit[i] = pit[i]+move[i]
    
    return 


def WriteTrajectCourse(filename="trajectEvolution.plt", nPart=1, N=[], E=[], PtInfo=[], linkInfo=[], posIni=[], angIni=[], posEvo=[], angEvo=[], timeLst=[], iteNumLst=[], title_line=[], variable_line=[], zone_lines=[], isMove=[]):
    
    # 新的点坐标信息
    PtInfoNew = copy.deepcopy(PtInfo)
    
    # 打印文件头
    print("start WriteTrajectCourse")
    traCourseF = open(filename,'w')
    
    # title
    for iLine in title_line:
        traCourseF.write(iLine)
        
    # varialbe
    for iLine in variable_line:
        traCourseF.write(iLine)
    
    print(iteNumLst)
    
    # 将linkInfo处理为数组
    linkInfo_ptr = [[[]for iCell in range(E[iPart])] for iPart in range(nPart)]
    for iPart in range(nPart):
        for iCell in range(E[iPart]):
            linkLine = linkInfo[iPart][iCell]
            subPtIndexStr = [int(i) for i in re.split('\s+',linkLine) if i not in (' ', '')]#使用空格划分行
            linkInfo_ptr[iPart][iCell].extend(subPtIndexStr)
    
    nIte = len(iteNumLst)
    for iIte in  range(nIte):
        iteStr='''ite%d_%f_'''%(iIte,timeLst[iIte])
        for iPart in range(nPart):
            if((iIte != 0) and (iPart not in isMove)):
                continue
            partStr='''p%d'''%(iPart)
            zoneStr_T = '"'+iteStr + partStr+'"'
            
            zoneOriginline = zone_lines[iPart]
            
            zoneNewline = re.sub(r'".*"', zoneStr_T, zoneOriginline, 1)
            traCourseF.write(zoneNewline)
            
            #对于每个部件，每个点，计算新坐标
            ptOldCord = [0.0, 0.0, 0.0]
            ptNewCord = [0.0, 0.0, 0.0]
            mrsp = [0.0, 0.0, 0.0]
            partOldPos = [ posIni[iPart][iDim] for iDim in range(nDim)]
            partNewPos = [ posEvo[iPart][iDim][iIte] for iDim in range(nDim)]
            partOldAng = [ angIni[iPart][0], angIni[iPart][1],angIni[iPart][2]]
            partNewAng = [ angEvo[iPart][0][iIte], angEvo[iPart][1][iIte],angEvo[iPart][2][iIte]]
            
            for iPoint in range(N[iPart]):
                ptOldCord[0] = PtInfo[iPart][0][iPoint]
                ptOldCord[1] = PtInfo[iPart][1][iPoint]
                ptOldCord[2] = PtInfo[iPart][2][iPoint]
                
                mrsp[0] = ptOldCord[0] - partOldPos[0]
                mrsp[1] = ptOldCord[1] - partOldPos[1]
                mrsp[2] = ptOldCord[2] - partOldPos[2]
                
                MoveRotateXYZ(mrsp, partNewPos, partOldAng[0], partOldAng[1], partOldAng[2], partNewAng[0], partNewAng[1], partNewAng[2])
                
                PtInfoNew[iPart][0][iPoint] = mrsp[0]
                PtInfoNew[iPart][1][iPoint] = mrsp[1]
                PtInfoNew[iPart][2][iPoint] = mrsp[2]
            
            # 处理完所有的点坐标之后，打印点
            iCol=0
            for iDim in range(nDim):
                iCol=0
                for iPoint in range(N[iPart]):
                    iCol+=1
                    traCourseF.write('''%e '''%(PtInfoNew[iPart][iDim][iPoint]))
                    if iCol==5 :
                        iCol = 0
                        traCourseF.write("\n")
                if iCol>0:
                    traCourseF.write("\n")
                        
            # 打印链接关系
            for iLine in linkInfo[iPart]:
                traCourseF.write(iLine)
        


if __name__=="__main__":

    _modelFile = 'initalModel.plt'
    _posEvoFile = 'posEvolution.txt'
    _angEvoFile = 'AngleEvolution.txt'
    _traEvoFile = 'trajectEvolution.plt'
    _motionFile = 'motion_config.txt'

    if len(sys.argv)>4:
        _traEvoFile = sys.argv[4]
    if len(sys.argv)>3:
        _angEvoFile = sys.argv[3]
    if len(sys.argv)>2:
        _posEvoFile = sys.argv[2]
    if len(sys.argv)>1:
        _modelFile = sys.argv[1]
    
    nPart = []
    N = []
    E = []
    PtInfo = []
    linkInfo = []
    posIni = []
    posEvo = []
    angIni = []
    angEvo = []
    title_line = []
    variable_line = []
    zone_lines = []
    timeLst= [] 
    iteNumLst = []
    isMove = [] #移动部件id


    print("nPart\n", nPart)
    print("N\n", N)
    print("E\n", E)
    # print "PtInfo\n",PtInfo
    # print "linkInfo\n",linkInfo
    
    WriteTrajectCourse(_traEvoFile, nPart=nPart[0], N=N, E=E, PtInfo=PtInfo, linkInfo=linkInfo, posIni=posIni,angIni=angIni, posEvo=posEvo, angEvo=angEvo, timeLst=timeLst, iteNumLst=iteNumLst, title_line=title_line, variable_line=variable_line, zone_lines=zone_lines, isMove=isMove)
    

