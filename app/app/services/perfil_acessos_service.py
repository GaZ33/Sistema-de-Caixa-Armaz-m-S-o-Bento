class PerfilAcessosService:
    def __init__(self, repository):
        self.repository = repository

    def create_perfil_acessos(self, perfil_acessos):
        return self.repository.create(perfil_acessos)

    def get_all_perfis_acessos(self):
        return self.repository.get_all()

    def get_perfil_acessos_by_id(self, perfil_acessos_id):
        return self.repository.get_by_id(perfil_acessos_id)

    def update_perfil_acessos(self, perfil_acessos):
        return self.repository.update(perfil_acessos)

    def delete_perfil_acessos(self, perfil_acessos_id):
        self.repository.delete(perfil_acessos_id)