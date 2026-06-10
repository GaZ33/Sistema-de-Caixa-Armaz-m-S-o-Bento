$(document).ready(function () {
    iniciarHome();
});

function abrirModal(id) {
    $('#' + id).addClass('aberto');
}

function fecharModal(id) {
    $('#' + id).removeClass('aberto');
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

/* ==================== CONTAS DO DIA (Home) ==================== */

function iniciarHome() {
    if (!$('#home-contas').length) return;
    carregarContasDoDia();
}

function inicioDoDia() {
    var agora = new Date();
    var inicio = new Date(agora);

    // dia começa às 4:30
    if (agora.getHours() < 4 || (agora.getHours() === 4 && agora.getMinutes() < 30)) {
        inicio.setDate(inicio.getDate() - 1);
    }
    inicio.setHours(4, 30, 0, 0);
    return inicio;
}

function carregarContasDoDia() {
    $.when(
        $.getJSON('/api/contas'),
        $.getJSON('/api/users')
    ).done(function(contasRes, usersRes) {
        var contas = contasRes[0];
        var users  = usersRes[0];

        var userMap = {};
        users.forEach(function(u) {
            userMap[u.id] = (u.nome || '') + (u.sobrenome ? ' ' + u.sobrenome : '');
        });

        var inicio = inicioDoDia();
        var contasDoDia = $.grep(contas, function (c) {
            return new Date(c.data_criacao) >= inicio;
        });

        if (!contasDoDia.length) {
            $('#home-contas').hide();
            return;
        }

        $('#home-contas').show();
        renderizarContasDoDia(contasDoDia, userMap);
    }).fail(function () {
        $('#home-contas').hide();
    });
}

function renderizarContasDoDia(contas, userMap) {
    var html = $.map(contas, function (c) {
        var status  = c.status === 'aberta' ? 'aberta' : 'fechada';
        var label   = c.status === 'aberta' ? 'Aberta' : 'Fechada';
        var total   = Number(c.valor_total || 0).toFixed(2).replace('.', ',');
        var data    = new Date(c.data_criacao);
        var hora    = data.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', timeZone: 'America/Sao_Paulo' });
        var cliente = c.cliente && userMap[c.cliente] ? userMap[c.cliente] : 'Não Informado';

        return '<div class="conta-card">' +
            '<div class="conta-info">' +
                '<strong>' + cliente + '</strong>' +
                '<span>Aberta às ' + hora + '</span>' +
                '<span>Total: R$ ' + total + '</span>' +
            '</div>' +
            '<span class="conta-status ' + status + '">' + label + '</span>' +
        '</div>';
    }).join('');

    $('#contas-list').html(html);
}

/* ==================== GLOBAL NAVIGATION ACTIONS ==================== */

function handleNavAction(targetPage, action) {
    var currentPath = window.location.pathname;
    var targetUrl = "/";
    if (targetPage === "clientes") {
        targetUrl = "/clientes/index.html";
    } else if (targetPage === "produtos") {
        targetUrl = "/produtos/index.html";
    }

    var isOnPage = false;
    if (targetPage === "home" && (currentPath === "/" || currentPath === "")) {
        isOnPage = true;
    } else if (targetPage === "clientes" && currentPath.indexOf("/clientes/index.html") !== -1) {
        isOnPage = true;
    } else if (targetPage === "produtos" && currentPath.indexOf("/produtos/index.html") !== -1) {
        isOnPage = true;
    }

    if (isOnPage) {
        triggerAction(action);
    } else {
        window.location.href = targetUrl + "#action=" + action;
    }
}

function triggerAction(action) {
    if (action === "cadastrar-funcionario") {
        abrirModal('modal-cadastrar-funcionario');
    } else if (action === "cadastrar-cliente") {
        abrirModal('modal-cadastrar');
    } else if (action === "procurar-cadastro") {
        if (typeof toggleBuscaCliente === 'function') {
            toggleBuscaCliente();
        }
    } else if (action === "cadastrar-produto") {
        abrirModal('modal-cadastrar-produto');
    } else if (action === "procurar-produto") {
        if (typeof toggleBuscaProduto === 'function') {
            toggleBuscaProduto();
        }
    } else if (action === "estoque-baixo") {
        if (typeof gerarRelatorioEstoque === 'function') {
            gerarRelatorioEstoque();
        }
    }
}

$(document).ready(function() {
    if (window.location.hash && window.location.hash.indexOf("#action=") === 0) {
        var action = window.location.hash.split("=")[1];
        window.location.hash = "";
        setTimeout(function() {
            triggerAction(action);
        }, 150);
    }
});