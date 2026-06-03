var editingId = null;

$(document).ready(function () {

    var $form        = $('#product-form');
    var $feedback    = $('#product-form-feedback');
    var $formTitle   = $('#form-title');
    var $searchInput = $('#search-query');
    var $productList = $('#product-list');
    var $deleteBtn   = $('#delete-product-button');

    var fields = {
        id:           $('#product-id'),
        nome:         $('#product-name'),
        codigo:       $('#product-code'),
        marca:        $('#product-brand'),
        preco_unidade:$('#product-price'),
        unidade:      $('#product-unit')
    };

    /* ---------- helpers ---------- */

    function setFeedback(message, type) {
        $feedback.text(message || '').attr('class', 'form-feedback ' + (type || 'info'));
    }

    function resetForm() {
        editingId = null;
        fields.id.val('');
        $deleteBtn.hide();
        setFeedback('');
    }

    function fillForm(produto) {
        editingId = produto.id;
        $('#cad-prod-nome').val(produto.nome || '');
        $('#cad-prod-codigo').val(produto.codigo || '');
        $('#cad-prod-marca').val(produto.marca || '');
        $('#cad-prod-preco').val(produto.preco_unidade || '');
        $('#cad-prod-unidade').val(produto.unidade || '');
        $('#modal-cadastrar-produto .modal-title').text('ALTERAR PRODUTO');
        $('#modal-prod-btn').data('editing', produto.id);
    }

    /* ---------- render ---------- */

    function renderProducts(products) {
        if (!products.length) {
            $productList.html('<p class="empty-message">Nenhum produto cadastrado.</p>');
            return;
        }
        var html = products.map(function (p) {
            return '<article class="product-card" data-id="' + p.id + '">' +
                '<div class="product-img-placeholder"><img src="/static/icones/Produto.png" alt="Produto"></div>' +
                '<div class="product-info">' +
                    '<span class="product-name">' + p.nome + '</span>' +
                    '<span class="product-detail">Preço: R$ ' + Number(p.preco_unidade).toFixed(2) + '</span>' +
                    '<span class="product-detail">Marca: ' + p.marca + '</span>' +
                    '<span class="product-detail">Unidade: ' + p.unidade + '</span>' +
                    '<span class="product-detail">Código: ' + p.codigo + '</span>' +
                '</div>' +
                '<div class="product-actions">' +
                    '<button class="action-btn" type="button" data-action="edit" data-id="' + p.id + '" title="Editar">' +
                        '<img src="/static/icones/EditarSimbolo.png" alt="Editar"></button>' +
                    '<button class="action-btn" type="button" data-action="delete" data-id="' + p.id + '" title="Excluir">' +
                        '<img src="/static/icones/Lixosimbolo.png" alt="Excluir"></button>' +
                '</div>' +
            '</article>';
        }).join('');
        $productList.html(html);
    }

    /* ---------- AJAX ---------- */

    window.refreshProducts = function(query) {
        var url = query ? '/api/produtos/buscar?query=' + encodeURIComponent(query) : '/api/produtos';
        $.ajax({
            url: url,
            method: 'GET',
            dataType: 'json',
            success: function (products) {
                renderProducts(products);
            },
            error: function () {
                $productList.html('<p class="empty-message">Não foi possível carregar os produtos.</p>');
            }
        });
    };

    /* ---------- eventos ---------- */

    $productList.on('click', 'button[data-action]', function () {
        var action = $(this).data('action');
        var id     = $(this).data('id');

        if (action === 'delete') {
            if (!window.confirm('Deseja excluir este produto?')) return;
            $.ajax({
                url: '/api/produtos/' + id,
                method: 'DELETE',
                success: function () {
                    refreshProducts('');
                },
                error: function () {
                    alert('Falha ao excluir o produto.');
                }
            });
        }

        if (action === 'edit') {
            $.getJSON('/api/produtos/' + id, function (produto) {
                fillForm(produto);
                abrirModal('modal-cadastrar-produto');
            });
        }
    });

    $searchInput.on('input', function () {
        refreshProducts($searchInput.val().trim());
    });

    $deleteBtn.hide();
    refreshProducts('');
});

/* ===== funções globais ===== */


function abrirModal(id) {
    $('#' + id).addClass('aberto');
}

function fecharModal(id) {
    $('#' + id).removeClass('aberto');
    $('#modal-cadastrar-produto .modal-title').text('CADASTRAR PRODUTO');
    $('#cad-prod-nome, #cad-prod-codigo, #cad-prod-marca, #cad-prod-preco').val('');
    $('#cad-prod-unidade').val('');
    $('#modal-prod-btn').removeData('editing');
    editingId = null;

}

