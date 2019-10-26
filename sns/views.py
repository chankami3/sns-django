from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages


from .models import Message,Group,Friend,Good
from .forms import SearchForm,GroupCheckForm,GroupSelectForm,FriendsForm,\
        CreateGroupForm,PostForm


from django.db.models import Q
from django.contrib.auth.decorators import login_required


@login_required(login_url='/admin/login/')
def index(request):
    # public userを取得
    (public_user, public_group) = get_public()

    # POST送信時の処理
    if request.method == 'POST':
        # Groupsのチェックを更新した時の処理
        if request.POST['mode'] == '__check_form__':
            # フォームの用意
            searchform = SearchForm()
            checkform = GroupCheckForm(request.user, request.POST)
            # チェックされたGroup名をリストにまとめる
            glist = []
            for item in request.POST.getlist('groups'):
                glist.append(item)
            # Messageの取得
            messages = get_your_group_message(request.user, glist, None)
        
        # Groupsメニューを変更した時の処理
        if request.POST['mode'] == '__search_form__':
            # フォームの用意
            searchform = SearchForm(request.POST)
            checkform = GroupCheckForm(request.user)
            # Groupのリストを取得
            gps = Group.objects.filter(owner=request.user)
            glist = [public_group]
            for item in gps:
                glist.append(item)
            # Messageの取得
            messages = get_your_group_message(request.user, glist, \
                    request.POST['search'])

    # Getアクセス時の処理
    else:
        # フォームの用意
        searchform = SearchForm()
        checkform = GroupCheckForm(request.user)
        # Groupのリストを取得
        gps = Group.objects.filter(owner=request.user)
        glist = [public_group]
        for item in gps:
                glist.append(item)
        # Messageの取得
        messages = get_your_group_message(request.user, glist, None)

    # 共通の処理
    params = {
        'login_user':request.user,
        'contents':messages,
        'check_form':checkform,
        'search_form':searchform,
    }

    return render(request, 'sns/index.html', params)


def get_public():
    public_user = User.objects.filter(username='public').first()
    public_group = Group.objects.filter(owner=public_user).first()
    
    return (public_user, public_group)


def get_your_group_message(owner, glist, find):
    # public userを取得
    (public_user, public_group) = get_public()
    # チェックされたGroupの取得
    groups = Group.objects.filter(Q(owner=owner) \
            | Q(owner=public_user)).filter(title__in=glist)
    # Groupに含まれるFriendの取得
    me_friends = Friend.objects.filter(group__in=groups)
    # FriendのUserをリストにまとめる
    me_users = []
    for f in me_friends:
        me_users.append(f.user)
    # UserリストのUserが作ったGroupの取得
    his_groups = Group.objects.filter(owner__in=me_users)
    his_friends = Friend.objects.filter(user=owner) \
            .filter(group__in=his_groups)
    me_groups = []
    for hf in his_friends:
        me_groups.append(hf.group)
    # groupがgroupsに含まれるか, me_groupsに含まれるMessageの取得
    if find == None:
        messages = Message.objects.filter(Q(group__in=groups) \
            | Q(group__in=me_groups))[:100]
    else:
        messages = Message.objects.filter(Q(group__in=groups) \
            | Q(group__in=me_groups)).filter(content__contains=find)[:100]

    return messages