from nullaLowLevel import core
import getpass

class Comment():
    def __init__(self, post, author, content):
        self.post = post
        while len(self.post) < 35:
            self.post = self.post + ' '
        self.post = self.post + '||'

        self.author = author
        while len(self.author) < 30:
            self.author = self.author + ' '
        self.author = self.author + '||'

        self.content = content

def help():
    print('help - отображает все команды и их описание')
    print('comments - отображает комментарии к недавним постам')
    print('exit - выход из админки')

def comments():
    print('Сбор постов')
    posts = core.get_recent_posts()
    endlen = len(posts.blogId)
    comments_table = []
    for ident in range(0, endlen):
        print('Организация комментариев в посте ' + str(ident+1))
        name = posts.title[ident]
        if name == None:
            name = 'Пост без имени'
        comments = core.get_comments(posts.blogId[ident])
        sublen = len(comments.content)
        if comments.content != []:
            for subtent in range(0, sublen):
                comments_table.append(Comment(name, comments.author.nickname[subtent], comments.content[subtent]))

    print('Пост                               ||Автор                       ||Содержание')
    for comment in comments_table:
        print(comment.post + comment.author + comment.content)

def exit():
    core.stop()

print('Запуск')        
core.start()

email = input('Логин: ')
password = getpass.getpass(prompt='Пароль: ')
core.login(email, password)

print('Вход в сообщество')
communities = core.get_communities()
core.enter_community(communities[0][1])

print('Вход успешен')
print('Ожидание комманд')

comd = ''
while comd != 'exit':
    comd = input()
    try:
        eval(comd + '()')

    except NameError:
        print('Такой команды нет')
