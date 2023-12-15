'''База рабочих'''
class Base_Work():
    '''класс базовой работы'''
    def __init__(self, task: str, quality: str, salary: int, id):
        self.task = task
        self.quality = quality
        self.salary = salary
        self.id = id

    def __str__(self):
        '''служебная строка'''
        return f'task: {self.task}, quality: {self.quality}, salary: {self.salary}, id: {self.id}'

    def get_task(self):
        '''функция для получения задания рабочего'''
        return self.task


class Work(Base_Work):
    '''класс обычной работы'''
    def __init__(self, task: str, quality: str, salary: int, id):
        super().__init__(task, quality, salary, id)


class Hourly_Work(Base_Work):
    '''класс почасовой работы'''
    def __init__(self, task: str, quality: str, salary: int, hours: int, id):
        super().__init__(task, quality, salary, id)
        self.hours = int(hours)
        self.salary = int(self.hours) * int(self.salary)


    def __str__(self):
        '''служебная строка'''
        return (f'task: {self.task}, quality: {self.quality}, salary: {self.salary},'
                f' id: {self.id}')


class Base_Worker():
    '''класс базового рабочего'''
    def __init__(self, status: str, name: str, surname: str, quality: str, id=0):
        self.status = status
        self.name = name
        self.surname = surname
        self.quality = quality
        self.id = id

    def __str__(self):
        '''служебная строка'''
        return (f'status: {self.status} name: {self.name},'
                f' surname: {self.surname}, quality: {self.quality},'
                f'id: {self.id}')

    def get_status(self):
        '''функция для получения статуса рабочего'''
        return self.status


class Hourly_Worker(Base_Worker):
    '''класс почасового рабочего'''
    def __init__(self, status: str, name: str, surname: str,
                 quality: str, id: int):
        super().__init__(status, name, surname, quality, id)


class Employee(Base_Worker):
    '''класс наёмного рабочего'''
    def __init__(self, status: str, name: str, surname: str,
                 quality: str, id: int):
        super().__init__(status, name, surname, quality, id)


menu = ('1 --> добавить рабочего\n'
        '2 --> удалить рабочего\n'
        '3 --> добавить работу\n'
        '4 --> удалить работу\n'
        '5 --> назначить работу работнику\n'
        '6 --> снять работника с работы\n'
        '7 --> вывод информации о работах\n'
        '8 --> вывод информации о сотрудниках')


class Departament():
    '''основной класс'''

    def __init__(self):
        self.workers = {
            -1: Base_Worker("free", "Roma", "Chort", "Employee", -1)
        }
        self.works = {
            -1: Work("писать (говно) код", "Employee", -1, -1)
        }

    def menu(self):
        '''функция меню'''
        id_counter = -1
        work_id = -1
        while True:
            print(menu)
            action = input()
            match action:
                case "1":
                    print('статус, имя, фамилия, квалификация(Hourly, Employee)')
                    worker = list(input().split())
                    id_counter += 1
                    worker.append(id_counter)
                    try:
                        worker = Base_Worker(*worker)
                        self.add_worker(worker, id_counter)
                        for i in self.workers:
                            print((self.workers[i]))
                    except TypeError:
                        print("--Вы ввели некоректные значения--\n")


                case "2":
                    print('введите id рабочего, которого нужно уволить')
                    try:
                        id_id = int(input())
                        self.del_worker(id_id)
                        for i in self.workers:
                            print((self.workers[i]))
                    except ValueError:
                        print('--вы ввели некорректное значение--\n')

                case "3":
                    work_id += 1
                    print('вакансия, квалификация, зарплата (если квалификация не равна "Hourly")\n'
                          'вакансия, квалификация, почасовая ставка, количество часов (в противном случае)')
                    work = list(input(">>> ").split())
                    work.append(work_id)
                    try:
                        if work[1] != 'Hourly':
                            work = Work(*work)
                            self.add_work(work, work_id)
                            for i in self.works:
                                print(self.works[i])
                        else:
                            work = Hourly_Work(*work)
                            self.add_work(work, work_id)
                            for i in self.works:
                                print(self.works[i])
                    except TypeError:
                        print('--вы ввели некорректное значение--\n')

                case "4":
                    print('введите id работы, которую нужно удалить')
                    try:
                        id_id = int(input())
                        if self.del_helper(id_id):
                            self.del_work(id_id)
                            for i in self.works:
                                print((self.works[i]))
                    except ValueError:
                        print('--вы ввели некорректное значение--\n')

                case '5':
                    print('введите id работы и id рабочего, которому нужно назначить работу')
                    try:
                        print('возможные работы:')
                        for i in self.works:
                            print(self.works[i])
                        print('возможные рабочие:')
                        for i in self.workers:
                            print(self.workers[i])
                        work_id, id_id = map(int, input().split())
                        check = self.check(work_id, id_id)
                        if check:
                            self.set_work(work_id, id_id)
                    except ValueError:
                        print('--вы ввели некорректное значение--\n')

                case '6':
                    print('введите id работы и рабочего, с которой его нужно снять')
                    try:
                        work_id, id_id = map(int, input().split())
                        self.diconect(work_id, id_id)
                    except ValueError:
                        print('--вы ввели некорректное значение--\n')

                case "7":
                    for i in self.works:
                        print(self.works[i])

                case '8':
                    for i in self.workers:
                        print(self.workers[i])

    def del_helper(self, work_id):
        '''помошник в удалении работы'''
        trigger_status = self.works[work_id].get_task()
        worker_counter = 0
        for i in self.workers:
            if self.workers[i].get_status() == trigger_status:
                worker_counter += 1
        if worker_counter == 0:
            return True
        else:
            print(f'на этой работу работают {worker_counter} сотрудников,'
                  f'вы уверены что хотите её удалить? (yes/no)')
            ans = input()
            if ans == 'yes':
                print('работа удалена, все сотрудники освобождены со своих должностей')
                for i in self.workers:
                    self.workers[i].status = 'free'
            else:
                return False

    def check(self, work_id, id):
        '''функция сверки id'''
        flag = True
        worker_quality = self.workers[id].quality
        work_quality = self.works[work_id].quality
        if work_quality == worker_quality:
            return flag
        else:
            flag = False
            print('квалификация рабочего не допустима для данного вида работы')
            return flag

    def add_work(self, work, work_id):
        '''функция добавления работы'''
        self.works.update(
            {
                work_id: work
            }
        )

    def del_worker(self, id):
        '''функция удаления работы'''
        del self.workers[id]

    def add_worker(self, worker, id_counter):
        '''функция добавления рабочего'''
        self.workers.update(
            {
                id_counter: worker
            }
        )

    def del_work(self, id):
        '''функция удаления работы'''
        del self.works[id]

    def set_work(self, work_id, id):
        '''функция назначения работнику работы'''
        cur_worker = self.workers[id]
        if cur_worker.status == 'free':
            cur_worker.status = self.works[work_id].get_task()
            print(f'работа: {self.works[work_id]}\n'
                  f'рабочий: {self.workers[id]}\n')
        else:
            print(f'рабочий уже работает здесь: {cur_worker.status} \n'
                  f'вы уверены, что хотите его переназначить? (yes, no)')
            ans = input()
            if ans == 'yes':
                cur_worker.status = self.works[work_id]
                print(cur_worker.status)
            else:
                pass

    def diconect(self, work_id, id):
        '''функция снятия рабочего с должности'''
        cur_worker = self.workers[id]
        cur_worker.status = 'free'
        print(cur_worker.status)


if __name__ == '__main__':
    departament = Departament()
    departament.menu()
