from flask import Flask,render_template,request,make_response,session,redirect,url_for,logging,flash
from werkzeug.utils import secure_filename, send_from_directory
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from scripts.Dynamic import DynamicContent
from scripts.MongoDriver import MgDriver
from scripts.dependencies.Logs import Logs
from scripts.Access import UserAccess
from scripts.dependencies.DirectoryTreeGenerator_lite import TreeExplorer
from inspect import getframeinfo,currentframe





# update urls the first time the server is initiate
# content=TreeExplorer()
# content.ExploreDirectories(path="static/content",mode="relative")
files_manager=TreeExplorer()
files_manager.ExploreDirectories(ignore="venv")
for dirs in files_manager.Dir_List:
    print(dirs)

#---------DEPENDENCIES------------
# Loads log messages module
# Mongo Database module
# Loads dynamic_content module in order to sent data to the frontend 
# Loads Wtf form class 
# Loads admin authentification module
# def GetCurrentFile():

#     cf=currentframe()
#     currentfile=getframeinfo(cf).filename
#     start=currentfile.rfind("\\")+1
#     end=len(currentfile)
#     string=""
#     for char in range(start,end):

#         string=string+currentfile[char]

#     return string

# current_file=GetCurrentFile()
# access=UserAccess()
# logs=Logs()
# dynamic_content=DynamicContent(logs)
# app=Flask(__name__)
# app.secret_key=access.GetItem("app")

# class Registration(Form):
#     username=StringField("User",[validators.Length(min=4,max=255),validators.DataRequired()])
#     password=PasswordField("Password",[validators.Length(min=4,max=255),validators.DataRequired()])

#---------INITIALIZATION------------
# Checks the current amount of files in the folder content. Creates a registry and uploads it ot the database cloud 
# Creates the classes necesary to manege each table in the current database 
# If the table/database doesnt exist then is created

# blueprint=dynamic_content.UpdateBlueprint()
# Urls=MgDriver(logs,"FlaskPortfolioApp","Url","FlaskPortFolioUrls",blueprint)
# Registry=MgDriver(logs,"FlaskPortfolioApp","Registry",logs.GetDate(),"First Entry")
# Articles=MgDriver(logs,"FlaskPortfolioApp","Projects","",{"description":"","link":""})
# Urls.SaveChanges("Url","_id","FlaskPortFolioUrls",blueprint)


#-----------ROUTES--------------- 

# @app.route("/")
# def main():

#     return render_template("home.html")



# @app.route("/")
# def main():

#     return render_template("home.html",
#     navbar_color=dynamic_content.GetColors("Default"))



# @app.route("/galleries")
# def galleries():

#     return render_template("galleries.html",
#     navbar_color=dynamic_content.GetColors("Default"),
#     red=dynamic_content.GetCollection("RED").values(),
#     red_link="/red_theme",
#     blue=dynamic_content.GetCollection("BLUE").values(),
#     blue_link="/blue_theme",
#     orange=dynamic_content.GetCollection("ORANGE").values(),
#     orange_link="/orange_theme",
#     gray=dynamic_content.GetCollection("GRAY").values(),
#     gray_link="/gray_theme",
#     others=dynamic_content.GetCollection("OTHERS").values(),
#     others_link="/others_theme")




# @app.route("/renders")
# def renders():

#     return render_template("renders.html",
#     navbar_color=dynamic_content.GetColors("Default"))



# @app.route("/assets")
# def assets():

#     return render_template("assets.html",
#     navbar_color=dynamic_content.GetColors("Default"),
#     galleries_themes=dynamic_content.GetCollection("ASSETS"))



# @app.route("/projects")
# def projects():

#     items=Articles.FindAll(Articles.table_name)

#     return render_template("projects.html",
#     navbar_color=dynamic_content.GetColors("Default"),
#     items=items)



# @app.route("/contact")
# def contact():

#     return render_template("contact.html",
#     navbar_color=dynamic_content.GetColors("Default"))


    
# #THEMED GALLERIES

# @app.route("/red_theme")
# def red_theme():

#     return render_template("red_theme.html",
#     navbar_color=dynamic_content.GetColors("RedTheme"),
#     pictures=dynamic_content.GetCollection("RED"))



# @app.route("/orange_theme")
# def orange_theme():

#     return render_template("orange_theme.html",
#     navbar_color=dynamic_content.GetColors("OrangeTheme"),
#     pictures=dynamic_content.GetCollection("ORANGE"))


