from lib.http import render_json

# Create your views here.
def get_rcmd_users(request):
    '''获取推荐列表'''
    return render_json(None)

def like(request):
    '''喜欢'''
    return render_json(None)

def superlike(request):
    '''超级喜欢'''
    return render_json(None)

def dislike(request):
    '''不喜欢'''
    return render_json(None)

def rewind(request):
    '''反悔'''
    return render_json(None)

def show_liked_me(request):
    '''获取谁喜欢我'''
    return render_json(None)