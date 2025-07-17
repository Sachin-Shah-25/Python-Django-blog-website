from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import blogmodel, commentmodel, profilemodel, likemodel
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import logging
from django.http import JsonResponse
from .dataclass.blogdata import BlogsData

logger = logging.getLogger(__name__)


def home(request):
    blogs = blogmodel.objects.all()
    update_data = []
    for blog in blogs:
        count = likemodel.objects.filter(blog=blog).count()
        obj = BlogsData(blog.id, blog.title, blog.image,
                        blog.category, blog.content, blog.dateandtime, count)

        update_data.append(obj)
    return render(request, "index.html", {"blogs": update_data})

def signup(request):
    if  request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        getUsername = request.POST['username']
        getUseremail = request.POST['useremail']
        getUserPassword1 = request.POST['password1']
        getUserPassword2 = request.POST['password2']
        userimage = request.FILES.get('userimage', "")

        if getUsername and getUseremail and getUserPassword1 and getUserPassword2:

            if len(getUserPassword1) < 6:
                messages.error(request, "Password too short!")
                return redirect("signup")

            elif not userimage:
                messages.error(request, "Please upload an image")
                return redirect("signup")

            else:
                isUserRegistered = User.objects.filter(
                    username=getUsername).first()
                if isUserRegistered:
                    messages.error(request, "User already registered")
                    return redirect("signup")

                elif getUserPassword1 == getUserPassword2:
                    try:
                        user = User.objects.create_user(
                            username=getUsername, email=getUseremail, password=getUserPassword1)
                        profilemodel.objects.create(
                            user=user, userimage=userimage)
                        return redirect("signin")

                    except Exception as e:
                        messages.error(request, "Something went wrong ", e)
                        logger.error(f"An error occured : {e}")
                        return redirect("signup")
                else:
                    messages.error(request, "Password doesn't match")
                    return redirect('signup')
        else:
            messages.error(request, "All Field are required")
            return redirect("signup")
    else:
        return render(request, "Signup.html")

