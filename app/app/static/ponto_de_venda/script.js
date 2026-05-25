let carrinho = [];
let produtoSelecionado = null;

function atualizarTabela() {
    let html = '';
    let total = 0;

    carrinho.forEach((item, index) => {
        const subtotal = item.preco * item.qtd;
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
    $('#valor_total').text(`R$ ${total.toFixed(2)}`);
}

function removerItem(index) {
    carrinho.splice(index, 1);
    atualizarTabela();
}

function configurarBusca() {
    $('#busca_produto').select2({
        placeholder: 'Digite o nome ou código do produto...',
        ajax: {
            url: '/api/produtos/buscar',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return { query: params.term };
            },
            processResults: function (data) {
                return {
                    results: data.map(function (produto) {
                        return {
                            id: produto.id,
                            text: `${produto.nome} - R$ ${Number(produto.preco_unidade).toFixed(2)}`,
                            nome: produto.nome,
                            preco: Number(produto.preco_unidade)
                        };
                    })
                };
            },
            cache: true
        },
        minimumInputLength: 2
    });
}

$(document).ready(function () {
    configurarBusca();

    $('#busca_produto').on('select2:select', function (event) {
        produtoSelecionado = event.params.data;
    });

    $('#btn_adicionar').on('click', function () {
        if (!produtoSelecionado) {
            alert('Selecione um produto antes de adicionar.');
            return;
        }

        $('#modalQuantidade').modal('show');
    });

    $('#confirmarQuantidade').on('click', function () {
        const quantidade = parseInt($('#quantidade').val(), 10);

        if (produtoSelecionado && quantidade > 0) {
            carrinho.push({
                id: produtoSelecionado.id,
                nome: produtoSelecionado.nome,
                preco: produtoSelecionado.preco,
                qtd: quantidade
            });

            atualizarTabela();
            produtoSelecionado = null;
            $('#busca_produto').val(null).trigger('change');
            $('#modalQuantidade').modal('hide');
        } else {
            alert('Quantidade inválida.');
        }
    });

    $('#modalQuantidade').on('shown.bs.modal', function () {
        $('#quantidade').focus();
    });

    $('#finalizar_venda').on('click', async function () {
        if (!carrinho.length) {
            alert('Adicione pelo menos um item ao carrinho.');
            return;
        }

        const dadosVenda = {
            carrinho,
            forma_pagamento: $('#forma_pagamento').val(),
            cliente_id: null
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

            alert('Venda realizada com sucesso!');
            carrinho = [];
            atualizarTabela();
        } catch (error) {
            alert(error.message);
        }
    });
});
