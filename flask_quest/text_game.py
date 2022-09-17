from threading import Lock


# Кдасс для создания только одного экземпляра класса во всей программе
# Локеры блокируют доступ к объектам, если с ними уже работает поток
class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    # Метод создает экземпляр класса с новыми параметрами, заменяя предыдущий экземпляр
    def __call__(cls, *args, **kwargs):
        with cls._lock:
            # Новый экземпляр создается только при первом вызове или передачи параметра в конструктор.
            # Это требуется для пезапуска игры без перезапуска сервера.
            if cls not in cls._instances or args or kwargs:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


# Класс описывает сам квест
class TextQuest(metaclass=SingletonMeta):
    def __init__(self, new=False):
        # Начальная позиция игрока
        self._horizontal_position = 0
        self._vertical_position = 1
        # Счетчик перемещений
        self.moves = -1
        # Карта помещений, где вы уже были
        self._rooms_map = [[0 for y in range(2)] for x in range(3)]
        self._rooms_map[self._horizontal_position][self._vertical_position] = 1
        # Описания помещений
        self._rooms_desc = (
            ("Вы входите в кладовку. Это темное холодное помещение. Практически все стены вокруг " \
             "заставлены стеллажами. На полках стеллажей вы видите большое количество колб и склянок" \
             " с разноцветными жидкостями, засушеные листья и коренья, старые потрепанные книги и" \
             " записки. Стеллажи простираются высоко вверх, верхних полок практически не видно. Вы" \
             " слишите ужасное громкое рачание и скрежет когтей. " \
             "Возможно, кто-то выбрался из того самого разлома. Вы быстро осматриваетесь и замечаете дверь на востоке и юге. " \
             "А, может, рычание доносится именно оттуда?! Скорее! Куда вы пойдете?",
             "Вы попадаете в подземелье, в углу справа от Вас вы замечаете череп и кости. Знак явно не добрый..."),
            (
                "Вы оказываетесь в большой комнате. Здесь относительно много света, вокруг на стенах расположились несколько киросиновых ламп. " \
                "В середине комнаты вы замечаете огромный котел. Кажется, из него можно накормить человек 20, " \
                "если человек вообще может съесть содержимое - в котле кипит и булькает темная густая маслянистая жидкость. " \
                "Вы чувствуете ужасный аммиачный запах и Вам становится не по себе. Видимо, вы попали на кухню, если это место можно так назвать." \
                "С северной стороны вы замечаете деревянную низкую дверцу, перед ней сидит крыса. Она замечает Вас, поворачивается и исчезает" \
                " между сколоченных в единое дверное полотно гнилых досок. Вы смотрите ей вслед и в ту же секунду за той самой дверцей " \
                "раздается жалобный крысиный писк и какой-то хруст. С каждой стороны есть двери. Они кажутся более дружелюбными. Куда пойдете?",
                "Вы оказываетесь в длинном прохладном коридоре. Кажется, когда-то здесь был выход на улицу, потому что вы видите большую входную дверь, " \
                "но она заколочена, как и окна, которые расположились справа и слева от нее. На двери много паутины, и, кажется, вы замечаете огромного " \
                "с человеческую голову паука. Или это не паук?.. В общем, через эту дверь не выйти.. Впрочем, вы замечаете двери с каждой стороны. Куда пойдете?"),
            (
                "Вы попали в помещение похожее на гостинную. Здесь есть большой диван, несколько кресел и стульев. Но один стул необычный, вы замечаете, " \
                "что к ручкам и ножкам стула пределаны ремни с застежками, а вокруг стула какие-то темные разводы. Вы замечаете на дальней стене окно, " \
                "оно наполовину занавешено, за окном темно. Как только вы решаетесь подойти к нему, в окне появляется пара желтых глаз и раздается рык. " \
                "Вам хочется поскорее покинуть это место, это чувство Вас часто посещает последнее время. В южной части и западной частях Вы замечаете дверь, пойдете туда?" \
                "Может, лучше назад?",
                "В комнате очень темно, вы вглядываетесь в темноту, похоже, вы замечаете кровать, вам кажется, что на ней кто-то лежит, Вы решаете, что " \
                "нужно скорее уйти, пока Вы еще можете это сделать. Стоп! Но куда? На запад или на север?.")
        )

    def end_text(self):
        return "Вы садитесь на корточки, ногой выбиваете старую дверь и ползком пробираетесь сквозь длинный сырой туннель. " \
               "Вы как-будто бы начинаете чувствовать запах свежего воздуха и видеть какой-то свет, но ваш восторг от скорого вызволения из этого кошмара " \
               "прерывает чей-то громкий вой. Вы на мгновенье замираете, но решаете, что обратно вы не вернетесь, что хуже уже не будет. " \
               "Вы ускоряетесь и скоро достигаете конца туннеля. Вы оказываетесь на заднем дворе какого-то старого дома или замка. " \
               "Вы встаете в полный рост, отряхиваетесь. Перед Вами ночное старое кладбище," \
               " которое освещает полная луна. Справа вы слышите шелест листвы, поворачиваетесь и замечате два желтых глаза из темноты и злобное рычание. Что ж.. Бегите..."

    def check_visited(self):
        if self._rooms_map[self._horizontal_position][self._vertical_position] == 1:
            return " Ваше сознание туманно, вы никак не можете прийти в себя, но Вам кажется, что вы здесь уже были."
        else:
            self._rooms_map[self._horizontal_position][self._vertical_position] = 1
            return ""

    def get_room_decs(self):
        return self._rooms_desc[self._horizontal_position][self._vertical_position]

    def move(self, direction):
        # Сначала проверим на прибытие в точку
        if direction == 0 and self._horizontal_position == 1 and self._vertical_position == 0:
            return 3
        # Проверяем можно ли туда двигаться
        if (direction == 0 and self._vertical_position == 0) or \
                (direction == 1 and self._horizontal_position == 2) or \
                (direction == 2 and self._vertical_position == 1) or \
                (direction == 3 and self._horizontal_position == 0):
            return 2
        # Раз можем, то двигаемся
        if direction == 0:
            self._vertical_position -= 1
        elif direction == 1:
            self._horizontal_position += 1
        elif direction == 2:
            self._vertical_position += 1
        elif direction == 3:
            self._horizontal_position -= 1
        self.moves += 1
        return 1

    def wrong_move_text(self):
        return "Вы упираетесь в стену, дальше идти нельзя."

    def start_text(self):
        return "Вы просыпаетесь на полу в непонятном промещении без окон. " \
               "Вы видите гигантский разлом в земле, в котором пляшут зловещие языки пламени. " \
               "Воздух здесь очень душный и насквозь пропитан запахом серы. Похоже вы в каком-то мрачном подземелье. " \
               "Вам повезло и вы замечаете, что в помещении имеются две лестницы, " \
               "ведущие куда-то наверх к дверям на севере и востоке Вашей темницы. " \
               "Дверь в северной части затянута паутиной, а каменная лестница потрескалась от старости " \
               "Путь к восточной двери, напротив, освещен горящими киросиновыми лампами, лестница выглядит надежной, " \
               "похоже, что ей часто пользуются. Вы слышите из разлома какой-то непонятный гул" \
               " и понимаете, что нужно срочно убираться прочь. Куда вы пойдете?"