from django.shortcuts import render

#Wroks with debug mode off. Check how does the static files get collected in that case
#Get a good page for 500.html
def page_not_found_custom(request):
        data = {}
        return render(request,'custom-404.html', data)
 
def error_500(request):
        data = {}
        return render(request,'myapp/error_500.html', data)