function abrirModal(id) {
    $('#' + id).addClass('aberto');
}

function fecharModal(id) {
    $('#' + id).removeClass('aberto');
    if (id === 'modal-cadastrar') {
        $('#modal-cadastrar .modal-title').text('CADASTRAR CLIENTE');
        $('#modal-cliente-btn').removeData('editing');
        $('#cad-nome, #cad-sobrenome, #cad-cpf, #cad-telefone, #cad-email, #cad-username, #cad-senha').val('');
    }
}

function cadastrarCliente() {
    var nome     = $('#cad-nome').val().trim();
    var sobrenome = $('#cad-sobrenome').val().trim();

    if (!nome) {
        alert('Nome é obrigatório.');
        return;
    }

    /* Nickname gerado pelo nome duas vezes escrito em minúsculo*/
    var nomeFormatado = nome.toLowerCase()
            .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
            .replace(/\s+/g, '');
        var username = nomeFormatado + nomeFormatado;

        var dados = {
            nome:      nome,
            sobrenome: sobrenome || undefined,
            cpf:       $('#cad-cpf').val().trim() || undefined,
            telefone:  $('#cad-telefone').val().trim() || undefined,
            email:     $('#cad-email').val().trim() || undefined,
            username:  username,
            senha:     nomeFormatado + nomeFormatado,
            salt:      'default',
            perfil_id: 3        // ← força a ser cliente (id3)
        };

    $.ajax({
        url: '/api/users',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(dados),
        dataType: 'json',
        success: function () {
            fecharModal('modal-cadastrar');
            if (typeof window.refresh === 'function') window.refresh();
        },
        error: function (xhr) {
            var data = xhr.responseJSON || {};
            alert(data.error || 'Falha ao cadastrar cliente.');
        }
    });
}

function atualizarCliente(id) {
    var dados = {
        nome:      $('#cad-nome').val().trim(),
        sobrenome: $('#cad-sobrenome').val().trim() || undefined,
        cpf:       $('#cad-cpf').val().trim() || undefined,
        telefone:  $('#cad-telefone').val().trim() || undefined,
        email:     $('#cad-email').val().trim() || undefined,
        username:  $('#cad-username').val().trim()
    };

    $.ajax({
        url: '/api/users/' + id,
        method: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify(dados),
        success: function () {
            fecharModal('modal-cadastrar');
            if (typeof window.refresh === 'function') window.refresh();
        },
        error: function (xhr) {
            alert('Erro ao atualizar cliente: ' + xhr.responseText);
        }
    });
}

function handleModalClienteBtn() {
    var id = $('#modal-cliente-btn').data('editing');
    if (id) {
        atualizarCliente(id);
    } else {
        cadastrarCliente();
    }
}

function toggleBuscaCliente() {
    var wrapper = document.getElementById('busca-wrapper-cliente');
    wrapper.classList.toggle('aberta');
    if (wrapper.classList.contains('aberta')) {
        document.getElementById('client-search').focus();
    }
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
                        '<span>Usuário: ' + (c.username || '-') + '</span>' +
                        '<span>Telefone: ' + (c.telefone || '-') + '</span>' +
                    '</div>' +
                    '<div class="client-actions">' +
                        '<button class="action-btn" data-action="edit" data-id="' + c.id + '" title="Editar">' +
                            '<img src="/static/icones/EditarSimbolo.png" alt="Editar"></button>' +
                        '<button class="action-btn" data-action="delete" data-id="' + c.id + '" title="Excluir">' +
                            '<img src="/static/icones/Lixosimbolo.png" alt="Excluir"></button>' +
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
                        if (c.perfil_id !== 3) return false;  // ← só clientes
                        var searchable = [c.nome, c.sobrenome, c.username, c.email, c.cpf]
                            .filter(Boolean).join(' ').toLowerCase();
                        return !term || searchable.indexOf(term) !== -1;
                    });
                    renderClients(filtered);
                },
            error: function () {
                $list.html('<p class="empty-message">Não foi possível carregar os clientes.</p>');
            }
        });
    };

    $list.on('click', 'button[data-action]', function () {
        var action = $(this).data('action');
        var id     = $(this).data('id');

        if (action === 'delete') {
            if (!window.confirm('Deseja excluir este cliente?')) return;
            $.ajax({
                url: '/api/users/' + id,
                method: 'DELETE',
                success: function () {
                    window.refresh();
                },
                error: function () {
                    alert('Falha ao excluir o cliente.');
                }
            });
        }

        if (action === 'edit') {
            $.getJSON('/api/users/' + id, function (cliente) {
                $('#cad-nome').val(cliente.nome || '');
                $('#cad-sobrenome').val(cliente.sobrenome || '');
                $('#cad-username').val(cliente.username || '');
                $('#cad-cpf').val(cliente.cpf || '');
                $('#cad-telefone').val(cliente.telefone || '');
                $('#cad-email').val(cliente.email || '');
                $('#modal-cadastrar .modal-title').text('ALTERAR CLIENTE');
                $('#modal-cliente-btn').data('editing', id);
                abrirModal('modal-cadastrar');
            });
        }
    $list.on('dblclick', '.client-card', function () {
    var id = $(this).find('button[data-action]').first().data('id');
    console.log('dblclick id:', id);
    if (id) {
        window.location.href = '/clientes/' + id + '/contas';
    }
});

    });

    $search.on('input', window.refresh);
    window.refresh();
});