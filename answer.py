import subprocess
import zipfile
from pathlib import Path

from chardet import detect

# from astyle_py import Astyle


class Answer:
    def __init__(self, file_path: Path, task: dict) -> None:
        self.file_path = file_path  # .replace("\\", "/")
        self.code_txt: str = ""
        self.result_txt: str = ""
        self.task_name: str = task["name"]
        self.task_lang: str = task["lang"]
        self.inputs = task.get("inputs", [{"input": ""}])
        self.args: list = task.get("args", [{"arg": []}])
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
                    if self.task_lang == "java":
                        self.code_txt = formating(self.code_txt)
        except Exception as e:
            self.code_txt = (
                "Open Error : " + str(self.file_path) + "\n手動で確認してください"
            )
            print(self.file_path, e)
        return self.code_txt

    def execute(self):
        proj_dir_abs_path = Path(__file__).parent
        jdk_abs_path = Path(proj_dir_abs_path, "tools", "jdk-21", "bin", "java.exe")
        if self.task_lang == "jar":
            cmd = [jdk_abs_path, "-jar", self.file_path]
        elif self.task_lang == "java":
            cmd = [jdk_abs_path, self.file_path]
        else:
            # self.result_txt = "cmd error"
            return

        for arg in self.args if self.args else [{"arg": []}]:
            arg_v: list[str] = arg["arg"]
            for inp in self.inputs if self.inputs else [{"input": ""}]:
                input_v: str = inp["input"]
                try:
                    result = subprocess.run(
                        args=cmd + arg_v,
                        encoding="utf-8",
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        input=input_v,
                        text=True,
                    )
                    if len(result.stdout) < 1:
                        raise Exception("stdout<1")
                    self.result_txt += (
                        f"{' TEST CASE ':=^70}\n"
                        f"args    = {arg_v}\n"
                        f"inputs  = \n\"\"\"\n{input_v}\n\"\"\"\n"
                        f"{' RESULT ':=^70}\n"
                        f"{result.stdout.strip()}\n\n"
                    )
                except Exception as e:
                    print(e)
                    self.result_txt += f"{' Exec Error ':!^70}"


def formating(code: str):
    """
    Artistic StyleによるJavaとCのフォーマットを行う。
    toolsディレクトリにあるexeを利用
    """
    proj_dir_abs_path = Path(__file__).parent
    # porj_to_jdk_path = path.join("tools", "jdk-21", "bin", "java.exe")
    # jdk_abs_path = path.join(proj_dir_abs_path, porj_to_jdk_path)
    # gjf_abs_path = path.join(
    #     proj_dir_abs_path, "tools", "google-java-format-1.23.0-all-deps.jar"
    # )
    astyle_abs_path = Path(proj_dir_abs_path, "tools", "astyle-3.6-x64", "astyle.exe")
    try:
        result = subprocess.run(
            # args=[jdk_abs_path, "-jar", gjf_abs_path, "-"],
            args=[astyle_abs_path, "--style=google", "--delete-empty-lines"],
            input=code,
            text=True,
            stdout=subprocess.PIPE,
        )
        result.check_returncode()
        return result.stdout
    except Exception:
        return code


def unpack_files(file_path, file_encoding=None):
    texts: str = ""
    file_list: list[str] = []
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


if __name__ == "__main__":
    print(
        formating(
            """
            public class ArrayTest {
            public static void main(String[] args){
            int[] array = new int[10];

                for(int i = 0; i < array.length; i++){
            array[i] = (i+1)*(i+1);
                }


                for(int i = array.length - 1; i >=0; i--)
                {
                            System.out.println(array[i]);
                }
            }
            }
            """
        )
    )
