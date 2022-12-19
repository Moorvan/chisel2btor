import argparse
import os
import shutil
import subprocess


class Converter:
    def __init__(self, chiselfv_dir: str):
        parser = argparse.ArgumentParser()
        parser.add_argument('chisel_file', help='Chisel file')
        # parser.add_argument('imports', help='import <package>')
        parser.add_argument('instance', help='new <top_module_name>')
        parser.add_argument('args', help='new module_name(<args>)')
        args = parser.parse_args()
        self.chisel_file = args.chisel_file
        self.instance = args.instance
        self.args = args.args
        self.chisel_dir = chiselfv_dir

    def __init__(self, chiselfv_dir: str, chisel_file: str, instance: str, args: str):
        self.chisel_file = chisel_file
        self.instance = instance
        self.args = args
        self.chisel_dir = chiselfv_dir

    def converter_gen(self, target: str = "."):
        script = f"""import chiselFv._

object Btor2Generator extends App {{
    Check.generateBtor(() => new {self.instance}({self.args}))
}}
"""
        with open(target + "/src/main/scala/Btor2Generator.scala", 'w') as f:
            f.write(script)

    def run(self):
        shutil.copy(self.chisel_file, self.chisel_dir + "/src/main/scala")
        self.converter_gen(self.chisel_dir)
        # run `sbt run Btor2Generator` in chisel_dir
        # You need to make sure there is only one Main in the project (that is, the Object that inherits from the App)
        subprocess.run(["sbt", "run"], cwd=self.chisel_dir)
        # copy the generated btor2 file(self.chisel_dir + self.instance + _ + btor + _ + gen + self.instance + .btor2) to the current directory
        shutil.copy(self.chisel_dir + "/" + self.instance + "_btor_gen/" + self.instance + ".btor2", ".")
        # remove src/main/scala/Btor2Generator.scala and src/main/scala/<chisel_file>
        os.remove(self.chisel_dir + "/src/main/scala/Btor2Generator.scala")
        os.remove(self.chisel_dir + "/src/main/scala/" + self.chisel_file.split("/")[-1])


if __name__ == '__main__':
    # chisel_file = "/Users/yuechen/Developer/chisel-projects/ChiselFV/src/main/scala/cases/Memory.scala"
    # run export JAVA_HOME=`/usr/libexec/java_home -v 17.0.1`
    # os.environ["JAVA_HOME"] = "/Library/Java/JavaVirtualMachines/jdk-17.0.1.jdk/Contents/Home"
    chiselfv_dir = "./ChiselFV"
    chisel_file = "./cases/Memory.scala"
    converter = Converter(chiselfv_dir, chisel_file, "Memory", "1024,8")
    converter.run()
