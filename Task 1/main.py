import traceback
import re

# Задание 1

class TestRunner(object):
    def __init__(self, name):
        self.name = name
        self.testNo = 1

    def expectTrue(self, cond):
        try:
            if cond():
                self._pass()
            else:
                self._fail()
        except Exception as e:
            self._fail(e)

    def expectFalse(self, cond):
        self.expectTrue(lambda: not cond())

    def expectException(self, block):
        try:
            block()
            self._fail()
        except:
            self._pass()

    def _fail(self, e=None):
        print(f'FAILED: Test  # {self.testNo} of {self.name}')
        self.testNo += 1
        if e is not None:
            traceback.print_tb(e.__traceback__)

    def _pass(self):
        print(f'PASSED: Test  # {self.testNo} of {self.name}')
        self.testNo += 1


def is_pattern(pattern):
    if not re.match("^[ad *|]+$", pattern):
        raise Exception('Неверный паттерн')


def match(string, pattern):
    is_pattern(pattern)

    if not len(string) == len(pattern):
        return False

    for index in range(len(pattern)):
        if pattern[index] == 'a':
            if not string[index].islower():
                return False
        elif pattern[index] == 'd':
            if not string[index].isdigit():
                return False
        elif pattern[index] == '*':
            if not (string[index].isdigit() or string[index].islower()):
                return False
        elif pattern[index] == ' ':
            if not string[index] == ' ':
                return False
    return True


def testMatch():
    runner = TestRunner('match')

    runner.expectFalse(lambda: match('xy', 'a'))
    runner.expectFalse(lambda: match('x', 'd'))
    runner.expectFalse(lambda: match('0', 'a'))
    runner.expectFalse(lambda: match('*', ' '))
    runner.expectFalse(lambda: match(' ',  'a'))

    runner.expectTrue(lambda:  match('01 xy', 'dd aa'))
    runner.expectTrue(lambda: match('1x', '**'))

    runner.expectException(lambda:  match('x', 'w'))

# Задание 2

tasks = {
    'id': 0,
    'name': 'Все задачи',
    'children': [
        {
            'id': 1,
            'name': 'Разработка',
            'children': [
                {'id': 2, 'name': 'Планирование разработок', 'priority': 1},
                {'id': 3, 'name': 'Подготовка релиза', 'priority': 4},
                {'id': 4, 'name': 'Оптимизация', 'priority': 2},
            ],
        },
        {
            'id': 5,
            'name': 'Тестирование',
            'children': [
                {
                    'id': 6,
                    'name': 'Ручное тестирование',
                    'children': [
                        {'id': 7, 'name': 'Составление тест-планов', 'priority': 3},
                        {'id': 8, 'name': 'Выполнение тестов', 'priority': 6},
                    ],
                },
                {
                    'id': 9,
                    'name': 'Автоматическое тестирование',
                    'children': [
                        {'id': 10, 'name': 'Составление тест-планов', 'priority': 3},
                        {'id': 11, 'name': 'Написание тестов', 'priority': 3},
                    ],
                },
            ],
        },
        {'id': 12, 'name': 'Аналитика', 'children': []},
    ],
}


def find_group(tasks, groupId, group):
    """Функция находит группу с id = groupId"""
    if tasks['id'] == groupId:
        if tasks.get('children') is not None:
            if len(tasks['children']) != 0:
                group.append(tasks)
            else:
                group.append(None)
        else:
            raise Exception("Группа является задачей")
    elif tasks.get('children') is not None:
        for task in tasks['children']:
            find_group(task, groupId, group)
    return group


def find_all_tasks(group, task_list):
    """Функция находит все задачи в группе"""
    for task in group:
        if task.get('children') is None:
            task_list.append(task)
        else:
             find_all_tasks(task['children'], task_list)

    return task_list


def max_task_priority(group):
    """Функция находит задачу с масимальным приоритетом в группе"""
    task_list = find_all_tasks(group, [])
    return sorted(task_list, key=lambda task: task['priority'], reverse=True)[0]


def findTaskHavingMaxPriorityInGroup(tasks, groupId):
    """Функция находит задачу с масимальным приоритетом в группе с id = groupId"""
    group = find_group(tasks, groupId, [])

    if len(group) == 0:
        raise Exception('Данной группы не существует')
    if group[0] is None:
        return None

    return max_task_priority(group)


def taskEquals(a, b):
    return (
        not 'children' in a and
        not 'children' in b and
        a['id'] == b['id'] and
        a['name'] == b['name'] and
        a['priority'] == b['priority']
    )


def testFindTaskHavingMaxPriorityInGroup():
    runner = TestRunner('findTaskHavingMaxPriorityInGroup')

    runner.expectException(lambda: findTaskHavingMaxPriorityInGroup(tasks, 13))
    runner.expectException(lambda: findTaskHavingMaxPriorityInGroup(tasks, 2))

    runner.expectTrue(lambda: findTaskHavingMaxPriorityInGroup(tasks, 12) is None)

    runner.expectTrue(lambda: taskEquals(findTaskHavingMaxPriorityInGroup(tasks, 0), {
        'id': 8,
        'name': 'Выполнение тестов',
        'priority': 6,
    }))
    runner.expectTrue(lambda: taskEquals(findTaskHavingMaxPriorityInGroup(tasks, 1), {
        'id': 3,
        'name': 'Подготовка релиза',
        'priority': 4,
    }))

    runner.expectTrue(lambda: findTaskHavingMaxPriorityInGroup(tasks, 9)['priority'] == 3)

# Запуск тестов
testMatch()
testFindTaskHavingMaxPriorityInGroup()




