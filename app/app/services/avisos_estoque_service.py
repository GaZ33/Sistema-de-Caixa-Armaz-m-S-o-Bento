class AvisosEstoqueService:
    def __init__(self, repository):
        self.repository = repository

    def create_aviso_estoque(self, aviso_estoque):
        return self.repository.create(aviso_estoque)

    def get_all_avisos_estoque(self):
        return self.repository.get_all()

    def get_aviso_estoque_by_id(self, aviso_estoque_id):
        return self.repository.get_by_id(aviso_estoque_id)

    def update_aviso_estoque(self, aviso_estoque_id, data):
        return self.repository.update(aviso_estoque_id, data)

    def delete_aviso_estoque(self, aviso_estoque_id):
        self.repository.delete(aviso_estoque_id)