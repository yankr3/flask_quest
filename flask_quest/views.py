from . import app
from flask import request, render_template, flash, redirect, url_for
from .projects.forms import StartForm, FinishForm, GameForm
from .text_game import TextQuest

global gamer


@app.route('/', methods=['GET', 'POST'])
def index():
    global gamer
    form = StartForm()
    if request.method == "POST" and form.validate_on_submit():
        # Создаем экземпляр класса, чтоб начать игру заново
        TextQuest(True)
        gamer = form.gamer_name.data
        return redirect(url_for("game", finish=0))
    return render_template('index.html', form=form)


@app.route('/game/<int:finish>', methods=['GET', 'POST'])
def game(finish=0):
    global gamer

    game_class = TextQuest()
    game_form = GameForm()

    # Проверяем не закончена ли игра
    if finish:
        finish_form = FinishForm()
        if request.method == "POST" and finish_form.validate_on_submit():
            return redirect(url_for('index'))
        # Защищаем сервер от попытки сразу перейти на финишную форму, без инициализации Имени игрока
        if game_class.moves <= 0:
            return redirect(url_for('index'))
        return render_template("endgame.html",
                               gamer=gamer,
                               moves=game_class.moves,
                               endgame_text=game_class.end_text(),
                               form=finish_form)

    # Если игра только началась, выводим привественные сообщения
    if game_class.moves == -1:
        flash("Добро пожаловать в игру", "primary")
        flash(game_class.start_text(), "success")
        game_class.moves = 0

    # Обрабатываем команды игрока
    if request.method == "POST" and game_form.validate_on_submit():
        for move in range(game_form.moves.data):
            # Двигаем персонажа и выдаем сообщение
            move_data = game_class.move(game_form.direction.data)
            if move_data == 1:
                flash(f"{game_class.get_room_decs()}{game_class.check_visited()}", "success")
            elif move_data == 2:
                flash(game_class.wrong_move_text(), 'danger')
                break
            elif move_data == 3:
                return redirect(url_for("game", finish=1))
    return render_template('game.html', form=game_form)
