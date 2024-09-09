import glob
import json
import multiprocessing
from os import path

from student import Student


def main():
    # settings.jsonと対象の回の提出物ディレクトリはinput内に配置
    settings_file_name = "settings.json"

    proj_dir_abs_path = path.dirname(path.abspath(__file__))
    input_dir_abs_path = path.join(proj_dir_abs_path, "input")
    output_dir_abs_path = path.join(proj_dir_abs_path, "output")
    settings_abs_path = path.join(input_dir_abs_path, settings_file_name)

    if not path.exists(settings_abs_path):
        print(f"対象フォルダ内に {settings_file_name} が存在しません")
        exit(1)

    try:
        with open(settings_abs_path) as f:
            settings = json.load(f)
    except Exception as e:
        print(f"{settings_file_name} 解析時にエラーが発生しました\n{e}")
        exit(1)

    student_dir_paths = glob.glob(
        path.join(input_dir_abs_path, settings["target"], "**") + "/"
    )
    students: list[Student] = []

    print("採点中...")
    for stu_path in student_dir_paths:
        students.append(Student(stu_path, settings))
    with open(
        path.join(output_dir_abs_path, f"result-{settings['target']}.txt"),
        "w",
        encoding="utf-8",
    ) as f:
        for stu in students:
            stu.set_answers()
            stu.get_results()
            f.write(stu.result)
    print("採点終了")


if __name__ == "__main__":
    main()
