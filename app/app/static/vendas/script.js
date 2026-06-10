var userMap = {};

window.verDetalhesVenda = function(contaId) {
    $.getJSON('/api/contas/' + contaId, function(conta) {
        $('#detalhe-id').text(conta.id);
        $('#detalhe-cliente').html(conta.cliente && userMap[conta.cliente] ? userMap[conta.cliente] : '<span class="text-muted">Não Informado</span>');
        
        var statusLabel = conta.status === 'fechada' ? '<span class="badge bg-success">Fechada</span>' : '<span class="badge bg-warning text-dark">Pendente (Fiado)</span>';
        $('#detalhe-status').html(statusLabel);
        
        var dataCriacao = conta.data_criacao ? new Date(conta.data_criacao).toLocaleString('pt-BR') : '-';
        $('#detalhe-criacao').text(dataCriacao);
        
        var dataFechamento = conta.data_fechamento ? new Date(conta.data_fechamento).toLocaleString('pt-BR') : '-';
        $('#detalhe-fechamento').text(dataFechamento);
        
        $('#detalhe-total').text(Number(conta.valor_total).toFixed(2).replace('.', ','));

        // Carregar os itens da conta
        $.getJSON('/api/produto_conta/conta/' + contaId, function(itens) {
            var $tbody = $('#tabela-detalhes-itens tbody').empty();
            if (itens.length === 0) {
                $tbody.append('<tr><td colspan="4" class="text-center" style="padding: 15px; color: #8a7a50; font-style: italic;">Nenhum produto nesta compra.</td></tr>');
            } else {
                itens.forEach(function(item) {
                    var preco = Number(item.preco_unitario).toFixed(2);
                    var subtotal = Number(item.subtotal).toFixed(2);
                    $tbody.append(
                        '<tr>' +
                            '<td style="font-weight: 600; color: #3a2a00;">' + (item.produto_nome || 'Produto Desconhecido') + '</td>' +
                            '<td>' + item.quantidade + '</td>' +
                            '<td>R$ ' + preco + '</td>' +
                            '<td style="font-weight: 700; color: #3a2a00;">R$ ' + subtotal + '</td>' +
                        '</tr>'
                    );
                });
            }
            abrirModal('modal-detalhes-venda');
        });
    });
};

$(document).ready(function () {
    console.log("Inicializando Tabela de Vendas...");

    $.getJSON('/api/users', function(users) {
        users.forEach(function(u) {
            userMap[u.id] = (u.nome || '') + (u.sobrenome ? ' ' + u.sobrenome : '') + ' (@' + u.username + ')';
        });

        $('#tabelaVendas').DataTable({
            ajax: {
                url: '/api/contas',
                dataSrc: ''
            },
            columns: [
                { data: 'id' },
                { 
                    data: 'cliente',
                    render: function(data) {
                        return data && userMap[data] ? userMap[data] : '<span class="text-muted">Não Informado</span>';
                    }
                },
                { 
                    data: 'status',
                    render: function(data) {
                        if(data === 'fechada') {
                            return '<span class="badge bg-success">Fechada</span>';
                        } else if (data === 'aberta') {
                            return '<span class="badge bg-warning text-dark">Pendente (Fiado)</span>';
                        }
                        return '<span class="badge bg-secondary">' + data + '</span>';
                    }
                },
                { 
                    data: 'data_criacao',
                    render: function(data) {
                        if(!data) return '-';
                        var date = new Date(data);
                        return date.toLocaleString('pt-BR');
                    }
                },
                { 
                    data: 'data_fechamento',
                    render: function(data) {
                        if(!data) return '-';
                        var date = new Date(data);
                        return date.toLocaleString('pt-BR');
                    }
                },
                { 
                    data: 'valor_total',
                    render: function(data) {
                        return 'R$ ' + Number(data).toFixed(2);
                    }
                },
                {
                    data: null,
                    orderable: false,
                    render: function(data, type, row) {
                        return `<button type="button" class="btn btn-sm" style="background:#f0b800; border:1px solid #c9a000; color:#3a2a00; font-weight:bold;" onclick="verDetalhesVenda(${row.id})">Ver</button>`;
                    }
                }
            ],
            order: [[0, 'desc']], // Ordenar por ID decrescente (mais recentes primeiro)
            language: {
                url: "https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json"
            },
            pageLength: 10,
            lengthMenu: [10, 25, 50, 100]
        });
    });
});
