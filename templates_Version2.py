TEMPLATES = {
    "Modern": [
        {"title": "Contact Information", "content": ""},
        {"title": "Summary", "content": ""},
        {"title": "Work Experience", "content": ""},
        {"title": "Education", "content": ""},
        {"title": "Skills", "content": ""},
    ],
    "Classic": [
        {"title": "Name & Contact", "content": ""},
        {"title": "Objective", "content": ""},
        {"title": "Experience", "content": ""},
        {"title": "Education", "content": ""},
        {"title": "References", "content": ""},
    ],
    # Add more templates as desired
}

def get_template(name):
    return TEMPLATES.get(name, [])