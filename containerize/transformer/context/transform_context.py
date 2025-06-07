

class TransformContext:
    def __init__(self, name="my-app", image="REPLACE_ME", replicas=1, helm_mode=False):
        self.name = name
        self.image = image
        self.replicas = replicas
        self.helm_mode = helm_mode