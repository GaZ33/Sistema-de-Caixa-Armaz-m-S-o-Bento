function abrirModal(id) {
    $('#' + id).addClass('aberto');
}

function fecharModal(id) {
    $('#' + id).removeClass('aberto');
}

function cadastrarCliente() {
    var dados = {
        nome:      $('#cad-nome').val().trim(),
        sobrenome: $('#cad-sobrenome').val().trim() || undefined,
        cpf:       $('#cad-cpf').val().trim() || undefined,
        telefone:  $('#cad-telefone').val().trim() || undefined,
        email:     $('#cad-email').val().trim() || undefined,
        username:  $('#cad-username').val().trim(),
        senha:     $('#cad-senha').val()
    };

    if (!dados.username || !dados.senha) {
        alert('UsuÃ¡rio e senha sÃ£o obrigatÃ³rios.');
        return;
    }

    $.ajax({
        url: '/api/users',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(dados),
        dataType: 'json',
        success: function () {
            fecharModal('modal-cadastrar');
            $('#cad-nome, #cad-sobrenome, #cad-cpf, #cad-telefone, #cad-email, #cad-username, #cad-senha').val('');
            if (typeof window.refresh === 'function') window.refresh();
        },
        error: function (xhr) {
            var data = xhr.responseJSON || {};
            alert(data.error || 'Falha ao cadastrar cliente.');
        }
    });
}

$(document).ready(function () {
    var $list   = $('#client-list');
    var $search = $('#client-search');

    function renderClients(clients) {
        if (!clients.length) {
            $list.html('<p class="empty-message">Nenhum cliente encontrado.</p>');
            return;
        }
        var html = $.map(clients, function (c) {
            return '<article class="client-card">' +
                '<div class="client-avatar"><img src="/static/icones/Login.png" alt="Cliente"></div>' +
                '<div class="client-info">' +
                    '<strong>' + (c.nome || '') + ' ' + (c.sobrenome || '') + '</strong>' +
                    '<span>UsuÃ¡rio: ' + (c.username || '-') + '</span>' +
                    '<span>Email: ' + (c.email || '-') + '</span>' +
                    '<span>CPF: ' + (c.cpf || '-') + '</span>' +
                    '<span>Telefone: ' + (c.telefone || '-') + '</span>' +
                '</div>' +
            '</article>';
        }).join('');
        $list.html(html);
    }

    window.refresh = function () {
        $.ajax({
            url: '/api/users',
            method: 'GET',
            dataType: 'json',
            success: function (clients) {
                var term = $search.val().trim().toLowerCase();
                var filtered = $.grep(clients, function (c) {
                    var searchable = [c.nome, c.sobrenome, c.username, c.email, c.cpf]
                        .filter(Boolean).join(' ').toLowerCase();
                    return !term || searchable.indexOf(term) !== -1;
                });
                renderClients(filtered);
            },
            error: function () {
                $list.html('<p class="empty-message">NÃ£o foi possÃ­vel carregar os clientes.</p>');
            }
        });
    };

    $search.on('input', window.refresh);
    window.refresh();
});

function toggleBusca() {
    var wrapper = document.getElementById('busca-wrapper');
    wrapper.classList.toggle('aberta');
    if (wrapper.classList.contains('aberta')) {
        document.getElementById('client-search').focus();
    }
}