function cadastrarProduto() {
    var dados = {
        nome:          $('#cad-prod-nome').val().trim(),
        marca:         $('#cad-prod-marca').val().trim(),
        codigo:        $('#cad-prod-codigo').val().trim(),
        unidade:       $('#cad-prod-unidade').val(),
        preco_unidade: parseFloat($('#cad-prod-preco').val()),
    };

    var quantidade     = parseFloat($('#cad-prod-quantidade').val()) || 0;
    var quantidade_min = parseFloat($('#cad-prod-quantidade-min').val()) || 0;

    if (!dados.nome || !dados.marca || !dados.codigo || !dados.preco_unidade) {
        alert('Preencha todos os campos obrigatórios.');
        return;
    }

    $.ajax({
        url: '/api/produtos',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(dados),
        success: function (produto) {
            $.ajax({
                url: '/api/estoque',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    produto_id: produto.id,
                    quantidade_atual: quantidade,
                    quantidade_minima: quantidade_min
                }),
                success: function () {
                    fecharModal('modal-cadastrar-produto');
                    refreshProducts('');
                },
                error: function () {
                    alert('Produto criado mas erro ao registrar estoque.');
                }
            });
        },
        error: function (xhr) {
            alert('Erro ao cadastrar produto: ' + xhr.responseText);
        }
    });
}

function atualizarProduto() {
    if (!editingId) return;

    var dados = {
        nome:          $('#cad-prod-nome').val().trim(),
        codigo:        $('#cad-prod-codigo').val().trim(),
        marca:         $('#cad-prod-marca').val().trim(),
        preco_unidade: parseFloat($('#cad-prod-preco').val()),
        unidade:       $('#cad-prod-unidade').val()
    };

    if (!dados.nome || !dados.codigo || !dados.marca || !dados.preco_unidade) {
        alert('Preencha todos os campos obrigatórios.');
        return;
    }

    $.ajax({
        url: '/api/produtos/' + editingId,
        method: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify(dados),
        success: function () {
            fecharModal('modal-cadastrar-produto');
            refreshProducts('');
        },
        error: function (xhr) {
            alert('Erro ao atualizar produto: ' + xhr.responseText);
        }
    });
}

function toggleBuscaProduto() {
    var wrapper = document.getElementById('busca-wrapper-produto');
    wrapper.classList.toggle('aberta');
    if (wrapper.classList.contains('aberta')) {
        document.getElementById('search-query').focus();
    }
}

function gerarRelatorioEstoque() {
    $.when(
        $.getJSON('/api/estoque'),
        $.getJSON('/api/produtos')
    ).done(function(estoqueRes, produtosRes) {
        var estoques  = estoqueRes[0];
        var produtos  = produtosRes[0];

        var produtoMap = {};
        produtos.forEach(function(p) {
            produtoMap[p.id] = p;
        });

        var baixos = estoques.filter(function(e) {
            return e.quantidade_minima !== null &&
                   e.quantidade_atual <= e.quantidade_minima;
        });

        if (!baixos.length) {
            alert('Nenhum produto com estoque baixo no momento.');
            return;
        }

        var linhas = 'RELATÓRIO DE ESTOQUE BAIXO\n';
        linhas += 'Gerado em: ' + new Date().toLocaleString('pt-BR') + '\n';
        linhas += '='.repeat(40) + '\n\n';

        baixos.forEach(function(e) {
            var produto = produtoMap[e.produto_id];
            linhas += 'Produto: ' + (produto ? produto.nome : 'ID ' + e.produto_id) + '\n';
            linhas += 'Marca: ' + (produto ? produto.marca : '-') + '\n';
            linhas += 'Quantidade atual: ' + e.quantidade_atual + '\n';
            linhas += 'Quantidade mínima: ' + e.quantidade_minima + '\n';
            linhas += '-'.repeat(30) + '\n';
        });

        var blob = new Blob([linhas], { type: 'text/plain;charset=utf-8' });
        var url  = URL.createObjectURL(blob);
        var a    = document.createElement('a');
        a.href     = url;
        a.download = 'estoque_baixo_' + new Date().toISOString().slice(0,10) + '.txt';
        a.click();
        URL.revokeObjectURL(url);
    }).fail(function() {
        alert('Não foi possível carregar os dados.');
    });
}

function handleModalProdBtn() {
    var id = $('#modal-prod-btn').data('editing');
    if (id) {
        editingId = id;
        atualizarProduto();
    } else {
        cadastrarProduto();
    }
}