# @app.route("/gray_theme")
# def gray_theme():

#     return render_template("gray_theme.html",
#     navbar_color=dynamic_content.GetColors("GrayTheme"),
#     pictures=dynamic_content.GetCollection("GRAY"))


# @app.route("/blue_theme")
# def blue_theme():

#     return render_template("blue_theme.html",
#     navbar_color=dynamic_content.GetColors("BlueTheme"),
#     pictures=dynamic_content.GetCollection("BLUE"))



# @app.route("/others_theme")
# def others_theme():

#     return render_template("others_theme.html",
#     navbar_color=dynamic_content.GetColors("MainTheme"),
#     pictures=dynamic_content.GetCollection("OTHERS"))



# @app.route("/user_login_page")
# def user_login():

#     form=Registration(request.form)
#     return render_template("login.html",
#     navbar_color=dynamic_content.GetColors("Default"),
#     form=form,access_denied=False)



# #---------------DATA MANAGEMENT-----------------------
# # Login process
# @app.route("/access",methods=["POST","GET"])
# def Access():

#     form=Registration(request.form)
#     if request.method=="POST" and form.validate():
#         user=form.username.data
#         password=form.password.data
#         if (access.CheckCredentials(user,password)==True):

#             session["username"]=user
#             return render_template("admin_panel.html",
#             navbar_color=dynamic_content.GetColors("Default"),
#             alert_instance=False,alert_message="Not a file",
#             alert_type="danger",
#             items=dynamic_content.UploadPath)
#         else:
#             return render_template("login.html",
#             navbar_color=dynamic_content.GetColors("Default"),
#             form=form,
#             access_denied=True)
 



# @app.route("/upload",methods=["POST","GET"])
# def upload():
    
#     if request.method=="POST":

#         if len(request.form) > 1 :

#             return render_template("admin_panel.html",
#             navbar_color=dynamic_content.GetColors("Default"),
#             alert_instance=True,alert_message="Files can only be uploaded into a single folder at the time",
#             alert_type="danger",
#             items=dynamic_content.UploadPath)

#         if "file[]" not in request.files:
#             flash('No file part')
#             return render_template("admin_panel.html",
#             navbar_color=dynamic_content.GetColors("Default"),
#             alert_instance=True,alert_message="Not a file",
#             alert_type="danger",
#             items=dynamic_content.UploadPath)

#         files = request.files.getlist('file[]')

#         if  len(files) == 0:
#             flash('No file selected')
#             return render_template("admin_panel.html",
#             navbar_color=dynamic_content.GetColors("Default"),
#             alert_instance=True,alert_message="No file detected",
#             alert_type="danger",
#             items=dynamic_content.UploadPath)

#         path=""

#         if dynamic_content.IsFileAllowed(files)==True:
           
#             path=dynamic_content.GetUploadFolderPath(request.form)
#             for file in files:
#                 file.save(path+file.filename)

#             return render_template("admin_panel.html",
#             navbar_color=dynamic_content.GetColors("Default"),
#             alert_instance=True,alert_message="File uploaded",
#             alert_type="success",
#             items=dynamic_content.UploadPath)
#         else:
#             return render_template("admin_panel.html",
#             navbar_color=dynamic_content.GetColors("Default"),
#             alert_instance=True,alert_message="File type not allowed",
#             alert_type="danger",
#             items=dynamic_content.UploadPath)




# @app.route("/search_file",methods=["POST","GET"])
# def Search():

#     if request.method=="POST":


#         if "search" in request.form:

#             if "target_file" in request.form:
#                 filename=request.form.get("target_file")
#                 result=dynamic_content.SearchFile(filename)
#                 if result != False:
#                     return render_template("admin_panel.html",
#                     navbar_color=dynamic_content.GetColors("Default"),
#                     search_match=True,search_type="success",
#                     search_message="File Match : "+result)  
#                 else:
#                     return render_template("admin_panel.html",
#                     navbar_color=dynamic_content.GetColors("Default"),
#                     search_match=True,search_type="danger",
#                     search_message="File not found") 
#             else:
#                 return render_template("admin_panel.html",
#                 navbar_color=dynamic_content.GetColors("Default"),
#                 search_match=True,search_type="primary",
#                 search_message="No file name provided")

#         if "delete" in request.form:
#             result=dynamic_content.DeleteFile()
#             if result==True:

