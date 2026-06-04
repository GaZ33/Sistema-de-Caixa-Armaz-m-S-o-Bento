var contaAtualId = null;

$(document).ready(function () {
    carregarContasCliente();
});

function carregarContasCliente() {
    $.when(
        $.getJSON('/api/users/' + clienteId),
        $.getJSON('/api/contas/cliente/' + clienteId)
    ).done(function(userRes, contasRes) {
        var user   = userRes[0];
        var contas = contasRes[0];

        $('#titulo-cliente').text('Contas de ' + (user.nome || '') + ' ' + (user.sobrenome || ''));

        var abertas = $.grep(contas, function(c) {
            return c.status === 'aberta';
        });

        if (!abertas.length) {
            $('#contas-cliente-list').html('<p class="empty-message">Nenhuma conta aberta para este cliente.</p>');
            return;
        }

        renderizarContasCliente(abertas);
    }).fail(function () {
        $('#contas-cliente-list').html('<p class="empty-message">Erro ao carregar contas.</p>');
    });
}

function renderizarContasCliente(contas) {
    var html = $.map(contas, function (c) {
        var total = Number(c.valor_total || 0).toFixed(2).replace('.', ',');
        var data  = new Date(c.data_criacao);
        var hora  = data.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', timeZone: 'America/Sao_Paulo' });

        return '<div class="conta-card">' +
            '<div class="conta-info">' +
                '<strong>Conta #' + c.id + '</strong>' +
                '<span>Aberta às ' + hora + '</span>' +
                '<span>Total: R$ ' + total + '</span>' +
            '</div>' +
            '<div class="conta-card-acoes">' +
                '<button class="btn-finalizar" onclick="abrirFinalizarConta(' + c.id + ')">Finalizar</button>' +
                '<button class="btn-cancelar" onclick="cancelarContaCliente(' + c.id + ')">Cancelar</button>' +
            '</div>' +
        '</div>';
    }).join('');

    $('#contas-cliente-list').html(html);
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
            status: 'fechada',
            forma_pagamento: formaPagamento,
            data_fechamento: new Date().toISOString()
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