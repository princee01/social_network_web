from django.shortcuts import render
from .models import post, Reaction, Profile
from .forms import PostForm, ReactionForm, UserRegForm,profileForm  
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse


# Create your views here.
def index(request):
    return render(request,'index.html')

def post_list(request):
    posts = post.objects.all().order_by('-created_at')
    for p in posts:
        p.like_count=p.total_likes()
        p.dislike_count=p.total_dislikes()

        if request.user.is_authenticated:
            user_reaction=Reaction.objects.filter(user=request.user, post=p).first()
            if user_reaction:
                p.user_reaction=user_reaction.reaction_type
            else:
                p.user_reaction=None
    return render(request, 'post_list.html', {'posts': posts})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect('/')
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form': form})

@login_required
def post_edit(request, post_id):
    post_instance = get_object_or_404(post, pk=post_id, user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post_instance)
        if form.is_valid():
            post_instance = form.save(commit=False)
            post_instance.user = request.user
            post_instance.save()
            return redirect('/')
    else:
        form = PostForm(instance=post_instance)
    return render(request, 'post_edit.html', {'form': form})

@login_required    
def post_delete(request, post_id):
    post_instance = get_object_or_404(post, pk=post_id, user=request.user)
    if request.method == 'POST':
        post_instance.delete()
        return redirect('/')
    return render(request, 'post_delete.html', {'post': post_instance})

def react_to_post(request, post_id):
    if request.method == 'POST':
        reaction_type=request.POST.get('reaction_type')
        user=request.user
        Post=post.objects.get(id=post_id)

        existing_reaction=Reaction.objects.filter(user=user, post=Post).first()

        if existing_reaction:
            if existing_reaction.reaction_type == reaction_type:
                existing_reaction.delete()
            else:
                existing_reaction.reaction_type = reaction_type
                existing_reaction.save()
        else:
            Reaction.objects.create(user=user, post=Post, reaction_type=reaction_type)

        like_count=Reaction.objects.filter(post=Post, reaction_type='like').count()  
        dislike_count=Reaction.objects.filter(post=Post, reaction_type='dislike').count()

        return JsonResponse({
            'like_count': like_count,
            'dislike_count': dislike_count,
        })        

def register(request):
    if request.method=='POST':
        form=UserRegForm(request.POST,request.FILES)
        if form.is_valid():
            user=form.save(commit=False)
            user.email=form.cleaned_data['email']
            user.set_password(form.cleaned_data['password1'])
            user.save()

            Profile.objects.create(
                user=user,
                profilePicture=form.cleaned_data['profilePicture'],
                dateOfBirth=form.cleaned_data['dateOfBirth']
            )
            login(request,user)
            return redirect('/')
    else:
        form=UserRegForm()
    return render(request, 'registration/register.html',{'form':form})


@login_required
def updateProfile(request):
    profile_instance=get_object_or_404(Profile, user=request.user)
    if request.method=='POST':
        form=profileForm(request.POST,request.FILES, instance=profile_instance)
        if form.is_valid():
            profile_instance=form.save(commit=False)
            profile_instance.user=request.user
            profile_instance.save()
            return redirect('/')
    else:
        form=profileForm(instance=profile_instance)
    return render(request, 'update_profile.html',{'form':form})

