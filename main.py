import json
import sys
from multiprocessing import Pool, cpu_count
from pathlib import Path

from jsonschema import validate

from student import Student


def main():
    # 対象となる回の提出物ディレクトリを絶対パスで指定
    if len(sys.argv) < 2:
        print("Error : 引数が足りません。対象となるディレクトリのパスを与えてください")
        exit(1)

    target_dir_path = Path(sys.argv[1])

    # 指定されたパスが存在するディレクトリか確認
    if not target_dir_path.is_dir():
        # カレントディレクトリ内に存在するディレクトリか確認
        tmp = target_dir_path.absolute()
        if tmp.is_dir():
            target_dir_path = tmp
        else:
            print("Error : 指定したディレクトリを発見できません")
            exit(1)

    target_dir_path = target_dir_path.resolve()

    # settings.jsonは対象の回の提出物ディレクトリ内に配置
    settings_file_name = "settings.json"
    settings_file_path = Path(target_dir_path, settings_file_name)
    jsonschema_file_name = "json-schema.json"
    jsonschema_path = Path(Path(__file__).parent, jsonschema_file_name)

    if not settings_file_path.is_file():
        print(f"Error : {target_dir_path} 内に {settings_file_name} が存在しません")
        exit(1)

    if not jsonschema_path.is_file():
        print(f"Error : {target_dir_path} 内に {settings_file_name} が存在しません")
        exit(1)

    try:
        with open(settings_file_path) as f:
            settings: dict = json.load(f)
        with open(jsonschema_path) as f:
            schema = json.load(f)
        validate(instance=settings, schema=schema)
    except Exception as e:
        print(f"Error : {settings_file_name} 解析時にエラーが発生しました\n{e}")
        exit(1)

    print("採点中...")
    student_dir_paths = [stu for stu in target_dir_path.iterdir() if stu.is_dir()]
    stu_vals = [(settings, stu) for stu in student_dir_paths]

    with Pool(cpu_count()) as pool:
        students = pool.map(exec_stu, stu_vals)

    with open(
        Path(target_dir_path, "result.txt"),
        "w",
        encoding="utf-8",
    ) as f:
        students.sort(key=lambda stu: stu.user)
        for stu in students:
            f.write(stu.result)
    print("採点終了")


def exec_stu(values: tuple[dict, Path]):
    settings, stu_path = values
    stu: Student = Student(stu_path, settings)
    stu.set_answers()
    stu.get_results()
    return stu


if __name__ == "__main__":
    main()
