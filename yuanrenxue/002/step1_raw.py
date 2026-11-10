"""
第 1 步：什么都不补，直接跑挑战体。
目的：观察第一个报错是什么 —— 报错就是"环境清单"的第一条线索。

用法: python3 step1_raw.py <challenge.js>
"""
import sys
import quickjs


def main():
    path = sys.argv[1]
    with open(path, encoding="utf-8") as f:
        challenge_js = f.read()

    ctx = quickjs.Context()
    ctx.set_time_limit(5)  # 5 秒超时，防死循环把进程卡死

    print(f"挑战体长度: {len(challenge_js)} 字符")
    print("直接执行，不做任何补环境...")
    print("-" * 60)

    try:
        ctx.eval(challenge_js)
        print("执行结束（没有抛异常）")
    except Exception as e:
        print(f"抛异常: {type(e).__name__}")
        print(f"错误信息: {e}")

    # 看看有没有产生 cookie
    try:
        js = 'typeof document !== "undefined" ? document.cookie : "(no document)"'
        print(f"document.cookie = {ctx.eval(js)}")
    except Exception as e:
        print(f"读 cookie 失败: {e}")


if __name__ == "__main__":
    main()
