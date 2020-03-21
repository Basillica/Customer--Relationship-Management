# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trial.db'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

###############################################################################
##################################### INDEX ###################################
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        lead = Lead(name=request.form['name'], company = request.form['company'],
                phone=request.form['phone'], email=request.form['email'],
                touch=Touch(description=request.form['description']))
        try:
            db.session.add(lead)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your shit'
    else:
        lead = Lead.query.order_by(Lead.id).all()
        return render_template('index.html', lead=lead)


@app.route('/add_task', methods=['POST', 'GET'])
def add_task():
    if request.method == 'POST':
        task = Lead(name=request.form['name'], company = request.form['company'],
                phone=request.form['phone'], email=request.form['email'],
                touch=Touch(description=request.form['description']))
        try:
            db.session.add(task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task!'
    else:
        task = Lead.query.order_by(Lead.id).all()
        return render_template('add_task.html', task=task)


@app.route('/delete/<int:id>')
def delete(id):
    lead_to_delete = Lead.query.get_or_404(id)
    touch_to_delete = Touch.query.filter_by(id=id).first()
    try:
        db.session.delete(touch_to_delete)
        db.session.delete(lead_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that lead'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Lead.query.get_or_404(id)

    if request.method == 'POST':
        oldId = request.form.get("oldId")
        task = Lead.query.filter_by(id=oldId).first()
        task.name = request.form['name']
        task.company = request.form['company']
        task.phone = request.form['phone']
        task.email = request.form['email']
        task.touch = Touch(description=request.form['description'])
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)

###############################################################################
################################## LEADS ######################################
@app.route('/leads' , methods=['POST', 'GET'])
def leads():
    if request.method == 'POST':
        data = Lead(name=request.form['name'], company = request.form['company'],
                phone=request.form['phone'], email=request.form['email'],
                touch=Touch(description=request.form['description']))
        try:
            db.session.add(data)
            db.session.commit()
            return redirect('/leads')
        except:
            return 'There was an issue adding your lead'
    else:
        lead = Lead.query.order_by(Lead.id).all()
        return render_template('lead.html', lead=lead)


@app.route('/add_lead', methods=['POST', 'GET'])
def add_lead():
    if request.method == 'POST':
        tc = Touch(description='')
        lead = Lead(name=request.form['name'], company = request.form['company'],
                phone=request.form['phone'], email=request.form['email'],
                touch=tc)
        try:
            db.session.add(lead)
            db.session.commit()
            return redirect('/leads')
        except:
            return 'There was an issue adding your lead!'
    else:
        lead = Lead.query.order_by(Lead.id).all()
        return render_template('add_lead.html', lead=lead)


@app.route('/delete_lead/<int:id>')
def delete_lead(id):
    lead_to_delete = Lead.query.get_or_404(id)
    touch_to_delete = Touch.query.filter_by(id=id).first()
    try:
        db.session.delete(lead_to_delete)
        db.session.delete(touch_to_delete)
        db.session.commit()
        return redirect('/leads')
    except:
        return 'There was a problem deleting that lead'


@app.route('/update_leads/<int:id>', methods=['GET', 'POST'])
def update_lead(id):
    lead = Lead.query.get_or_404(id)

    if request.method == 'POST':
        oldId = request.form.get("oldId")
        lead = Lead.query.filter_by(id=oldId).first()
        lead.name = request.form['name']
        lead.company = request.form['company']
        lead.phone = request.form['phone']
        lead.email = request.form['email']
        try:
            db.session.commit()
            return redirect('/leads')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update_lead.html', lead=lead)

###########################################################################
########################### TOUCHES #######################################
@app.route('/touches', methods=['POST', 'GET'])
def touches():
    if request.method == 'POST':
        data = Touch(description = request.form['description'])
        lead = Lead(name='', company = '', phone = '',
                email='',touch=data)
        try:
            db.session.add(data)
            db.session.commit()
            return redirect('/touches')
        except:
            return 'There was an issue adding your task'
    else:
        touch = Touch.query.order_by(Touch.id).all()
        return render_template('touch.html', touch=touch)


@app.route('/add_touch', methods=['POST', 'GET'])
def add_touch():
    if request.method == 'POST':
        tc = Touch(description = request.form['description'])
        lead = Lead(name='', company = '', phone = '',
                email='', touch=tc)
        try:
            db.session.add(lead)
            db.session.commit()
            return redirect('/touches')
        except:
            return 'There was an issue adding your touch!'
    else:
        lead = Lead.query.order_by(Lead.id).all()
        return render_template('add_touch.html', lead=lead)



@app.route('/delete_touch/<int:id>')
def delete_touch(id):
    touch_to_delete = Touch.query.get_or_404(id)
    lead_to_delete = Lead.query.filter_by(id=id).first()
    try:
        db.session.delete(touch_to_delete)
        db.session.delete(lead_to_delete)
        db.session.commit()
        return redirect('/touches')
    except:
        return 'There was a problem deleting that touch'


@app.route('/update_touch/<int:id>', methods=['GET', 'POST'])
def update_touch(id):
    touch = Touch.query.get_or_404(id)

    if request.method == 'POST':
        oldId = request.form.get("oldId")
        touch = Touch.query.filter_by(id=oldId).first()
        touch.description = request.form['description']
        try:
            db.session.commit()
            return redirect('/touches')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update_touch.html', touch=touch)


#############################################################
######################## MODELS #############################
class Lead(db.Model):
    __tablename__ = 'lead'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    touch_id = db.Column(db.Integer, db.ForeignKey('touch.id'), nullable=False,
            autoincrement = True)
    touch = db.relationship('Touch', cascade="all,delete", backref = db.backref('touches'), lazy=True)

    def __repr__(self):
        return '<Lead model {}>'.format(self.id)


class Touch(db.Model):
    __tablename__ = 'touch'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    description = db.Column(db.String(100))
    date = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)

    def __repr__(self):
        return '<Touch model {}>'.format(self.id)
###############################################################


if __name__ == '__main__':
    app.run(debug=True)
