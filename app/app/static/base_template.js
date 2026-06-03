$(document).ready(function () {

});

function abrirModal(id) {
    $('#' + id).addClass('aberto');
}

function fecharModal(id) {
    $('#' + id).removeClass('aberto');
}

/* ==================== NOVA CONTA (Home) ==================== */

var carrinhoLocal = [];
var clienteSelecionadoId = null;

function renderizarItensConta() {
    var $tbody = $('#conta-itens');
    if (!$tbody.length) return;
    $tbody.empty();
    var total = 0;

    $.each(carrinhoLocal, function (index, item) {
        total += item.subtotal;
        $tbody.append(
            '<tr>' +
                '<td>' + item.nome + '</td>' +
                '<td>' + item.marca + '</td>' +
                '<td>' + item.quantidade + '</td>' +
                '<td>R$ ' + item.preco_unitario.toFixed(2) + '</td>' +
                '<td>R$ ' + item.subtotal.toFixed(2) + '</td>' +
                '<td><button class="action-btn" onclick="removerItemConta(' + index + ')">' +
                    '<img src="/static/icones/Lixosimbolo.png" alt="Remover"></button></td>' +
            '</tr>'
        );
    });

    $('#conta-valor-total').text(total.toFixed(2).replace('.', ','));
}

function removerItemConta(index) {
    carrinhoLocal.splice(index, 1);
    renderizarItensConta();
}

function adicionarACliente() {
    carregarClientesModal();
    abrirModal('modal-selecionar-cliente');
}

function cancelarConta() {
    if (!confirm('Deseja cancelar a conta?')) return;
    carrinhoLocal = [];
    clienteSelecionadoId = null;
    $('#cliente-selecionado-label').text('');
    fecharModal('modal-nova-conta');
}

function finalizarConta() {
    if (!carrinhoLocal.length) {
        alert('Adicione pelo menos um produto antes de finalizar.');
        return;
    }
    abrirModal('modal-pagamento');
}

function confirmarPagamento(formaPagamento) {
    var carrinho = $.map(carrinhoLocal, function (item) {
        return { id: item.id, qtd: item.quantidade };
    });

    $.ajax({
        url: '/api/venda/finalizar',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            carrinho: carrinho,
            forma_pagamento: formaPagamento,
            cliente_id: clienteSelecionadoId
        }),
        dataType: 'json',
        success: function () {
            alert('Venda finalizada com sucesso!');
            carrinhoLocal = [];
            clienteSelecionadoId = null;
            $('#cliente-selecionado-label').text('');
            fecharModal('modal-pagamento');
            fecharModal('modal-nova-conta');
        },
        error: function (xhr) {
            var data = xhr.responseJSON || {};
            alert(data.error || 'Erro ao finalizar venda.');
        }
    });
}

/* ==================== BUSCAR PRODUTO (modal-adicionar-produto) ==================== */

var produtoSelecionado = null;

function buscarProdutoNaConta() {
    var query = $('#busca-produto').val();
    if (query.length < 2) {
        $('#resultado-busca').empty();
        return;
    }

    $.getJSON('/api/produtos/buscar', { query: query }, function (produtos) {
        var $div = $('#resultado-busca').empty();
        $.each(produtos, function (i, p) {
            var $btn = $('<button class="topbar-btn"></button>')
                .css({ width: '100%', 'flex-direction': 'row', 'justify-content': 'flex-start', gap: '8px', height: 'auto', padding: '8px' })
                .text(p.nome + ' â€” ' + p.marca + ' â€” R$ ' + Number(p.preco_unidade).toFixed(2))
                .on('click', function () { selecionarProduto(p, $(this)); });
            $div.append($btn);
        });
    });
}

function selecionarProduto(produto, $btn) {
    produtoSelecionado = produto;
    $('#resultado-busca button').css('background', '');
    $btn.css('background', '#ffd700');
}

