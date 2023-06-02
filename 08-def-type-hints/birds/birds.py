class Bird:
    pass


class Duck(Bird):  # Duck是Bird的子类
    def quack(self):
        print("Quack!")


def alert(birdie):  # alert没有类型提示，mypy忽略它
    birdie.quack()


def alert_duck(birdie: Duck) -> None:  # alert_duck接收Duck类型参数
    birdie.quack()


def alert_bird(birdie: Bird) -> None:  # alert_bird接收Bird类型参数
    birdie.quack()


"""
$ mypy birds/birds.py 
birds/birds.py:19: error: "Bird" has no attribute "quack"  [attr-defined]
Found 1 error in 1 file (checked 1 source file)
"""
