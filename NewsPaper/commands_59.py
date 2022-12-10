from news.models import *

# создание пользователей
for _ in ['Ann', 'Jack']: NewsUser.objects.create_user(_)

# создание авторов
for _ in NewsUser.objects.all(): Author.objects.create(user=_)

# создание категорий
for _ in ['politics', 'animals', 'art', 'cosmos']: Category.objects.create(title=_)

# статья 1
_author = Author.objects.get(pk=1)
_type = Post.article
_title = '''Плюралистический социализм: правовое государство или легитимность власти?'''
_content = '''Как уже подчеркивалось, политическое учение Монтескье верифицирует кризис легитимности. Конституционная демократия, однако, ограничивает субъект политического процесса. Социализм неизбежен. Понятие политического конфликта, согласно традиционным представлениям, означает политический процесс в современной России.

В постмодернистской перспективе глобализация формирует марксизм. Политическое учение Платона интегрирует антропологический феномен толпы. Кризис легитимности определяет гносеологический субъект власти. Авторитаризм неравномерен.

Конституционная демократия иллюстрирует субъект политического процесса. Понятие политического участия определяет гносеологический постиндустриализм. Понятие модернизации случайно.'''
_post1 = Post.objects.create(author=_author, type=_type, title=_title, content=_content)

# категории статьи 1
_post1.categories.add(Category.objects.get(pk=1))
_post1.categories.add(Category.objects.get(pk=4))

# статья 2
_author = Author.objects.get(pk=2)
_type = Post.article
_title = '''Пахотный гумус: предпосылки и развитие'''
_content = '''Траншея растягивает внутрипочвенный латерит, однозначно свидетельствуя о неустойчивости процесса в целом. В лабораторных условиях было установлено, что эвапотранспирация параллельна. С другой стороны, определение содержания в почве железа по Тамму показало, что гранулометрический анализ окисляет подпахотный педон. Восстановление, если принять во внимание воздействие фактора времени, окисляет осадочный карбонат кальция в полном соответствии с законом Дарси. В ходе почвенно-мелиоративного исследования территории было установлено, что подбур двумерно возникает упруго-пластичный бюкс, хотя этот факт нуждается в дальнейшей тщательной экспериментальной проверке.

В ходе почвенно-мелиоративного исследования территории было установлено, что гумус теоретически возможен. Рендзина параллельна. Промерзание охлаждает лесной солеперенос даже в том случае, если непосредственное наблюдение этого явления затруднительно.

При прочих равных условиях чизелевание растягивает желтозём. Скелетана когерентна. Сушильный шкаф по определению интуитивно понятен. Определение количественно растягивает мозаичный гончарный дренаж.'''
_post2 = Post.objects.create(author=_author, type=_type, title=_title, content=_content)

# категории статьи 2
_post2.categories.add(Category.objects.get(pk=2))
_post2.categories.add(Category.objects.get(pk=3))

# новость 1
_author = Author.objects.get(pk=1)
_type = Post.news
_title = '''Выставка современного искусства'''
_content = '''Выставка современного искусства «В поисках утраченного времени» открылась в Нижегородском государственном выставочном комплексе.

На выставке один экспонат, на котором написано: "Нарисовано в 2007 году, нарисовано с помощью компьютера".'''
_post3 = Post.objects.create(author=_author, type=_type, title=_title, content=_content)

# категории новости 1
_post3.categories.add(Category.objects.get(pk=3))

#комментарии
_user = NewsUser.objects.get(pk=2)
_content = '''У Балабобы нет своего мнения или знания.'''
_comment1 = Comment.objects.create(post=_post1, user=_user, content=_content)

_user = NewsUser.objects.get(pk=2)
_content = '''Он умеет только подражать — писать тексты так, чтобы они были максимально похожи на реальные тексты из интернета.'''
_comment2 = Comment.objects.create(post=_post1, user=_user, content=_content)

_user = NewsUser.objects.get(pk=1)
_content = '''Здесь YaLM используется для развлечения.'''
_comment3 = Comment.objects.create(post=_post2, user=_user, content=_content)

_user = NewsUser.objects.get(pk=1)
_content = '''с помощью нейросетей семейства YaLM можно продолжать тексты на любую тему, сохраняя связность и заданный стиль.'''
_comment4 = Comment.objects.create(post=_post3, user=_user, content=_content)

# лайки-дизлайки
_post1.like()
_post1.like()
_post1.dislike()
_post2.dislike()
_post3.like()

_comment1.like()
_comment1.like()
_comment1.like()
_comment2.dislike()
_comment2.dislike()
_comment3.like()
_comment4.like()

# рейтинги авторов
for _ in Author.objects.all(): _.update_rating()

# лучший пользователь
_top_author = Author.objects.all().order_by('-rating').first()
print(_top_author.user.username, _top_author.rating)

# лучшая статья
_top_post = Post.objects.all().order_by('-rating').first()
print(
    _top_post.create_ts,
    _top_post.author.user.username,
    _top_post.title,
    _top_post.preview()
)

# комментарии к лучшей статье
for _ in Comment.objects.filter(post=_top_post):
    print(
        _.create_ts,
        _.user.username,
        _.rating,
        _.content
    )
