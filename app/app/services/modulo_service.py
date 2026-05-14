class ModuloService:
    def __init__(self, repository):
        self.repository = repository

    def create_modulo(self, modulo):
        return self.repository.create(modulo)

    def get_all_modulos(self):
        return self.repository.get_all()

    def get_modulo_by_id(self, modulo_id):
        return self.repository.get_by_id(modulo_id)

    def update_modulo(self, modulo):
        return self.repository.update(modulo)

    def delete_modulo(self, modulo_id):
        self.repository.delete(modulo_id)