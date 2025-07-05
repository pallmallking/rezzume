class Section:
    def __init__(self, title, content="", tags=None):
        self.title = title
        self.content = content
        self.tags = tags or {}

class SectionManager:
    def __init__(self):
        self.sections = []

    def add(self, title):
        self.sections.append(Section(title))

    def remove(self, idx):
        if 0 <= idx < len(self.sections):
            del self.sections[idx]

    def get_content(self, idx):
        if 0 <= idx < len(self.sections):
            s = self.sections[idx]
            return s.content, s.tags
        return "", {}

    def set_content(self, idx, content, tags):
        if 0 <= idx < len(self.sections):
            self.sections[idx].content = content
            self.sections[idx].tags = tags

    def get_all(self):
        return [(s.title, s.content, s.tags) for s in self.sections]

    def clear(self):
        self.sections = []