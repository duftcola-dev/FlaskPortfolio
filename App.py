from os import chdir
from flask import Flask,render_template,request,make_response,session,redirect,url_for,logging,flash
from werkzeug.utils import secure_filename, send_from_directory
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from scripts.Dynamic import DynamicContent
from scripts.MongoDriver import MgDriver
from scripts.dependencies.Logs import Logs
from scripts.Access import UserAccess
from scripts.UploadManager import Upload
from scripts.dependencies.DirectoryTreeGenerator_lite import TreeExplorer
from scripts.PathTempStorage import PathStorage
from inspect import getframeinfo,currentframe

#--------METHODS--------------

def UpdateContent():
    pass

def GetCurrentFile():

    cf=currentframe()
    currentfile=getframeinfo(cf).filename
    start=currentfile.rfind("/")+1
    end=len(currentfile)
    string=""
    for char in range(start,end):

        string=string+currentfile[char]

    return string

#---------INITIALIZATION------------

# update urls the first time the server is initiate
# loads log messages module
# urls of files in the contetnfolder only
# urls of all files in the app
# get current file name for loggin purposes
# user validation data
# database initialization
pathstorage=PathStorage()
content=TreeExplorer()
files_manager=TreeExplorer()
logs=Logs()
dynamic_content=DynamicContent(logs)
upload_manager=Upload(logs)

content.ExploreDirectories(path="static/content",mode="relative")
files_manager.ExploreDirectories(mode="",ignore="venv") 
current_file=GetCurrentFile()

# load user validation
access=UserAccess(files_manager.Files_Registry.get("pasw.json"))

# creating app urls of files and pictures
dynamic_content.DefineContentFolders(content.Dir_Registry)
dynamic_content.DefineContentUrls(content.Files_Registry)
dynamic_content.DefineUploadPathUrls(content.Dir_Registry)
dynamic_content.DefinePicturesUrls(content.Files_List)

# adding galleriy thumnails links 

dynamic_content.SetGalleryThumbnailsLink("RED","/red_theme")
dynamic_content.SetGalleryThumbnailsLink("BLUE","/blue_theme")
dynamic_content.SetGalleryThumbnailsLink("ORANGE","/orange_theme")
dynamic_content.SetGalleryThumbnailsLink("GRAY","/gray_theme")
dynamic_content.SetGalleryThumbnailsLink("OTHERS","/others_theme")
dynamic_content.SetGalleryThumbnailsLink("ASSETS","/assets")

# getting app urls of files and pictures


pathstorage.content_urls=dynamic_content.GetContentFilesUrls()
pathstorage.pictures_urls=dynamic_content.GetPicturesUrls()
pathstorage.upload_urls=dynamic_content.GetUploadPathUrls()
pathstorage.thumbnails_urls=dynamic_content.GetGalleriesThumnails()

# load themes colors
color_default=dynamic_content.GetColors("Default")
color_red=dynamic_content.GetColors("Red")
color_blue=dynamic_content.GetColors("Blue")
color_orange=dynamic_content.GetColors("Orange")
color_gray=dynamic_content.GetColors("Gray")
color_others=dynamic_content.GetColors("Others")
color_main=dynamic_content.GetColors("MainTheme")

# Initilizing mongo database cloud

Urls=MgDriver(logs,"FlaskPortfolioApp","Url","FlaskPortFolioUrls",pathstorage.pictures_urls)
Registry=MgDriver(logs,"FlaskPortfolioApp","Registry",logs.GetDate(),"First Entry")
Articles=MgDriver(logs,"FlaskPortfolioApp","Projects","",{"description":"","link":""})
Urls.SaveChanges("Url","_id","FlaskPortFolioUrls",pathstorage.pictures_urls)


app=Flask(__name__)
app.secret_key=access.GetItem("app")

class Registration(Form):
    username=StringField("User",[validators.Length(min=4,max=255),validators.DataRequired()])
    password=PasswordField("Password",[validators.Length(min=4,max=255),validators.DataRequired()])

#---------CONTENT UPDATE--------

