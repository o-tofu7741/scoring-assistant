import os
import re
import subprocess
import zipfile
from pathlib import Path

from astyle_py import Astyle
from chardet import detect

# windowsとそれ以外だとコマンドの区切り文字が違うため...
if os.name == "nt":
    sep = ";"
else:
    sep = ":"


class Answer:
    def __init__(self, file_path: Path, task: dict) -> None:
        self.file_path: Path = file_path
        self.code_txt: str = ""
        self.result_txt: str = ""
        self.task_name: str = task["name"]
        self.task_lang: str = task["lang"]
        self.inputs: list[dict[str, str]] = task.get("inputs", [{"inputs_value": ""}])
        self.args: list[dict[str, list[str]]] = task.get("args", [{"args_value": []}])
        self.classpath: list[str] | None = task.get("classpath", None)
        if self.classpath is not None:
            self.classpath = [str(Path(cp).resolve()) for cp in self.classpath]
        self.file_list: list[str] = [self.task_name]

    def __str__(self) -> str:
        return (
            f"{self.file_path = }\n"
            f"{self.code_txt = }\n"
            f"{self.result_txt = }\n"
            f"{self.task_name = }\n"
            f"{self.task_lang = }\n"
            f"{self.inputs = }\n"
            f"{self.args = }\n"
            f"{self.file_list = }\n"
        )

    def get_code(self) -> str:
        """
        taskの言語に合わせて中身を取得
        jar,zipの場合は中身を展開する
        """
        try:
            if self.task_lang in ["jar", "zip"]:
                self.code_txt, f_list = unpack_files(self.file_path)
                self.file_list += f_list
            else:
                with open(self.file_path, mode="rb") as f:
                    b = f.read()
                    enc = detect(b)["encoding"]
                    if enc is None:
                        enc = "utf-8"
                    self.code_txt = b.decode(enc, errors="backslashreplace")

                    # packageの除外とファイルの作成
                    if self.task_lang == "java":
                        self.code_txt = re.sub(
                            "(^package.*)",
                            r"// \1 // commented out by scoring-assistant",
                            formating(self.code_txt),
                            flags=re.MULTILINE,
                        )
                        self.file_path = Path(
                            self.file_path.parent, "format", self.file_path.name
                        )
                        self.file_path.parent.mkdir(exist_ok=True)
                        with self.file_path.open(mode="w") as ff:
                            ff.write(self.code_txt)

        except Exception as e:
            self.code_txt = (
                "Open Error : " + str(self.file_path) + "\n手動で確認してください"
            )
            print(self.file_path, e)
        self.code_txt = self.code_txt.strip()
        return self.code_txt

    def execute(self):
        # 対象ユーザのディレクトリでコンパイル
        if self.task_lang == "java":
            cmd = ["javac"]
            if self.classpath is not None and len(self.classpath[0]) > 1:
                cmd += ["-classpath", sep.join(self.classpath)]
            cmd += [self.file_path.name]
            result = subprocess.run(
                args=cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=self.file_path.parent,
            )
            result_b: bytes = result.stdout
            enc: str = detect(result_b)["encoding"] or "utf-8"
            result = result_b.decode(enc, errors="backslashreplace")
            self.result_txt += (
                f"{' COMPILE RESULT ':-^70}\n"
                # f"CMD = {' '.join(cmd)}\n\n"
                f"{result.strip()}\n"
            )

        elif self.task_lang == "c":
            executable = self.file_path.with_suffix('.out')
            cmd = ["gcc", "-Wall", self.file_path.name, "-o", executable.name]
            result = subprocess.run(
                args=cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=self.file_path.parent,
            )
            result_b: bytes = result.stdout
            enc: str = detect(result_b)["encoding"] or "utf-8"
            result = result_b.decode(enc, errors="backslashreplace")
            self.result_txt += (
                f"{' COMPILE RESULT ':-^70}\n"
                f"{result.strip()}\n"
            )

            cmd = [f"./{executable.name}"]
            for arg in self.args if self.args else [{"args_value": []}]:
                arg_v: list[str] = arg["args_value"]
                for inp in self.inputs if self.inputs else [{"inputs_value": ""}]:
                    inputs: str = inp["inputs_value"]
                    cmd += arg_v
                    try:
                        result = subprocess.run(
                            args=cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            input=inputs.encode(),
                            cwd=self.file_path.parent,
                        )
                        result_b: bytes = result.stdout
                        enc: str = detect(result_b)["encoding"] or "utf-8"
                        result = result_b.decode(enc, errors="backslashreplace")
                        self.result_txt += (
                            f"{' TEST CASE ':-^70}\n"
                            f"args  = {arg_v}\n\n"
                            f"input ↓ \n\"\"\"\n{inputs}\n\"\"\"\n"
                            f"{' RESULT ':-^70}\n"
                            f"{result.strip()}\n\n"
                        )
                    except Exception as e:
                        self.result_txt += f"Exec Error : 手動で確認してください\n{e}\n"

        # 対象ユーザのディレクトリで実行
        if self.task_lang == "jar":
            cmd = ["java", "-jar", self.file_path.name]
        elif self.task_lang == "java":
            cmd = ["java"]
            if self.classpath is not None and len(self.classpath[0]) > 1:
                cmd += ["--class-path", sep.join(self.classpath + ["."])]
            cmd += [self.file_path.stem]
        else:
            return

        for arg in self.args if self.args else [{"args_value": []}]:
            arg_v: list[str] = arg["args_value"]
            for inp in self.inputs if self.inputs else [{"inputs_value": ""}]:
                inputs: str = inp["inputs_value"]
                cmd += arg_v
                try:
                    result = subprocess.run(
                        args=cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        input=inputs.encode(),
                        cwd=self.file_path.parent,
                    )
                    result_b: bytes = result.stdout
                    enc: str = detect(result_b)["encoding"] or "utf-8"
                    result = result_b.decode(enc, errors="backslashreplace")
                    self.result_txt += (
                        f"{' TEST CASE ':-^70}\n"
                        f"args  = {arg_v}\n\n"
                        f"input ↓ \n\"\"\"\n{inputs}\n\"\"\"\n"
                        f"{' RESULT ':-^70}\n"
                        # f"CMD = {' '.join(cmd)}\n\n"
                        f"{result.strip()}\n\n"
                    )
                except Exception as e:
                    self.result_txt += f"Exec Error : 手動で確認してください\n{e}\n"
        self.result_txt = self.result_txt.strip()

        return self.result_txt


def formating(code: str):
    """
    Artistic StyleによるJavaとCのフォーマットを行う。
    toolsディレクトリにあるexeを利用
    """
    try:
        formatter = Astyle("3.4.7")
        formatter.set_options("--style=google --delete-empty-lines --indent=spaces=2")
        res_code = formatter.format(code)
        return res_code.strip()
    except Exception:
        return code


def unpack_files(file_path, file_encoding=None):
    texts: str = ""
    file_list: list[str] = []
    text = ""
    with zipfile.ZipFile(file_path, metadata_encoding=file_encoding) as zf:
        for zip_info in zf.infolist():
            if zip_info.filename.endswith((".java", ".txt")):
                text = ""
                # ファイルのバイトデータを読み込んでテキストに変換する
                b = zf.read(zip_info)
                enc: str | None = detect(b)["encoding"]
                if enc is None:
                    text += "文字コードの推定に失敗しました。一部をエスケープシーケンスで置き換えました。"
                    enc = "utf-8"
                text += formating(b.decode(enc, errors="backslashreplace").strip())
                texts += f"{Path(zip_info.filename).name:-^70}\n{text}\n\n"
                file_list.append(Path(zip_info.filename).name)

    return texts.strip() if len(text) > 0 else "javaファイル無し", file_list
