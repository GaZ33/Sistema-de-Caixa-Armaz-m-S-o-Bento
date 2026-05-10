let carrinho = [];

// Função para atualizar a tabela na tela
function atualizarTabela() {
    let html = '';
    let total = 0;
    carrinho.forEach((item, index) => {
        let subtotal = item.preco * item.qtd;
        total += subtotal;
        html += `<tr>
            <td>${item.nome}</td>
            <td>R$ ${item.preco.toFixed(2)}</td>
            <td>${item.qtd}</td>
            <td>R$ ${subtotal.toFixed(2)}</td>
            <td><button onclick="removerItem(${index})" class="btn btn-danger btn-sm">X</button></td>
        </tr>`;
    });
    $('#tabela_venda tbody').html(html);
    $('#valor_total').text('R$ ' + total.toFixed(2));
}

// Função para buscar produtos no backend e exibir sugestões
$('#busca_produto').select2({
    placeholder: 'Digite o nome ou código do produto...',
    ajax: {
        url: '/api/produtos/buscar',
        dataType: 'json',
        delay: 250,
        data: function(params) {
            return {
                query: params.term // Termo de busca
            };
        },
        processResults: function(data) {
            return {
                results: data.map(function(produto) {
                    return {
                        id: produto.id,
                        text: `${produto.nome} - R$ ${produto.preco_unidade.toFixed(2)}`,
                        nome: produto.nome,
                        preco: produto.preco_unidade
                    };
                })
            };
        },
        cache: true
    },
    minimumInputLength: 2
});

// Adiciona o produto selecionado ao carrinho
$(document).ready(function() {
    let produtoSelecionado = null;

    $('#busca_produto').select2({
        placeholder: 'Digite o nome ou código do produto...',
        ajax: {
            url: '/api/produtos/buscar',
            dataType: 'json',
            delay: 250,
            data: function(params) {
                return {
                    query: params.term // Termo de busca
                };
            },
            processResults: function(data) {
                return {
                    results: data.map(function(produto) {
                        return {
                            id: produto.id,
                            text: `${produto.nome} - R$ ${produto.preco_unidade.toFixed(2)}`,
                            nome: produto.nome,
                            preco: produto.preco_unidade
                        };
                    })
                };
            },
            cache: true
        },
        minimumInputLength: 2
    });

    // Garante que o Select2 abra automaticamente ao carregar a página
    $(document).ready(function() {
        const buscaProduto = $('#busca_produto');

        // Foca no campo de busca
        buscaProduto.focus();

        // Aguarda um pequeno intervalo para garantir que o Select2 esteja inicializado antes de abrir
        setTimeout(() => {
            buscaProduto.select2('open');
        }, 100);

        // Abre automaticamente a busca do select2 ao focar no campo
        buscaProduto.on('focus', function() {
            $(this).select2('open');
        });
    });

    // Exibe o modal ao clicar no botão "Adicionar"
    $('#btn_adicionar').off('click').on('click', function() {
        console.log('Botão Adicionar clicado'); // Log para depuração
        const selectedData = $('#busca_produto').select2('data');
        console.log('Produto selecionado:', selectedData); // Log para verificar o produto selecionado
        if (selectedData.length > 0) {
            produtoSelecionado = selectedData[0];
            $('#modalQuantidade').modal('show'); // Garante que o modal seja exibido
            console.log('Modal exibido'); // Log para confirmar que o modal foi chamado
        } else {
            alert('Selecione um produto antes de adicionar.');
        }
    });

    // Adiciona o produto ao carrinho com a quantidade definida
    $('#confirmarQuantidade').off('click').on('click', function() {
        const quantidade = parseInt($('#quantidade').val());
        console.log('Quantidade confirmada:', quantidade); // Log para verificar a quantidade
        if (produtoSelecionado && quantidade > 0) {
            carrinho.push({
                id: produtoSelecionado.id,
                nome: produtoSelecionado.nome,
                preco: produtoSelecionado.preco,
                qtd: quantidade
            });
            console.log('Produto adicionado ao carrinho:', carrinho); // Log para verificar o carrinho
            atualizarTabela();
            $('#busca_produto').val(null).trigger('change'); // Limpa a seleção
            $('#modalQuantidade').modal('hide'); // Fecha o modal após adicionar
        } else {
            alert('Quantidade inválida.');
        }
    });

    // Garante que o modal seja inicializado corretamente
    $('#modalQuantidade').on('shown.bs.modal', function() {
        $('#quantidade').focus(); // Foca no campo de quantidade ao abrir o modal
    });
});

// Exemplo de como enviar os dados para o Flask
$('#finalizar_venda').click(function() {
    let dadosVenda = {
        carrinho: carrinho,
        forma_pagamento: $('#forma_pagamento').val(),
        cliente_id: null // Opcional
    };

    $.ajax({
        url: '/api/venda/finalizar',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(dadosVenda),
        success: function(response) {
            alert("Venda realizada com sucesso!");
            carrinho = [];
            atualizarTabela();
        },
        error: function(err) { alert("Erro ao finalizar venda."); }
    });
});