def UpdateContent():

    content.ExploreDirectories(path="static/content",mode="relative")
    files_manager.ExploreDirectories(mode="",ignore="venv") 
    pathstorage.content_urls=dynamic_content.GetContentFilesUrls()
    pathstorage.pictures_urls=dynamic_content.GetPicturesUrls()
    pathstorage.upload_urls=dynamic_content.GetUploadPathUrls()
    pathstorage.thumbnails_urls=dynamic_content.GetGalleriesThumnails()


#-----------ROUTES--------------- 


@app.route("/")
def main():

    return render_template("home.html",
    navbar_color=color_default)


@app.route("/galleries")
def galleries():

    return render_template("galleries.html",navbar_color=color_default,thumbnails=pathstorage.thumbnails_urls)


@app.route("/assets")
def assets():
    print(pathstorage.pictures_urls.get("ASSETS"))
    return render_template("assets.html",navbar_color=color_default,pictures=pathstorage.pictures_urls.get("ASSETS"))


@app.route("/contact")
def contact():

    return render_template("contact.html",navbar_color=color_default)



@app.route("/red_theme")
def red_theme():

    return render_template("red_theme.html",navbar_color=color_red,pictures=pathstorage.pictures_urls.get("RED"))



@app.route("/orange_theme")
def orange_theme():

    return render_template("orange_theme.html",navbar_color=color_orange,pictures=pathstorage.pictures_urls.get("ORANGE"))


@app.route("/gray_theme")
def gray_theme():

    return render_template("gray_theme.html",navbar_color=color_gray,pictures=pathstorage.pictures_urls.get("GRAY"))


@app.route("/blue_theme")
def blue_theme():

    return render_template("blue_theme.html",navbar_color=color_blue,pictures=pathstorage.pictures_urls.get("BLUE"))



@app.route("/others_theme")
def others_theme():

    return render_template("others_theme.html",navbar_color=color_main,pictures=pathstorage.pictures_urls.get("OTHERS"))



#--------- ADMIN LOGIN / VALIDATION ---------------------

@app.route("/access",methods=["POST","GET"])
def Access():

    form=Registration(request.form)
    if request.method=="POST" and form.validate():
        user=form.username.data
        password=form.password.data
        if (access.CheckCredentials(user,password)==True):

            session["username"]=user
            return render_template("admin_panel.html",navbar_color=color_default,alert_instance=False)
        else:
            return render_template("login.html",navbar_color=color_default,form=form,access_denied=True)
 

@app.route("/user_login_page")
def user_login():

    form=Registration(request.form)
    return render_template("login.html",navbar_color=color_default,form=form,access_denied=False)


@app.route("/logout")
def logout():

    session.pop("username")
    return render_template("home.html",navbar_color=color_default)



#---------------DATA MANAGEMENT-----------------------


@app.route("/projects")
def projects():

    items=Articles.FindAll(Articles.table_name)

    return render_template("projects.html",navbar_color=color_default,items=items)



@app.route("/upload",methods=["POST","GET"])
def upload():
    
    if request.method=="POST":

        if len(request.form) > 1 :
            message="Files can only be uploaded into a single folder at the time"
            return render_template("admin_panel.html",navbar_color=color_default,
            alert_instance=True,alert_message=message,alert_type="danger")

        if "file[]" not in request.files:
            message="Not a file"
            return render_template("admin_panel.html",navbar_color=color_default,
            alert_instance=True,alert_message=message,alert_type="danger")

        files = request.files.getlist('file[]')

        if  len(files) == 0:
            message="No file detected"
            return render_template("admin_panel.html",navbar_color=color_default,
            alert_instance=True,alert_message=message,alert_type="danger")

        path=""

        if upload_manager.IsFileAllowed(files)==True:
           
            path=upload_manager.GetUploadPath(request.form,pathstorage.upload_urls)

            if path==False:
                files.clear()
                message="File uploaded"
                return render_template("admin_panel.html",navbar_color=color_default,
                alert_instance=True,alert_message=message,alert_type="success")
                
            for file in files:
                file.save(path+file.filename)

            message="File uploaded"
            return render_template("admin_panel.html",navbar_color=color_default,
            alert_instance=True,alert_message=message,alert_type="success")

        else:

            message="File type not allowed"
            return render_template("admin_panel.html",navbar_color=color_default,
            alert_instance=True,alert_message=message,alert_type="danger")




