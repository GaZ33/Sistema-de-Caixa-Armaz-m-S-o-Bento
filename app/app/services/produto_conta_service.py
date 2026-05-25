class ProdutoContaService:
    def __init__(self, repository):
        self.repository = repository

    def create_produto_conta(self, produto_conta):
        return self.repository.create(produto_conta)

    def get_all_produtos_conta(self):
        return self.repository.get_all()

    def get_produto_conta_by_id(self, produto_conta_id):
        return self.repository.get_by_id(produto_conta_id)

    def update_produto_conta(self, produto_conta_id, data):
        return self.repository.update(produto_conta_id, data)

    def delete_produto_conta(self, produto_conta_id):
        self.repository.delete(produto_conta_id)