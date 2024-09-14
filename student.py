from pathlib import Path

from answer import Answer


class Student:
    def __init__(self, student_dir_path: Path, settings: dict) -> None:
        self.dir_path = student_dir_path
        self.user = self.dir_path.name  # .split("@")[0]
        self.answers: list[Answer] = []
        self.tasks: list[dict] = settings["tasks"]
        self.not_exist_tasks: list[str] = []
        self.result: str = ""

    def set_answers(self):
        ans_paths = list(self.dir_path.iterdir())
        for task in self.tasks:
            for p in ans_paths:
                if task["name"] == p.name:
                    self.answers.append(Answer(p, task))
                    break
            else:
                self.not_exist_tasks.append(task["name"])

    def get_results(self):
        self.result += (
            f"{' USER : ' + self.user + ' ':#^70}\n\n"
            f"課題ファイル無し or 名前ミス : {', '.join(self.not_exist_tasks) if len(self.not_exist_tasks)>0 else 'ミスしているファイルはありません'}\n\n"
        )

        for ans in self.answers:
            ans.get_code()
            ans.execute()
            self.result += (
                f"{' 課題 : ' + ans.task_name + ' ':=^70}\n\n"
                f"FILE LIST : {ans.file_list}\n\n"
                f"{' コード ':-^70}\n\n"
                f"{ans.code_txt}\n\n"
                f"{' 実行結果 ' + ans.task_name + ' ':-^70}\n\n"
                f"{ans.result_txt}\n\n"
            )
        print(f"FINISH : {self.user}")
