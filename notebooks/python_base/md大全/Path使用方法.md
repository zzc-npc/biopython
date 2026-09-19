# 1. 创建与拼接
from pathlib import Path
## "data" → Path 对象 → / 运算符拼接 → 得到新 Path → 原路径不变
p = Path("data") / "sub" / "a.txt"
此时p=data/sub/a.txt

## 拼接多个部分 → 得到 Path
p = Path("data").joinpath("sub", "a.txt")
此时p=data/sub/a.txt

## ~ → 展开为用户主目录 → 得到新 Path
p = Path("~/docs/a.txt").expanduser()
p=home/zzc/docs/a.txt

## 常用类方法：
Path.cwd()      # 当前工作目录 → Path
Path.home()     # 用户主目录 → Path
Path("a/b.txt") # 字符串 → Path

# 2. 取路径信息
p = Path("/home/user/docs/a.tar.gz")

p.parent        # /home/user/docs → 上一级目录
p.parents       # 所有父目录 → 可迭代
p.name          # a.tar.gz → 最后一部分
p.stem          # a.tar → 去掉最后一个后缀
p.suffix        # .gz → 最后一个后缀
p.suffixes      # ['.tar', '.gz'] → 所有后缀
p.parts         # ('/', 'home', 'user', 'docs', 'a.tar.gz') → 各部分
p.anchor        # / → 根部分
p.as_posix()    # /home/user/docs/a.tar.gz → 转成 / 分隔字符串

## 改文件名 / 后缀：
p.with_name("b.txt")      # /home/user/docs/b.txt → 换文件名
p.with_suffix(".md")      # /home/user/docs/a.tar.md → 换最后一个后缀
p.relative_to("/home")    # user/docs/a.tar.gz → 相对路径
p.is_relative_to("/home") # True → 是否在 /home 下
*注意*：双引号

# 3. 判断路径状态
p.exists()       # 存在？
p.is_file()      # 是文件？
p.is_dir()       # 是目录？
p.is_symlink()   # 是符号链接？
p.is_absolute()  # 是绝对路径？
p.match("*.py")  # 是否匹配模式？

# 4. 读写文件
## 文件 → 读取全部文本 → 返回 str
text = p.read_text(encoding="utf-8")

## 文件 → 读取全部字节 → 返回 bytes
data = p.read_bytes()

## 字符串 → 覆盖写入文件 → 返回写入字符数
p.write_text("你好\n", encoding="utf-8")

## 字节 → 覆盖写入文件 → 返回写入字节数
p.write_bytes(b"hello")


# 5. 目录与文件操作
## 创建单级目录 → 父目录不存在则报错
p.mkdir()

## 创建多级目录 → 已存在不报错
p.mkdir(parents=True, exist_ok=True)

## 创建空文件 → 或更新修改时间
p.touch()

## 删除文件 → 不存在不报错
p.unlink(missing_ok=True)

## 删除空目录 → 非空会报错
p.rmdir()

## 重命名/移动 → 返回新 Path
p.rename("new.txt")

## 替换/移动 → 返回新 Path
p.replace("new.txt")