def signin(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        getUsername = request.POST['username']
        getUseremail = request.POST['useremail']
        getUserPassword = request.POST['password']

        if getUsername and getUseremail:
            messages.error(request, "Choose One Username or Useremail")
            return redirect("signin")

        if (getUsername or getUseremail) and (getUserPassword):

            if getUsername:
                if not User.objects.filter(username=getUsername).exists():
                    messages.error(request, "User Not Registred")
                    return redirect("signin")

                getUser = auth_fun(request, getUsername, getUserPassword)
                if getUser:
                    login(request, getUser)
                    return redirect("index")

                else:
                    messages.error(request, "User not registered")
                    return redirect("signin")

            elif getUseremail:
                findUser = User.objects.get(email=getUseremail)

                if not findUser:
                    messages.error(request, "Email not registred")
                    return redirect("signin")

                if auth_fun(request, findUser.username, getUserPassword):
                    login(request, findUser)
                    return redirect("index")
        else:
            messages.error(request, "invalid details")
            return redirect('signin')
    else:
        return render(request, "Signin.html")

def auth_fun(request, getUsername, getUserPassword):
    user = authenticate(
        request, username=getUsername, password=getUserPassword)
    return user

def log_out(request):
    logout(request)
    return redirect("signin")

def create(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please Login Again")
        return redirect("signin")

    if request.method == "POST":
        getTitle = request.POST['title']
        getContent = request.POST['content']
        getCategory = request.POST['category']

        if not getTitle or not getContent or not getCategory:
            messages.error(request, "All field are required")
            return redirect("create")

        getImage = request.FILES.get("blogimage", "")
        if not getImage:
            messages.error(request, "Image Not Found ")
            return redirect("create")

        try:
            blogmodel.objects.create(user=request.user, image=getImage,
                                     title=getTitle, content=getContent, category=getCategory)
            return redirect("index")

        except Exception as e:
            messages.error(request, "Something went wrong : ", e)
            logger.error(f"Something went wrong : {e}")
            return redirect("Create")

    else:
        return render(request, "Create.html")

def blogs(request):
    blogs = blogmodel.objects.all()
    
    return render(request, "blog.html",{"blogs":blogs})

def blogview(request, id):
    try:
        getBlog = blogmodel.objects.get(id=id)
        comments = commentmodel.objects.filter(blog_id=id).order_by("-id")
        totalliked = likemodel.objects.filter(blog=getBlog).count()

        comment_profile = []
        for comment in comments:
            getProfile = profilemodel.objects.get(user=comment.user)
            comment_profile.append({
                "id": comment.id,
                "commentbyimage": getProfile.userimage.url,
                "commentbyname": comment.user.username,
                "comment": comment.comment,
                "totalLiked": totalliked
            })

        return render(request, "view.html", {"blog": getBlog, "comments": comment_profile, "totalLiked": totalliked, "total_comment": len(comments)})

    except blogmodel.DoesNotExist:
        messages.error(request, "Not Found")
        return redirect("index")

def blogupdate(request, id):
    if request.method == "POST":
        getTitle = request.POST['title']
        getContent = request.POST['content']
        getCategory = request.POST['category']

        if not request.user.is_authenticated:
            messages.error(request, "Please Login Again")
            return redirect("Signin")

        try:
            getBlog = blogmodel.objects.get(id=id)
            getImage = request.FILES['blogimage'] if 'blogimage' in request.FILES else getBlog.image
            getBlog.title = getTitle
            getBlog.content = getContent
            getBlog.category = getCategory
            getBlog.image = getBlog.image if not getImage else getImage
            getBlog.save()
            
            return redirect("profile")

        except Exception as e:
            messages.error(request, "Something went wrong : ", e)
            logger.error(f"Something went wrong : {e}")
            return redirect("create")

    else:
        getBlog = blogmodel.objects.get(id=id)
        return render(request, "create.html", {"blog": getBlog})

def blogdelete(request, id):
    try:
        getDeletedItem = blogmodel.objects.get(id=id)
        getDeletedItem.delete()
        messages.success(request, "Deleted !")
        return redirect("profile")

    except blogmodel.DoesNotExist:
        messages.error(request, "Not Found ")
        return redirect("profile")

def profile(request):
    if not request.user.is_authenticated:
        messages.error(request, "Login Again!")
        return redirect("signin")
    getUser = request.user
    getBlogs = blogmodel.objects.filter(user_id=getUser).order_by("-id")
    getProfile = profilemodel.objects.get(user=request.user)

    blogandliked = []
    for blog in getBlogs:
        getLiked = likemodel.objects.filter(blog=blog).count()
        blogandliked.append({
            "id": blog.id,
            "category": blog.category,
            "title": blog.title,
            "content": blog.content,
            "dateandtime": blog.dateandtime,
            "blogimage": blog.image.url,
            "liked": getLiked
        })

    return render(request, "Profile.html", {"blogs": blogandliked, "getProfile": getProfile.userimage.url})

def comment(request, id):
    if not request.user.is_authenticated:
        messages.error(request, "Please Login again !")
        return redirect("signin")

    getComment = request.POST['comment']

    if not getComment:
        messages.error(request, "Invalid Details")
        return redirect(f"/view/{id}")

    try:
        getBlog = blogmodel.objects.get(id=id)
        user = request.user
        commentmodel.objects.create(
            user=user, blog=getBlog, comment=getComment)
        return redirect(f"/view/{id}")

    except getBlog.DoesNotExist or user.DoesNotExist:
        messages.error(request, "Not Found ")
        return redirect("index")

    except Exception as e:
        messages.error(request, f"Something went wrong : {e} ")
        return redirect(f"/view/{id}")

def commentdel(request, id):
    try:

        commentmodel.objects.get(id=id).delete()
        return JsonResponse({"data": "Delete"})
    except commentmodel.DoesNotExist:
        return JsonResponse({"error": "Something went wrong "+e})
    except Exception as e:
        return JsonResponse({"error": "Something went wrong "+e})

def increaselike(request, id):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Please log in"}, status=401)
        blog = blogmodel.objects.get(id=id)
        if likemodel.objects.filter(user=request.user, blog=blog).exists():
            likemodel.objects.get(user=request.user, blog=blog).delete()
            return JsonResponse({"success": "Alread liked"}, status=200)
        likemodel.objects.create(user=request.user, blog=blog)

        return JsonResponse({"success": "Done"}, status=200)
    except blog.DoesNotExist as e:

        return JsonResponse({"error": "something went wrong "}, status=500)
    except Exception as e:

        return JsonResponse({"error": "something went wrong "+e})

def contact(request):
    if not request.user.is_authenticated:
        messages.error(request, "Login Again !")
        return redirect("signin")
    else:
        return render(request, "contact.html", {"user": request.user})
