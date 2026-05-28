$(document).ready(function() {

});

function abrirModal(id) {
    document.getElementById(id).classList.add('aberto');
}

function fecharModal(id) {
    document.getElementById(id).classList.remove('aberto');
}

// Nova Conta
function abrirNovaConta() {
    carregarItensConta();
    abrirModal('modal-nova-conta');
}

function carregarItensConta() {
    fetch('/api/produto_conta')
        .then(r => r.json())
        .then(itens => renderizarItensConta(itens))
        .catch(e => console.error('Erro ao carregar itens:', e));
}

function renderizarItensConta(itens) {
    const tbody = document.getElementById('conta-itens');
    tbody.innerHTML = '';
    let total = 0;

    itens.forEach(item => {
        total += item.subtotal;
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${item.produto_id}</td>
            <td>—</td>
            <td>${item.quantidade}</td>
            <td>R$ ${item.preco_unitario.toFixed(2)}</td>
            <td>R$ ${item.subtotal.toFixed(2)}</td>
            <td>
                <button class="action-btn" onclick="removerItemConta(${item.id})">
                    <img src="/static/icones/Lixosimbolo.png" alt="Remover">
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });

    document.getElementById('conta-valor-total').textContent = total.toFixed(2).replace('.', ',');
}

function removerItemConta(id) {
    fetch(`/api/produto_conta/${id}`, { method: 'DELETE' })
        .then(() => carregarItensConta())
        .catch(e => console.error('Erro ao remover item:', e));
}

function adicionarACliente() {
    // será implementado ao ligar ao backend
    console.log('Adicionar a cliente');
}

function cancelarConta() {
    if (!confirm('Deseja cancelar a conta?')) return;
    fecharModal('modal-nova-conta');
}

function finalizarConta() {
    // será implementado ao ligar ao backend
    console.log('Finalizar conta');
}

let produtoSelecionado = null;

function buscarProdutoNaConta() {
    const query = document.getElementById('busca-produto').value;
    if (query.length < 2) {
        document.getElementById('resultado-busca').innerHTML = '';
        return;
    }

    fetch(`/api/produtos/buscar?query=${encodeURIComponent(query)}`)
        .then(r => r.json())
        .then(produtos => {
            const div = document.getElementById('resultado-busca');
            div.innerHTML = '';
            produtos.forEach(p => {
                const btn = document.createElement('button');
                btn.className = 'topbar-btn';
                btn.style = 'width:100%; flex-direction:row; justify-content:flex-start; gap:8px; height:auto; padding:8px;';
                btn.textContent = `${p.nome} — ${p.marca} — R$ ${p.preco_unidade.toFixed(2)}`;
                btn.onclick = () => selecionarProduto(p, btn);
                div.appendChild(btn);
            });
        });
}

function selecionarProduto(produto, btn) {
    produtoSelecionado = produto;
    document.querySelectorAll('#resultado-busca button').forEach(b => b.style.background = '');
    btn.style.background = '#ffd700';
}

function confirmarAdicionarProduto() {
    if (!produtoSelecionado) return alert('Selecione um produto.');
    const quantidade = parseFloat(document.getElementById('quantidade-produto').value);
    console.log('Adicionar:', produtoSelecionado, 'Qtd:', quantidade);
    // quando ligar ao backend: fetch('/api/produto_conta', { method: 'POST', ... })
    fecharModal('modal-adicionar-produto');
    produtoSelecionado = null;
}