function confirmarAdicionarProduto() {
    if (!produtoSelecionado) return alert('Selecione um produto.');
    var quantidade = parseFloat($('#quantidade-produto').val());
    if (!quantidade || quantidade <= 0) return alert('Informe uma quantidade vÃ¡lida.');

    var preco_unitario = Number(produtoSelecionado.preco_unidade);
    var subtotal = preco_unitario * quantidade;

    carrinhoLocal.push({
        id: produtoSelecionado.id,
        nome: produtoSelecionado.nome,
        marca: produtoSelecionado.marca,
        quantidade: quantidade,
        preco_unitario: preco_unitario,
        subtotal: subtotal
    });

    renderizarItensConta();
    fecharModal('modal-adicionar-produto');

    $('#busca-produto').val('');
    $('#resultado-busca').empty();
    $('#quantidade-produto').val('1');
    produtoSelecionado = null;
}

/* ==================== SELECIONAR CLIENTE ==================== */

function carregarClientesModal() {
    $.getJSON('/api/users', function (users) {
        renderClientesModal(users);
    }).fail(function () {
        console.error('Erro ao carregar clientes.');
    });
}

function renderClientesModal(users) {
    var $div = $('#resultado-clientes').empty();
    if (!users.length) {
        $div.html('<p style="padding:8px;">Nenhum cliente encontrado.</p>');
        return;
    }
    $.each(users, function (i, u) {
        var $btn = $('<button class="topbar-btn"></button>')
            .css({ width: '100%', 'flex-direction': 'row', 'justify-content': 'flex-start', gap: '8px', height: 'auto', padding: '8px' })
            .text((u.nome || '') + ' ' + (u.sobrenome || '') + ' â€” @' + u.username)
            .on('click', function () { confirmarClienteSelecionado(u, $(this)); });
        $div.append($btn);
    });
}

function filtrarClientesModal() {
    var query = ($('#busca-cliente-modal').val() || '').toLowerCase();
    $.getJSON('/api/users', function (users) {
        var filtrados = $.grep(users, function (u) {
            var text = [u.nome, u.sobrenome, u.username, u.email].filter(Boolean).join(' ').toLowerCase();
            return !query || text.indexOf(query) !== -1;
        });
        renderClientesModal(filtrados);
    });
}

function confirmarClienteSelecionado(user, $btn) {
    clienteSelecionadoId = user.id;
    $('#resultado-clientes button').css('background', '');
    $btn.css('background', '#ffd700');
    $('#cliente-selecionado-label').text('Cliente: ' + (user.nome || '') + ' ' + (user.sobrenome || '') + ' (@' + user.username + ')');
    fecharModal('modal-selecionar-cliente');
}

function cadastrarFuncionario() {
    var nome     = $('#func-nome').val().trim();
    var telefone = $('#func-telefone').val().trim();
    var username = $('#func-username').val().trim();
    var senha    = $('#func-senha').val().trim();

    if (!nome) { alert('Nome é obrigatório.'); return; }
    if (!telefone) { alert('Telefone é obrigatório.'); return; }
    if (!username) { alert('Usuário é obrigatório.'); return; }
    if (!senha) { alert('Senha é obrigatória.'); return; }

    var dados = {
        nome:      nome,
        sobrenome: $('#func-sobrenome').val().trim() || undefined,
        telefone:  telefone,
        cpf:       $('#func-cpf').val().trim() || undefined,
        email:     $('#func-email').val().trim() || undefined,
        username:  username,
        senha:     senha,
        perfil_id: 2
    };

    $.ajax({
        url: '/api/users',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(dados),
        success: function () {
            fecharModal('modal-cadastrar-funcionario');
            $('#func-nome, #func-sobrenome, #func-telefone, #func-cpf, #func-email, #func-username, #func-senha').val('');
            alert('Funcionário cadastrado com sucesso!');
        },
        error: function (xhr) {
            var data = xhr.responseJSON || {};
            alert(data.error || 'Falha ao cadastrar funcionário.');
        }
    });
}