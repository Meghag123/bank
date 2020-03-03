from flask import render_template,flash,redirect,url_for
from app_package import app,db,mongo
from flask_login import current_user,login_user,logout_user,login_required
from app_package.forms import LoginForm,RegistrationForm,AddCustomerForm,DeleteCustomerForm,DisplayForm,DepositForm,WithDrawForm
from app_package.models import User


check=True
cust_id=0
@app.route("/" ,methods=["GET" , "POST"])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("menu"))
    else:
        form=LoginForm()
        if form.validate_on_submit():
            user=User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash("Invalid user")
                return redirect(url_for("index"))
            else:
                login_user(user,remember=form.remember_me.data)
                return redirect(url_for("menu"))
        else: 
            return render_template("login.html",form=form)
       
@app.route("/register",methods=["GET","POST"])
def register():
        form=RegistrationForm() 
        if form.validate_on_submit():
            user=User(username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("User registered.You may login now")
            return redirect(url_for("index"))
        else:
            return render_template ("register.html",form=form)
            
@app.route("/menu")
@login_required
def menu():
    return render_template("menu.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
 
        
@app.route("/add_customer",methods=["GET","POST"])  
@login_required
def add_customer():
    global cust_id
    global check
    form=AddCustomerForm()
    if form.validate_on_submit():
        fields=["_id","cname","caccno","caadhar","cmobile","ctype","cbalance"]
        cust_col=mongo.db.customers
        if check:
                check=False
                if cust_col.count()==0:
                    cust_id=0
                else:
                    cust=cust_col.find().sort("_id",-1).limit(1)
                    tmp=cust.next()
                    cust_id=tmp["_id"]
        cust_id+=1
        values=[cust_id,form.cname.data,form.caccno.data,form.caadhar.data,form.cmobile.data,form.ctype.data,form.cbalance.data]
        customer=dict(zip(fields,values))
        cust_col=mongo.db.customers
        query={"caccno":form.caccno.data}
        customers=cust_col.find_one(query)
        if not bool(customers) :
            if form.ctype.data=='ordinary' and form.cbalance.data>=10000 or form.ctype.data=='priority' and form.cbalance.data>=50000:
                temp=cust_col.insert_one(customer)
                if temp.inserted_id==cust_id:
                    flash("user added")
                    return redirect(url_for("menu"))
            
            else:
                flash("Type and Amount does not matches........")
                return redirect(url_for("add_customer"))
        else:
            flash("Account number already exists ")
            return redirect(url_for("add_customer"))
    else:
        return render_template("add_customer.html",form=form)

              
              
@app.route("/display_customer",methods=["GET","POST"])
@login_required
def display_customers():    
    form=DisplayForm()
    if form.validate_on_submit():
        cust_col=mongo.db.customers
        query={"caccno":form.caccno.data}
        customers=cust_col.find_one(query)
        if bool(customers):
            return render_template("display.html",customers=customers,form=form)
        else:
            flash("Account dosen't exist")
            return redirect(url_for("menu"))      
    else:
        return render_template("display_customer.html",form=form)
        
    
    
@app.route("/deposit",methods=["GET","POST"])
@login_required
def deposit():
    form=DepositForm()
    if form.validate_on_submit():
        cust_col=mongo.db.customers
        query={"caccno":form.caccno.data}
        cust=cust_col.find_one(query)
        if bool(cust):
            bal=cust["cbalance"]
            new_bal=int(bal)+int(form.amt.data)
            new_val={"$set":{"cbalance":new_bal}}
            cust_col.update_one(query,new_val)
            flash("Amount Deposited")
            return render_template("menu.html",form=form) 
        else:
            flash("Account dosen't exist")
            return redirect(url_for("menu"))
    else:
        return render_template("deposit.html",form=form)  
        
        
        
@app.route("/withdraw",methods=["GET","POST"])
def withdraw():
    form=WithDrawForm()
    if form.validate_on_submit():
        cust_col=mongo.db.customers
        query={"caccno":form.caccno.data}
        cust=cust_col.find_one(query)
        if bool(cust):
            bal=cust["cbalance"]
            atype=cust["ctype"]
            new_bal=bal-form.amt.data
            if atype=="priority" and new_bal<50000 or atype=="ordinary" and new_bal<10000:
                flash("upon withdrawal min balance is not maintained")
                return redirect(url_for("menu"))
            else:
                new_data={"$set":{"cbalance":new_bal}}
                cust_col.update_one(query,new_data)      
                flash("Withdrawal done")
                return redirect(url_for("menu"))
        else:
            flash("Account dosen't exist")
            return render_template("menu.html",form=form)
        
    else:
        return render_template("withdraw.html",form=form)
        
        
@app.route("/delete_customer",methods=["GET","POST"])
@login_required  
def delete_customer():
    form=DeleteCustomerForm()
    #redirect(url_for("confirmdelete.html"))
    if form.validate_on_submit():
        cust_col=mongo.db.customers
        query={"caccno":form.caccno.data}
        customers=cust_col.find({"caccno":form.caccno.data})
        acc=cust_col.find_one(query)
        if bool(acc):
            return render_template("confirm_delete.html",customers=customers,form=form)
        else:
            flash("Account dosen't exist")
            return render_template("delete_customer.html",form=form)
    else:
        return render_template("delete_customer.html",form=form)

@app.route("/confirm_delete",methods=["GET","POST"])
@login_required  
def confirm_delete():
    form=DeleteCustomerForm()
    cust_col=mongo.db.customers
    query={"caccno":form.caccno.data} 
    cust_col.delete_one(query)
    flash("Customer Deleted")
    return redirect(url_for("menu"))
    
    
    
    
@app.route("/display_all_customers",methods=["GET","POST"])
@login_required
def display_all_customers():    
    cust_col=mongo.db.customers
    customers=cust_col.find()
    return render_template("display_all_customers.html",customers=customers) 
        
       
              
              

                


