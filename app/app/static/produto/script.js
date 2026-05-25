document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('product-form');
    const feedback = document.getElementById('product-form-feedback');
    const formTitle = document.getElementById('form-title');
    const searchInput = document.getElementById('search-query');
    const searchButton = document.getElementById('search-product-button');
    const newButton = document.getElementById('new-product-button');
    const cancelButton = document.getElementById('cancel-product-button');
    const deleteButton = document.getElementById('delete-product-button');
    const productList = document.getElementById('product-list');

    const fields = {
        id: document.getElementById('product-id'),
        nome: document.getElementById('product-name'),
        codigo: document.getElementById('product-code'),
        marca: document.getElementById('product-brand'),
        preco_unidade: document.getElementById('product-price'),
        unidade: document.getElementById('product-unit')
    };

    let editingId = null;

    const setFeedback = (message, type = 'info') => {
        feedback.textContent = message || '';
        feedback.className = `form-feedback ${type}`;
    };

    const resetForm = () => {
        editingId = null;
        form.reset();
        fields.id.value = '';
        formTitle.textContent = 'Novo produto';
        deleteButton.style.display = 'none';
        setFeedback('');
    };

    const readForm = () => ({
        nome: fields.nome.value.trim(),
        codigo: fields.codigo.value.trim(),
        marca: fields.marca.value.trim(),
        preco_unidade: Number(fields.preco_unidade.value),
        unidade: fields.unidade.value
    });

    const renderProducts = (products) => {
        if (!products.length) {
            productList.innerHTML = '<p class="empty-message">Nenhum produto cadastrado.</p>';
            return;
        }

        productList.innerHTML = products.map((produto) => `
            <article class="product-card" data-id="${produto.id}">
                <div class="product-img-placeholder">
                    <img src="/static/icones/Produto.png" alt="Produto">
                </div>
                <div class="product-info">
                    <span class="product-name">${produto.nome}</span>
                    <span class="product-detail">Preço: R$ ${Number(produto.preco_unidade).toFixed(2)}</span>
                    <span class="product-detail">Marca: ${produto.marca}</span>
                    <span class="product-detail">Unidade: ${produto.unidade}</span>
                    <span class="product-detail">Código: ${produto.codigo}</span>
                </div>
                <div class="product-actions">
                    <button class="action-btn" type="button" data-action="edit" data-id="${produto.id}" title="Editar">
                        <img src="/static/icones/EditarSimbolo.png" alt="Editar">
                    </button>
                    <button class="action-btn" type="button" data-action="delete" data-id="${produto.id}" title="Excluir">
                        <img src="/static/icones/Lixosimbolo.png" alt="Excluir">
                    </button>
                </div>
            </article>
        `).join('');
    };

    const loadProducts = async (query = '') => {
        const url = query
            ? `/api/produtos/buscar?query=${encodeURIComponent(query)}`
            : '/api/produtos';

        const response = await fetch(url, { headers: { Accept: 'application/json' } });
        if (!response.ok) {
            throw new Error('Nao foi possivel carregar os produtos.');
        }

        return response.json();
    };

    const refreshProducts = async (query = '') => {
        try {
            const products = await loadProducts(query);
            renderProducts(products);
            setFeedback('');
        } catch (error) {
            setFeedback(error.message, 'error');
        }
    };

    const fillForm = (produto) => {
        editingId = produto.id;
        fields.id.value = produto.id;
        fields.nome.value = produto.nome || '';
        fields.codigo.value = produto.codigo || '';
        fields.marca.value = produto.marca || '';
        fields.preco_unidade.value = produto.preco_unidade || '';
        fields.unidade.value = produto.unidade || '';
        formTitle.textContent = `Editando produto #${produto.id}`;
        deleteButton.style.display = 'inline-flex';
        setFeedback('');
    };

    const submitProduct = async (event) => {
        event.preventDefault();

        const payload = readForm();
        const method = editingId ? 'PUT' : 'POST';
        const endpoint = editingId ? `/api/produtos/${editingId}` : '/api/produtos';

        try {
            setFeedback('Salvando...', 'info');

            const response = await fetch(endpoint, {
                method,
                headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await response.json().catch(() => ({}));
            if (!response.ok) {
                throw new Error(data.error || 'Falha ao salvar o produto.');
            }

            setFeedback(editingId ? 'Produto atualizado com sucesso.' : 'Produto criado com sucesso.', 'success');
            resetForm();
            await refreshProducts(searchInput.value.trim());
        } catch (error) {
            setFeedback(error.message, 'error');
        }
    };

    const deleteProduct = async () => {
        if (!editingId) {
            return;
        }

        if (!window.confirm('Deseja excluir este produto?')) {
            return;
        }

        try {
            const response = await fetch(`/api/produtos/${editingId}`, { method: 'DELETE', headers: { Accept: 'application/json' } });
            if (!response.ok) {
                throw new Error('Falha ao excluir o produto.');
            }

            setFeedback('Produto excluido com sucesso.', 'success');
            resetForm();
            await refreshProducts(searchInput.value.trim());
        } catch (error) {
            setFeedback(error.message, 'error');
        }
    };

    productList.addEventListener('click', async (event) => {
        const actionButton = event.target.closest('button[data-action]');
        if (!actionButton) {
            return;
        }

        const { action, id } = actionButton.dataset;
        const response = await fetch(`/api/produtos/${id}`, { headers: { Accept: 'application/json' } });
        const produto = await response.json();

        if (action === 'edit') {
            fillForm(produto);
            return;
        }

        if (action === 'delete') {
            fillForm(produto);
            deleteProduct();
        }
    });

    form.addEventListener('submit', submitProduct);
    searchButton.addEventListener('click', () => refreshProducts(searchInput.value.trim()));
    searchInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            refreshProducts(searchInput.value.trim());
        }
    });
    newButton.addEventListener('click', resetForm);
    cancelButton.addEventListener('click', resetForm);
    deleteButton.addEventListener('click', deleteProduct);

    deleteButton.style.display = 'none';
    refreshProducts();
});
