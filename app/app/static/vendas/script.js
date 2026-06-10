$(document).ready(function () {
    console.log("Inicializando Tabela de Vendas...");

    $('#tabelaVendas').DataTable({
        ajax: {
            url: '/api/contas',
            dataSrc: ''
        },
        columns: [
            { data: 'id' },
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
                    // Format ISO date to local string
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
