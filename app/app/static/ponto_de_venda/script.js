$(document).ready(function () {
let carrinho = [];
let produtoSelecionado = null;
let formaPagamentoSelecionada = 'dinheiro'; // Default payment option

function atualizarTabela() {
    let html = '';
    let total = 0;

    carrinho.forEach((item, index) => {
        const subtotal = item.preco * item.qtd;
        total += subtotal;

        html += `<tr>
            <td style="font-weight: 600; color: #3a2a00;">${item.nome}</td>
            <td>R$ ${item.preco.toFixed(2)}</td>
            <td>
                <div class="qtd-control">
                    <button type="button" onclick="alterarQuantidade(${index}, -1)" class="qtd-btn">-</button>
                    <span class="qtd-value">${item.qtd}</span>
                    <button type="button" onclick="alterarQuantidade(${index}, 1)" class="qtd-btn">+</button>
                </div>
            </td>
            <td style="font-weight: 700; color: #3a2a00;">R$ ${subtotal.toFixed(2)}</td>
            <td>
                <button type="button" onclick="removerItem(${index})" class="remove-btn" title="Remover Item">
                    <img src="/static/icones/Lixosimbolo.png" alt="Excluir">
                </button>
            </td>
        </tr>`;
    });

    if (carrinho.length === 0) {
        html = '<tr><td colspan="5" class="text-center" style="padding: 24px; color: #8a7a50; font-style: italic;">Nenhum produto adicionado à venda.</td></tr>';
    }

    $('#tabela_venda tbody').html(html);
    $('#valor_total').text(`R$ ${total.toFixed(2).replace('.', ',')}`);
}

function alterarQuantidade(index, delta) {
    if (carrinho[index]) {
        carrinho[index].qtd += delta;
        if (carrinho[index].qtd <= 0) {
            removerItem(index);
        } else {
            atualizarTabela();
        }
    }
}

function removerItem(index) {
    carrinho.splice(index, 1);
    atualizarTabela();
}

let tabelaProdutos;

function configurarModalDataTables() {
    tabelaProdutos = $('#tabelaProdutosDataTables').DataTable({
        ajax: {
            url: '/api/produtos',
            dataSrc: ''
        },
        columns: [
            { data: 'codigo', defaultContent: '-' },
            { data: 'nome' },
            { data: 'marca', defaultContent: '-' },
            { 
                data: 'preco_unidade',
                render: function(data, type, row) {
                    return 'R$ ' + Number(data).toFixed(2);
                }
            },
            {
                data: null,
                orderable: false,
                render: function(data, type, row) {
                    return `<button type="button" class="btn btn-sm" style="background:#f0b800; border:1px solid #c9a000; color:#3a2a00; font-weight:bold;" data-id="${row.id}" data-nome="${row.nome}" data-preco="${row.preco_unidade}">Adicionar</button>`;
                }
            }
        ],
        language: {
            url: "https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json"
        },
        pageLength: 5,
        lengthMenu: [5, 10, 25, 50]
    });
            console.log("AAAAAAAAAA");

    // Evento de clique no botão de adicionar dentro do DataTable
    $('#tabelaProdutosDataTables tbody').on('click', 'button', function () {
        var id = $(this).data('id');
        var nome = $(this).data('nome');
        var preco = $(this).data('preco');

        if(id) {
            adicionarProdutoAoCarrinho({
                id: parseInt(id, 10),
                nome: nome,
                preco: Number(preco)
            });
            
            // Fecha o modal do bootstrap
            var modalEl = document.getElementById('modalProdutos');
            var modalInst = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
            modalInst.hide();
        }
    });
}

function carregarClientes() {
    $.getJSON('/api/users', function (users) {
        console.log("AAAAAAAAAA");
        var $select = $('#busca_cliente').empty();
        $select.append('<option value="">Selecione um cliente (opcional)...</option>');
        
        users.forEach(function (user) {
            if (user.perfil_id === 3) { // Only Cliente (Customers)
                var label = (user.nome || '') + ' ' + (user.sobrenome || '') + ' (@' + user.username + ')';
                $select.append($('<option></option>').val(user.id).text(label));
            }
        });
        
        $select.select2({
            placeholder: 'Associar cliente (opcional)...',
            allowClear: true
        });

        // Habilitar/desabilitar botão pendurar ao alterar cliente
        $select.on('change', function() {
            var val = $(this).val();
            var $btnPendurar = $('#btn_pendurar_pdv');
            if (val) {
                $btnPendurar.prop('disabled', false);
            } else {
                $btnPendurar.prop('disabled', true);
                if (formaPagamentoSelecionada === 'pendurar') {
                    // Reset to money if pendurar was active but client was cleared
                    setFormaPagamento('dinheiro');
                }
            }
        });
    });
}

function setFormaPagamento(value) {
    formaPagamentoSelecionada = value;
    
    // Update active class on buttons
    $('.payment-btn').removeClass('selected');
    $(`.payment-btn[data-value="${value}"]`).addClass('selected');
}

function adicionarProdutoAoCarrinho(produto) {
    // Verifica se o item já existe no carrinho para apenas somar quantidade
    const indexExistente = carrinho.findIndex(item => item.id === produto.id);
    if (indexExistente !== -1) {
        carrinho[indexExistente].qtd += 1;
    } else {
        carrinho.push({
            id: produto.id,
            nome: produto.nome,
            preco: produto.preco,
            qtd: 1
        });
    }
    atualizarTabela();
}

$(document).ready(function () {
    console.log("========= INICIANDO PDV SCRIPT =========");
    try {
    // Diagnóstico
    $('#diag-script').text("script.js: OK");
    $('body').append('<div id="debug-info" data-jq="' + (typeof jQuery) + '" data-s2="' + (typeof $.fn.select2) + '" data-bp="' + (typeof $('#busca_produto').select2) + '" data-instance="' + (!!$('#busca_produto').data('select2')) + '"></div>');

    // Configurações iniciais
    console.log("Configurando Modal DataTables...");
    configurarModalDataTables();
    console.log("Carregando Clientes...");
    carregarClientes();
    console.log("Atualizando Tabela...");
    atualizarTabela();

    // Eventos antigos do Select2 removidos pois agora usamos o Modal de Produtos

    // Seletores de forma de pagamento
    $('.payment-btn').on('click', function() {
        if ($(this).prop('disabled')) return;
        var val = $(this).data('value');
        setFormaPagamento(val);
    });

    // Atalho de teclado F2 para finalizar a venda
    $(document).on('keydown', function(e) {
        if (e.key === 'F2') {
            e.preventDefault();
            $('#finalizar_venda').trigger('click');
        }
    });

    // Finalizar Venda
    $('#finalizar_venda').on('click', async function () {
        if (!carrinho.length) {
            alert('Adicione pelo menos um item ao carrinho.');
            return;
        }

        var clienteId = $('#busca_cliente').val() || null;
        var pendurar = (formaPagamentoSelecionada === 'pendurar');

        if (pendurar && !clienteId) {
            alert('Selecione um cliente para poder pendurar a conta.');
            return;
        }

        // Formata os itens do carrinho para o payload da API
        const itensPayload = carrinho.map(item => {
            return {
                id: item.id,
                qtd: item.qtd
            };
        });

        const dadosVenda = {
            carrinho: itensPayload,
            forma_pagamento: pendurar ? null : formaPagamentoSelecionada,
            cliente_id: clienteId ? parseInt(clienteId, 10) : null,
            pendurar: pendurar
        };

        try {
            const response = await fetch('/api/venda/finalizar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(dadosVenda)
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Erro ao finalizar venda.');
            }

            alert(pendurar ? 'Venda pendurada no cliente com sucesso!' : 'Venda finalizada com sucesso!');
            
            // Reset do estado do PDV
            carrinho = [];
            produtoSelecionado = null;
            atualizarTabela();
            $('#busca_produto').val(null).trigger('change');
            $('#busca_cliente').val(null).trigger('change');
            setFormaPagamento('dinheiro');

        } catch (error) {
            alert(error.message);
        }
    });
    } catch (err) {
        console.error("ERRO DURANTE INICIALIZAÇÃO:", err);
        alert("Erro na inicialização do PDV: " + err.message);
    }
});
});