#                 dynamic_content.UpdateBlueprint()
#                 Registry.AddOneIntoCollection(logs.GetDate(),"Content Update , file deleted : "+dynamic_content.last_deleted_file)
#                 return render_template("admin_panel.html",
#                 navbar_color=dynamic_content.GetColors("Default"),
#                 search_match=True,
#                 search_type="success",
#                 search_message="File Deleted . Dont forget to update the database content")
                
        
#             if result==False:
#                 return render_template("admin_panel.html",
#                 navbar_color=dynamic_content.GetColors("Default"),
#                 search_match=True,
#                 search_type="warning",
#                 search_message="You must search the file first! . No file have been deleted ")

#             if result==-1:
#                 return render_template("admin_panel.html",
#                 navbar_color=dynamic_content.GetColors("Default"),
#                 search_match=True,
#                 search_type="danger",
#                 search_message="error, file no longer exist or wrong path")

#         if "show" in request.form:
#             files=dynamic_content.ShowFiles()
#             return render_template("admin_panel.html",
#             navbar_color=dynamic_content.GetColors("Default"),
#             show_files=True,
#             searched_files=files)


#         if "update" in request.form:
#                 blueprint=dynamic_content.UpdateBlueprint()
#                 Urls.SaveChanges("Url","_id","FlaskPortFolioUrls",blueprint)
#                 return render_template("admin_panel.html",
#                 navbar_color=dynamic_content.GetColors("Default"),
#                 search_match=True,
#                 search_type="primary",
#                 search_message="Updating database")
                




# @app.route("/new_article",methods=["POST","GET"])
# def UploadArticle():

#     if request.method=="POST":

#         if "show" in request.form:
          
#             items=Articles.FindAll(Articles.table_name)
#             return render_template("admin_panel.html",
#             navbar_color=dynamic_content.GetColors("Default"),
#             article_search=True,articles=items) 

#         if "search" in request.form:
            
#             if "title" in request.form:

#                 result=Articles.GetData(Articles.table_name,"_id",request.form.get("title"))
#                 if result != False:
#                     return render_template("admin_panel.html",
#                     navbar_color=dynamic_content.GetColors("Default"),
#                     article_upload=True,article_type="primary",
#                     article_result="Article found : "+request.form.get("title")) 
#                 else:
#                     return render_template("admin_panel.html",
#                     navbar_color=dynamic_content.GetColors("Default"),
#                     article_upload=True,article_type="warning",
#                     article_result="Article not found") 
#             else:
#                 return render_template("admin_panel.html",
#                 navbar_color=dynamic_content.GetColors("Default"),
#                 article_upload=True,article_type="warning",
#                 article_result="Title is required for this search") 
          
#         if "delete" in request.form:

#             if "title" in request.form:
#                 Articles.DeleteOne(Articles.table_name,"_id",request.form.get("title"))
#                 return render_template("admin_panel.html",
#                 navbar_color=dynamic_content.GetColors("Default"),
#                 article_upload=True,article_type="success",
#                 article_result="Article removed")
#             else:
#                 return render_template("admin_panel.html",
#                 navbar_color=dynamic_content.GetColors("Default"),
#                 article_upload=True,article_type="warning",
#                 article_result="Title is required for this search")


#         if "upload" in request.form:
        
#             if "title" in request.form and "content" in request.form and "link" in request.form:

#                 title=request.form.get("title")
#                 content=request.form.get("content")
#                 link=request.form.get("link")

               
#                 Articles.data["description"]=content
#                 Articles.data["link"]=link

#                 Articles.AddOneIntoCollection(Articles.table_name,title,Articles.data)
#                 return render_template("admin_panel.html",
#                 navbar_color=dynamic_content.GetColors("Default"),
#                 article_upload=True,article_type="success",
#                 article_result="New article uploaded")

#             else:
#                 return render_template("admin_panel.html",
#                 navbar_color=dynamic_content.GetColors("Default"),
#                 article_upload=True,article_type="warning",
#                 article_result="All fileds are required")

#     return render_template("admin_panel.html",
#     navbar_color=dynamic_content.GetColors("Default"))     




# @app.route("/logout")
# def logout():

#     session.pop("username")
#     return render_template("home.html",navbar_color=dynamic_content.GetColors("Default"))


# @app.route("/googlec434280252cfb790.html")
# def verification():

#     return render_template("googlec434280252cfb790.html")


# if __name__ ==  '__main__':
#     app.run(debug = False,host="0.0.0.0",port="8000")