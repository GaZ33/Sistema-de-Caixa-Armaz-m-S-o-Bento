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

    var editingId = null;

    /* ---------- helpers ---------- */

    function setFeedback(message, type) {
        $feedback.text(message || '').attr('class', 'form-feedback ' + (type || 'info'));
    }

    function resetForm() {
        editingId = null;
        $form[0].reset();
        fields.id.val('');
        $formTitle.text('Novo produto');
        $deleteBtn.hide();
        setFeedback('');
    }

    function readForm() {
        return {
            nome:          fields.nome.val().trim(),
            codigo:        fields.codigo.val().trim(),
            marca:         fields.marca.val().trim(),
            preco_unidade: Number(fields.preco_unidade.val()),
            unidade:       fields.unidade.val()
        };
    }

    function fillForm(produto) {
        editingId = produto.id;
        fields.id.val(produto.id);
        fields.nome.val(produto.nome || '');
        fields.codigo.val(produto.codigo || '');
        fields.marca.val(produto.marca || '');
        fields.preco_unidade.val(produto.preco_unidade || '');
        fields.unidade.val(produto.unidade || '');
        $formTitle.text('Editando produto #' + produto.id);
        $deleteBtn.show();
        setFeedback('');
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
                    '<span class="product-detail">PreÃ§o: R$ ' + Number(p.preco_unidade).toFixed(2) + '</span>' +
                    '<span class="product-detail">Marca: ' + p.marca + '</span>' +
                    '<span class="product-detail">Unidade: ' + p.unidade + '</span>' +
                    '<span class="product-detail">CÃ³digo: ' + p.codigo + '</span>' +
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

    function refreshProducts(query) {
        var url = query ? '/api/produtos/buscar?query=' + encodeURIComponent(query) : '/api/produtos';
        $.ajax({
            url: url,
            method: 'GET',
            dataType: 'json',
            success: function (products) {
                renderProducts(products);
                setFeedback('');
            },
            error: function () {
                setFeedback('NÃ£o foi possÃ­vel carregar os produtos.', 'error');
            }
        });
    }

    function submitProduct(event) {
        event.preventDefault();
        var payload  = readForm();
        var method   = editingId ? 'PUT' : 'POST';
        var endpoint = editingId ? '/api/produtos/' + editingId : '/api/produtos';

        setFeedback('Salvando...', 'info');
        $.ajax({
            url: endpoint,
            method: method,
            contentType: 'application/json',
            data: JSON.stringify(payload),
            dataType: 'json',
            success: function () {
                setFeedback(editingId ? 'Produto atualizado com sucesso.' : 'Produto criado com sucesso.', 'success');
                resetForm();
                refreshProducts($searchInput.val().trim());
            },
            error: function (xhr) {
                var data = xhr.responseJSON || {};
                setFeedback(data.error || 'Falha ao salvar o produto.', 'error');
            }
        });
    }

    function deleteProduct() {
        if (!editingId) return;
        if (!window.confirm('Deseja excluir este produto?')) return;

        $.ajax({
            url: '/api/produtos/' + editingId,
            method: 'DELETE',
            success: function () {
                setFeedback('Produto excluÃ­do com sucesso.', 'success');
                resetForm();
                refreshProducts($searchInput.val().trim());
            },
            error: function () {
                setFeedback('Falha ao excluir o produto.', 'error');
            }
        });
    }

    /* ---------- eventos ---------- */

    $form.on('submit', submitProduct);

    $productList.on('click', 'button[data-action]', function () {
        var action = $(this).data('action');
        var id     = $(this).data('id');
        $.getJSON('/api/produtos/' + id, function (produto) {
            fillForm(produto);
            if (action === 'delete') deleteProduct();
        });
    });

    $('#search-product-button').on('click', function () {
        refreshProducts($searchInput.val().trim());
    });

    $searchInput.on('keydown', function (e) {
        if (e.key === 'Enter') { e.preventDefault(); refreshProducts($searchInput.val().trim()); }
    });

    $('#new-product-button').on('click', resetForm);
    $('#cancel-product-button').on('click', resetForm);
    $deleteBtn.on('click', deleteProduct);

    $deleteBtn.hide();
    refreshProducts();
});

/* ===== funÃ§Ãµes globais (fora do ready) ===== */

function limparFormulario() {
    $('#product-id, #product-name, #product-price, #product-unit, #product-brand, #product-code').val('');
}

function abrirModal(id) {
    $('#' + id).addClass('aberto');
}

function fecharModal(id) {
    $('#' + id).removeClass('aberto');
}

function cadastrarProduto() {
    var dados = {
        nome:          $('#cad-prod-nome').val().trim(),
        codigo:        $('#cad-prod-codigo').val().trim(),
        marca:         $('#cad-prod-marca').val().trim(),
        preco_unidade: Number($('#cad-prod-preco').val()),
        unidade:       $('#cad-prod-unidade').val()
    };

    if (!dados.nome || !dados.codigo || !dados.marca || !dados.preco_unidade || !dados.unidade) {
        alert('Preencha todos os campos obrigatÃ³rios.');
        return;
    }

    $.ajax({
        url: '/api/produtos',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(dados),
        dataType: 'json',
        success: function () {
            fecharModal('modal-cadastrar-produto');
            $('#cad-prod-nome, #cad-prod-codigo, #cad-prod-marca, #cad-prod-preco').val('');
            $('#cad-prod-unidade').val('');
            $('#search-product-button').trigger('click');
        },
        error: function (xhr) {
            var data = xhr.responseJSON || {};
            alert(data.error || 'Falha ao cadastrar produto.');
        }
    });
}
