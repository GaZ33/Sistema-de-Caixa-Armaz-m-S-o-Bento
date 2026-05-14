class ProdutoService:
    def __init__(self, repository):
        self.repository = repository

    def create_produto(self, produto):
        return self.repository.create(produto)

    def get_all_produtos(self):
        return self.repository.get_all()

    def get_produto_by_id(self, produto_id):
        return self.repository.get_by_id(produto_id)

    def update_produto(self, produto):
        return self.repository.update(produto)

    def delete_produto(self, produto_id):
        self.repository.delete(produto_id)

    def buscar_produtos(self, query):
        return self.repository.buscar(query)