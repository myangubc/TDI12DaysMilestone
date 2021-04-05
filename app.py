from flask import Flask,render_template, request, redirect

app_lulu = Flask(__name__)
app_lulu.vars={}

app_lulu.questions={}
app_lulu.questions['How many eyes do you have?']=('1','2','3')
app_lulu.questions['Which fruit do you like best?']=('banana','mango','pineapple')
app_lulu.questions['Do you like cupcakes?']=('yes','no','maybe')

app_lulu.nquestions=len(app_lulu.questions)


@app_lulu.route("/index_lulu",methods=['GET','POST'])
def index_lulu():
    nquestions = 5
    if request.method == 'GET':
        return render_template('userinfo_lulu.html',num=nquestions)
    else:
        # request was a post
        app_lulu.vars['name'] = request.form['name_lulu']
        app_lulu.vars['age'] = request.form['age_lulu']

        f = open('%s_%s.txt'%(app_lulu.vars['name'],app_lulu.vars['age']),'w')
        f.write('Name:%s\n'%(app_lulu.vars['name']))
        f.write('Age:%s\n\n'%(app_lulu.vars['age']))
        f.close()

#        return render_template('layout_lulu.html',num=1,question='How many eyes do you have?',ans1='1',ans2='2',ans3='3') 
#        return 'request.method was not a GET!'
        return redirect('/main_lulu')
@app_lulu.route('/main_lulu')
def main_lulu():
    if len(app_lulu.questions)==0:
       return render_template('end_lulu.html')
    return redirect('/next_lulu')

@app_lulu.route('/next_lulu',methods=['GET'])
def next_lulu(): # function name does not need to be same with URL (next_lulu)
    n = app_lulu.nquestions - len(app_lulu.questions)+1
    q = list(app_lulu.questions.keys())[0]
    a1,a2,a3 = list(app_lulu.questions.values())[0]

    app_lulu.currentq = q
    return render_template('layout_lulu.html',num=n,question=q,ans1=a1,ans2=a2,ans3=a3)

@app_lulu.route('/next_lulu',methods=['POST'])
def next_lulu2(): # can't have two functions with same name
    f = open('%s_%s.txt'%(app_lulu.vars['name'],app_lulu.vars['age']),'a')
    f.write('%s\n'%(app_lulu.currentq))
    f.write('%s\n\n'%(request.form['answer_from_layout_lulu']))
    f.close()

    del app_lulu.questions[app_lulu.currentq]

    return redirect('/main_lulu')
    


if __name__ == "__main__":
     app_lulu.run(debug=True)
