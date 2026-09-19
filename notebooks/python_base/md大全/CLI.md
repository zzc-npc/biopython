# 命令解析器
parser = argparse.ArgumentParser(...)
→ 创建主解析器 → 负责总入口。

subparsers = parser.add_subparsers(dest="command", required=True)
→ 给主解析器添加“子命令分发区”
→ 返回一个子解析器管理对象 → 常命名为 subparsers
→ *dest="command"* → 把用户输入的子命令名存到 args.command
→ required=True → 必须指定子命令。

p_stats = subparsers.add_parser("stats", help="统计 FASTA")
→ 在子命令分发区里注册一个名为 stats 的子命令
→ 返回一个子解析器对象 → 赋给 p_stats
→ 这个 p_stats 本身也是 ArgumentParser 类型的对象 → 可以继续加参数。

p_stats.add_argument("--input", required=True, ...)
→ 给 stats 子命令添加 --input 参数。

p_stats.set_defaults(func=cmd_stats)
→ 给 stats 子命令绑定*默认属性* func=cmd_stats
→ 之后解析到 stats 时 → args.func 就是 cmd_stats。

args = parser.parse_args()
→ 解析命令行
→ 如果输入 stats --input a.fa --out out
→ 主解析器识别子命令 stats
→ 交给 stats 子解析器解析剩余参数
→ 得到 args.command = "stats"、args.input = "a.fa"、args.out = "out"、args.func = cmd_stats。

args.func(args)
→ 调用 cmd_stats(args) → 真正执行 stats 子命令逻辑。

# 全流程解析
## 从用户输入开始
用户输入命令→主解析器parser，识别出子命令，分发给子命令解析器subparsers→
子命令解析器分析参数parser.parser_args()，返回一个Namespace（分表）→
将这个子命令赋值给args总表→
总表参数func指向默认函数args.func(args)，然后带着其他属性找到我们自定义的默认函数cmd_stats，开始具体执行
## 如何创建一个新个子命令
1. 在创建解析器函数build_parser()那里加一个子命令注册
2. 写一个对应的执行默认函数