@app.route("/search_file",methods=["POST","GET"])
def Search():

    if request.method=="POST":


        if "search" in request.form:

            if "target_file" in request.form:
                
                filename=request.form.get("target_file")
                result=upload_manager.SearchFile(filename,content.Files_Registry)
                if result != False:
                    return render_template("admin_panel.html",navbar_color=color_default,
                    search_match=True,search_type="success",search_message="File Match : "+result)  
                else:
                    return render_template("admin_panel.html",
                    navbar_color=color_default,search_match=True,
                    search_type="danger",search_message="File not found") 
            else:
                return render_template("admin_panel.html",
                navbar_color=color_default,search_match=True,search_type="primary",
                search_message="No file name provided")

        if "delete" in request.form:

            result=upload_manager.DeleteFile(content.Files_Registry)

            if result==True:

                UpdateContent()

                message="File Deleted . Dont forget to update the database content"
                Registry.AddOneIntoCollection(logs.GetDate(),"Content Update , file deleted : "+upload_manager.last_deleted_file)
                return render_template("admin_panel.html",navbar_color=color_default,search_match=True,
                search_type="success",search_message=message)
                        
            if result==False:
                message="You must search the file first! . No file have been deleted "
                return render_template("admin_panel.html",navbar_color=color_default,search_match=True,
                search_type="warning",search_message=message)

            if result==-1:
                message="error, cannot find file / file no longer exist or wrong path"
                return render_template("admin_panel.html",navbar_color=color_default,
                search_match=True,search_type="danger",search_message=message)

        if "show" in request.form:
            files=content.Files_Registry.keys()
            return render_template("admin_panel.html",navbar_color=color_default,
            show_files=True,searched_files=files)


        if "update" in request.form:
                
                UpdateContent()

                Urls.SaveChanges("Url","_id","FlaskPortFolioUrls",pathstorage.content_urls)
                return render_template("admin_panel.html",navbar_color=color_default,
                search_match=True,search_type="primary",search_message="Updating database")
                




@app.route("/new_article",methods=["POST","GET"])
def UploadArticle():

    if request.method=="POST":

        if "show" in request.form:
          
            items=Articles.FindAll(Articles.table_name)
            return render_template("admin_panel.html",navbar_color=color_default,
            article_search=True,articles=items) 

        if "search" in request.form:
            
            if "title" in request.form:

                result=Articles.GetData(Articles.table_name,"_id",request.form.get("title"))
                if result != False:
                    return render_template("admin_panel.html",
                    navbar_color=color_default,article_upload=True,article_type="primary",
                    article_result="Article found : "+request.form.get("title")) 
                else:
                    return render_template("admin_panel.html",navbar_color=color_default,
                    article_upload=True,article_type="warning",article_result="Article not found") 
            else:
                message="Title is required for this search"
                return render_template("admin_panel.html",navbar_color=color_default,
                article_upload=True,article_type="warning",article_result=message) 
          
        if "delete" in request.form:

            if "title" in request.form:
                Articles.DeleteOne(Articles.table_name,"_id",request.form.get("title"))
                return render_template("admin_panel.html",
                navbar_color=color_default,
                article_upload=True,article_type="success",
                article_result="Article removed")
            else:
                return render_template("admin_panel.html",
                navbar_color=color_default,
                article_upload=True,article_type="warning",
                article_result="Title is required for this search")


        if "upload" in request.form:
        
            if "title" in request.form and "content" in request.form and "link" in request.form:

                title=request.form.get("title")
                content=request.form.get("content")
                link=request.form.get("link")

               
                Articles.data["description"]=content
                Articles.data["link"]=link

                Articles.AddOneIntoCollection(Articles.table_name,title,Articles.data)
                return render_template("admin_panel.html",
                navbar_color=color_default,
                article_upload=True,article_type="success",
                article_result="New article uploaded")

            else:
                return render_template("admin_panel.html",
                navbar_color=color_default,
                article_upload=True,article_type="warning",
                article_result="All fileds are required")

    return render_template("admin_panel.html",
    navbar_color=dynamic_content.GetColors("Default"))     





if __name__ ==  '__main__':

    app.run(debug = True,host="0.0.0.0",port="8000")