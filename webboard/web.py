import os ,json
from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)

@app.route('/')
def index():
    with open('webboard_db.json')as k:
        all_data = json.load(k)
    return render_template('show.html',data = all_data)
    
@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/insert',methods=["POST"])
def insert():
    if request.method == "POST":
        id_topic = request.form["id_topic"]
        topic = request.form["topic"]
        detail = request.form["detail"]
    with open('webboard_db.json')as k:
        all_data = json.load(k)
    new_data ={
        "id_topic" : id_topic,
        "topic" : topic,
        "detail" : detail
    }
    all_data.append(new_data)
    with open('webboard_db.json','w')as k:
        k.write((json.dumps(all_data)))
    return redirect('/')

@app.route('/show_comment/<id_topic>')
def show_comment(id_topic):
    with open('webboard_db.json')as k:  # select topic form webboard_db.json
        all_data = json.load(k)
    select_data = {}
    for row in all_data:
        if row["id_topic"] == id_topic:
            select_data["id_topic"] = row["id_topic"]
            select_data["topic"] = row["topic"]
            select_data["detail"] = row["detail"]
    with open('comment_db.json')as k:
        comment_db = json.load(k)
    
    comment_data = []
    for row in comment_db:          # select row from comment_db.json that have key = id_topic
        if row["id_topic"] == id_topic:
            comment_data.append(row)
                                    # send 2 variables to show_comment.html
                                    
    return render_template('show_comment.html',select_data = select_data,comment_data = comment_data)

@app.route('/delete/<id_topic>')
def delete(id_topic):
    with open('webboard_db.json')as k:
        all_data = json.load(k)
    new_data = []
    for row in all_data:
        if row["id_topic"] != id_topic:
            new_data.append(row)
    #print("new_data is",new_data)
    
    with open('webboard_db.json','w')as k:
        k.write((json.dumps(new_data)))
    return redirect('/')
    
@app.route('/editpage/<id_topic>')
def editpage(id_topic):
    
    with open('webboard_db.json')as k:
        all_data = json.load(k)
        
    edit_data = {}
    for row in all_data:
        if row["id_topic"] == id_topic:
            edit_data["id_topic"] = row["id_topic"]
            edit_data["topic"] = row["topic"]
            edit_data["detail"] = row["detail"]
        #print("edit data is",edit_data)
    
    return render_template('editpage.html',edit_data=edit_data)
    
@app.route('/edit',methods=["POST"])
def edit():
    if request.method == "POST":
        id_topic = request.form["id_topic"]
        topic = request.form["topic"]
        detail = request.form["detail"]
    
    with open('webboard_db.json')as k:
        all_data = json.load(k)
    print("all_data ",all_data)
    
    for row in all_data:
        if row["id_topic"] == id_topic:
            row["topic"] = topic
            row["detail"] = detail
    
    with open('webboard_db.json','w')as k:
        k.write((json.dumps(all_data)))
    return redirect('/')
    
@app.route('/insert_comment',methods=["POST"])
def insert_comment():
    if request.method == "POST":
        id_topic = request.form["id_topic"]   # get id_topic from show_comment.html
        comment = request.form["comment"]
    
    with open('comment_db.json')as k:
        all_data = json.load(k)
                                # generate the id_latest for build new row in comment_db.json
    if len(all_data) == 0 :
        id_latest ="1"
    else :
        last_row = all_data[len(all_data)-1]
        id_latest = int(last_row["id_comment"]) +1
        id_latest = str(id_latest)
                            # end generate the id_latest
    new_data ={
        "id_comment" : id_latest, # primary key use for edit comment only
        "id_topic" : id_topic,    # use for link with webboard_db.json  -
        "comment" : comment       # call every row if  They have the same topic
    }
    all_data.append(new_data)
    with open('comment_db.json','w')as k:
        k.write((json.dumps(all_data)))
        
    return redirect('/show_comment/'+id_topic)
    
@app.route('/edit_comment/<id_comment>')
def edit_comment(id_comment):
    with open('comment_db.json')as k:
        comment_all_data = json.load(k)

    for row in comment_all_data:
        if row["id_comment"] == id_comment:
            edit_comment_data = row

    return render_template('edit_comment_page.html',edit_comment_data=edit_comment_data)

@app.route('/edit_comment2',methods=["POST"])
def edit_comment2():
    if request.method == "POST":
        id_comment = request.form["id_comment"]
        update_id_topic = request.form["id_topic"]
        update_comment = request.form["comment"]
    
    with open('comment_db.json')as k:
        all_comment_data = json.load(k)
    for row in all_comment_data:
        if row["id_comment"]== id_comment:
            row["id_topic"] = update_id_topic
            row["comment"] = update_comment
    #print("all_comment_data",all_comment_data)
    
    with open('comment_db.json','w')as k:
        k.write((json.dumps(all_comment_data)))
    return redirect('/show_comment/'+update_id_topic)

@app.route('/delete_comment/<id_comment>/<id_topic>')
def delete_comment(id_comment,id_topic):
    print("id_comment is",id_comment)
    print("id_topic is",id_topic)
    with open('comment_db.json')as k:
        all_comment_data = json.load(k)
    new_comment_data = []
    for row in all_comment_data:
        if row["id_comment"] != id_comment:
            new_comment_data.append(row)
    
    for x in new_comment_data:
        print(x)
    
    with open('comment_db.json','w')as k:
        k.write((json.dumps(new_comment_data)))
    
    return redirect('/show_comment/'+id_topic)
if __name__ == "__main__":
    app.debug = True
    host = os.getenv('IP','0.0.0.0')
    port = os.getenv('PORT','8080')
    app.run(host=host, port=port)