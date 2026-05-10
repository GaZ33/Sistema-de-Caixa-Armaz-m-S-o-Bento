class EstoqueService:
    def __init__(self, repository):
        self.repository = repository

    def create_estoque(self, estoque):
        return self.repository.create(estoque)

    def get_all_estoques(self):
        return self.repository.get_all()

    def get_estoque_by_id(self, estoque_id):
        return self.repository.get_by_id(estoque_id)

    def update_estoque(self, estoque):
        return self.repository.update(estoque)

    def delete_estoque(self, estoque_id):
        self.repository.delete(estoque_id)