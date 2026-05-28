$(document).ready(function() {

});

function abrirModal(id) {
    document.getElementById(id).classList.add('aberto');
}

function fecharModal(id) {
    document.getElementById(id).classList.remove('aberto');
}

function cadastrarCliente() {
    const dados = {
        nome: document.getElementById('cad-nome').value,
        cpf: document.getElementById('cad-cpf').value,
        telefone: document.getElementById('cad-telefone').value,
        email: document.getElementById('cad-email').value,
        endereco: document.getElementById('cad-endereco').value,
    };

    console.log("Cadastrar cliente:", dados);
    // quando ligar ao backend: fetch('/api/users', { method: 'POST', body: JSON.stringify(dados) })

    fecharModal('modal-cadastrar');
}