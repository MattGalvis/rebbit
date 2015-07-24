from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
# Create your views here.
from django.template import RequestContext
from Rebbit.models import Post, Person, Sub_rebb



def homepage(request):
    subs = Sub_rebb.objects.order_by('sub_r')
    return render_to_response("Rebbit/homepage.html", {
        'Post_list': Post.objects.all(),
        'Subrebb_list': subs,
    }, context_instance=RequestContext(request))

def createpost(request):
    subs = Sub_rebb.objects.order_by('sub_r')
    c = {
        'Subrebb_list': subs,
    }
    c.update(csrf(request))
    return render_to_response("Rebbit/createpost.html",c,context_instance=RequestContext(request))

def auth_post(request):
    post = Post()
    post.title = request.POST.get('posttitle')
    web_user = Person.objects.get(username=request.session['user_username'])
    post.creator = web_user
    post.rpost = request.POST.get('postdescription')
    postsubr = Sub_rebb.objects.get(sub_r=request.POST.get('Topic'))
    if postsubr.sub_r not in Sub_rebb.objects.filter(sub_r=postsubr.sub_r):
        return redirect("/signin")
    post.subreddit = postsubr
    post.save()
    return redirect("/index")

def subredditdetail(request,sub_id,post_id = 1):
    post_info = Post.objects.get(id=post_id)
    return render_to_response("Rebbit/subredditdetail.html", {
        'Post_list': post_info
    }, context_instance=RequestContext(request))

def subreddit(request,sub_id):
    sub = Sub_rebb.objects.get(sub_r=sub_id)
    sub_info = Post.objects.filter(subreddit=sub)
    return render_to_response("Rebbit/subreddit.html", {
        'subname': sub,
        'sub_list': sub_info,
        'reg_sub_list': Sub_rebb.objects.all(),
    }, context_instance=RequestContext(request))

def signup(request):
    c = {}
    c.update(csrf(request))
    return render_to_response("Rebbit/signup.html",c)

def auth_signup(request):
    person = Person()
    person.first_name = request.POST.get('firstname')
    person.last_name = request.POST.get('lastname')
    person.email = request.POST.get('email')
    person.username = request.POST.get('username')
    person.password = request.POST.get('password')
    person.save()
    return redirect("/signin")

def signin(request):
    c = {}
    c.update(csrf(request))
    return render_to_response("Rebbit/signin.html",c)

def accounthome(request):

    return render_to_response("Rebbit/userhome.html", {
        'Person_list': Person.objects.all()
    }, context_instance=RequestContext(request))

def auth_verify(request):

    try:
        user = Person.objects.get(username=request.POST['username'])
         # the password verified for the user
        if user.password == request.POST['password']:
            request.session['user_fname'] = user.first_name
            request.session['user_lname'] = user.last_name
            request.session['user_email'] = user.email
            request.session['user_username'] = user.username
            return redirect("/account")
        else:
            return render_to_response("Rebbit/signin.html", {
            'invalid': True
            }, context_instance=RequestContext(request))
    except Person.DoesNotExist:
        user = None
        # the authentication system was unable to verify the username and password
        return render_to_response("Rebbit/signin.html", {
        'bothinvalid': True
        }, context_instance=RequestContext(request))

def logout(request):
    if request.session.get('user_username', None):
        request.session.flush()
        return redirect("/index")
    else:
        return render_to_response("Rebbit/signin.html", {
            'notlogged': True
            }, context_instance=RequestContext(request))


def createsub(request):
    c = {}
    c.update(csrf(request))
    return render_to_response("Rebbit/createsub.html",c)

def auth_sub(request):
    sub = Sub_rebb()
    sub.sub_r = request.POST.get('subname')
    sub.save()
    return redirect("/createpost")