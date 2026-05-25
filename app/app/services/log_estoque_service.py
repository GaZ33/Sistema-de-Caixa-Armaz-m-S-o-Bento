class LogEstoqueService:
    def __init__(self, repository):
        self.repository = repository

    def create_log_estoque(self, log_estoque):
        return self.repository.create(log_estoque)

    def get_all_logs_estoque(self):
        return self.repository.get_all()

    def get_log_estoque_by_id(self, log_estoque_id):
        return self.repository.get_by_id(log_estoque_id)

    def update_log_estoque(self, log_estoque_id, data):
        return self.repository.update(log_estoque_id, data)

    def delete_log_estoque(self, log_estoque_id):
        self.repository.delete(log_estoque_id)