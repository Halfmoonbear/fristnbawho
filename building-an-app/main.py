from flask import Flask, render_template, request
import pandas as pd

def highnba(b):
    a = 1.27*b-31.75
    return a

def rank(albat):
    if albat == 'A':
        return 100
    elif albat == 'B':
        return 80
    elif albat == 'C':
        return 60
    elif albat == 'D':
        return 40
    elif albat =='E':
        return 20

def calculation(h1,s1,s2,s3,s4,s5,s6):
    #1 나의키 nba키로 변환
    hight = int(h1)
    hightnba = round(highnba(hight))
    if hightnba<=160:
        hightnba=161
    if hightnba>=232:
        hightnba=231
    hightnba_range = [hightnba-1,hightnba,hightnba+1]


    #2 능력치등급을 수치로 변환
    cls = rank(s1)
    med = rank(s2)
    Tpt = rank(s3)
    finish = rank(s4)
    technic = rank(s5)
    defense = rank(s6)


    #3 전체nba데이터에서 비슷한 키 데이터 찾기
    nba_df = pd.read_csv(r'static\NBA_DATA.csv')
    Data_one = pd.DataFrame()
    for a in hightnba_range:
        a = nba_df[ a == nba_df['Height']]
        Data_one = Data_one.append(a)
        # Data_one = pd.concat([Data_one,a])
        # Data_one = pd.merge(Data_one,a)
    Data_one=Data_one.reset_index()
    degree_list = list()
    for a in range(0,len(Data_one)):
        st1 = cls-int(Data_one.loc[a,['Cls']])
        st2 = med-int(Data_one.loc[a,['Med']])
        st3 = Tpt-int(Data_one.loc[a,['3PT']])
        st4 = finish-int(Data_one.loc[a,['Finish']])
        st5 = technic-int(Data_one.loc[a,['Technic']])
        st6 = defense-int(Data_one.loc[a,['Defense']])
        persent = (600-abs(st1)-abs(st2)-abs(st3)-abs(st4)-abs(st5)-abs(st6))/6
        degree_list.append(round(persent,1))
    Data_one.insert(0,'Degree',degree_list)
    Data_one=Data_one.reset_index()
    Data_one.sort_values(by=['Degree','Ovr'],axis=0,ascending= [False,True],inplace=True)
    Data_one=Data_one.drop_duplicates(['Name'],keep="first")
    Data_fin = Data_one.iloc[0:10]
    # html = Data_fin.to_html(index=False, justify='center',classes='data')
    final_list = Data_fin.to_dict('r')
    return final_list

app = Flask(__name__)
app.debug = True #디버그 모드 온

@app.route("/")
def index():
    return render_template('home_fianl.html')

@app.route("/claculate", methods =['post'])
def rood():
    Hight = request.form['Hight']
    Cls = request.form['Cls']
    Med = request.form['Med']
    Tpt = request.form['Tpt']
    finish = request.form['finish']
    technic = request.form['technic']
    defence = request.form['defence']
    
    output = calculation(Hight,Cls,Med,Tpt,finish,technic,defence)
    indexnum= len(output)
    return render_template('output_final.html', op=output, num = indexnum)
