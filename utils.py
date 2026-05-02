
import json


def read_data():
    try:
        with open("course.json", "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        return []


def save_data(data):
    with open("course.json", "w") as fs:
        json.dump(data, fs, indent=4)


def get_next_id(data):
    if not data:
        return 1

    max_id = max(item["id"] for item in data)
    return max_id + 1


# def check_id_exists(data, course_id):
#     for item in data:
#         if item["id"] == course_id:
#             return True
#     return False


