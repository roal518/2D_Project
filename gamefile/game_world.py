objects = [[],[]]
#객체별 계층 생성? 어려운데???
def add_object(o , depth = 0):
    objects[depth].append(o)
def add_objects(ol,depth = 0):
    objects[depth] += ol

def update():
    for layer in objects:
        for o in layer:
            o.update()
def render():
    for layer in objects:
        for o in layer:
            o.draw()

def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            return
        #더 지울 대상은 없기에 return
    raise ValueError('cannot remove non-existing obj')