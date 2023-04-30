from flask import Flask, render_template, redirect, request
from forms.user import RegisterForm, LoginForm
from data.users import User
from data.games import Game

from config import key
from data import db_session


app = Flask(__name__)
app.config['SECRET_KEY'] = key


games = [
    Game(title="Portal", price=200, genre="Puzzle", studio="Valve Interactive",
         about='''Portal — компьютерная игра в жанре головоломки от первого лица, 
         разработанная американской компанией Valve Corporation. События игры разворачиваются во вселенной Half-Life, 
         в Лаборатории исследования природы порталов (Aperture Science). 
         Игрок выступает в роли девушки по имени Челл, которая проходит испытания внутри этой Лаборатории. 
         Игровой процесс основан на решении головоломок при помощи переносного устройства, 
         позволяющего создавать на плоских поверхностях «порталы» — два связанных разрыва материи, 
         через которые можно мгновенно перемещаться в пространстве самому или переносить предметы'''),
    Game(title="Ведьмак 3: Дикая Охота", price=500, genre="RPG", studio="CD Projekt RED",
         about='''Ведьмак 3: Дикая Охота - компьютерная игра в жанре action/RPG, разработанная польской студией 
         CD Projekt RED. Выпущенная 19 мая 2015 года на Windows, PlayStation 4 и Xbox One. Является продолжением 
         игр «Ведьмак» (2007) и «Ведьмак 2: Убийцы королей» (2011). Это третья игра, действие которой 
         происходит в литературной вселенной книжной серии «Ведьмак», 
         созданной польским писателем Анджеем Сапковским, а также последняя, которая повествует 
         о приключениях Геральта из Ривии. Игра в стиле фэнтези, мир которой основан на славянской 
         мифологии, повествует о ведьмаке Геральте из Ривии, охотнике на чудовищ, чья приёмная дочь Цири 
         находится в опасности, будучи преследуемой Дикой Охотой — загадочной потусторонней силой, 
         тайна которой раскрывается по ходу игры.Перейти к разделу «#Сюжет» Многие детали сюжета отсылают 
         к книгам, написанным Сапковским, но сюжет остаётся связанным с первыми двумя частями и 
         подводит итог трилогии, начатой первой игрой, вышедшей восемью годами ранее. 
         В отличие от предыдущих игр, действие «Ведьмака 3» происходит в открытом мире и фокусируется на 
         использовании боевых и детективных навыков Геральта для выполнения заказов и изучения окружающей среды.'''),
    Game(title="The Elder Scrolls V: Skyrim", price=700, genre="RPG", studio="Bethesda Game Studios",
         about='''The Elder Scrolls V: Skyrim  — компьютерная игра в жанре action/RPG с открытым миром, 
         разработанная студией Bethesda Game Studios и выпущенная компанией Bethesda Softworks. 
         Это пятая часть в серии The Elder Scrolls. Подобно предыдущим играм серии, Skyrim предоставляет
         игроку возможность свободно путешествовать по обширному игровому миру, исследуя его и 
         самостоятельно находя новые места и задания. Сюжет игры в жанре классического фэнтези использует
         мотивы скандинавской мифологии, а также понятия и атрибутику эпохи викингов.
         Действие происходит в провинции Скайрим на материке Тамриэль, что на планете Нирн спустя 
         двести лет после событий предыдущей игры серии — The Elder Scrolls IV: Oblivion. 
         Основная сюжетная линия игры связана с появлением в Скайриме могущественного дракона Алдуина; 
         на главного героя, «Драконорождённого», возложена задача остановить 
         возвращение драконов и сразить Алдуина.'''),
    Game(title="Elden Ring", price=2000, genre="Souls-like", studio="From Software",
         about='''Elden Ring — компьютерная игра в жанре action/RPG с открытым миром, 
         разработанная японской компанией FromSoftware и изданная компанией Bandai Namco Entertainment 
         для платформ Windows, PlayStation 4, PlayStation 5, Xbox One и Xbox Series X/S. 
         Руководителем разработки игры является Хидэтака Миядзаки, а американский писатель Джордж Мартин, 
         известный по циклу книг «Песнь льда и огня», выступил консультантом и соавтором сценария'''),
    Game(title="Дота 2", price=0, genre="MOBA", studio="Valve Interactive",
         about='''Игра про мелких речных раков''')
         ]


@app.route("/", methods=["GET", "POST"])
@app.route("/main")
def main_page():
    log = request.form.get('login')
    reg = request.form.get('registrate')
    if log:
        return redirect("/sign_in")
    elif reg:
        return redirect("/sign_up")
    return render_template("main.html", title="Приветственная страница")


@app.route("/sign_in", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.name.data not in [user.name for user in db_sess.query(User).all()]:
            return render_template("sign_in.html", title='Вход в аккаунт',
                                   form=form, message="Такого пользователя не существует")
        us = db_sess.query(User).filter(User.name == form.name.data)
        for u in us:
            if u.check_password(form.password.data):
                return redirect('/shop_page')
        user = db_sess.query(User).filter(User.name == form.name.data, User.hashed_password == form.password.data)
        return render_template("sign_in.html", title='Вход в аккаунт',
                               form=form, message="Неправильный пароль")
    return render_template("sign_in.html", title='Вход в аккаунт', form=form)


@app.route("/sign_up", methods=['GET', 'POST'])
def registrate():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('sign_up.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('sign_up.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/shop_page')
    return render_template('sign_up.html', title='Регистрация', form=form)


@app.route("/shop_page")
def shop_page():
    return render_template('shop.html', title='Регистрация', games=db_sess.query(Game).all())


if __name__ == "__main__":
    db_session.global_init("db/games_shop.sqlite")
    db_sess = db_session.create_session()

    for game in games:
        db_sess.add(game)
    db_sess.commit()

    app.run(port=8080, host='127.0.0.1')
