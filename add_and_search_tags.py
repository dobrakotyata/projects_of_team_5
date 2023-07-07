class Note: # Для представления заметки с заголовком, содержимым и тегами
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.tags = []

    def add_tag(self, tag):
        self.tags.append(tag)

    def has_tag(self, tag):
        return tag in self.tags


class NoteManager: # Для управления заметками, включая добавление и поиск заметок по тегам, а также сортировку заметок по тегам.
    def __init__(self):
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

    def search_notes_by_tag(self, tag):
        matching_notes = []
        for note in self.notes:
            if note.has_tag(tag):
                matching_notes.append(note)
        return matching_notes

    def sort_notes_by_tag(self):
        return sorted(self.notes, key=lambda note: note.tags)

"""

Пример использования

Создание заметок
note1 = Note("Заметка 1", "Содержимое заметки 1")
note2 = Note("Заметка 2", "Содержимое заметки 2")
note3 = Note("Заметка 3", "Содержимое заметки 3")

Добавление тегов к заметкам
note1.add_tag("python")
note1.add_tag("programming")

note2.add_tag("java")
note2.add_tag("programming")

note3.add_tag("python")
note3.add_tag("data science")

Создание менеджера заметок и добавление заметок
note_manager = NoteManager()
note_manager.add_note(note1)
note_manager.add_note(note2)
note_manager.add_note(note3)

Поиск заметок по тегу
matching_notes = note_manager.search_notes_by_tag("python")
for note in matching_notes:
    print(f"Заметка с тегом 'python': {note.title}")

Сортировка заметок по тегам
sorted_notes = note_manager.sort_notes_by_tag()
for note in sorted_notes:
    print(f"Заметка с тегами: {note.title} - {note.tags}")

"""