var contaAtualId = null;

function abrirModal(id) {
    $('#' + id).addClass('aberto');
}

function fecharModal(id) {
    $('#' + id).removeClass('aberto');
}

$(document).ready(function () {
    carregarContasCliente();
});

function carregarContasCliente() {
    $.getJSON('/api/users/' + clienteId)
        .then(function(user) {
            $('#titulo-cliente').text('Contas de ' + (user.nome || '') + (user.sobrenome ? ' ' + user.sobrenome : ''));
            return $.getJSON('/api/contas/cliente/' + clienteId);
        })
        .then(function(contas) {
            var abertas = $.grep(contas, function(c) {
                return c.status === 'aberta';
            });

            if (!abertas.length) {
                $('#contas-cliente-list').html('<p class="empty-message">Nenhuma conta aberta para este cliente.</p>');
                return;
            }

            renderizarContasCliente(abertas);
        })
        .fail(function(xhr) {
            $('#contas-cliente-list').html('<p class="empty-message">Erro ao carregar contas. Status: ' + xhr.status + '</p>');
        });
}

function renderizarContasCliente(contas) {
    var html = $.map(contas, function (c) {
        var total = Number(c.valor_total || 0).toFixed(2).replace('.', ',');
        var data  = new Date(c.data_criacao);
        var dataFormatada = data.toLocaleDateString('pt-BR', { timeZone: 'America/Sao_Paulo' });

        return '<div class="conta-card">' +
            '<div class="conta-info" style="text-align:left; width:100%;">' +
                '<strong>' + dataFormatada + '</strong>' +
                '<span>Total: R$ ' + total + '</span>' +
                '<div id="produtos-conta-' + c.id + '" style="margin-top:6px;">' +
                    '<span style="color:#a07800; font-size:12px;">Carregando produtos...</span>' +
                '</div>' +
            '</div>' +
            '<div class="conta-card-acoes">' +
                '<button class="btn-finalizar" onclick="abrirFinalizarConta(' + c.id + ')">Finalizar</button>' +
                '<button class="btn-cancelar" onclick="cancelarContaCliente(' + c.id + ')">Cancelar</button>' +
            '</div>' +
        '</div>';
    }).join('');

    $('#contas-cliente-list').html(html);

    contas.forEach(function(c) {
        $.getJSON('/api/produto_conta/conta/' + c.id, function(itens) {
            var lista = itens.map(function(i) {
                return '<span style="display:block; font-size:13px; color:#5a4000;">• ' +
                    i.quantidade + 'x ' + (i.produto_nome || 'Produto #' + i.produto_id) +
                    ' — R$ ' + Number(i.subtotal).toFixed(2).replace('.', ',') +
                '</span>';
            }).join('');
            $('#produtos-conta-' + c.id).html(lista || '<span style="font-size:12px;color:#a07800;">Sem itens</span>');
        }).fail(function() {
            $('#produtos-conta-' + c.id).html('');
        });
    });
}

function abrirFinalizarConta(id) {
    contaAtualId = id;
    abrirModal('modal-finalizar-conta');
}

function finalizarContaCliente(formaPagamento) {
    $.ajax({
        url: '/api/contas/' + contaAtualId,
        method: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify({
            status: 'fechada'
        }),
        success: function () {
            fecharModal('modal-finalizar-conta');
            contaAtualId = null;
            carregarContasCliente();
        },
        error: function (xhr) {
            alert('Erro ao finalizar conta: ' + xhr.responseText);
        }
    });
}

function cancelarContaCliente(id) {
    if (!confirm('Deseja cancelar esta conta?')) return;
    $.ajax({
        url: '/api/contas/' + id,
        method: 'DELETE',
        success: function () {
            carregarContasCliente();
        },
        error: function () {
            alert('Erro ao cancelar conta.');
        }
    });
}