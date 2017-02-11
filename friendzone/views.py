from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from forms import SignInForm, RegistrationForm, ChangeProfilePic, EditProfile, QuestionForm, AnswerForm, MessageForm
from django.contrib.auth.models import User
from users.models import UserProfile
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from posts.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from comments.models import Comment
from inbox.models import Message


def home(request):
    if request.user.is_authenticated():
        user = request.user
        user_profile = UserProfile.objects.get(user=user)

        if request.method == 'POST':
            form = QuestionForm(request.POST)

            if form.is_valid():
                form = form.clean()
                title = form['title']
                content = form['content']
                # anonymous = form['anonymous']

                # Create Post object
                Post.objects.create_post(title=title, author=user, content=content).save()

        # Retrieve all posts but limit number of posts shown on home page to 10.
        post_list = Post.objects.all()
        paginator = Paginator(post_list, 10)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            posts = paginator.page(paginator.num_pages)

        form = QuestionForm()
        comments = Comment.objects.all()
        return render(request, 'home.html', {'posts': posts, 'user_profile': user_profile, 'form': form, 'comments': comments})

    else:
        return HttpResponseRedirect(reverse('login'))


def register(request):
    errors = []

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        # Form validation
        if form.is_valid():
            # Extract user's information from the RegistrationForm.
            form = form.clean()  # Cleans and validates fields
            first_name = form['first_name']
            last_name = form['last_name']
            email = form['email']
            password = form['password']
            password_verify = form['password_verify']
            birth_date = form['birth_date']
            gender = form['gender']
            username = form['username']

            # Verify if passwords match
            if password != password_verify:
                form = RegistrationForm(request.POST)
                errors.append("Passwords do not match. Please try again.")
                return render(request, 'registration.html', {'form': form, 'errors': errors})
            else:
                # Create User and UserProfile objects that automatically saves to database once instantiated.
                # Redirect user to home page if registration is successful.
                # Return error message if registration unsuccessful.
                try:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password_verify,
                        first_name=first_name,
                        last_name=last_name
                    )
                    # Save the additional user attributes
                    UserProfile(gender=gender, birth_date=birth_date, user_id=int(user.id)).save()
                    user = authenticate(username=username, password=password_verify)
                    login(request, user)

                    return HttpResponseRedirect(reverse('home'))
                except IntegrityError:
                    errors.append("The email address provided has already been registered.")
                    form = RegistrationForm(request.POST)

                    return render(request, 'registration.html', {'form': form, 'errors': errors})

    else:
        form = RegistrationForm()
        return render(request, 'registration.html', {'form': form})


def signin(request):
    errors = []

    if request.method == 'POST':
        form = SignInForm(request.POST)

        if form.is_valid():
            form = form.clean()  # Clean form and validate fields
            email = form['email']
            password = form['password']

            # Authenticate user. Because authentication requires username and not email, we need to see if the
            # email provided exists in the database (i.e. we have a user object). If it does, we can use the
            # email address to retrieve the user's username.
            query_user = User.objects.filter(email=email)  # This returns a query set of user objects.

            # If the length query_user is > 0, then user objects exists. We can then extract the user's username.
            if len(query_user) > 0:
                user = query_user[0]  # Retrieves the user object from the query set. Length of set should always be 1.
            else:
                errors.append("The email address or password is invalid. Please try again or register.")
                form = SignInForm(request.POST)
                return render(request, 'signin.html', {'form': form, 'errors': errors})

            user = authenticate(username=user.username, password=password)

            # If authentication is successful, user object is returned.
            # If no user object is returned, either that user doesn't exist or user provided invalid credentials.
            if user is not None:
                # Verify if user is still active.
                if user.is_active:
                    # if account is valid AND active, log user in and redirect them to the home page.
                    login(request, user)
                    return HttpResponseRedirect(reverse('home'))
                else:
                    return HttpResponse("The account is no longer active.")
            else:
                errors.append("The email address or password provided is invalid. Please try again.")
                form = SignInForm(request.POST)
                return render(request, 'signin.html', {'form': form, 'errors': errors})
    else:
        form = SignInForm()

    return render(request, 'signin.html', {'form': form, 'errors': errors})


@login_required
def user_logout(request):
    logout(request)

    # Take them back to the login page.
    return HttpResponseRedirect(reverse('home'))


def profile_page(request, username):
    if request.user.is_authenticated():
        user = get_object_or_404(User, username=username)
        user_profile = UserProfile.objects.get(user=user)
        age = user_profile.calculate_age()

        # Form that allows users to change their profile picture.
        if request.method == 'POST':
            form = ChangeProfilePic(request.POST, request.FILES or None)
            profile_pic = request.FILES['picture']

            # Save profile pic
            user_profile.profile_pic = profile_pic
            user_profile.save()
        else:
            form = ChangeProfilePic()
            return render(request, 'profile.html',
                          {'form': form, 'user': user, 'user_profile': user_profile, 'age': age})

        return render(request, 'profile.html',
                      {'form': form,
                       'user': user, 'user_profile': user_profile,
                       'age': age})
    else:
        return HttpResponseRedirect(reverse('home'))


def edit_profile(request):
    errors = []

    if request.user.is_authenticated():
        user = request.user
        user_profile = UserProfile.objects.get(user=user)

        if request.method == 'POST':
            form = EditProfile(request.POST)

            if form.is_valid():
                form = form.clean()
                first_name = form['first_name']
                last_name = form['last_name']
                email = form['email']
                username = form['username']
                birth_date = form['birth_date']
                gender = form['gender']
                bio = form['bio']

                try:
                    user.first_name = first_name
                    user.last_name = last_name
                    user.email = email
                    user.username = username
                    user_profile.birth_date = birth_date
                    user_profile.gender = gender
                    user_profile.bio = bio

                    user.save()
                    user_profile.save()

                    return HttpResponseRedirect(reverse('edit_profile_success'))
                except IntegrityError:
                    errors.append("The email address or username provided is already taken.")
                    form = RegistrationForm(request.POST)
                    return render(request, 'edit_profile.html', {'form': form, 'errors': errors})
        else:
            form = EditProfile()
            return render(request, 'edit_profile.html', {'form': form, 'errors': errors})
    else:
        return HttpResponseRedirect(reverse('home'))


def edit_profile_success(request):
    if request.user.is_authenticated():
        return render(request, 'edit_profile_success.html')
    else:
        return HttpResponseRedirect(reverse('home'))


def post(request, username, post_id):
    if request.user.is_authenticated():
        try:
            post_id = int(post_id)
        except ValueError:
            raise Http404

        post = Post.objects.get(id=post_id)
        user = User.objects.get(id=post.author_id)

        if request.method == 'POST':
            form = AnswerForm(request.POST)

            if form.is_valid():
                form = form.clean()
                answer = form['comment']

            # Create Comment object
            Comment.objects.create_post(user=request.user, post=post, comment=answer).save()
            return HttpResponseRedirect(post.get_absolute_url())

        form = AnswerForm()
        comments = Comment.objects.filter(post_id=post_id)
        comment_count = comments.count()
        return render(request, 'post.html', {
            'comments': comments,
            'post': post,
            'form': form,
            'comment_count': comment_count})
    else:
        return HttpResponseRedirect(reverse('home'))


def about(request):
    return render(request, 'about.html')


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user.id != request.user.id:
        raise Http404
    comment.delete()
    return HttpResponseRedirect(comment.get_absolute_url())


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author.id != request.user.id:
        raise Http404
    post.delete()
    return HttpResponseRedirect(reverse('home'))


@login_required
def messages(request):
    return render(request, 'messages.html')