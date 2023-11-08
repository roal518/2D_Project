from pico2d import load_image


class Idle:
    pass
class Run:
    pass
# 공은 매개변수가 1이 되면 멈춰야 한다 IDLE
# 충돌하면 이동하는 식이 변경되고 매개변수도 0이 된다. RUN - RUN
# 클래스 너무 어렵다
# 스테이트 머신 ?
# 필드 밖으로 충돌하면 식 변경
# 매개변수는 2차를 쓰도록 하자 점에 대해서 이동하게 하면 된다. 식은 이미 갖고 있음
# 
class Ball:
    def __init__(self, x = 400, y = 300, velocity = 1):
        self.image = load_image('ball21x21.png')
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        self.x += self.velocity
        self.y += self.velocity
