from containerize.transformer.task_transformers import TaskTransformer

class PlaybookTransformer:
    def __init__(self, playbook: dict):
        self.playbook = playbook
        self.output = []
    
    def transform(self):
        for play in self.playbook:
            tasks = play.get("tasks", [])
            for task in tasks:
                result = TaskTransformer.transform_task(task)
                if result:
                    self.output.append(result)
        return self.output
    
    
        