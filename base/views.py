from django.shortcuts import render, redirect
from django.contrib import messages
from .models import NewsPage, Category, User, Comment, Staff
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from django.db.models import Q

# Create your views here.


def registerPage(request):


    if request.method == "POST":
    
        # Determine if the user is unique
        email=request.POST.get("email")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect(registerPage)
        
        # Determine if passwords are identical
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if (password1 != password2):
            messages.error(request, "The Passwords are not the Same")
            return redirect(registerPage)
        
        user = User.objects.create(
            first_name=request.POST.get("firstname"),
            last_name=request.POST.get("lastname"),
            username=request.POST.get("firstname"),
            email=email,
            phone=request.POST.get("phone"),
            avatar=request.POST.get("profile-pic"),
            password=make_password(password1)
        )
        user.save()
        login(request, user=user)
        return redirect(home)

    return render(request, 'base/registration-page.html')

def loginPage(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            if Staff.objects.filter(user=user).exists() == False:
                return redirect(home)

            if user.is_superuser:
                return redirect(adminPanel)
            
            staff = Staff.objects.get(user=user)

            return redirect(staffPage, pk=staff.id)
        else:
            messages.error(request, "Username or password does not exist")
            return redirect(loginPage)

    return render(request, 'base/loginPage.html')

def home(request):
    categories = Category.objects.all()[:5]
    newsPages = NewsPage.objects.all()
    mynewsPages = []
    lastNewsPages = []

    # Get the first 3 recently added news pages in all category
    for category in categories:
        
        mynewsPages.append(category.newspage_set.all()[1:3])
        lastNewsPages.append(category.newspage_set.first())

    context = {"categories":categories, "newsPages": mynewsPages, "lastNewsPages":lastNewsPages}
    return render(request, "base/index.html", context)

def categoryPage(request, pk):
    category = Category.objects.get(id=pk)
    categories = Category.objects.all()
    pages = category.newspage_set.all()
    context = {"pages":pages, "category":category, "categories":categories}
    return render(request, "base/category-page.html", context)

def newsPage(request, pk):
    page = NewsPage.objects.get(id=pk)

    if request.method == "POST":
        comment = Comment.objects.create(
            text=request.POST.get("comment"),
            news_page = page
        )
        return redirect(newsPage, pk=pk)
        
    # Spliting the textarea content into appropriate paragraphs


    paragraphs = page.news_content.split('\n')
    first_paragraphs = paragraphs[:3]
    last_paragraphs = paragraphs[3:]

    categories = Category.objects.all()[:4]

    comments = page.comment_set.all()

    context = {"page":page, 'first_paragraphs':first_paragraphs, 'last_paragraphs':last_paragraphs, "categories":categories, "comments":comments}
    return render(request, 'base/news-page.html', context)

def adminPanel(request):
    return render(request, 'base/adminstrationPage.html')

def addStaff(request):
    if request.method == "POST":
        user = User.objects.get(
            email=request.POST.get("email")
            )
        
        if Staff.objects.filter(user=user).exists():
            messages.error(request, "This user is already a staff")
            return redirect(adminPanel)
        
        if user is not None:
            Staff.objects.create(
                user=user,
                field=request.POST.get("work"),
                date_of_birth=request.POST.get("dob"),
                avatar=request.FILES.get("image1")
            )
            print(Staff)
            return redirect(adminPanel)
        else:
            messages.error(request, "This is not a user")
            return redirect(registerPage)
        
        
    return render(request, 'base/add-staff.html')

def updateStaff(request, pk):
    staff_info = Staff.objects.get(id=pk)

    if request.method == "POST":

        staff_info.field=request.POST.get("work")

        if request.POST.get("dob"):
            staff_info.date_of_birth=request.POST.get("dob")

        if request.FILES.get("image1"):
            staff_info.avatar=request.FILES.get("image1")

        staff_info.save()

        return redirect(staffPage, pk=pk)
    
    context = {"staff":staff_info}
    return render(request, 'base/update-staff.html', context)

def staffPage(request, pk):
    categories = Category.objects.all()[:4]
    staff = Staff.objects.get(id=pk)
    firstname = staff.user.first_name
    lastname = staff.user.last_name

    # News pages he has covered
    works = NewsPage.objects.filter(Q(author__icontains=firstname) &
                                    Q(author__icontains=lastname))
    
    context = {"categories":categories, "staff":staff, "works":works}
    return render(request, 'base/staff-page.html', context)

def allStaffs(request):
    staffs = Staff.objects.all()
    categories = Category.objects.all()[:4]
    context = {"staffs":staffs, "categories":categories}
    return render(request, 'base/staff-log.html', context)

def createPage(request):

    if request.method == 'POST':

        category, created = Category.objects.get_or_create(name=request.POST.get('category'))
        page = NewsPage.objects.create(
            headline = request.POST.get('headline'),
            author = request.POST.get('author'),
            category = category,
            main_image = request.FILES.get('image1'),
            main_image_title = request.POST.get('image1-title'),
            sub_image = request.FILES.get('image2'),
            sub_image_title = request.POST.get('image2-title'),
            news_content = request.POST.get('news-content')
        )
        page.save()
        return redirect(home)
    
    return render(request, 'base/createPage.html')

def deleteStaff(request, pk):
    staff = Staff.objects.get(id=pk)
    staff.delete()
    return redirect(allStaffs)